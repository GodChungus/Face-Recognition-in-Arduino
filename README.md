<div align="center">

# 👱🏻 Facial Recognition using Arduino

This project combines **Python**, **OpenCV**, **DeepFace**, and **Arduino**
to create a facial recognition door locking system. Once a face is
successfully verified, the Arduino unlocks the door by rotating a
servo motor. If the face is not recognized, the door remains locked.

This project uses **Python**, **OpenCV**, **DeepFace**, and **Arduino**
to create a facial recognition door locking/unlocking system. Once a
face is verified, the Arduino unlocks the door by rotating a servo motor
connected physically to the door to unlock it. If the face is not verified,
the door remains locked.

</div>

---

## 🐍 How It Works(Python)

* 📷 **OpenCV** opens the webcam and continuously captures video frames.
* 🧠 **DeepFace** analyzes each frame and scans the database to find matching faces.
* 🔌 **Serial** allows for communication between Python and the Arduino.
* ✅ When a face is successfully recognized for several consecutive frames, Python sends a **'1'** to the Arduino.
* ❌ If the face is not recognized, Python sends a **'0'**.

---

## ⚙️ How It Works(Arduino)

* 🟢 **Signal '1'**

  * Turns on the green LED.
  * Rotates the servo motor **90°**.
  * Unlocks the door.

* 🔴 **Signal '0'**

  * Turns on the red LED.
  * Returns (or keeps) the servo motor at **0°**.
  * Keeps the door locked.

---

## 🛠️ Software/Hardware Used

* 🐍 Python
* 📷 OpenCV
* 😊 DeepFace
* 🔌 Serial
* 🤖 Arduino
* ⚙️ Servo Motor
* 🩸 LEDs

---

## 📝 Notes

* Multiple frames are taken to verify the accuracy of the face scan.
</div>
