# Project Setup and Execution Guide

## Getting Started

### Install Required Libraries
```sh
pip install -r requirement.txt
```
### Set Up Environment Variables
setup .env file with gemini credentials
1.gemini api key

### enable services:
Vertex AI API
Generative Language API

2.serper api key
3.gcp project id
4.google application credential

### finally execute command to start FastAPI services

 uvicorn main:app --reload
 Go to http://127.0.0.1:8000/docs 

## Debugging Instructions

### Changes made in the code:
**1. Requirements.txt updated for better performance.**
***we removed opentelemetry because we was not using it, these can be removed to reduce complexity.***
***Excluded Google Cloud client libraries and embedchain due to dependency conflicts.*** 

**Changes to Python Code (main.py)**
Replaced ChatGoogleGenerativeAI with ChatLiteLLM
```sh
from langchain_community.chat_models import ChatLiteLLM
```
**Modified llm (Language Model) Instantiation:**
The llm object, used by CrewAI agents, was significantly updated to properly connect to Google's Gemini Pro model via Vertex AI using LiteLLM.



