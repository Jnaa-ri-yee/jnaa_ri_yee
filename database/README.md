# Database – Dataset de Lengua de Señas

Este repositorio contiene la estructura, scripts y configuración para trabajar con un dataset de lengua de señas, organizado por:

- Alfabeto  
  - Consonantes (b, c, d, f, g, …, z, ñ)  
  - Vocales (a, e, i, o, u)  
- Frases (como-estas, de-nada, me-llamo, mucho-gusto)  
- Palabras  
  - Cortesía (disculpa, gracias, perdon, por-favor)  
  - Saludos (hola, adios, buenos-dias, buenas-tardes, buenas-noches)

La estructura completa de carpetas se incluye en el repositorio, aunque muchas de ellas estén vacías.

---

## 📷 Sobre las imágenes del dataset

Este proyecto cuenta con un dataset real de aproximadamente:

> **500 imágenes** de personas realizando señas.

Sin embargo:

- Por **protección de la identidad y privacidad** de las personas que colaboraron,
- Y por respeto a los acuerdos de uso del material,

🔒 **Las imágenes no se incluyen en este repositorio público/compartido.**

En su lugar:

- Se mantiene únicamente la **estructura de carpetas vacías**.
- Las imágenes reales se gestionan de forma privada y segura.
- Los scripts y servicios del proyecto están preparados para trabajar con esas imágenes cuando se agregan en un entorno autorizado.

---

## 📁 Estructura del proyecto
```
database/
├── datasets/ # Estructura del dataset (sin imágenes por privacidad)
├── generated/ # Archivos generados automáticamente
├── prisma/ # Esquema y migraciones de base de datos
├── src/ # Código fuente (servicios, utilidades, importadores)
├── package.json # Configuración del proyecto Node/TS
└── tsconfig.json # Configuración TypeScript
```


---

## ⚠️ Importante

Si deseas usar este proyecto con datos reales:

1. Debes contar con autorización para usar las imágenes.
2. Coloca las imágenes en las carpetas correspondientes dentro de `database/datasets/`.
3. Respeta siempre la privacidad y el consentimiento de las personas que aparecen en el dataset.

---

## 🎯 Objetivo del proyecto

Este repositorio busca:

- Facilitar la organización de datasets de lengua de señas.
- Proveer herramientas para importar, procesar y gestionar imágenes.
- Mantener buenas prácticas de ética, privacidad y protección de datos.
