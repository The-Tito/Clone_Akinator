"""
Motor de decisión del Akinator
==============================
Implementa el algoritmo de scoring y selección de preguntas.

Flujo:
  1. Al iniciar sesión → todos los personajes tienen score igual (1.0)
  2. Por cada respuesta → se recalcula el score de cada personaje
  3. Se elige la siguiente pregunta con mayor ganancia de información
  4. Si un personaje supera UMBRAL_ADIVINANZA → adivinar
"""

from sqlalchemy.orm import Session
from app.models import Personaje, Pregunta, Atributo

UMBRAL_ADIVINANZA = 0.75
MAX_PREGUNTAS = 20


def calcular_compatibilidad(respuesta_usuario: int, valor_atributo: int) -> float:
    return 1.0 - abs(respuesta_usuario - valor_atributo) / 2.0


def calcular_ganancia_informacion(
    pregunta_id: int,
    scores_actuales: dict,
    db: Session
) -> float:
    atributos = db.query(Atributo).filter(Atributo.pregunta_id == pregunta_id).all()

    total_score = sum(scores_actuales.values())
    if total_score == 0:
        return 0.0

    mejor_ganancia = 0.0

    for respuesta_simulada in [1, 0, -1]:
        scores_si = []
        scores_no = []

        for atributo in atributos:
            pid = atributo.personaje_id
            if pid not in scores_actuales:
                continue

            compat = calcular_compatibilidad(respuesta_simulada, atributo.valor)
            nuevo_score = scores_actuales[pid] * compat

            if compat >= 0.5:
                scores_si.append(nuevo_score)
            else:
                scores_no.append(nuevo_score)

        total_si = sum(scores_si)
        total_no = sum(scores_no)
        total = total_si + total_no

        if total > 0:
            balance = 1.0 - abs(total_si - total_no) / total
            mejor_ganancia = max(mejor_ganancia, balance)

    return mejor_ganancia


def siguiente_pregunta(scores: dict, preguntas_hechas: list, db: Session):
    todas_preguntas = db.query(Pregunta).all()
    preguntas_disponibles = [p for p in todas_preguntas if p.id not in preguntas_hechas]

    if not preguntas_disponibles:
        return None

    mejor_pregunta = max(
        preguntas_disponibles,
        key=lambda p: calcular_ganancia_informacion(p.id, scores, db)
    )

    return mejor_pregunta


def actualizar_scores(scores: dict, pregunta_id: int, respuesta_usuario: int, db: Session) -> dict:
    atributos = db.query(Atributo).filter(Atributo.pregunta_id == pregunta_id).all()
    nuevos_scores = dict(scores)

    for atributo in atributos:
        pid = atributo.personaje_id
        if pid in nuevos_scores:
            compat = calcular_compatibilidad(respuesta_usuario, atributo.valor)
            nuevos_scores[pid] = nuevos_scores[pid] * compat

    return nuevos_scores


def evaluar_adivinanza(scores: dict, db: Session):
    total = sum(scores.values())
    if total == 0:
        return None, 0.0

    mejor_id = max(scores, key=lambda pid: scores[pid])
    mejor_score = scores[mejor_id]
    confianza = mejor_score / total

    if confianza >= UMBRAL_ADIVINANZA:
        personaje = db.query(Personaje).filter(Personaje.id == mejor_id).first()
        return personaje, confianza

    return None, confianza


def scores_iniciales(db: Session) -> dict:
    personajes = db.query(Personaje).all()
    return {p.id: 1.0 for p in personajes}
