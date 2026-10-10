CLI AI Assistant — Project Documentation
-- Project Overview
CLI AI Assistant is an AI-powered personal assistant designed to work through two interfaces:

CLI (Command Line Interface) — a lightweight terminal-based assistant.

Web Application — a browser-based interface built with Streamlit and powered by a FastAPI backend.

The project combines a Large Language Model (LLM) with external tools such as web search, weather information, and calculations. The goal is to create an assistant that can understand a user's request, decide whether a tool is required, execute that tool, and then provide a useful response.

-- Purpose of the Project
The main purpose of this project is to build a practical AI agent rather than a simple chatbot.

A traditional chatbot generally follows:

User
 ↓
LLM
 ↓
Response

Our assistant is designed to work differently:

User
 ↓
Agent
 ↓
LLM
 ↓
Does the request require a tool?
 ↓
 ┌───────────────┐
 │               │
YES              NO
 │               │
 ↓               ↓
Tool            Response
 │
 ↓
Tool Result
 │
 ↓
LLM
 │
 ↓
Final Response

This allows the assistant to perform real tasks instead of only generating text.

-- Main Features
The assistant is designed to provide:

 AI Conversation
The assistant uses a Hugging Face-hosted LLM to understand user questions and generate responses.

 Calculator
The calculator tool allows the agent to perform mathematical calculations.

Example:

User:
Calculate 245 * 37

Assistant:
9053

 Weather
The weather tool uses Open-Meteo to retrieve weather information without requiring a weather API key.

Example:

User:
What's the weather in Lahore?

Assistant:
The current temperature is ...

 Web Search
The web-search tool uses Tavily to retrieve current information from the web.

Example:

User:
What are the latest AI developments?

Assistant:
[Searches the web]
...
 CLI Interface
Users can interact with the assistant directly from a terminal.

Web Interface
A browser-based interface is provided using Streamlit.

 Backend API
FastAPI provides the backend API between the web interface and the agent.

--Technology Stack
Technology	Purpose
Python	Main programming language
Hugging Face	LLM/inference
FastAPI	Backend API
Uvicorn	FastAPI server
Streamlit	Web frontend
Tavily	Web search
Open-Meteo	Weather data
Requests	HTTP requests
python-dotenv	Environment variable management
Virtual Environment	Dependency isolation



--Explanation of Each Component
agent/
This is the brain of the application.

loop.py
Contains the main agent loop.

It manages the interaction between:

User

LLM

Tools

Tool results

Final response

prompts.py
Contains system prompts and instructions given to the LLM.

schemas.py
Contains the schemas describing available tools and their parameters.

For example:

calculator
    └── expression

weather
    └── location

web_search
    └── query

context.py
Can manage the current conversation/context of the agent.

-- tools/
This directory contains the actual capabilities of the assistant.

calculator.py
Handles mathematical operations.

weather.py
Communicates with Open-Meteo to retrieve weather information.

Open-Meteo does not require an API key for its free usage.

web_search.py
Uses Tavily to search the web.

registry.py
The tool registry keeps track of the tools available to the agent.



-- llm/
This layer handles communication with the AI model.

client.py
The LLM client communicates with Hugging Face.

The API token is not hardcoded into the Python code.

Instead:

.env
 ↓
HF_TOKEN
 ↓
llm/client.py
 ↓
Hugging Face

This keeps credentials separate from application code.

-- Backend — FastAPI
The backend is responsible for exposing the agent through an API.

Streamlit
    │
    │ HTTP Request
    ▼
FastAPI
    │
    ▼
Agent
    │
    ├── Hugging Face
    ├── Calculator
    ├── Weather
    └── Web Search



-- Frontend — Streamlit
Streamlit provides the browser-based user interface.

Instead of building the frontend manually with:

HTML
CSS
JavaScript

we can create the interface directly in Python.

The user interacts with the Streamlit application, which sends requests to the FastAPI backend.

--CLI Application

The CLI remains the default lightweight version of the assistant.

The user can run:

python main.py

and interact directly through the terminal.

The CLI uses the same agent and tools as the web application.

This avoids duplicating the AI logic.




-- Requirements
The current dependencies are:

huggingface_hub
python-dotenv
requests
tavily-python
fastapi
uvicorn
streamlit

Each dependency has a specific responsibility:

huggingface_hub → LLM
python-dotenv   → Environment variables
requests        → HTTP requests
tavily-python   → Web search
fastapi         → Backend API
uvicorn         → FastAPI server
streamlit       → Web frontend

-- How the Agent Works
Suppose the user asks:

What's the weather in Lahore?

The process is:

1. User enters request
          ↓
2. Interface receives request
          ↓
3. Agent processes request
          ↓
4. LLM determines that weather information is needed
          ↓
5. Agent selects weather tool
          ↓
6. weather.py calls Open-Meteo
          ↓
7. Weather data is returned
          ↓
8. Agent gives the data back to the LLM
          ↓
9. LLM generates a natural-language response
          ↓
10. User receives the answer

For a web-search question:

User
 ↓
Agent
 ↓
LLM
 ↓
web_search tool
 ↓
Tavily
 ↓
Search results
 ↓
LLM
 ↓
Final answer



-- Project Goal
The ultimate goal of this project is to understand and implement the architecture of a modern tool-using AI agent.

Rather than creating only a chatbot, the project demonstrates how an AI system can:

Understand natural-language requests

Decide when external tools are necessary

Call those tools

Process their results

Generate a final response

Operate through both CLI and web interfaces

Be structured for future deployment and expansion