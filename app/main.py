from fastapi import FastAPI
from app.database.database import Base, engine
from app.routers.AssetRouter import router as assetRouter
from app.routers.ContributionRuleRouter import router as contributionRuleRouter
from app.routers.SimulationRouter import router as simulationRouter
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging

load_dotenv(dotenv_path="../.env")
ui_url = os.getenv("UI_URL")
if not ui_url:
    raise RuntimeError("UI_URL environment variable not set")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        ui_url, 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Basic configuration
logging.basicConfig(
    level=logging.INFO,          # minimum level to log
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app.include_router(assetRouter)
app.include_router(contributionRuleRouter)
app.include_router(simulationRouter)
# Create tables automatically on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

