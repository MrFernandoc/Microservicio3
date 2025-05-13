import pymongo
import random
from datetime import datetime
from tqdm import tqdm  # Barra de progreso

# Conexión a MongoDB
client = pymongo.MongoClient('mongodb://172.31.23.130:27017/')  # URI de tu MongoDB
db = client['lab_exams_db']  # Nombre de la base de datos
examenes_collection = db['examenes']  # Nombre de la colección donde se guardarán los exámenes

# Tipos de examen
tipos_examen = [
    "Sangre", "Radiografía", "Tomografía", "Ultrasonido", "Electrocardiograma",
    "COVID", "Orina", "Biopsia", "Colesterol", "Hígado"
]

# Lógica del resultado según tipo
def generar_resultado(tipo):
    if tipo == "Sangre":
        return {
            "Hemoglobina": f"{round(random.uniform(12, 17), 1)} g/dL",
            "Glóbulos blancos": f"{random.randint(4000, 11000)} /µL",
            "Plaquetas": f"{random.randint(150000, 450000)} /µL"
        }
    elif tipo == "Radiografía":
        return {
            "Observación": random.choice(["Sin fracturas", "Lesión detectada", "Neumonía sospechosa"])
        }
    elif tipo == "Tomografía":
        return {
            "Área analizada": random.choice(["Craneo", "Tórax", "Abdomen"]),
            "Resultado": random.choice(["Normal", "Anomalía detectada"])
        }
    elif tipo == "Ultrasonido":
        return {
            "Hígado": random.choice(["Normal", "Inflamado"]),
            "Riñones": random.choice(["Normal", "Piedras detectadas"])
        }
    elif tipo == "Electrocardiograma":
        return {
            "Ritmo": random.choice(["Normal", "Arritmia"]),
            "Frecuencia": f"{random.randint(60, 100)} bpm"
        }
    elif tipo == "COVID":
        return {
            "Resultado": random.choice(["Positivo", "Negativo"]),
            "Carga viral": f"{random.randint(1000, 100000)} copias/mL"
        }
    elif tipo == "Orina":
        return {
            "Color": random.choice(["Amarillo", "Ámbar", "Claro"]),
            "Proteínas": random.choice(["Negativo", "Traza", "Positivo"]),
            "Glucosa": random.choice(["Negativo", "Positivo"])
        }
    elif tipo == "Biopsia":
        return {
            "Diagnóstico": random.choice(["Benigno", "Maligno"]),
            "Inflamación": random.choice(["Presente", "Ausente"])
        }
    elif tipo == "Colesterol":
        return {
            "LDL": f"{random.randint(70, 190)} mg/dL",
            "HDL": f"{random.randint(40, 90)} mg/dL",
            "Triglicéridos": f"{random.randint(100, 250)} mg/dL"
        }
    elif tipo == "Hígado":
        return {
            "ALT": f"{random.randint(10, 50)} U/L",
            "AST": f"{random.randint(10, 40)} U/L",
            "Bilirrubina": f"{round(random.uniform(0.3, 1.2), 1)} mg/dL"
        }
    else:
        return {"Observación": "Sin resultados"}

# Creador de examen
def crear_examen(id_examen):
    tipo_examen = random.choice(tipos_examen)
    fecha = datetime.now().isoformat()
    estado = random.choice(["pendiente", "completado", "cancelado"])

    return {
        "pacienteId": str(random.randint(10000000, 99999999)),
        "medicoId": str(random.randint(1, 100)),
        "tipoExamen": tipo_examen,
        "fecha": fecha,
        "estado": estado,
        "resultado": generar_resultado(tipo_examen),
        "comentarios": f"Observación general del examen {id_examen}" if random.random() > 0.2 else None
    }

# Envío masivo con barra de progreso
errores = []

for i in tqdm(range(1, 101), desc="Insertando exámenes"):
    examen = crear_examen(i)
    try:
        # Insertar examen directamente en la colección de MongoDB
        examen_id = examenes_collection.insert_one(examen).inserted_id
        if not examen_id:
            errores.append((i, "InsertError", "No se insertó el examen"))
    except pymongo.errors.PyMongoError as e:
        errores.append((i, "MongoDBError", str(e)))

# Reporte final
print(f"\n✅ Finalizado. Total de errores: {len(errores)}")
if errores:
    with open("errores_insert.txt", "w", encoding="utf-8") as f:
        for e in errores:
            f.write(f"Examen {e[0]} - Error: {e[1]} - {e[2]}\n")
    print("❌ Errores guardados en 'errores_insert.txt'")
