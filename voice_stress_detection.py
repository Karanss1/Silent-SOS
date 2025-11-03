import torch
import numpy as np
import sounddevice as sd
import torchaudio
from transformers import Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor
import requests
import os
import time
from collections import deque


model_name = "superb/wav2vec2-base-superb-er"
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)


# Sampling rate must be 16000 for this model
SAMPLE_RATE = 16000
DURATION = 3  # seconds per recording chunk


stress_emotions = ["angry", "sad", "fearful", "frustrated"]
last_alert_time = 0
alert_delay = 120  # seconds between alerts (2 minutes)


# Sliding window for smoothing predictions
window_size = 5
emotion_window = deque(maxlen=window_size)
confidence_window = deque(maxlen=window_size)


def predict_emotion_from_audio(audio_data):
    input_values = feature_extractor(audio_data, sampling_rate=SAMPLE_RATE, return_tensors="pt").input_values
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    labels = model.config.id2label
    emotion = labels[predicted_ids[0].item()]
    confidence = torch.softmax(logits, dim=-1)[0, predicted_ids[0]].item()
    return emotion, confidence


def send_stress_event(patient_id, severity, description):
    url = "http://localhost:8000/api/events/"
    data = {
        "patient": patient_id,
        "event_type": "voice",
        "severity": severity,
        "description": description
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            print("Stress event sent successfully")
        else:
            print(f"Failed to send event: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Request error: {e}")


def callback(indata, frames, time_info, status):
    global last_alert_time
    audio = indata[:, 0]  # Use first channel only
    emotion, confidence = predict_emotion_from_audio(audio)
    emotion_window.append(emotion)
    confidence_window.append(confidence)

    if len(emotion_window) == window_size:
        # Majority vote of emotions in window
        emotion_counts = {}
        for e in emotion_window:
            emotion_counts[e] = emotion_counts.get(e, 0) + 1
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        avg_confidence = sum(confidence_window) / window_size

        print(f"Dominant emotion: {dominant_emotion} with avg confidence {avg_confidence:.2f}")

        if dominant_emotion.lower() in stress_emotions and avg_confidence > 0.75:
            current_time = time.time()
            if current_time - last_alert_time > alert_delay:
                send_stress_event(1, "high", f"Detected stressed emotion: {dominant_emotion}")
                last_alert_time = current_time


def main():
    print(f"Recording {DURATION} second chunks of audio with sample rate {SAMPLE_RATE}...")
    with sd.InputStream(channels=1, samplerate=SAMPLE_RATE, callback=callback):
        print("Press Ctrl+C to stop.")
        try:
            while True:
                sd.sleep(DURATION * 1000)
        except KeyboardInterrupt:
            print("Stopping...")


if __name__ == "__main__":
    main()
