from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

from db import models
from db.database import engine
from routes import subscriptions, newsletters

# Create tables for all models in database if it doesn't exist
models.Base.metadata.create_all(bind=engine)

# Create server
app = FastAPI()

# Load environment variables in app globally
load_dotenv()

# Separate routes to handle APIs for each model
app.include_router(subscriptions.router)
app.include_router(newsletters.router)


# API for health check
@app.get("/", tags=["Health check"], response_class=HTMLResponse)
def home():
    return "<h1>The server is running fine 🚀</h1>"
