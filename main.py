from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from db import models
from db.database import engine
from routes import subscriptions, newsletters, auth, email

# Create tables for all models in database if it doesn't exist
models.Base.metadata.create_all(bind=engine)

# Create server
app = FastAPI()

# Load environment variables in app globally
load_dotenv()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://abhijha-newsletter.netlify.app",
                   "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Separate routes to handle APIs for each model
app.include_router(auth.router)
app.include_router(subscriptions.router)
app.include_router(newsletters.router)
app.include_router(email.router)


# API for health check
@app.get("/", tags=["Health check"], response_class=HTMLResponse)
def home():
    return "<h1>The server is running fine 🚀</h1>"
