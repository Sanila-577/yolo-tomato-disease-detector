---
title: Tomato Leaf Disease Assistant API
emoji: 🍅
colorFrom: green
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---
# Neuro Leaf: Tomato Leaf Disease Assistant - Backend

This is the FastAPI backend for the Tomato Leaf Disease Assistant, powered by YOLO 11l and a LangGraph-based RAG agent.

# Backend URL - 

## 🚀 Features

* **Vision:** YOLO 11l model for real-time disease detection.
* **RAG Agent:** LangGraph workflow using FAISS and PDFs for expert treatment advice.
* **Search:** Integrated Tavily search for the latest agricultural trends.
* **API:** Highly modular FastAPI structure.

## 🛠️ Tech Stack

* **AI Model:** Ultralytics YOLO11
* **Orchestration:** LangGraph / LangChain
* **Vector DB:** FAISS
* **Server:** FastAPI & Uvicorn
* **Deployment:** Docker on Hugging Face Spaces

## 📦 Deployment Instructions

This backend is designed to be deployed as a Docker container.

1. Ensure `TAVILY_API_KEY` and `OPENROUTER_API_KEY` are set in the Space Secrets.
2. The server runs on port 7860.

## 🛣️ API Endpoints

* `POST /detect`: Accepts an image and returns YOLO detections + Base64 annotated image.
* `POST /chat`: Handles multi-turn RAG conversations about tomato health.
* `GET /health`: Basic heartbeat check.
