"""
Router de sesión — endpoints principales del juego
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Personaje, Pregunta
from app import engine as motor
from app.schemas import (
    SesionOut, RespuestaIn, EstadoOut, SiguientePreguntaOut,
    CandidatoOut, PersonajeOut, PreguntaOut
)

router = APIRouter(prefix="/sesion", tags=["Sesión"])

# ── Almacenamiento en memoria de las sesiones activas ──────────────────────
# { sesion_id: { "scores": {...}, "preguntas_hechas": [...], "turno": int, "terminado": bool } }
sesiones: dict = {}


# ── POST /sesion/nueva ─────────────────────────────────────────────────────
@router.post("/nueva", response_model=SesionOut)
def nueva_sesion(db: Session = Depends(get_db)):
    """
    Inicia una nueva partida.
    Devuelve un sesion_id único para identificar esta partida.
    """
    sesion_id = str(uuid.uuid4())

    sesiones[sesion_id] = {
        "scores": motor.scores_iniciales(db),
        "preguntas_hechas": [],
        "turno": 0,
        "terminado": False,
    }

    return SesionOut(
        sesion_id=sesion_id,
        mensaje="¡Piensa en un personaje famoso y empecemos!"
    )


# ── GET /sesion/{id}/pregunta ──────────────────────────────────────────────
@router.get("/{sesion_id}/pregunta", response_model=SiguientePreguntaOut)
def obtener_pregunta(sesion_id: str, db: Session = Depends(get_db)):
    """
    Devuelve la siguiente pregunta óptima para esta sesión.
    Si ya hay un ganador claro o se agotaron las preguntas → terminado=True.
    """
    sesion = _get_sesion(sesion_id)

    if sesion["terminado"]:
        adivinanza, confianza = motor.evaluar_adivinanza(sesion["scores"], db)
        return SiguientePreguntaOut(
            pregunta=None,
            terminado=True,
            adivinanza=PersonajeOut.model_validate(adivinanza) if adivinanza else None,
            confianza=confianza
        )

    # Verificar si ya debemos adivinar
    adivinanza, confianza = motor.evaluar_adivinanza(sesion["scores"], db)
    if adivinanza or sesion["turno"] >= motor.MAX_PREGUNTAS:
        sesion["terminado"] = True
        return SiguientePreguntaOut(
            pregunta=None,
            terminado=True,
            adivinanza=PersonajeOut.model_validate(adivinanza) if adivinanza else _mejor_candidato(sesion["scores"], db),
            confianza=confianza
        )

    # Obtener la siguiente pregunta más informativa
    pregunta = motor.siguiente_pregunta(
        sesion["scores"],
        sesion["preguntas_hechas"],
        db
    )

    if not pregunta:
        sesion["terminado"] = True
        return SiguientePreguntaOut(
            pregunta=None,
            terminado=True,
            adivinanza=_mejor_candidato(sesion["scores"], db),
            confianza=confianza
        )

    return SiguientePreguntaOut(
        pregunta=PreguntaOut.model_validate(pregunta),
        terminado=False,
        adivinanza=None,
        confianza=confianza
    )


# ── POST /sesion/{id}/respuesta ────────────────────────────────────────────
@router.post("/{sesion_id}/respuesta", response_model=EstadoOut)
def responder(sesion_id: str, respuesta: RespuestaIn, db: Session = Depends(get_db)):
    """
    Recibe la respuesta del usuario a la última pregunta.
    Actualiza los scores y devuelve el estado actual de la partida.

    respuesta.valor:
      1  = Sí
      0  = No sé
     -1  = No
    """
    sesion = _get_sesion(sesion_id)

    if sesion["terminado"]:
        raise HTTPException(status_code=400, detail="La sesión ya terminó")

    if respuesta.valor not in [-1, 0, 1]:
        raise HTTPException(status_code=422, detail="valor debe ser -1, 0 o 1")

    # La última pregunta hecha es la que el usuario está respondiendo
    if not sesion["preguntas_hechas"]:
        raise HTTPException(status_code=400, detail="No hay pregunta activa para responder")

    pregunta_id = sesion["preguntas_hechas"][-1]

    # Actualizar scores
    sesion["scores"] = motor.actualizar_scores(
        sesion["scores"],
        pregunta_id,
        respuesta.valor,
        db
    )
    sesion["turno"] += 1

    # Evaluar si hay ganador
    adivinanza, confianza = motor.evaluar_adivinanza(sesion["scores"], db)
    if adivinanza or sesion["turno"] >= motor.MAX_PREGUNTAS:
        sesion["terminado"] = True

    # Construir lista de candidatos ordenados por score
    candidatos = _construir_candidatos(sesion["scores"], db)

    return EstadoOut(
        sesion_id=sesion_id,
        turno=sesion["turno"],
        candidatos=candidatos,
        adivinanza=PersonajeOut.model_validate(adivinanza) if adivinanza else None,
        confianza=confianza,
        terminado=sesion["terminado"]
    )


# ── POST /sesion/{id}/preguntar ────────────────────────────────────────────
@router.post("/{sesion_id}/preguntar/{pregunta_id}", response_model=PreguntaOut)
def registrar_pregunta(sesion_id: str, pregunta_id: int, db: Session = Depends(get_db)):
    """
    Registra que se hizo una pregunta específica en esta sesión.
    El frontend llama esto justo antes de mostrar la pregunta al usuario.
    """
    sesion = _get_sesion(sesion_id)

    pregunta = db.query(Pregunta).filter(Pregunta.id == pregunta_id).first()
    if not pregunta:
        raise HTTPException(status_code=404, detail="Pregunta no encontrada")

    if pregunta_id not in sesion["preguntas_hechas"]:
        sesion["preguntas_hechas"].append(pregunta_id)

    return PreguntaOut.model_validate(pregunta)


# ── GET /sesion/{id}/estado ────────────────────────────────────────────────
@router.get("/{sesion_id}/estado", response_model=EstadoOut)
def estado_sesion(sesion_id: str, db: Session = Depends(get_db)):
    """
    Devuelve el estado completo actual de la sesión.
    Útil para debug y para el panel de desarrollo.
    """
    sesion = _get_sesion(sesion_id)
    adivinanza, confianza = motor.evaluar_adivinanza(sesion["scores"], db)
    candidatos = _construir_candidatos(sesion["scores"], db)

    return EstadoOut(
        sesion_id=sesion_id,
        turno=sesion["turno"],
        candidatos=candidatos,
        adivinanza=PersonajeOut.model_validate(adivinanza) if adivinanza else None,
        confianza=confianza,
        terminado=sesion["terminado"]
    )


# ── Helpers ────────────────────────────────────────────────────────────────

def _get_sesion(sesion_id: str) -> dict:
    if sesion_id not in sesiones:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    return sesiones[sesion_id]


def _construir_candidatos(scores: dict, db: Session) -> list[CandidatoOut]:
    total = sum(scores.values()) or 1
    personajes = db.query(Personaje).all()
    candidatos = []

    for p in personajes:
        if p.id in scores:
            candidatos.append(CandidatoOut(
                personaje=PersonajeOut.model_validate(p),
                score=round(scores[p.id] / total, 4)
            ))

    return sorted(candidatos, key=lambda c: c.score, reverse=True)


def _mejor_candidato(scores: dict, db: Session):
    if not scores:
        return None
    mejor_id = max(scores, key=lambda pid: scores[pid])
    personaje = db.query(Personaje).filter(Personaje.id == mejor_id).first()
    return PersonajeOut.model_validate(personaje) if personaje else None
