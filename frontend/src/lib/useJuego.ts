"use client"

import { useState, useCallback } from "react"
import type { EstadoJuego, ValorRespuesta, Personaje, Pregunta } from "@/types"
import {
  nuevaSesion,
  obtenerPregunta,
  registrarPregunta,
  enviarRespuesta,
} from "@/lib/api"

// ── Estado inicial ──────────────────────────────────────────────────────────

const ESTADO_INICIAL: EstadoJuego = {
  fase: "inicio",
  sesionId: null,
  preguntaActual: null,
  turno: 0,
  confianza: 0,
  adivinanza: null,
  terminado: false,
}

// ── Hook ────────────────────────────────────────────────────────────────────

export function useJuego() {
  const [estado, setEstado] = useState<EstadoJuego>(ESTADO_INICIAL)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState<string | null>(null)

  // ── Helpers internos ──────────────────────────────────────────────────────

  const limpiarError = () => setError(null)

  const manejarError = (err: unknown) => {
    const mensaje = err instanceof Error ? err.message : "Error inesperado"
    setError(mensaje)
  }

  // ── Cargar siguiente pregunta ─────────────────────────────────────────────

  const cargarSiguientePregunta = useCallback(async (sesionId: string) => {
    const resultado = await obtenerPregunta(sesionId)

    // El juego terminó → mostrar adivinanza
    if (resultado.terminado || !resultado.pregunta) {
      setEstado((prev) => ({
        ...prev,
        fase: "fin",
        adivinanza: resultado.adivinanza,
        confianza: resultado.confianza ?? prev.confianza,
        terminado: true,
        preguntaActual: null,
      }))
      return
    }

    // Registrar la pregunta en el backend antes de mostrarla
    await registrarPregunta(sesionId, resultado.pregunta.id)

    setEstado((prev) => ({
      ...prev,
      fase: "jugando",
      preguntaActual: resultado.pregunta as Pregunta,
      confianza: resultado.confianza ?? prev.confianza,
    }))
  }, [])

  // ── Iniciar juego ─────────────────────────────────────────────────────────

  const iniciarJuego = useCallback(async () => {
    setCargando(true)
    limpiarError()

    try {
      const sesion = await nuevaSesion()

      setEstado({
        ...ESTADO_INICIAL,
        fase: "jugando",
        sesionId: sesion.sesion_id,
      })

      await cargarSiguientePregunta(sesion.sesion_id)
    } catch (err) {
      manejarError(err)
    } finally {
      setCargando(false)
    }
  }, [cargarSiguientePregunta])

  // ── Responder pregunta ────────────────────────────────────────────────────

  const responder = useCallback(
    async (valor: ValorRespuesta) => {
      if (!estado.sesionId || !estado.preguntaActual) return

      setCargando(true)
      limpiarError()

      try {
        const estadoActualizado = await enviarRespuesta(estado.sesionId, valor)

        setEstado((prev) => ({
          ...prev,
          turno: estadoActualizado.turno,
          confianza: estadoActualizado.confianza ?? prev.confianza,
          terminado: estadoActualizado.terminado,
        }))

        // Si el backend marcó como terminado, mostrar adivinanza
        if (estadoActualizado.terminado) {
          setEstado((prev) => ({
            ...prev,
            fase: "fin",
            adivinanza: estadoActualizado.adivinanza,
          }))
          return
        }

        // Siguiente pregunta
        await cargarSiguientePregunta(estado.sesionId)
      } catch (err) {
        manejarError(err)
      } finally {
        setCargando(false)
      }
    },
    [estado.sesionId, estado.preguntaActual, cargarSiguientePregunta]
  )

  // ── Reiniciar ─────────────────────────────────────────────────────────────

  const reiniciar = useCallback(() => {
    setEstado(ESTADO_INICIAL)
    setError(null)
  }, [])

  return {
    estado,
    cargando,
    error,
    iniciarJuego,
    responder,
    reiniciar,
  }
}
