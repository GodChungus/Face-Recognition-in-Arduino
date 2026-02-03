import cv2
from deepface import DeepFace
import io
from contextlib import redirect_stdout
import serial
import time
import os

# =======================================
# SETTINGS
# =======================================

DB_PATH = "faces"
MODEL_NAME = "Facenet512"
THRESHOLD = 0.5
DETECTOR = "retinaface"

AUTHORIZED_PEOPLE = ["Prakrit", "Ira"] # Folder names for authorized people
SERIAL_PORT = "COM7"
BAUD_RATE = 9600
# =======================================

arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

cap = cv2.VideoCapture(0)

last_sent = None  # avoid spamming

while True:
    ret, frame = cap.read()
    if not ret:
        break

    name = "Unknown"
    authorized = False

    try:
        f = io.StringIO()
        with redirect_stdout(f):
            results = DeepFace.find(
                img_path=frame,
                db_path=DB_PATH,
                model_name=MODEL_NAME,
                detector_backend=DETECTOR,
                distance_metric="cosine",
                enforce_detection=True,
                threshold=THRESHOLD
            )

        if len(results) > 0 and not results[0].empty:
            top_match = results[0].iloc[0]
            identity_path = top_match["identity"]
            name = os.path.basename(os.path.dirname(identity_path))

            if name in AUTHORIZED_PEOPLE:
                authorized = True

    except Exception:
        pass

    # =======================================
    # Sends signal to Arduino
    # =======================================
    signal = "1" if authorized else "0"
    if signal != last_sent:
        arduino.write((signal + "\n").encode())
        last_sent = signal

    # =======================================
    # Display text on screen
    # =======================================
    color = (0, 255, 0) if authorized else (0, 0, 255)
    cv2.putText(
        frame,
        name,
        (30, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        2
    )

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
