# Jña'a ri y'ë'ë 🤟

Sistema de reconocimiento de Lengua de Señas Mexicana (LSM) mediante visión por computadora e inteligencia artificial

## 📋 Tabla de Contenidos
- [Descripción General](#-descripción-general)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Repositorios del Proyecto](#-repositorios-del-proyecto)
- [Estado Actual del Desarrollo](#-estado-actual-del-desarrollo)
- [Componentes del Sistema](#-componentes-del-sistema)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## 🎯 Descripción General

Jña'a ri y'ë'ë es un proyecto integral diseñado para facilitar la comunicación entre personas que utilizan la Lengua de Señas Mexicana (LSM) y aquellas que no la conocen. El sistema utiliza técnicas avanzadas de visión por computadora y aprendizaje automático para reconocer y traducir señas en tiempo real.

El nombre "Jña'a Ri Y'ë'ë" proviene del MAZAHUA y donde "Jña'a" significa hablar, continua "Ri" que es el modo indicativo y finalmente encontramos el sustantivo "Y'ë'ë",a tra vez de esta frase se comprende de forma figurativa la acción las manos hablan o en su forma retórica corresponde a "La Mano Que Habla".

### 🎯 Objetivo del Proyecto

Desarrollar una plataforma accesible y precisa que permita:
- Reconocimiento en tiempo real de señas LSM
- Traducción bidireccional entre LSM y español escrito/hablado
- Aprendizaje interactivo de LSM para personas oyentes
- Preservación y digitalización del lenguaje de señas mexicano

## 🏗️ Arquitectura del Proyecto

El proyecto Jnaa-ri-yee está organizado en un ecosistema modular que facilita el desarrollo y la escalabilidad:

### Estructura General

```
Jnaa-ri-yee/
├── Demo          → Prototipo funcional y validación de conceptos
├── Web           → Plataforma web y comunidad
├── App           → Aplicación móvil multiplataforma
└── Server        → Infraestructura backend y modelos ML
```

### Repositorios del Ecosistema

| Repositorio | Descripción | Estado |
|------------|-------------|--------|
| **Demo** | Prototipo inicial con reconocimiento de alfabeto LSM | ✅ Funcional |
| **Web** | Sitio web institucional y plataforma comunitaria | ✅ Funcional |
| **App** | Aplicación móvil Flutter (Android, iOS, Web) | 🚧 En desarrollo |
| **Server** | Backend con API REST y modelos de IA | ✅ Funcional |

## 📂 Repositorios del Proyecto

### 1️⃣ Repositorio Demo
**Prototipo Funcional - Fase 1**
[text](https://github.com/AEUS-06/jnaa_ri_yee)

Sistema de demostración que valida el concepto técnico del reconocimiento de señas LSM.

**Características:**
- Reconocimiento de alfabeto LSM (vocales: A, E, I, O, U)
- Modelos de Machine Learning (Random Forest y CNN)
- Interfaz gráfica de prueba
- Sistema de evaluación y métricas de precisión
- Dataset de entrenamiento con más de 100 muestras por letra

**Tecnologías principales:**
- Python + TensorFlow/Keras para modelos CNN
- scikit-learn para modelos clásicos
- Flask/FastAPI para API REST
- OpenCV para procesamiento de imágenes

### 2️⃣ Repositorio Web
**Plataforma Institucional y Comunidad**
[text](link)

Sitio web que sirve como punto central de información y colaboración del proyecto.

**Secciones principales:**
- **Inicio**: Presentación del proyecto y demostración interactiva
- **Sobre el Proyecto**: Historia, objetivos y equipo
- **Comunidad**: Blog, noticias y recursos educativos
- **Contacto**: Formulario para voluntarios y colaboradores
- **Donaciones**: Sistema de apoyo al proyecto
- **Dataset**: Portal para contribución de datos

**Características técnicas:**
- Aplicación Next.js con TypeScript
- Sistema de autenticación (NextAuth)
- Base de datos PostgreSQL con Prisma ORM
- Sistema de badges y reconocimientos para colaboradores
- API RESTful para integración con otros componentes

### 3️⃣ Repositorio App
**Aplicación Móvil Multiplataforma**
***Este mismo repositorio***

Aplicación construida con Flutter para uso en producción del sistema de reconocimiento LSM.

**Funcionalidades planificadas:**
- Cámara en tiempo real para reconocimiento de señas
- Traducción instantánea LSM ↔ Español
- Modo de aprendizaje interactivo
- Historial de traducciones
- Perfil de usuario y progreso

**Plataformas objetivo:**
- Android
- iOS
- Web
- Desktop (Windows, macOS, Linux)

### 4️⃣ Repositorio Server
**Infraestructura Backend y Modelos ML**
[text](https://github.com/Jnaa-ri-yee)

Servidor de producción desplegado en Raspberry Pi 5 con arquitectura containerizada.

**Componentes:**
- **API REST**: Endpoints para reconocimiento y entrenamiento
- **Modelos ML/DL**: 
  - Random Forest para clasificación clásica
  - CNN (Redes Neuronales Convolucionales) para vocales
  - Sistema de versionado de modelos
- **Sistema de evaluación**: Métricas, matrices de confusión, reportes
- **Logging**: Monitoreo y trazabilidad del sistema

**Infraestructura:**
- Raspberry Pi 5 (8GB RAM)
- Docker + Docker Compose
- Python 3.12+ con TensorFlow/Keras
- Sistema de almacenamiento optimizado

## 🚀 Estado Actual del Desarrollo

### Fase 1 - Prototipo (Completada ✅)
- ✅ Reconocimiento funcional del alfabeto LSM (vocales)
- ✅ Modelos base entrenados con 95%+ de precisión
- ✅ Interfaz de demostración operativa
- ✅ Pipeline de entrenamiento establecido

### Fase 2 - Sistema Completo (En Progreso 🚧)
- ✅ Sitio web operativo
- ✅ Backend con API REST funcional
- ✅ Modelos ML desplegados en producción
- 🚧 Aplicación móvil multiplataforma
- 🚧 Expansión del dataset (alfabeto completo)
- ⏳ Reconocimiento de palabras y frases

### Fase 3 - Producción (Planeada 📋)
- 📋 Lanzamiento público de la aplicación
- 📋 Sistema de feedback de usuarios
- 📋 Expansión masiva de vocabulario LSM
- 📋 Optimización y escalabilidad

## 🧩 Componentes del Sistema

### Sistema Web (Next.js)

La plataforma web incluye:

**Frontend:**
- Páginas públicas (inicio, proyecto, comunidad, contacto)
- Sistema de autenticación seguro
- Blog con artículos sobre LSM y Desarrollo de la APP
- Portal de contribución de datasets

**Backend:**
- API RESTful con endpoints seguros
- Gestión de usuarios y sesiones
- Sistema de badges para colaboradores
- Validación y sanitización de datos
- Protección CSRF

### Aplicación Móvil (Flutter)

Estructura modular con:
- Pantallas principales (Home, Cámara, Información)
- Servicios de comunicación con API
- Sistema de navegación fluido
- Widgets reutilizables y animaciones

### Servidor Backend (Python + Docker)

Arquitectura de microservicios:
- API principal de reconocimiento
- Sistema de modelos ML/DL
- Gestión de datasets de entrenamiento
- Logs y monitoreo centralizado

## 🛠️ Tecnologías Utilizadas

### Frontend
- **Flutter** - Framework multiplataforma para app móvil
- **Next.js** - Framework React para sitio web
- **TypeScript** - Lenguaje tipado para web
- **Tailwind CSS** - Estilos y diseño responsivo

### Backend
- **Python** - Lenguaje principal para ML
- **Node.js + TypeScript** - Runtime para API web
- **FastAPI/Flask** - Framework para API de modelos
- **Prisma ORM** - Gestión de base de datos
- **PostgreSQL** - Base de datos relacional

### Machine Learning
- **TensorFlow/Keras** - Redes neuronales profundas
- **scikit-learn** - Modelos clásicos de ML
- **OpenCV** - Procesamiento de imágenes
- **NumPy, Pandas** - Manipulación de datos

### Infraestructura
- **Docker** - Contenedorización de servicios
- **Raspberry Pi 5** - Servidor de producción
- **Git** - Control de versiones

## 📊 Datasets

### Estructura de Datos

El proyecto maneja diferentes categorías de datos:

**Alfabeto LSM:**
- Vocales: A, E, I, O, U (cada una con 100+ muestras)
- Consonantes: B-Z, Ñ (en expansión)

**Formato de Imágenes:**
- Resolución preferida: 640x640 píxeles
- Formatos: JPG, JPEG, PNG
- Nomenclatura estructurada para organización

**Recolección de Datos:**
- Contribución comunitaria a través de la web
- Validación y etiquetado manual
- Diversidad de personas, iluminación y ángulos
- Implementación de videos

## 📈 Roadmap

### Q1 2026
- ✅ Lanzamiento del sitio web institucional
- ✅ Backend funcional con modelos de vocales
- 🚧 Expansión del dataset de alfabeto completo
- 🚧 Beta de aplicación móvil

### Q2 2026
- 📋 Dataset de palabras comunes (100+ palabras)
- 📋 Modelos de reconocimiento de palabras
- 📋 Lanzamiento beta público de la app
- 📋 Sistema de feedback y mejora continua

### Q3 2026
- 📋 Dataset de frases (50+ frases)
- 📋 Reconocimiento de secuencias temporales
- 📋 Optimización de rendimiento

### Q4 2026
- 📋 Expansión de vocabulario LSM
- 📋 Funciones avanzadas (traducción inversa)
- 📋 Programa de embajadores y difusión

## 👥 Contribución

### Formas de Colaborar

El proyecto necesita apoyo en múltiples áreas:

#### 📸 Recolección de Datos
- Grabación de señas LSM
- Diversidad de personas y contextos
- Validación de calidad de datos

#### 🤖 Machine Learning
- Investigación de nuevos algoritmos
- Optimización de modelos existentes
- Evaluación y métricas

#### 💻 Desarrollo
- Frontend (Flutter, Next.js)
- Backend (Python, Node.js)
- Infraestructura y DevOps

#### 📝 Documentación
- Tutoriales y guías
- Traducción de contenidos
- Material educativo sobre LSM

#### 🎨 Diseño
- UI/UX para aplicaciones
- Material gráfico y multimedia
- Experiencia de usuario

#### 🌐 Difusión
- Redes sociales
- Eventos y talleres
- Relaciones con instituciones

### Proceso de Colaboración

Para colaborar con el proyecto, por favor contacta al equipo a través de:
- Formulario de contacto en el sitio web
- Email oficial del proyecto
- Redes sociales

**Nota importante:** Este repositorio está disponible únicamente para evaluación académica y técnica. No está permitido copiar, modificar o redistribuir el código sin autorización previa del equipo Jña'a Ri Y'ë'ë.

## 📄 Licencia

```
Copyright (c) 2026
Equipo / Team: Jña'a Ri Y'ë'ë

Todos los derechos reservados.
All rights reserved.

────────────────────────────────────────────────────────────
ESPAÑOL
────────────────────────────────────────────────────────────

Este software y su código fuente son propiedad exclusiva del equipo Jña'a Ri Y'ë'ë.

Se permite el acceso público al repositorio únicamente con fines de:
- Evaluación académica
- Revisión técnica
- Participación en convocatorias, hackatones o concursos

Queda estrictamente prohibido:
- Copiar total o parcialmente el código
- Modificarlo o crear obras derivadas
- Redistribuirlo en cualquier forma
- Usarlo con fines comerciales o no comerciales
- Entrenar o reentrenar modelos basados en este código

Cualquier uso fuera de los permitidos requiere autorización previa y por escrito 
del equipo Jña'a Ri Y'ë'ë.

El software se proporciona "tal cual", sin garantías de ningún tipo, expresas o 
implícitas.

────────────────────────────────────────────────────────────
ENGLISH
────────────────────────────────────────────────────────────

This software and its source code are the exclusive property of the Jña'a Ri Y'ë'ë 
team.

Public access to this repository is granted solely for the purposes of:
- Academic evaluation
- Technical review
- Participation in calls for proposals, hackathons, or competitions

The following actions are strictly prohibited:
- Copying the code, in whole or in part
- Modifying it or creating derivative works
- Redistributing it in any form
- Using it for commercial or non-commercial purposes
- Training or retraining models based on this code

Any use beyond the permitted purposes requires prior written authorization from 
the Jña'a Ri Y'ë'ë team.

This software is provided "as is", without warranty of any kind, express or implied.
```

## 🎓 Contexto Académico

Este proyecto forma parte de un equipo de 6 estudiantes que trata de desarollar:
- Aplicaciones de IA para inclusión social
- Procesamiento de lenguaje de señas con visión por computadora
- Tecnología asistiva y accesibilidad
- Preservación digital de lenguas de señas

## 📞 Contacto

- **Sitio Web**: [En construcción]
- **Email**: [jnaariyee@gmail.com]
- **Redes Sociales**: [Enlaces en desarrollo]

## 🙏 Agradecimientos

- Intérpretes certificados de LSM
- Colaboradores y voluntarios del proyecto
- Instituciones educativas de apoyo

---

**Hecho con ❤️ para hacer el mundo más inclusivo**

---

*Última actualización: Enero 2026*
