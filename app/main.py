import random
import string
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app.database import get_db, engine, Base
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

@app.get("/health")
def health_check():
    return {"status": "ok"}

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

@app.post("/shorten", response_model=schemas.URLResponse)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    while db.query(models.URL).filter(models.URL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = models.URL(original_url=url.original_url, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url

@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    db_url.clicks += 1
    db.commit()

    return RedirectResponse(url=db_url.original_url)

@app.get("/stats/{short_code}", response_model=schemas.URLResponse)
def get_stats(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    return db_url