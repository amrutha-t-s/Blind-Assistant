from gtts import gTTS
from deep_translator import GoogleTranslator
import pygame
import threading
import time
import os

pygame.mixer.init()

selected_language = "en"

last_message = ""
last_time = 0
cooldown = 3

# Prevent multiple threads playing at once
voice_lock = threading.Lock()


def set_language(language):
    global selected_language
    selected_language = language


def speak(text):

    global last_message, last_time

    current = time.time()

    if text == last_message and current - last_time < cooldown:
        return

    last_message = text
    last_time = current

    threading.Thread(
        target=play,
        args=(text,),
        daemon=True
    ).start()


def play(text):

    global selected_language

    # Only one voice can play at a time
    with voice_lock:

        try:

            translated_text = text

            if selected_language != "en":

                translated_text = GoogleTranslator(
                    source="en",
                    target=selected_language
                ).translate(text)

            filename = f"voice_{int(time.time()*1000)}.mp3"

            tts = gTTS(
                text=translated_text,
                lang=selected_language,
                slow=False
            )

            tts.save(filename)

            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            if os.path.exists(filename):
                os.remove(filename)

        except Exception as e:
            print("Voice Error:", e)