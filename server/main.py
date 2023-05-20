from fastapi import FastAPI
from db import schemas, models, crud
from db.database import SessionLocal, engine
from routes import subscriptions, newsletters

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(subscriptions.router)
app.include_router(newsletters.router)


@app.get("/")
def home():
    return {"message": "The server is running fine 😎"}
