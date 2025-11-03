# Silent-SOS
SilentSOS is an AI system that detects silent distress and falls in patients who cannot call for help. It uses facial emotion analysis, voice-stress cues, and movement monitoring to trigger automatic caregiver alerts and offer a calming response. Built with fine-tuned pre-trained models, Django backend, and Streamlit dashboard.


SilentSOS — Multi-Modal Silent Emergency Detection System

SilentSOS is an AI-driven safety system designed for dementia and high-risk patients who may be unable to verbally request help.
It performs continuous passive monitoring and automatically triggers alerts when distress is detected, without requiring any user interaction.

System Capabilities

Real-time facial emotion recognition

Voice stress analysis

Fall and inactivity detection

Automated alert dispatch to caregivers (SMS / push)

Calming response module for patient reassurance

Live monitoring dashboard with event logs

Technical Overview

SilentSOS integrates three independent signals to infer patient distress:

Component	Implementation
Emotion detection	DeepFace (fine-tuned)
Audio stress analysis	Librosa feature extraction, stress heuristics
Pose / fall recognition	MediaPipe Pose landmarks + custom fall logic
Backend API	Django REST Framework
Alerting	Twilio / Firebase Cloud Messaging
Monitoring UI	Streamlit dashboard

The system operates continuously and pushes events to a backend pipeline responsible for decision logic, notification delivery, and logging.

Model Performance

Fine-tuned pre-trained emotion and fall-detection models (transfer learning)

mAP@0.5 = 0.87 on custom evaluation dataset

Dataset included staged distress events, fall simulations, stillness periods, and emotion-variation recordings.
