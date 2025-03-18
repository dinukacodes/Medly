from fastapi import FastAPI
from api.diagnosis_endpoints import router as diagnosis_router
from api.evidence_endpoints import router as evidence_router
from api.streaming import router as streaming_router
from api.feedback_endpoints import router as feedback_router
from database.db_setup import init_db
from core.config_loader import load_config
from core.logging import setup_logging

app = FastAPI()

# Load configurations
config = load_config()

# Set up logging
setup_logging(config['logging'])

# Initialize database
init_db()

# Mount API routers
app.include_router(diagnosis_router, prefix="/api")
app.include_router(evidence_router, prefix="/api")
app.include_router(streaming_router, prefix="/api")
app.include_router(feedback_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
