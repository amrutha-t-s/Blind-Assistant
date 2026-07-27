# 🦯 Blind Assistant System using AI

An AI-powered Blind Assistant System that helps visually impaired individuals navigate their surroundings using real-time object detection, distance estimation, OCR, multilingual voice feedback, and emergency assistance.

---

## 📌 Features

- 🎥 Real-time Camera Detection
- 🤖 YOLOv8 Object Detection
- 📏 Distance Estimation
- 🧭 Navigation Assistance
- 🔊 Voice Alerts
- 🌐 Multi-language Voice Support
  - English
  - Hindi
  - Kannada
- 📄 OCR (Text Reading)
- 📢 OCR + Voice Output
- 📳 Vibration Feedback
- 🚨 SOS Emergency Alert

---

## 🛠️ Technologies Used

- Python
- OpenCV
- YOLOv8 (Ultralytics)
- EasyOCR
- pyttsx3
- Google Translator
- NumPy
- Raspberry Pi (Future Deployment)

---

## 📂 Project Structure

```
BlindAssistant/
│
├── modules/
│   ├── camera.py
│   ├── detector.py
│   ├── navigation.py
│   ├── voice.py
│   ├── vibration.py
│   ├── ocr.py
│   ├── translator.py
│   └── ...
│
├── models/          # Ignored from Git
├── output/
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 🚀 How It Works

1. Captures live video from the camera.
2. Detects surrounding objects using YOLOv8.
3. Estimates the distance of detected objects.
4. Provides navigation guidance.
5. Reads nearby text using OCR.
6. Converts detected information into speech.
7. Supports multiple languages.
8. Activates vibration feedback for obstacles.
9. Sends an SOS alert during emergencies.

---

## 📸 Modules

### Camera

Captures live video frames.

### Object Detection

Detects objects using a trained YOLOv8 model.

### Navigation

Provides movement instructions based on object positions.

### Distance Estimation

Calculates the approximate distance between the user and detected objects.

### OCR

Reads printed text from images or live camera feed.

### Voice Alerts

Converts detections into spoken feedback.

### Translation

Translates voice messages into different languages.

### Vibration Feedback

Provides haptic alerts for nearby obstacles.

### SOS Alert

Allows users to trigger emergency assistance.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/BlindAssistant.git
```

Move into the project folder:

```bash
cd BlindAssistant
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

```bash
python main.py
```

---

## 📋 Requirements

- Python 3.10+
- Webcam
- YOLOv8 Model
- OpenCV
- EasyOCR
- Internet connection (for translation)

---

## ⚠️ Note

Large model files (`*.pt`) are not included in this repository because of GitHub's file size limits.

Place your trained YOLO model inside the `models/` directory before running the project.

Example:

```
models/
    pothole.pt
    yolov8n.pt
```

---

## 🎯 Future Improvements

- Raspberry Pi deployment
- GPS navigation
- Face recognition
- Currency recognition
- Traffic signal detection
- Wearable smart glasses integration
- Offline translation
- AI-powered scene description

---

## 👨‍💻 Author

**Amrutha**

Final Year Computer Science Engineering Student

---

## 📄 License

This project is intended for educational and research purposes.
