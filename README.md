# Insurance Premium Predictor

AI-powered insurance premium prediction system using FastAPI and Streamlit.

## Features
- FastAPI backend with ML model
- Streamlit frontend interface
- Risk assessment based on user inputs
- RESTful API endpoints

## Local Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run FastAPI: `uvicorn app1:app --reload`
4. Run Streamlit: `streamlit run streamlit_app.py`

## API Endpoints
- `GET /` - Home page
- `GET /health` - Health check
- `POST /predict` - Make predictions

## Deployment
Deployed on Render with automatic deployment from GitHub.