# ======================================================                     *
#  Project      : algorithms                                                 *
#  File         : model.py                                                   *
#  Team         : Equipo Jña'a Ri Y'ë'ë                                      *
#  Developer    : Axel Eduardo Urbina Secundino                              *
#  Created      : 2025-10-30                                                 *
#  Last Updated : 2026-01-17 16:20                                           *
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

# model/model.py
import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image as kimage
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from PIL import Image
import io
import joblib

class DLClassifier:
    """Deep learning classifier using MobileNetV2 base + head."""
    def __init__(self, model_path=None, input_shape=(224,224,3)):
        self.input_shape = input_shape
        self.model = None
        if model_path:
            self.load(model_path)

    def build(self, num_classes, base_trainable=False):
        base = MobileNetV2(weights='imagenet', include_top=False, input_shape=self.input_shape)
        base.trainable = base_trainable
        x = base.output
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(256, activation='relu')(x)
        x = layers.Dropout(0.4)(x)
        out = layers.Dense(num_classes, activation='softmax')(x)
        model = models.Model(inputs=base.input, outputs=out)
        model.compile(optimizer=tf.keras.optimizers.Adam(1e-4),
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
        self.model = model
        self._base = base
        return model

    def load(self, model_path):
        self.model = tf.keras.models.load_model(model_path)
        return self.model

    def predict_proba(self, np_image_batch):
        """np_image_batch: shape (N,h,w,3) normalized [0,1]"""
        if self.model is None:
            raise ValueError("DL model not loaded")
        #asegurar que la entrada está preprocesada
        x = preprocess_input(np_image_batch * 255.0)
        preds = self.model.predict(x, verbose=0)
        return preds


class FeatureExtractor:
    """Extract embeddings from MobileNetV2 base (global average pooled)."""
    def __init__(self, input_shape=(224,224,3)):
        self.input_shape = input_shape
        self.base = MobileNetV2(weights='imagenet', include_top=False, input_shape=input_shape)
        # We'll output GAP features
        inp = self.base.input
        x = self.base.output
        x = layers.GlobalAveragePooling2D()(x)
        self.model = models.Model(inputs=inp, outputs=x)

    def extract(self, np_image_batch):
        """Return 2D features array (N, features)"""
        x = preprocess_input(np_image_batch * 255.0)
        feats = self.model.predict(x, verbose=0)
        return feats


class MLClassifier:
    """Wrapper to save/load sklearn classifier (RandomForest)"""
    def __init__(self, model_path=None):
        self.clf = None
        if model_path:
            self.load(model_path)

    def fit(self, X, y):
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=200, n_jobs=-1, random_state=42)
        clf.fit(X, y)
        self.clf = clf
        return clf

    def predict_proba(self, X):
        if self.clf is None:
            raise ValueError("ML classifier not trained/loaded")
        return self.clf.predict_proba(X)

    def save(self, path):
        joblib.dump(self.clf, path)

    def load(self, path):
        self.clf = joblib.load(path)
        return self.clf


# Utility helpers
def load_class_names(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def preprocess_pil_image_bytes(image_bytes, target_size=(224,224)):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(target_size)
    arr = np.asarray(img).astype('float32') / 255.0
    return arr  # shape (h,w,3)
