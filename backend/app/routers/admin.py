"""
routers/admin.py — Endpoints para administrar el juego

  GET    /admin/personajes              → lista todos los personajes
  POST   /admin/personajes              → agrega un personaje
  GET    /admin/preguntas               → lista todas las preguntas
  POST   /admin/preguntas               → agrega una pregunta
  POST   /admin/atributos               → define atributo (personaje + pregunta + valor)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Personaje, Pregunta, Atributo
from app.schemas import (
    PersonajeOut, PersonajeCreate,
    PreguntaOut, PreguntaCreate,
    AtributoCreate,
)

router = APIRouter(prefix="/admin", tags=["Admin"])


# ── Personajes ─────────────────────────────────────────────────────────────────

@router.get("/personajes", response_model=list[PersonajeOut])
def listar_personajes(db: Session = Depends(get_db)):
    return db.query(Personaje).all()


@router.post("/personajes", response_model=PersonajeOut, status_code=201)
def crear_personaje(payload: PersonajeCreate, db: Session = Depends(get_db)):
    existente = db.query(Personaje).filter(Personaje.nombre == payload.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un personaje con ese nombre")

    personaje = Personaje(**payload.model_dump())
    db.add(personaje)
    db.commit()
    db.refresh(personaje)
    return personaje


# ── Preguntas ──────────────────────────────────────────────────────────────────

@router.get("/preguntas", response_model=list[PreguntaOut])
def listar_preguntas(db: Session = Depends(get_db)):
    return db.query(Pregunta).all()


@router.post("/preguntas", response_model=PreguntaOut, status_code=201)
def crear_pregunta(payload: PreguntaCreate, db: Session = Depends(get_db)):
    existente = db.query(Pregunta).filter(Pregunta.texto == payload.texto).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe esa pregunta")

    pregunta = Pregunta(**payload.model_dump())
    db.add(pregunta)
    db.commit()
    db.refresh(pregunta)
    return pregunta


# ── Atributos ──────────────────────────────────────────────────────────────────

@router.post("/atributos", status_code=201)
def crear_atributo(payload: AtributoCreate, db: Session = Depends(get_db)):
    if payload.valor not in (-1, 0, 1):
        raise HTTPException(status_code=400, detail="El valor debe ser -1, 0 o 1")

    # Verificar que existen personaje y pregunta
    if not db.query(Personaje).filter(Personaje.id == payload.personaje_id).first():
        raise HTTPException(status_code=404, detail="Personaje no encontrado")
    if not db.query(Pregunta).filter(Pregunta.id == payload.pregunta_id).first():
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    # Upsert: si ya existe, actualizar el valor
    existente = db.query(Atributo).filter(
        Atributo.personaje_id == payload.personaje_id,
        Atributo.pregunta_id == payload.pregunta_id,
    ).first()

    if existente:
        existente.valor = payload.valor
        db.commit()
        return {"mensaje": "Atributo actualizado", "id": existente.id}

    atributo = Atributo(**payload.model_dump())
    db.add(atributo)
    db.commit()
    db.refresh(atributo)
    return {"mensaje": "Atributo creado", "id": atributo.id}
