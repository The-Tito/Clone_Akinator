"use client"

import Image from "next/image"
import type { Personaje } from "@/types"

interface Props {
  adivinanza: Personaje | null
  confianza: number
  turno: number
  onReiniciar: () => void
}

export function Resultado({ adivinanza, confianza, turno, onReiniciar }: Props) {
  const porcentaje = Math.round(confianza * 100)

  return (
    <div className="flex flex-col items-center gap-8 text-center fade-up" style={{ maxWidth: 420 }}>
      {adivinanza ? (
        <>
          <div style={{ fontFamily: "var(--font-display)", fontSize: "0.8rem", letterSpacing: "0.2em", color: "var(--cyan-glow)", textTransform: "uppercase" }}>
            El Pug Oráculo ha hablado
          </div>

          {adivinanza.imagen_url && (
            <div className="aura-ring" style={{ borderRadius: "50%", padding: 4, background: "linear-gradient(135deg, #f97316, #a855f7)" }}>
              <div style={{ width: 160, height: 160, borderRadius: "50%", overflow: "hidden", position: "relative" }}>
                <Image src={adivinanza.imagen_url} alt={adivinanza.nombre} fill className="object-cover" unoptimized />
              </div>
            </div>
          )}

          <div>
            <p style={{ fontFamily: "var(--font-display)", fontSize: "2rem", fontWeight: 900, color: "var(--text-primary)", marginBottom: 8 }}>
              {adivinanza.nombre}
            </p>
            {adivinanza.descripcion && (
              <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", lineHeight: 1.5 }}>
                {adivinanza.descripcion}
              </p>
            )}
          </div>

          <div style={{ display: "flex", gap: 24, color: "var(--text-muted)", fontSize: "0.85rem" }}>
            <span><strong style={{ color: "var(--text-primary)" }}>{turno}</strong> preguntas</span>
            <span><strong style={{ color: "#10b981" }}>{porcentaje}%</strong> confianza</span>
          </div>
        </>
      ) : (
        <>
          <p style={{ fontFamily: "var(--font-display)", fontSize: "1.2rem", color: "var(--text-primary)" }}>
            El Pug no logró adivinarlo 😔
          </p>
          <p style={{ color: "var(--text-muted)" }}>¡Eres demasiado misterioso!</p>
        </>
      )}

      <button
        onClick={onReiniciar}
        className="btn-respuesta"
        style={{ marginTop: 8, flexDirection: "row", gap: 10, padding: "16px 40px", minWidth: "auto", fontSize: "0.9rem" }}
      >
        <span>🔄</span>
        <span style={{ color: "var(--text-primary)" }}>Jugar de nuevo</span>
      </button>
    </div>
  )
}
