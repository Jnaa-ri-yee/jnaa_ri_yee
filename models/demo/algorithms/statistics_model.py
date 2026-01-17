# model/statistics_model.py
import os, json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from model import DLClassifier, FeatureExtractor
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
EVAL_ROOT = os.path.join(BASE_DIR, "evaluacion")
os.makedirs(EVAL_ROOT, exist_ok=True)

def run_evaluation(keras_model_path=None, ml_model_path=None, dataset_dir="../dataset/train/"):
    if keras_model_path is None:
        keras_model_path = os.path.join(MODEL_DIR, "vowels_model.h5")
    if ml_model_path is None:
        ml_model_path = os.path.join(MODEL_DIR, "ml_rf_joblib.pkl")

    dl = DLClassifier(model_path=keras_model_path)
    fe = FeatureExtractor()
    ml = joblib.load(ml_model_path)

    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    val_gen = datagen.flow_from_directory(
        os.path.join(BASE_DIR, dataset_dir),
        target_size=(224,224),
        batch_size=16,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    # Predictions
    val_gen.reset()
    dl_preds = dl.model.predict(val_gen, verbose=1)
    # ML features
    val_gen.reset()
    feats = []
    y = []
    steps = int(np.ceil(val_gen.samples / val_gen.batch_size))
    for i in range(steps):
        xb, yb = next(val_gen)
        feats.append(fe.extract(xb))
        y.append(np.argmax(yb, axis=1))
    Xval = np.vstack(feats)
    ytrue = np.concatenate(y)
    ml_probs = ml.predict_proba(Xval)

    # Ensemble:
    probs = (dl_preds[:len(ml_probs)] + ml_probs) / 2.0
    ypred = np.argmax(probs, axis=1)

    # Metrics + save
    cm = confusion_matrix(ytrue, ypred)
    report = classification_report(ytrue, ypred, output_dict=True)
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outdir = os.path.join(EVAL_ROOT, f"evaluacion_{fecha}")
    os.makedirs(outdir, exist_ok=True)

    # save report
    with open(os.path.join(outdir, "classification_report.json"), "w", encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title("Matriz de Confusión (ensemble)")
    plt.savefig(os.path.join(outdir, "confusion_matrix.png"))
    plt.close()

    print("Saved evaluation to", outdir)
    return outdir, report

if __name__ == "__main__":
    run_evaluation()
