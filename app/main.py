from fastapi import FastAPI
from app.database.database import Base, engine
from app.routers.AssetRouter import router as assetRouter
from app.routers.ContributionRuleRouter import router as contributionRuleRouter
from app.routers.SimulationRouter import router as simulationRouter
import logging


app = FastAPI()

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

