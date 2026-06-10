from fastapi import FastAPI, Depends

from src.config.db import engine, get_db
from src.config import models
from sqlalchemy.orm import Session
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



@app.get("/")
def test_api():
    return{
        "message":"ok"
    }

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data":posts}
