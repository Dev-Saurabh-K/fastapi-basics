from fastapi import FastAPI, Depends

from src.config.db import engine, get_db
from src.config import models
from sqlalchemy.orm import Session
import src.post as post
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)



@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts = db.query(models.Post).all()
    return {"data":posts}