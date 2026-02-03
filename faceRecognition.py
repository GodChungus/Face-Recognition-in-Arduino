import cv2
import time
import os
import serial
import io
from deepface import DeepFace
from contextlib import redirect_stdout, redirect_stderr

# ========================================================
# Settings
# ========================================================
db_path = "faces"
authorizedPeople = ["Prakrit", "Ira"]

detectorModel = "Facenet"
detector = "mtcnn"
distThreshold = 0.9

serialPort = "COM7"
baudRate = 9600

checkInterval = 0.5 # Seconds between recognition
resizeScale = 0.5

arduino = serial.Serial(serialPort, baudRate, timeout=1)
time.sleep(2)

# ========================================================
# Camera Setup
# ========================================================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

last_check = 0
last_sent = None

name = "Unknown"
authorized = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # ========================================================
    # Face recognition code
    # ========================================================
    if time.time() - last_check > checkInterval:
        last_check = time.time()

        try:
            small_frame = cv2.resize(
                frame, (0, 0),
                fx=resizeScale,
                fy=resizeScale
            )

            f = io.StringIO()
            with redirect_stdout(f), redirect_stderr(f):
                results = DeepFace.find(
                    img_path=small_frame,
                    db_path=db_path,
                    model_name=detectorModel,
                    detector_backend=detector,
                    distance_metric="cosine",
                    enforce_detection=True
                )

            if len(results) > 0 and not results[0].empty:
                top = results[0].iloc[0]
                distance = top["distance"]
                identity_path = top["identity"]
                detected_name = os.path.basename(os.path.dirname(identity_path))

                if distance < distThreshold and detected_name in authorizedPeople:
                    name = detected_name
                    authorized = True
                else:
                    name = "Unknown"
                    authorized = False
            else:
                # No face detected
                name = "Unknown"
                authorized = False


        except Exception:
            name = "Unknown"
            authorized = False

    # ========================================================
    # Sends signal if and only if the state changes
    # ========================================================
    signal = "1" if authorized else "0"
    if signal != last_sent:
        arduino.write((signal + "\n").encode())
        last_sent = signal

    # ========================================================
    # Adding text to the screen
    # ========================================================
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
