from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, crud

router = APIRouter()


@router.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, client)

@router.get("/clients/", response_model=list[schemas.Client])
def read_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()