# Project Book-my-event – Team RoboAgentic  
**Google Agentic AI Hackathon Solution**

---

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Solution](#solution)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Overview

**Project Drishti** is an AI-powered situational awareness platform designed to improve safety at large public events. It acts as a “central nervous system” for event safety, providing real-time, actionable intelligence, predictive analytics, and automated resource dispatch to help commanders anticipate and mitigate risks.

This repository contains the source code for the Project Drishti platform, combining FastAPI, React.js, Firebase/Cloud Functions, and LangChain with Google AI technologies.

---

## Problem Statement

> **Improving Safety at Large Public Events**

Large-scale public events like music festivals or rallies are incredibly complex to manage. The fluid dynamics of large crowds create significant risks, from dangerous bottlenecks and crushing to difficulties in locating individuals in medical distress. Security teams need a way to move from reactive monitoring to proactive, intelligent intervention.

---

## Solution

Project Drishti aims to empower security teams and event commanders with an agentic AI platform that provides:

- **Predictive Bottleneck Analysis**: Real-time ingestion and analysis of video feeds to forecast crowding issues.
- **AI-Powered Situational Summaries**: Natural language querying of real-time event intelligence.
- **Automated Intelligent Resource Dispatch**: Immediate, data-driven coordination of response units.
- **Multimodal Anomaly Detection**: AI-driven alerts for abnormal patterns (e.g., smoke, fire, panic).
- **Innovative AI Features**: Lost & Found via photo matching, crowd sentiment analysis, and autonomous drone dispatch.

The solution harnesses Google’s Vertex AI Vision, Vertex AI Forecasting, Gemini models, Vertex AI Agent Builder, and Firebase for a robust, scalable deployment.

---

## Architecture

```
+------------------+      +-------------------+      +-------------------+
|    Frontend      |      |       API         |      |  Backend & Agents |
|  (React.js)      |<---->|   (FastAPI)       |<---->|  (LangChain,      |
+------------------+      +-------------------+      |   Google VertexAI,|
                                                     |   Gemini,         |
                                                     |   Firebase)       |
                                                     +-------------------+
      |                         |                          |
      v                         v                          v
  User Interaction      RESTful APIs / WebSocket    AI-powered Analytics,
  (Commanders,         endpoints                    Summaries, Dispatch,
  Security Staff)                                   Anomaly Detection
```

- **Frontend**: Real-time dashboards and chat interface for security teams.
- **API Layer**: FastAPI-powered backend for all business logic and AI orchestration.
- **Backend/Agents**: LangChain orchestrates AI agents; Firebase Cloud Functions handle scalable backend logic; Google Vertex AI services power vision, forecasting, and agentic intelligence.

---

## Tech Stack

- **Frontend**: [React.js](https://reactjs.org/)
- **Backend API**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Orchestration**: [LangChain](https://www.langchain.com/) (Python)
- **Cloud Functions**: [Firebase](https://firebase.google.com/)
- **Database & Auth**: [Firebase Firestore & Auth](https://firebase.google.com/docs/firestore)
- **AI/ML**: Google Vertex AI Vision, Vertex AI Forecasting, Vertex AI Agent Builder, Gemini (multimodal)
- **Deployment**: Firebase Hosting, Google Cloud Platform

---

## Features

- **Predictive Bottleneck Analysis**
  - Real-time crowd metrics from video feeds via Vertex AI Vision
  - Forecasting potential bottlenecks 15–20 minutes in advance (Vertex AI Forecasting)
- **AI-Powered Situational Summaries**
  - Natural language chat interface for querying event safety status
  - Summarizes security concerns, fuses data from video, reports, and social media (Gemini model)
- **Automated Resource Dispatch**
  - Incident detection triggers automated GPS-based response with Google Maps integration
- **Multimodal Anomaly Detection**
  - Alerts for smoke, fire, panic surges, and other visual anomalies (Gemini multimodal)
- **Innovative Features**
  - AI-powered Lost & Found: Photo matching for missing persons across video feeds
  - Crowd sentiment analysis for early panic detection
  - Autonomous drone dispatch for high-priority incidents

---

## How It Works

1. **Video Feeds Ingestion**: Drones/fixed cameras stream video to Vertex AI Vision.
2. **Crowd Analytics**: Vertex AI Forecasting models predict crowd flow and bottlenecks.
3. **Incident Detection**: AI agents detect anomalies (e.g., fire, panic) and trigger alerts.
4. **Command Center Dashboard**: React frontend displays real-time analytics, summaries, and chat with the AI agent.
5. **Resource Dispatch**: On incidents, the agent identifies the nearest team and dispatches via the fastest route.
6. **Natural Language Interface**: Commanders interact with the system using everyday language queries.

---

## Getting Started

### Prerequisites

- [Python 3.9+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/)
- [Firebase CLI](https://firebase.google.com/docs/cli)
- [Google Cloud SDK](https://cloud.google.com/sdk)
- Access to Google Vertex AI and Gemini models

### Setup

#### 1. Clone the repository

```bash
git clone https://github.com/AbhijitDutta338/Chatbot_AI.git
cd Chatbot_AI
```

#### 2. Backend (FastAPI + LangChain)

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set up environment variables for Vertex AI, Gemini, Firebase, etc.
uvicorn main:app --reload
```

#### 3. Frontend (React.js)

```bash
cd frontend
npm install
npm start
```

#### 4. Firebase/Cloud Functions

```bash
cd functions
npm install
firebase deploy --only functions
```

#### 5. Environment Configuration

- Set up `.env` files for API keys, Firebase, and Google Cloud credentials as required by each component.

---

## Deployment

- **Firebase Hosting**: Deploy the React frontend and Cloud Functions using Firebase CLI.
- **Google Cloud Platform**: Configure Vertex AI, Gemini models, and set up service accounts for secure access.
- **Continuous Deployment**: Recommended to use GitHub Actions or Google Cloud Build for CI/CD.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bug fixes, enhancements, or new features.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- **Google Agentic AI Hackathon** for the opportunity and challenge
- **Google Cloud Team** for cutting-edge AI/ML technology
- **LangChain, FastAPI, React, and Firebase** open-source communities

---

**Team RoboAgentic – Project Drishti**  
Empowering proactive safety for large public events with AI.
