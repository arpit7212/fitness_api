from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.crud import get_all_subjects_with_slots

router = APIRouter()



@router.post("/subjects/", response_model=schemas.Subject)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)

@router.get("/subjects/", response_model=list[schemas.Subject])
def read_subjects(db: Session = Depends(get_db)):
    return get_all_subjects_with_slots(db)