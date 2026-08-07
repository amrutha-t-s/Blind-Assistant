import cv2

from modules.camera import start_camera
from modules.detector import detect
from modules.navigation import navigation_message
from modules.voice import speak, set_language
from modules.ocr import read_text
from modules.sos import send_sos_email

from modules.vibration import (
    vibrate_left,
    vibrate_right,
    vibrate_both,
    cleanup
)

# ==========================================
# WINDOWS KEYBOARD LISTENER (REDUNDANT)
# ==========================================
try:
    import win32api
    WINDOWS = True
except ImportError:
    WINDOWS = False

if WINDOWS:
    import threading
    import time

    key_pressed_o = False
    key_pressed_s = False
    key_pressed_esc = False

    def keyboard_listener():
        global key_pressed_o, key_pressed_s, key_pressed_esc
        VK_O = 0x4F
        VK_S = 0x53
        VK_ESC = 0x1B
        
        prev_o = False
        prev_s = False
        prev_esc = False
        
        while True:
            try:
                state_o = bool(win32api.GetAsyncKeyState(VK_O) & 0x8000)
                state_s = bool(win32api.GetAsyncKeyState(VK_S) & 0x8000)
                state_esc = bool(win32api.GetAsyncKeyState(VK_ESC) & 0x8000)
                
                if state_o and not prev_o:
                    key_pressed_o = True
                if state_s and not prev_s:
                    key_pressed_s = True
                if state_esc and not prev_esc:
                    key_pressed_esc = True
                    
                prev_o = state_o
                prev_s = state_s
                prev_esc = state_esc
            except Exception:
                pass
            time.sleep(0.01)

    t = threading.Thread(target=keyboard_listener, daemon=True)
    t.start()

# ==========================================
# LANGUAGE SELECTION
# ==========================================

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

# ==========================================
# CAMERA
# ==========================================

cap = start_camera()

if cap is None:
    exit()

cv2.namedWindow("Blind Assistant")

# False = Object Detection
# True = OCR
ocr_mode = False

# Prevent repeating the same voice continuously
last_message = ""

print("\nControls")
print("--------------------------------")
print("O -> OCR Mode")
print("S -> Send SOS")
print("ESC -> Exit")
print("--------------------------------")

while True:

    ret, frame = cap.read()

    if not ret:
        break
    
        # ==========================================
    # OCR MODE
    # ==========================================

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

            print("\nDetected Text:")
            print(text)

            speak(text)

        cv2.imshow("Blind Assistant", frame)

        key = cv2.waitKey(1) & 0xFF

        is_o = (key in (ord('o'), ord('O')))
        is_s = (key in (ord('s'), ord('S')))
        is_esc = (key == 27)

        if WINDOWS:
            if key_pressed_o:
                is_o = True
                key_pressed_o = False
            if key_pressed_s:
                is_s = True
                key_pressed_s = False
            if key_pressed_esc:
                is_esc = True
                key_pressed_esc = False

        if is_o:

            print("Object Detection Mode")

            speak("Object Detection Mode")

            ocr_mode = False

        elif is_s:

            print("Sending SOS...")

            speak("Emergency Alert Activated")

            send_sos_email()

        elif is_esc:

            break

        continue

    # ==========================================
    # OBJECT DETECTION
    # ==========================================

    detections = detect(frame)

    priority = None
    direction = None
    highest_priority = 0

    for obj in detections:

        x1, y1, x2, y2 = obj["box"]

        name = obj["name"]
        confidence = obj["confidence"]

        label = f"{name} {confidence:.2f}"

        # Draw Bounding Box

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

        # Draw Label

        cv2.putText(
            frame,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

        # Navigation

        message, obj_direction = navigation_message(
            obj,
            frame.shape[1],
            frame.shape[0]
        )

        # Priority System

        #if obj["type"] == "pothole":

            #if highest_priority < 3:

                #priority = message
                #direction = obj_direction
                #highest_priority = 3

        if name == "person":

            if highest_priority < 2:

                priority = message
                direction = obj_direction
                highest_priority = 2

        elif obj["type"] == "currency":

            if highest_priority < 1:

                priority = message
                direction = obj_direction
                highest_priority = 1

        elif highest_priority == 0:

            priority = message
            direction = obj_direction
            


    # ==========================================
    # VOICE + VIBRATION
    # ==========================================

    if not priority:
        last_message = ""

    if priority:

        if priority != last_message:
            speak(priority)
            last_message = priority

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
    
        # ==========================================
    # KEYBOARD CONTROLS
    # ==========================================

    key = cv2.waitKey(1) & 0xFF

    is_o = (key in (ord('o'), ord('O')))
    is_s = (key in (ord('s'), ord('S')))
    is_esc = (key == 27)

    if WINDOWS:
        if key_pressed_o:
            is_o = True
            key_pressed_o = False
        if key_pressed_s:
            is_s = True
            key_pressed_s = False
        if key_pressed_esc:
            is_esc = True
            key_pressed_esc = False

    if is_o:

        print("\nOCR Mode")

        speak("OCR Mode")

        ocr_mode = True

    elif is_s:

        print("\nSending SOS...")

        speak("Emergency Alert Activated")

    

        try:

            send_sos_email()

            print("SOS Sent Successfully")

            speak("SOS Message Sent")

        except Exception as e:

            print("SOS Failed:", e)

            speak("SOS Failed")

    elif is_esc:

        print("\nClosing Blind Assistant...")

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

cleanup()

cv2.destroyAllWindows()

print("\nBlind Assistant Closed Successfully.")