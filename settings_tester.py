#!/usr/bin/env python3
# sweep_picam_settings.py
from picamera2 import Picamera2
import time, os, csv, json, uuid
from datetime import datetime

# === Carpetas de salida ===
OUT_DIR = "barrido_configuraciones"
IMG_DIR = os.path.join(OUT_DIR, "imgs")
META_DIR = os.path.join(OUT_DIR, "meta")
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# === Barridos (ajústalos a tu escena) ===
# Tiempos de obturador en microsegundos (1/2000s=500, 1/1000s=1000, 1/500s=2000, 1/100s=10000, etc.)
EXPOSURES_US = [500, 1000, 2000]      # empieza corto para congelar pelota
# Ganancias analógicas (≈ ISO). 1.0 es bajo, 2.0-4.0 suben brillo (y ruido).
GAINS = [1.0, 1.5, 2.0, 3.0, 4.0]

# Opcionales (puedes dejar uno solo si no quieres barrer tanto)
SATURATIONS = [1.0, 1.2]          # 1.0 = por defecto
CONTRASTS   = [1.0, 1.2]          # 1.0 = por defecto
COLOUR_GAINS = [(1.0, 1.0)]       # (R, B). Puedes probar (1.2, 1.2) para colores más vivos

# ¿Usar auto white balance? Mejor manual para escenas blanco/negro (fondo negro)
AWB_ENABLE = False

# Pausa para que la cámara estabilice tras cambiar controles
STABILIZE_S = 0.15

# === Inicializar cámara ===
picam2 = Picamera2()
cfg = picam2.create_still_configuration()
picam2.configure(cfg)
picam2.start()

# Registrar cabecera del manifest
manifest_path = os.path.join(OUT_DIR, "manifest.csv")
with open(manifest_path, "w", newline="") as fcsv:
    writer = csv.writer(fcsv)
    writer.writerow([
        "filename","timestamp_iso",
        "ExposureTime_us","AnalogueGain","FrameDuration_us_min","FrameDuration_us_max",
        "Saturation","Contrast","ColourGains_R","ColourGains_B","AwbEnable",
        # algunos metadatos reportados por el sensor (si están disponibles)
        "meta_ExposureTime","meta_AnalogueGain","meta_DigitalGain","meta_FrameDuration",
        "meta_ColourTemperature","meta_SensorTemperature","meta_Lux"
    ])

    uid = uuid.uuid4().hex[:8]

    for exp in EXPOSURES_US:
        # FrameDuration >= ExposureTime para que no “estire” el frame
        frame_us = max(500, exp)  # mínimo 500us para evitar rarezas
        for gain in GAINS:
            for sat in SATURATIONS:
                for con in CONTRASTS:
                    for cg_r, cg_b in COLOUR_GAINS:
                        # Controles totalmente manuales para evitar que “auto” oscurezca/aclarare solo
                        controls = {
                            "AeEnable": False,
                            "AwbEnable": AWB_ENABLE,
                            "ExposureTime": int(exp),
                            "AnalogueGain": float(gain),
                            "FrameDurationLimits": (int(frame_us), int(frame_us)),
                            "Saturation": float(sat),
                            "Contrast": float(con),
                            "ColourGains": (float(cg_r), float(cg_b))
                        }
                        picam2.set_controls(controls)
                        time.sleep(STABILIZE_S)

                        # Nombre del archivo con settings codificados
                        name = f"{uid}_exp{exp}us_gain{gain}_fd{frame_us}us_sat{sat}_con{con}_cg{cg_r}-{cg_b}_awb{int(AWB_ENABLE)}.jpg"
                        img_path = os.path.join(IMG_DIR, name)

                        # Capturar
                        picam2.capture_file(img_path)

                        # Metadatos reales tras la captura (útil para confirmar lo aplicado)
                        meta = picam2.capture_metadata()  # puede devolver la última metadata conocida
                        # A veces es mejor hacer una captura "dummy" de metadata, pero suele bastar
                        meta = meta or {}

                        # Guardar metadatos JSON por imagen
                        meta_path = os.path.join(META_DIR, name.replace(".jpg", ".json"))
                        with open(meta_path, "w") as fj:
                            json.dump({"controls": controls, "metadata": meta}, fj, indent=2)

                        # Registrar en manifest.csv
                        writer.writerow([
                            name,
                            datetime.now().isoformat(timespec="seconds"),
                            exp, gain, frame_us, frame_us,
                            sat, con, cg_r, cg_b, int(AWB_ENABLE),
                            meta.get("ExposureTime"),
                            meta.get("AnalogueGain"),
                            meta.get("DigitalGain"),
                            meta.get("FrameDuration"),
                            meta.get("ColourTemperature"),
                            meta.get("SensorTemperature"),
                            meta.get("Lux")
                        ])
                        print("✅", name)

picam2.close()
print(f"\nListo. Imágenes en: {IMG_DIR}\nManifest: {manifest_path}\nMetadatos: {META_DIR}")
