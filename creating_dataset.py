from picamera2 import Picamera2, Preview
import time
import uuid
import os

# 📂 Carpeta donde se guardarán las fotos
OUTPUT_DIR = "fotos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ⏱️ Intervalo entre fotos (segundos)
INTERVALO = 0.1

# 📸 Número total de fotos a tomar
NUM_FOTOS = 50

shutter_time = 1000


# Inicializar cámara
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

picam2.set_controls({"ExposureTime": 1000, 
"AeEnable": False,
"AwbEnable": False,
"AnalogueGain":1.0 , 
"Brightness": -0.3,
"Contrast":1.0,
"Saturation":1.2,
"FrameDurationLimits":(2000,2000),
"ColourGains":(float(1.0),float(1.0)),
"AwbMode":2
})
time.sleep(0.5)
print(f"📷 Tomando {NUM_FOTOS} fotos cada {INTERVALO} segundos...")
run_id= uuid.uuid4()
for i in range(1, NUM_FOTOS + 1):
    # Generar nombre con UUID y número de foto
    nombre = f"{run_id}-{i}.jpg"
    ruta = os.path.join(OUTPUT_DIR, nombre)

    # Capturar y guardar
    picam2.capture_file(ruta)
    print(f"✅ Foto {i} guardada en {ruta}")

    # Esperar antes de la siguiente
    time.sleep(INTERVALO)

print("✨ Captura finalizada")
picam2.close()
