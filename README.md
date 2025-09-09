# 🌱 AgroIA Consciente
**Tecnología que siembra soluciones**

Backend desarrollado en **FastAPI** para el proyecto *AgroIA Consciente*.  
La aplicación permite gestionar usuarios, lotes, diagnósticos y recomendaciones del sector agropecuario.  
Además, incluye un prototipo de carga de imágenes para diagnóstico asistido con IA.

---

## 📂 Estructura principal del proyecto

AgroIA_Consciente/
├─ main.py # Backend FastAPI
├─ requirements.txt # Dependencias Python
├─ Procfile # Comando para despliegue en Render
├─ .env.example # Ejemplo de variables de entorno
├─ static/
│ └─ upload.html # Formulario de prueba para subir imágenes
├─ uploads/ # Carpeta local para imágenes subidas
└─ docs/ # Diagramas y documentación


---

## ⚙️ Requisitos previos
- Python 3.10+  
- MySQL o MariaDB (local o en la nube)  
- Git instalado  

---

## 🚀 Ejecutar local (mínimo)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Javilaamaya97/AgroIA_Consciente.git
   cd AgroIA_Consciente

python -m venv .venv
.\.venv\Scripts\activate    # En Windows

pip install -r requirements.txt

copy .env.example .env
DB_HOST=localhost
DB_USER=root
DB_PASS=1234
DB_NAME=agroia_consciente
UPLOAD_DIR=uploads

uvicorn main:app --reload --port 8000
