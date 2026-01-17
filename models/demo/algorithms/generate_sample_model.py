import tensorflow as tf
from tensorflow.keras import layers, models
import os, json

# Configuracion
output_dir = "models/"
os.makedirs(output_dir, exist_ok=True)

num_classes = 5
img_size = (224, 224, 3)
class_names = ['A', 'E', 'I', 'O', 'U']

# Modelo simple
model = models.Sequential([
    layers.Input(shape=img_size),
    layers.Conv2D(16, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D(2,2),

    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.save(os.path.join(output_dir, "vowels_model.h5"))

# Guardar clases
with open(os.path.join(output_dir, "class_names.json"), "w") as f:
    json.dump(class_names, f, indent=4)

print("Modelo de muestra y clases generadas correctamente.")
