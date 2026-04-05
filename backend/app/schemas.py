from pydantic import BaseModel
from typing import Optional


# ── Personaje ──────────────────────────────────────────────────────────────

class PersonajeOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    imagen_url: Optional[str]

    model_config = {"from_attributes": True}


# ── Pregunta ───────────────────────────────────────────────────────────────

class PreguntaOut(BaseModel):
    id: int
    texto: str
    categoria: Optional[str]

    model_config = {"from_attributes": True}


# ── Sesión ─────────────────────────────────────────────────────────────────

class SesionOut(BaseModel):
    sesion_id: str
    mensaje: str


# ── Respuesta del usuario ──────────────────────────────────────────────────

class RespuestaIn(BaseModel):
    """
    valor:
      1  = Sí
      0  = No sé / más o menos
     -1  = No
    """
    valor: int  # -1, 0 o 1


# ── Estado de la sesión ────────────────────────────────────────────────────

class CandidatoOut(BaseModel):
    personaje: PersonajeOut
    score: float


class EstadoOut(BaseModel):
    sesion_id: str
    turno: int
    candidatos: list[CandidatoOut]
    adivinanza: Optional[PersonajeOut]
    confianza: Optional[float]
    terminado: bool


# ── Siguiente pregunta ─────────────────────────────────────────────────────

class SiguientePreguntaOut(BaseModel):
    pregunta: Optional[PreguntaOut]
    terminado: bool
    adivinanza: Optional[PersonajeOut]
    confianza: Optional[float]
