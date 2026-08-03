import random
import string
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

from app.database import get_db, engine, Base
from app import models, schemas

from typing import List

from app.security import hash_password, verify_password,create_access_token, decode_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

outh2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(outh2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

app = FastAPI(title="URL Shortener")
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/health")
def health_check():
    return {"status": "ok"}

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

@app.post("/shorten", response_model=schemas.URLResponse)
@limiter.limit("10/minute")
def create_short_url(
    request: Request,
    url: schemas.URLCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    short_code = generate_short_code()

    while db.query(models.URL).filter(models.URL.short_code == short_code).first():
        short_code = generate_short_code()

    db_url = models.URL(
        original_url=url.original_url,
        short_code=short_code,
        owner_id=current_user.id
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    return db_url

@app.get("/my_urls", response_model=list[schemas.URLResponse])
def get_my_urls(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    return db.query(models.URL).filter(models.URL.owner_id == current_user.id).all()

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

@app.post("/register", response_model=schemas.UserResponse)
@limiter.limit("5/minute")
def register_user(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = models.User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(request: Request, from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == from_data.username).first()

    if not user or not verify_password(from_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


