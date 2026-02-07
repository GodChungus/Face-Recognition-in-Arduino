<div align="center">
  <h1><b>👱🏻Facial Recognition using Arduino👱🏻</b></h1>

  <h3><b>How does it work?</b></h3>
  <p>
    The Python code has three main libraries: DeepFace, Serial, and CV2. CV2 is just OpenCV, which is a library that allows for opening of a camera window and some other commands relating to it in Python. 
    DeepFace is a facial recognition library that allows for easy facial recognition, and Serial is just a library that allows for communication between Python and the hardware components(in this case, the Arduino).
  </p>
  <p>
    The camera window is opened, which then recognizes your face. For a few seconds, it verifies to prevent any false recognitions. Once your face has been identified, it sends a signal '1' to the Arduino indicating
    that your face has been recognized, along with displaying your name in green text on the screen. In the case your face has not been recognized, a red text spelling "Unknown" appears on the screen, and the script
    sends a signal '0' to the Arduino indicating your face has not been recognized.
  </p>
  <p>
    If the signal received by the Arduino is '1', a green LED turns on, and a servo motor is rotated 90 degrees. The servo motor has an accessory attached to it that basically acts like a door lock, which when
    rotated by 90 degrees would unlock the door. If the signal received by the Arduino is '0', a red LED turns on, and the servo motor either does not move or goes back to zero degrees, depending on it's position,
    thus locking the door.
  </p>
</div>
