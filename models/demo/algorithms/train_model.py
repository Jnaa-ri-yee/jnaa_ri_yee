# ======================================================                     *
#  Project      : algorithms                                                 *
#  File         : train_model.py                                             *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 16:21                                           *
# ======================================================                     *
#                                                                            *
#  License:                                                                  *
# © 2026 Equipo Jña'a Ri Y'ë'ë                                               *
#                                                                            *
# Este software y su código fuente son propiedad exclusiva                   *
# del equipo Jña'a Ri Y'ë'ë.                                                 *
#                                                                            *
# Uso permitido únicamente para:                                             *
# - Evaluación académica                                                     *
# - Revisión técnica                                                         *
# - Convocatorias, hackatones o concursos                                    *
#                                                                            *
# Queda prohibida la copia, modificación, redistribución                     *
# o uso sin autorización expresa del equipo.                                 *
#                                                                            *
# El software se proporciona "tal cual", sin garantías.                      *

# model/train_model.py
import os, re, json, numpy as np
from datetime import datetime
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.utils import class_weight
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from .model import DLClassifier, FeatureExtractor, MLClassifier, load_class_names
import joblib


def main():
    # Directorios
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TRAIN_DIR = os.path.join(BASE_DIR, "../dataset/train/")
    MODEL_DIR = os.path.join(BASE_DIR, "models")
    EVAL_ROOT = os.path.join(BASE_DIR, "evaluacion")
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(EVAL_ROOT, exist_ok=True)

    # Limpiar imágenes inválidas o corruptas
    def limpiar_imagenes_invalidas(base_dir):
        print(f"Verificando imágenes en {base_dir} ...")
        for root, _, files in os.walk(base_dir):
            for file in files:
                path = os.path.join(root, file)
                nuevo = re.sub(r'[^a-zA-Z0-9_.-]', '_', file)
                if len(nuevo) > 60:
                    base, ext = os.path.splitext(nuevo)
                    nuevo = base[:50] + ext
                nuevo_path = os.path.join(root, nuevo)
                if path != nuevo_path:
                    os.rename(path, nuevo_path)
                    path = nuevo_path
                try:
                    with Image.open(path) as img:
                        img.verify()
                except Exception:
                    print("Imagen inválida:", path)
                    os.remove(path)
        print("Limpieza completada.")

    limpiar_imagenes_invalidas(TRAIN_DIR)

    # Generadores de datos
    IMG_SIZE = (224, 224)
    BATCH = 16
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=25,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.2,
        shear_range=0.1,
        brightness_range=(0.75, 1.25),
        horizontal_flip=True,
        validation_split=0.2
    )

    train_gen = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH,
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    val_gen = datagen.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    class_names = list(train_gen.class_indices.keys())
    num_classes = len(class_names)

    # Generar y entrenar modelo DL
    dl = DLClassifier()
    model = dl.build(num_classes, base_trainable=False)

    # Callbacks
    checkpoint_path = os.path.join(MODEL_DIR, "vowels_model_best.h5")
    checkpoint = ModelCheckpoint(checkpoint_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    early = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True, verbose=1)
    reduce = ReduceLROnPlateau(monitor='val_loss', factor=0.3, patience=4, min_lr=1e-6, verbose=1)

    # Class weights
    weights = class_weight.compute_class_weight('balanced', classes=np.unique(train_gen.classes), y=train_gen.classes)
    cw = dict(enumerate(weights))

    # Train
    history = model.fit(
        train_gen,
        validation_data=val_gen,
        epochs=40,
        callbacks=[checkpoint, early, reduce],
        class_weight=cw,
        verbose=1
    )

    # Save final Keras model
    final_keras_path = os.path.join(MODEL_DIR, "vowels_model.h5")
    model.save(final_keras_path)

    # Save class names
    with open(os.path.join(MODEL_DIR, "class_names.json"), "w", encoding='utf-8') as f:
        json.dump(class_names, f, ensure_ascii=False, indent=2)

    print("DL model saved:", final_keras_path)

    # Extraer características y entrenar modelo ML
    fe = FeatureExtractor()
    datagen_plain = ImageDataGenerator(rescale=1./255)
    full_gen = datagen_plain.flow_from_directory(
        TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH, class_mode='categorical', shuffle=False
    )

    full_gen.reset()
    feats = []
    labels = []
    steps = int(np.ceil(full_gen.samples / full_gen.batch_size))
    for i in range(steps):
        xbatch, ybatch = next(full_gen)
        f = fe.extract(xbatch)
        feats.append(f)
        labels.append(np.argmax(ybatch, axis=1))
    X = np.vstack(feats)
    y = np.concatenate(labels)

    print("Features shape:", X.shape, "Labels shape:", y.shape)

    # Train ML classifier
    ml = MLClassifier()
    ml.fit(X, y)
    ml_path = os.path.join(MODEL_DIR, "ml_rf_joblib.pkl")
    ml.save(ml_path)
    print("ML model saved:", ml_path)

    # Evaluación conjunta DL + ML
    val_plain = ImageDataGenerator(rescale=1./255, validation_split=0.2)
    val_gen2 = val_plain.flow_from_directory(
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    val_gen2.reset()
    dl_preds = model.predict(val_gen2, verbose=1)

    # Extract validation features
    val_gen2.reset()
    feats_val = []
    y_val = []
    steps_val = int(np.ceil(val_gen2.samples / val_gen2.batch_size))
    for i in range(steps_val):
        xb, yb = next(val_gen2)
        feats_val.append(fe.extract(xb))
        y_val.append(np.argmax(yb, axis=1))
    Xval = np.vstack(feats_val)
    ytrue = np.concatenate(y_val)

    # ML predictions
    ml_probs = ml.predict_proba(Xval)

    # Ensemble: average probabilities
    ensemble_probs = (dl_preds[:len(ml_probs)] + ml_probs) / 2.0
    ypred = np.argmax(ensemble_probs, axis=1)

    # Confusion matrix and report
    cm = confusion_matrix(ytrue, ypred)
    report = classification_report(ytrue, ypred, target_names=class_names, output_dict=True)
    print("Classification report (ensemble):")
    print(classification_report(ytrue, ypred, target_names=class_names))

    # Guardar artefactos de evaluación
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    evdir = os.path.join(EVAL_ROOT, f"evaluacion_{fecha}")
    os.makedirs(evdir, exist_ok=True)

    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, fmt='d', xticklabels=class_names, yticklabels=class_names, cmap='Blues')
    plt.title("Confusion matrix (ensemble)")
    plt.savefig(os.path.join(evdir, "confusion_matrix.png"))
    plt.close()

    plt.figure()
    plt.plot(history.history.get('accuracy', []), label='train_acc')
    plt.plot(history.history.get('val_accuracy', []), label='val_acc')
    plt.legend(); plt.title("Accuracy")
    plt.savefig(os.path.join(evdir, "accuracy.png")); plt.close()

    plt.figure()
    plt.plot(history.history.get('loss', []), label='train_loss')
    plt.plot(history.history.get('val_loss', []), label='val_loss')
    plt.legend(); plt.title("Loss")
    plt.savefig(os.path.join(evdir, "loss.png")); plt.close()

    with open(os.path.join(evdir, "classification_report.json"), "w", encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("Evaluation saved in", evdir)
    print("All done.")


# Solo ejecuta el entrenamiento si este archivo se corre directamente
if __name__ == "__main__":
    main()
