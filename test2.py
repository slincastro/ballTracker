from picamera2 import Picamera2
import time, uuid, os, numpy as np

OUT = "fotos"; os.makedirs(OUT, exist_ok=True)
SHUTTER_US = 1000         # 1/1000 s para congelar
GAIN_MIN, GAIN_MAX = 1.0, 8.0
TARGET_MEAN = 0.12        # brillo objetivo (0–1). Sube a 0.15–0.2 si quieres más claro
STEP = 0.5                # incremento de ganancia

picam2 = Picamera2()
cfg = picam2.create_still_configuration()
picam2.configure(cfg)
picam2.start()

# Modo 100% manual
picam2.set_controls({"AeEnable": False, "AwbEnable": False})
time.sleep(0.2)
picam2.set_controls({
    "ExposureTime": SHUTTER_US,
    "AnalogueGain": GAIN_MIN,
    "FrameDurationLimits": (SHUTTER_US, SHUTTER_US)
})

# Pequeño lazo: mide brillo y sube ISO hasta ver señal
gain = GAIN_MIN
for _ in range(20):
    # toma un frame rápido del sensor para medir brillo
    arr = picam2.capture_array()          # RGB np.array
    gray = np.dot(arr[..., :3], [0.2126, 0.7152, 0.0722]) / 255.0
    mean = float(gray.mean())
    if mean >= TARGET_MEAN or gain >= GAIN_MAX:
        break
    gain = min(gain + STEP, GAIN_MAX)
    picam2.set_controls({"AnalogueGain": gain})
    time.sleep(0.1)

# Captura final con el ISO que logró “levantar” señal
name = f"{uuid.uuid4().hex[:8]}_exp{SHUTTER_US}_gain{gain:.1f}.jpg"
picam2.capture_file(os.path.join(OUT, name))
print(f"✅ Capturada {name} (mean≈{mean:.3f}, gain={gain:.1f})")

picam2.close()
