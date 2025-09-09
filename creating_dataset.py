from picamera2 import Picamera2, Preview
import time
import uuid
import os

OUTPUT_DIR = "fotos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

INTERVALO = 0.05
NUM_FOTOS = 40

# Inicializar cámara
picam2 = Picamera2()
camera_config_preview = picam2.create_preview_configuration()
camera_config = picam2.create_still_configuration()
picam2.configure(camera_config_preview)
picam2.start_preview(Preview.QTGL)

picam2.start()

picam2.set_controls({
    "ExposureTime": 1000, 
    #"AeEnable": False,
    #"AwbEnable": False,
    #"AnalogueGain":1.0 , 
    "Brightness": 0.1,
    #"Contrast":1.0,
    "Saturation":1.2,
    #"FrameDurationLimits":(2000,2000),
    "ColourGains":(float(1.0),float(1.0)),
    #"AwbMode":2
})
time.sleep(0.5)

print(f"📷 Tomando {NUM_FOTOS} fotos cada {INTERVALO} segundos...")
run_id= uuid.uuid4()
os.makedirs(f"{OUTPUT_DIR}/{str(run_id)}", exist_ok=True)

cycles = 10

for j in range(0, cycles):
    for i in range(1, NUM_FOTOS + 1):
        nombre = f"{run_id}/{i}.jpg"
        ruta = os.path.join(OUTPUT_DIR, nombre)

        picam2.capture_file(ruta)
        print(f"✅ Foto {i} guardada en {ruta}")

        time.sleep(INTERVALO)
    
    time.sleep(1)
    print("3-"*20)
    time.sleep(1)
    print("2-"*20)
    time.sleep(1)
    print("1-"*20)

print("✨ Captura finalizada")
picam2.close()
