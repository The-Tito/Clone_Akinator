"""
Seed inicial: Harry Potter, Lionel Messi, Albert Einstein
Ejecutar con: python seed.py
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine
from app.models import Base, Personaje, Pregunta, Atributo

# ── 1. Crear tablas si no existen ──────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── 2. Datos ───────────────────────────────────────────────────────────────

PERSONAJES = [
    {
        "nombre": "Harry Potter",
        "descripcion": "Mago ficticio protagonista de la saga de J.K. Rowling",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/en/d/d7/Harry_Potter_character_poster.jpg",
    },
    {
        "nombre": "Lionel Messi",
        "descripcion": "Futbolista argentino considerado uno de los mejores de la historia",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/b/b4/Lionel-Messi-Argentina-2022-FIFA-World-Cup_%28cropped%29.jpg",
    },
    {
        "nombre": "Albert Einstein",
        "descripcion": "Físico teórico alemán, creador de la teoría de la relatividad",
        "imagen_url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
    },
]

PREGUNTAS = [
    {"texto": "¿Es una persona real?",                  "categoria": "identidad"},
    {"texto": "¿Es un personaje de ficción?",           "categoria": "identidad"},
    {"texto": "¿Es deportista?",                        "categoria": "profesion"},
    {"texto": "¿Es científico?",                        "categoria": "profesion"},
    {"texto": "¿Usa magia o poderes sobrenaturales?",   "categoria": "habilidades"},
    {"texto": "¿Es conocido mundialmente?",             "categoria": "fama"},
    {"texto": "¿Es de origen argentino?",               "categoria": "origen"},
    {"texto": "¿Nació en el siglo XX?",                 "categoria": "epoca"},
    {"texto": "¿Es famoso principalmente por su inteligencia?", "categoria": "fama"},
    {"texto": "¿Aparece en libros o películas famosas?","categoria": "media"},
]

# Matriz de atributos: [Harry Potter, Messi, Einstein]
# Orden de preguntas igual al array PREGUNTAS arriba
#  1 = Sí  |  -1 = No  |  0 = Más o menos
ATRIBUTOS = {
    "¿Es una persona real?":                           [-1,  1,  1],
    "¿Es un personaje de ficción?":                    [ 1, -1, -1],
    "¿Es deportista?":                                 [-1,  1, -1],
    "¿Es científico?":                                 [-1, -1,  1],
    "¿Usa magia o poderes sobrenaturales?":            [ 1, -1, -1],
    "¿Es conocido mundialmente?":                      [ 1,  1,  1],
    "¿Es de origen argentino?":                        [-1,  1, -1],
    "¿Nació en el siglo XX?":                          [-1,  1,  1],
    "¿Es famoso principalmente por su inteligencia?":  [ 1, -1,  1],
    "¿Aparece en libros o películas famosas?":         [ 1, -1,  0],
}

# ── 3. Insertar datos ──────────────────────────────────────────────────────

def seed():
    db = SessionLocal()

    # Limpiar tablas en orden para respetar FK
    db.query(Atributo).delete()
    db.query(Pregunta).delete()
    db.query(Personaje).delete()
    db.commit()

    # Insertar personajes
    personajes_db = []
    for p in PERSONAJES:
        obj = Personaje(**p)
        db.add(obj)
        personajes_db.append(obj)
    db.commit()
    for p in personajes_db:
        db.refresh(p)

    print(f"✅ {len(personajes_db)} personajes insertados")

    # Insertar preguntas
    preguntas_db = []
    for q in PREGUNTAS:
        obj = Pregunta(**q)
        db.add(obj)
        preguntas_db.append(obj)
    db.commit()
    for q in preguntas_db:
        db.refresh(q)

    print(f"✅ {len(preguntas_db)} preguntas insertadas")

    # Insertar atributos
    nombres_personajes = [p["nombre"] for p in PERSONAJES]
    count = 0

    for pregunta_db in preguntas_db:
        valores = ATRIBUTOS[pregunta_db.texto]
        for i, personaje_db in enumerate(personajes_db):
            atributo = Atributo(
                personaje_id=personaje_db.id,
                pregunta_id=pregunta_db.id,
                valor=valores[i],
            )
            db.add(atributo)
            count += 1

    db.commit()
    print(f"✅ {count} atributos insertados")
    print("\n🎉 Seed completado con éxito!")
    print(f"   Personajes: {', '.join(nombres_personajes)}")

    db.close()


if __name__ == "__main__":
    seed()
