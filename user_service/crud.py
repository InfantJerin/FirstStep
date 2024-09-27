from sqlalchemy.orm import Session

from . import models, schemas

def get_user_by_adhaar(db: Session, adhaar_number: str):
    return db.query(models.PersonDetails).filter(models.PersonDetails.adhaar_number == adhaar_number).first()

def create_user(db: Session, user: schemas.PersonDetailsModel):
    db_user = models.PersonDetails(adhaar_number=user.adhaar_number, person_info=user.person_info.model_dump_json())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)