from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.client import Client, Domicilio
from app.schemas.client_schema import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    DomicilioCreate,
    DomicilioUpdate,
    DomicilioResponse,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])

# --- Clientes ---


@router.post("/", response_model=ClientResponse)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


@router.get("/", response_model=List[ClientResponse])
def get_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Client).offset(skip).limit(limit).all()


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client: ClientUpdate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    update_data = client.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(db_client)
    db.commit()
    return {"message": "Cliente eliminado"}


# --- Domicilios ---


@router.post("/{client_id}/domicilios/", response_model=DomicilioResponse)
def create_domicilio_for_client(
    client_id: int, domicilio: DomicilioCreate, db: Session = Depends(get_db)
):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    db_domicilio = Domicilio(**domicilio.model_dump(), cliente_id=client_id)
    db.add(db_domicilio)
    db.commit()
    db.refresh(db_domicilio)
    return db_domicilio


@router.get("/{client_id}/domicilios/", response_model=List[DomicilioResponse])
def get_domicilios_for_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_client.domicilios


@router.get("/domicilios/{domicilio_id}", response_model=DomicilioResponse)
def get_domicilio(domicilio_id: int, db: Session = Depends(get_db)):
    db_domicilio = db.query(Domicilio).filter(Domicilio.id == domicilio_id).first()
    if db_domicilio is None:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    return db_domicilio


@router.put("/domicilios/{domicilio_id}", response_model=DomicilioResponse)
def update_domicilio(
    domicilio_id: int, domicilio: DomicilioUpdate, db: Session = Depends(get_db)
):
    db_domicilio = db.query(Domicilio).filter(Domicilio.id == domicilio_id).first()
    if db_domicilio is None:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")

    update_data = domicilio.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_domicilio, key, value)

    db.commit()
    db.refresh(db_domicilio)
    return db_domicilio


@router.delete("/domicilios/{domicilio_id}")
def delete_domicilio(domicilio_id: int, db: Session = Depends(get_db)):
    db_domicilio = db.query(Domicilio).filter(Domicilio.id == domicilio_id).first()
    if db_domicilio is None:
        raise HTTPException(status_code=404, detail="Domicilio no encontrado")
    db.delete(db_domicilio)
    db.commit()
    return {"message": "Domicilio eliminado"}
