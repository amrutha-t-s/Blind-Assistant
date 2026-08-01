from ultralytics import YOLO
from config import *

print("Loading AI Models...")

# Load models
general_model = YOLO(GENERAL_MODEL)
currency_model = YOLO(CURRENCY_MODEL)
pothole_model = YOLO(POTHOLE_MODEL)

print("All Models Loaded Successfully")


def run_model(model, frame, object_type):

    detections = []

    try:

        print(f"\nRunning {object_type} model...")

        # Check camera frame
        if frame is None:
            print("Frame is None")
            return detections

        print("Frame Shape:", frame.shape)

        results = model.predict(
            source=frame,
            conf=CONFIDENCE,
            imgsz=640,
            verbose=False
        )

        print(f"{object_type} model prediction successful.")

        for result in results:

            for box in result.boxes:

                cls = int(box.cls.item())
                conf = float(box.conf.item())

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                name = model.names[cls]

                detections.append({
                    "type": object_type,
                    "name": name,
                    "confidence": conf,
                    "box": (x1, y1, x2, y2)
                })

    except Exception as e:

        print(f"\nERROR while running {object_type} model")
        print(type(e).__name__)
        print(e)

    return detections


def detect(frame):

    detections = []

    detections.extend(run_model(
        general_model,
        frame,
        "general"
    ))

    detections.extend(run_model(
        currency_model,
        frame,
        "currency"
    ))

    detections.extend(run_model(
        pothole_model,
        frame,
        "pothole"
    ))

    return detections