import os
import random
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import mysql.connector

# Inicializar FastAPI
app = FastAPI(title="AgroIA Backend Ajustado a BD")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", #desarrollo local
                  "https://agro-ia-frontend-osy7.vercel.app",
                  ],  # en producción restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Carpeta uploads
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Config BD (ajusta con tu pass)
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",   # sin contraseña
    "database": "agroia_consciente"
}

@app.get("/")
def home():
    return {"msg": "Backend AgroIA funcionando ✅"}

@app.post("/api/upload")
async def upload_image(
    id_usuario: int = Form(...),
    id_lote: int = Form(...),
    file: UploadFile = File(...)
):
    try:
        # Guardar imagen en uploads/
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        with open(filepath, "wb") as f:
            f.write(await file.read())

        # Diagnóstico simulado
        enfermedades = ["Oídio", "Tizón tardío", "Roya", "Antracnosis", "Sano"]
        enfermedad_detectada = random.choice(enfermedades)
        probabilidad = round(random.uniform(70, 99), 2)
        recomendacion = f"Revisar tratamiento para '{enfermedad_detectada}'."

        # Conectar BD
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1️⃣ Insertar en historial
        cursor.execute(
            "INSERT INTO historial (id_usuario, id_lote, diagnostico, recomendacion, fecha) VALUES (%s, %s, %s, %s, %s)",
            (id_usuario, id_lote, enfermedad_detectada, recomendacion, datetime.now())
        )
        id_historial = cursor.lastrowid

        # 2️⃣ Insertar en diagnostico
        cursor.execute(
            "INSERT INTO diagnostico (id_historial, descripcion, fecha) VALUES (%s, %s, %s)",
            (id_historial, f"Imagen procesada: {filename}", datetime.now())
        )

        # 3️⃣ Insertar en recomendacion
        cursor.execute(
            "INSERT INTO recomendacion (id_historial, contenido, fecha) VALUES (%s, %s, %s)",
            (id_historial, recomendacion, datetime.now())
        )

        conn.commit()
        cursor.close()
        conn.close()

        return JSONResponse(content={
            "usuario": id_usuario,
            "lote": id_lote,
            "diagnostico": enfermedad_detectada,
            "probabilidad": probabilidad,
            "recomendacion": recomendacion,
            "archivo": filepath
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
