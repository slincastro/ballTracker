from picamera2 import Picamera2
import time
import uuid
import os

# 📂 Carpeta donde se guardarán las fotos
OUTPUT_DIR = "fotos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ⏱️ Intervalo entre fotos (segundos)
INTERVALO = 5

# 📸 Número total de fotos a tomar
NUM_FOTOS = 10

# Inicializar cámara
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

print(f"📷 Tomando {NUM_FOTOS} fotos cada {INTERVALO} segundos...")

for i in range(1, NUM_FOTOS + 1):
    # Generar nombre con UUID y número de foto
    nombre = f"{uuid.uuid4()}-{i}.jpg"
    ruta = os.path.join(OUTPUT_DIR, nombre)

    # Capturar y guardar
    picam2.capture_file(ruta)
    print(f"✅ Foto {i} guardada en {ruta}")

    # Esperar antes de la siguiente
    time.sleep(INTERVALO)

print("✨ Captura finalizada")
picam2.close()
