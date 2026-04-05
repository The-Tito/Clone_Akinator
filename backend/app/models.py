from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Personaje(Base):
    """
    Representa a un personaje que el Akinator puede adivinar.
    Ej: Harry Potter, Messi, Einstein
    """
    __tablename__ = "personajes"

    id          = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    imagen_url  = Column(String(255), nullable=True)

    # Un personaje tiene muchos atributos (sus respuestas a las preguntas)
    atributos = relationship("Atributo", back_populates="personaje", cascade="all, delete")


class Pregunta(Base):
    """
    Una pregunta que el Akinator puede hacer.
    Ej: '¿Es una persona real?', '¿Es deportista?'
    """
    __tablename__ = "preguntas"

    id        = Column(Integer, primary_key=True, index=True)
    texto     = Column(String(255), nullable=False, unique=True)
    categoria = Column(String(100), nullable=True)  # 'identidad', 'profesion', 'origen', etc.

    # Una pregunta tiene muchos atributos (una respuesta por personaje)
    atributos = relationship("Atributo", back_populates="pregunta", cascade="all, delete")


class Atributo(Base):
    """
    Tabla pivote que relaciona Personaje <-> Pregunta con un valor.

    valor:
      1  = Sí      (el personaje cumple la condición)
     -1  = No      (el personaje NO cumple la condición)
      0  = Más o menos / no aplica
    """
    __tablename__ = "atributos"

    id            = Column(Integer, primary_key=True, index=True)
    personaje_id  = Column(Integer, ForeignKey("personajes.id"), nullable=False)
    pregunta_id   = Column(Integer, ForeignKey("preguntas.id"), nullable=False)
    valor         = Column(Integer, nullable=False)  # -1, 0 o 1

    personaje = relationship("Personaje", back_populates="atributos")
    pregunta  = relationship("Pregunta",  back_populates="atributos")
