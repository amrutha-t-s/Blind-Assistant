import cv2

from modules.camera import start_camera
from modules.detector import detect
from modules.voice import speak, set_language
from modules.navigation import navigation_message
from modules.ocr import read_text

from modules.vibration import (
    vibrate_left,
    vibrate_right,
    vibrate_both,
    cleanup
)

# ===========================================
# Language Selection
# ===========================================

print("\n===================================")
print("      Blind Assistant System")
print("===================================")

print("\nSelect Voice Language")
print("1. English")
print("2. Hindi")
print("3. Kannada")
print("4. Tamil")
print("5. Telugu")
print("6. Malayalam")

choice = input("\nEnter your choice (1-6): ")

language_map = {
    "1": "en",
    "2": "hi",
    "3": "kn",
    "4": "ta",
    "5": "te",
    "6": "ml"
}

VOICE_LANGUAGE = language_map.get(choice, "en")

set_language(VOICE_LANGUAGE)

speak("Welcome to Blind Assistant System")

# ===========================================
# Camera
# ===========================================

cap = start_camera()

if cap is None:
    exit()

# False = Object Detection
# True = OCR Mode
ocr_mode = False

print("\nPress 'O' to switch between Object Detection and OCR Mode.")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # ===========================================
    # OCR MODE
    # ===========================================

    if ocr_mode:

        cv2.putText(
            frame,
            "OCR MODE",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

        text = read_text(frame)

        if text:

            print("Detected Text:", text)

            speak(text)

        cv2.imshow("Blind Assistant", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('o'):
            print("Object Detection Mode")
            ocr_mode = False

        elif key == 27:
            break

        continue

    # ===========================================
    # OBJECT DETECTION MODE
    # ===========================================

    detections = detect(frame)

    priority = None
    direction = None
    highest_priority = 0

    for obj in detections:

        x1, y1, x2, y2 = obj["box"]

        name = obj["name"]
        confidence = obj["confidence"]

        label = f"{name} {confidence:.2f}"

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        message, obj_direction = navigation_message(
            obj,
            frame.shape[1],
            frame.shape[0]
        )

        # Priority System

        if obj["type"] == "pothole":

            if highest_priority < 3:
                priority = message
                direction = obj_direction
                highest_priority = 3

        elif name == "person":

            if highest_priority < 2:
                priority = message
                direction = obj_direction
                highest_priority = 2

        elif obj["type"] == "currency":

            if highest_priority < 1:
                priority = message
                direction = obj_direction
                highest_priority = 1

        else:

            if highest_priority == 0:
                priority = message
                direction = obj_direction

    # ===========================================
    # Voice + Vibration
    # ===========================================

    if priority:

        speak(priority)

        if direction == "left":
            vibrate_left()

        elif direction == "right":
            vibrate_right()

        else:
            vibrate_both()

    cv2.putText(
        frame,
        "OBJECT DETECTION MODE",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 0, 0),
        2
    )

    cv2.imshow("Blind Assistant", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('o'):
        print("OCR Mode")
        ocr_mode = True

    elif key == 27:
        break

cap.release()

cleanup()

cv2.destroyAllWindows()