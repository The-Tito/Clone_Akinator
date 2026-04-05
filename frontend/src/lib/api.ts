import type {
  SesionOut,
  EstadoOut,
  SiguientePreguntaOut,
  ValorRespuesta,
  Pregunta,
} from "@/types"

// ── Config ─────────────────────────────────────────────────────────────────

const API_URL = process.env.NEXT_PUBLIC_API_URL

if (!API_URL) {
  throw new Error("NEXT_PUBLIC_API_URL no está definida en las variables de entorno")
}

// ── Helper interno ─────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Error desconocido" }))
    throw new Error(error.detail ?? `HTTP ${res.status}`)
  }

  return res.json() as Promise<T>
}

// ── Endpoints ──────────────────────────────────────────────────────────────

/**
 * Inicia una nueva sesión de juego.
 * Devuelve el sesion_id único para esta partida.
 */
export async function nuevaSesion(): Promise<SesionOut> {
  return apiFetch<SesionOut>("/sesion/nueva", { method: "POST" })
}

/**
 * Obtiene la siguiente pregunta óptima para la sesión.
 * Si terminado=true, incluye la adivinanza final.
 */
export async function obtenerPregunta(sesionId: string): Promise<SiguientePreguntaOut> {
  return apiFetch<SiguientePreguntaOut>(`/sesion/${sesionId}/pregunta`)
}

/**
 * Registra en el backend que se está mostrando esta pregunta.
 * Debe llamarse justo antes de mostrar la pregunta al usuario.
 */
export async function registrarPregunta(
  sesionId: string,
  preguntaId: number
): Promise<Pregunta> {
  return apiFetch<Pregunta>(`/sesion/${sesionId}/preguntar/${preguntaId}`, {
    method: "POST",
  })
}

/**
 * Envía la respuesta del usuario a la pregunta actual.
 *  1 = Sí
 *  0 = No sé
 * -1 = No
 */
export async function enviarRespuesta(
  sesionId: string,
  valor: ValorRespuesta
): Promise<EstadoOut> {
  return apiFetch<EstadoOut>(`/sesion/${sesionId}/respuesta`, {
    method: "POST",
    body: JSON.stringify({ valor }),
  })
}

/**
 * Obtiene el estado completo de la sesión.
 * Útil para debug o para recuperar estado tras un reload.
 */
export async function obtenerEstado(sesionId: string): Promise<EstadoOut> {
  return apiFetch<EstadoOut>(`/sesion/${sesionId}/estado`)
}
