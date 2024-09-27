from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "First FastAPI app"}

@app.post("/create_user")
def create_user(user: schemas.PersonDetailsModel, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_adhaar(db, adhaar_number=user.adhaar_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Adhaar number already registered")
    return crud.create_user(db=db, user=user)


@app.get("/get_user_by_adhaar", response_model=schemas.PersonDetailsModel)
def get_user_by_adhaar(adhaar_number: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_adhaar(db, adhaar_number=adhaar_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Adhaar number not found")
    return db_user

