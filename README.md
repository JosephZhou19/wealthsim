# WealthSim Project
This is a Python application that handles creating monte carlo simulations for various asset classes

This project includes a PostgreSQL DB, a FastAPI Python Service, and connects to OpenAI for qualitative analysis.

## Architecture
The architecture for this project is rather simple.

React (vite) -> Python (FastApi) -> PostgreSQL DB
                    ↳ Monte Carlo Engine
                    ↳ AI Interpretation Layer

There is no plans to deploy this application since it stores financial data.

## Local Setup
Before setup, create a copy of the `.env.example` file named `.env` with your own enviroment variables.

If this is your first time setting up the app, please download Docker and run the command.
```docker compose up --build```
This creates a local container for the database. Make sure the container is up and running.

Next up, run the following to install all required Python Packages.
```pip install -r requirements.txt```

From there, all that is left is to run the application. This app uses uvicorn
```python -m uvicorn app.main:app --reload```

There is a front-end to this project. That belongs in [WealthSimUI](https://github.com/JosephZhou19/wealthsimUI)
