import cv2
from deepface import DeepFace
import requests
import signal
import sys
import time

API_ENDPOINT = "http://127.0.0.1:8000/api/events/"  # Your backend API endpoint
PATIENT_ID = 1  # Hardcoded patient ID for this demo

cap = None  # Declare globally to access in signal handler

last_alert_time = 0
alert_delay = 120  # seconds between alerts (2 minutes)

def send_event(patient_id, emotion, severity='high'):
    event = {
        "patient": patient_id,
        "event_type": "emotion",  # must match your model choice field
        "severity": severity,
        "description": f"Detected emotion: {emotion}"
    }
    try:
        response = requests.post(API_ENDPOINT, json=event)
        print(f"Event sent for patient {patient_id}: {response.status_code}")
    except Exception as e:
        print("Failed to send event:", e)

def signal_handler(sig, frame):
    print('\nExiting gracefully...')
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    sys.exit(0)

def main():
    global cap, last_alert_time
    cap = cv2.VideoCapture(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            if isinstance(analysis, list):
                analysis = analysis[0]

            emotion = analysis['dominant_emotion']

            cv2.putText(frame, f'Emotion: {emotion}', (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            if emotion in ['fear', 'sad', 'angry', 'disgust']:
                current_time = time.time()
                if current_time - last_alert_time > alert_delay:
                    send_event(PATIENT_ID, emotion)
                    last_alert_time = current_time

        except Exception as e:
            print("Error analyzing frame:", e)

        cv2.imshow('Facial Emotion Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
