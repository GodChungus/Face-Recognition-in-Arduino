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

authorizedPeople = [
    "Prakrit", "Ira", "Aaravi", "Aarush", "Anit", "Areena", "Asal", "Bishal", "Brazen", "Celsa", "Deepson",
    "Jasmine", "Kaben", "Megsha", "Modika", "Rajan", "Sujan", "Sukriti", "Surasa", "Suyog", "Upashak", "Yulene"
]

detectorModel = "Facenet"
detector = "opencv"
distThreshold = 0.45   # stricter

serialPort = "COM7"
baudRate = 9600

checkInterval = 1.0 # Seconds between recognition
resizeScale = 0.4

requiredTime = 2.5   # seconds needed to confirm identity

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

current_candidate = None
candidate_start_time = None

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

                    if detected_name == current_candidate:
                        elapsed = time.time() - candidate_start_time
                        if elapsed >= requiredTime:
                            name = detected_name
                            authorized = True
                        else:
                            name = f"Verifying {detected_name}..."
                            authorized = False
                    else:
                        current_candidate = detected_name
                        candidate_start_time = time.time()
                        name = f"Verifying {detected_name}..."
                        authorized = False
                else:
                    current_candidate = None
                    candidate_start_time = None
                    name = "Unknown"
                    authorized = False
            else:
                # No face detected
                current_candidate = None
                candidate_start_time = None
                name = "Unknown"
                authorized = False

        except Exception:
            current_candidate = None
            candidate_start_time = None
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
    if authorized:
        color = (0, 255, 0)
    elif "Verifying" in name:
        color = (0, 255, 255)
    else:
        color = (0, 0, 255)

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
