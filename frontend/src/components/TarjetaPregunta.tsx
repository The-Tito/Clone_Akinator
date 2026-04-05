"use client"

import type { Pregunta, ValorRespuesta } from "@/types"

interface Props {
  pregunta: Pregunta
  cargando: boolean
  onResponder: (valor: ValorRespuesta) => void
}

const BOTONES: {
  label: string
  valor: ValorRespuesta
  emoji: string
  color: string
  bg: string
}[] = [
  { label: "Sí",       valor:  1, emoji: "✓", color: "#10b981", bg: "rgba(16,185,129,0.15)" },
  { label: "No",       valor: -1, emoji: "✕", color: "#ef4444", bg: "rgba(239,68,68,0.15)"  },
  { label: "No lo sé", valor:  0, emoji: "?", color: "#a855f7", bg: "rgba(168,85,247,0.15)" },
]

export function TarjetaPregunta({ pregunta, cargando, onResponder }: Props) {
  return (
    <div className="flex flex-col items-center gap-8 w-full">
      <div className="speech-bubble bubble-in max-w-sm w-full text-center">
        <p style={{ fontFamily: "var(--font-body)", fontSize: "1.2rem", fontWeight: 700, color: "var(--text-primary)", lineHeight: 1.4 }}>
          {pregunta.texto}
        </p>
      </div>

      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap", justifyContent: "center" }} className="fade-up">
        {BOTONES.map(({ label, valor, emoji, color, bg }) => (
          <button
            key={valor}
            onClick={() => onResponder(valor)}
            disabled={cargando}
            className="btn-respuesta"
          >
            <span className="icon-circle" style={{ background: bg, color, fontWeight: 900 }}>
              {emoji}
            </span>
            <span style={{ color: "var(--text-muted)" }}>{label}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
