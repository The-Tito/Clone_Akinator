// ── Entidades base ─────────────────────────────────────────────────────────

export interface Personaje {
  id: number
  nombre: string
  descripcion: string | null
  imagen_url: string | null
}

export interface Pregunta {
  id: number
  texto: string
  categoria: string | null
}

// ── Respuestas de la API ───────────────────────────────────────────────────

export interface SesionOut {
  sesion_id: string
  mensaje: string
}

export interface Candidato {
  personaje: Personaje
  score: number
}

export interface EstadoOut {
  sesion_id: string
  turno: number
  candidatos: Candidato[]
  adivinanza: Personaje | null
  confianza: number | null
  terminado: boolean
}

export interface SiguientePreguntaOut {
  pregunta: Pregunta | null
  terminado: boolean
  adivinanza: Personaje | null
  confianza: number | null
}

// ── Valores de respuesta ───────────────────────────────────────────────────

export type ValorRespuesta = 1 | 0 | -1

export interface RespuestaIn {
  valor: ValorRespuesta
}

// ── Estado del juego en el cliente ─────────────────────────────────────────

export type FaseJuego = "inicio" | "jugando" | "adivinando" | "fin"

export interface EstadoJuego {
  fase: FaseJuego
  sesionId: string | null
  preguntaActual: Pregunta | null
  turno: number
  confianza: number
  adivinanza: Personaje | null
  terminado: boolean
}
