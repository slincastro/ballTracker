from picamera2 import Picamera2, Preview
import time, os, uuid

OUTPUT_DIR = "fotos_individual"
os.makedirs(OUTPUT_DIR, exist_ok=True)

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.set_controls({"ExposureTime": 500000, "AnalogueGain":1.0, "Brightness": -0.1})
picam2.start()

run_id= uuid.uuid4()

nombre = f"{run_id}.jpg"
ruta = os.path.join(OUTPUT_DIR, nombre)

    # Capturar y guardar
#picam2.capture_file(ruta)

time.sleep(200)

