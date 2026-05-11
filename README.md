# Nordic Travel Chatbot 

An AI-powered travel recommendation chatbot built with:
- Pydantic-AI
- FastAPI
- Streamlit
- MLflow
- Docker 
- Azure
- PostgreSQL

The application helps users discover attractions, restaurants, and activities in Scandinavian cities based on their preferences.

## Project Overview

The chatbot allows user to enter travel preferences such as:
- destination country
- destination city
- number of travel days
- budget 

The chatbot then generates:
- attraction recommendations
- restaurants recommendations
- activities
- follow-up suggestions
- simple travel itineraries

Example prompts:
```
I am visting Stockholm for 3 days.
I like nature, museums, and cheap food.
Traveling with family.

```

## Tech Stack

### Backend
- FastAPI
- Pydantic AI
- MLflow
- PostgreSQL
- Docker

### Frontend
- Streamlit
- Docker

### Cloud & Infrastructure
- Azure Container Apps
- Azure Container Registry (ACR)
- Azure Database for PostgreSQL Flexible Server

## Architecture
```
Frontend (Streamlit)
        ↓
Backend API (FastAPI + Pydantic-AI)
        ↓
MLflow Tracking Server
        ↓
PostgreSQL Backend Store
```

## Features

### Core Features
- AI travel assistant chatbot
- Scandinavian city recommendations
- Attractions, restaurants and activities
- Follow-up conversational flow
- Structured recommendation responses

### LLMOps Features
- Prompt versioning with MLflow
- Prompt registry support
- Prompt evalutation
- Request logging
- Experiment tracking
- Dockerized services
- Azure cloud deployment

## Supported cities
This current project supports:
- Stockholm
- Oslo
- Copenhagen
- Helsiniki
- Rejkavik

The dataset kan easily be expanded with more Scandinavians cities. 

## Project structure
```
llomps_fullstack_project/
│
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   ├── api/
│   │   ├── core/
│   │   ├── middlewares/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── __init__.py
│   │   └── main.py
│   │
│   ├── data/
│   ├── tests/
│   └── __init__.py
│
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── __init__.py
│
├── monitoring/
│   ├── register_prompts.py
│   ├── run_evaluation.py
│   └── __init__.py
│
├── dockerfiles/
│   ├── backend.dockerfile
│   ├── frontend.dockerfile
│   └── mlflow.dockerfile
│
├── docker-compose.yaml
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

## Environment Variables
Create a `.env` file in the project root.

### Required Variables
```
OPENROUTER_API_KEY=your_openrouter_key
MLFLOW_TRACKING_URI=http://localhost:5000
MLFLOW_EXPERIMENT_NAME=travel_chatbot_scandinavia
```

## Local Development

### 1. Clone the repository
```
git clone <repo-url>
cd llomps_fullstack_project
```
### 2. Install dependencies

 Using uv:
```
uv sync
```

### 3. Register prompts in MLflow
```
uv run python -m monitoring.register_prompts
```

### 4. Start Docker services
```
docker compose up --build
```

Services:
```
Service         Port

Backend API     8000
Frontend        8501
MLflow          5001
```

## Running Without Docker

### Start MLflow
```
uv run mlflow ui --backend-store-uri sqlite:///monitoring/mlflow.db --port 5001
```
### Start backend
```
uv run uvircorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
### Start frontend
```
uv run streamlit run frontend/src/app.py
```

## API endpoints

### Health check
```
GET /health
```
### Chat endpoint
```
POST /chat 
```

Example request:
```
{
    "message": "I am visiting Stockholm for 2 days with family"
}
```

## MLflow integration
The project uses MLflow for:
- prompt versioning
- evaluation tracking
- experiment tracking
- logging chatbot request and responses

### Prompt registration
Prompts are registred through:
```
uv run python -m monitoring.register_prompts
```
### Evaluation
Run evaluations with:

```
uv run python -m monitoring.run_evaluation
```

## Azure deployment
The application is deployed using:
- Azure Container Apps
- Azure Container Registry
- Azure Database for PostgreSQL Flexible Server 

## Deployed Components

### Frontend
- Streamlit Web App
### Backend
- FastAPI Container App
### MLflow
- MLflow Tracking Server Container App
### Database
- PostgreSQL Flexible Server
### Registry
- Azure Container Registry (ACR)

## Docker Images
### Backend
```
docker build -f dockerfiles/backend.dockerfile -t backend:v1 .
```
### Frontend 
```
docker build -f dockerfiles/frontend.docerkfile -t frontend:v1 .
```

### Evaluation Strategy

The project evaluates:
- relevance
- structure quality
- hallucination risk
- instruction following
- recommendation usefulness

Example evaluation prompts:

- "2 days in Stockholm with low budget"
- "Family-friendly activties in Copenhagen"
- "Rainy day in Oslo"
- "Romantic weekend in Bergen"

## Team Workflow

### Git Strategy
- feature branches
- pull requests
- code reviews
- no direct pushes to main

### Project Management
- GitHub Projects
- Kanban board
- Issues
- Working agreement

## Future Improvements

Potential future improvements include:
- vector database retrieval
- semantic search
- real RAG architecture 
- authentication
- user histrory
- multilingual support
- itinerary export
- booking integrations

## Contributors
Developed as part of an LLMOps "university" project

Team members contributed across:
- backend engineering
- frontend develeopment
- cloud deployment
- MLflow monitoring
- prompt engineering
- evalutation workflows 
- Docker infrastructure

## License
Educational project


