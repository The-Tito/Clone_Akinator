"use client"

interface Props {
  confianza: number
  turno: number
}

export function BarraConfianza({ confianza, turno }: Props) {
  const porcentaje = Math.round(confianza * 100)

  return (
    <div style={{ width: "100%", maxWidth: 400 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 8 }}>
        <span style={{ fontFamily: "var(--font-display)", fontSize: "0.65rem", letterSpacing: "0.15em", color: "#06b6d4", textTransform: "uppercase" }}>
          Aura Mental
        </span>
        <span style={{ fontFamily: "var(--font-body)", fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: 700 }}>
          {turno > 0 ? `Pregunta ${turno}` : ""} {porcentaje > 0 ? `· ${porcentaje}%` : ""}
        </span>
      </div>
      <div className="aura-bar-track">
        <div className="aura-bar-fill" style={{ width: `${Math.max(porcentaje, 4)}%` }} />
      </div>
    </div>
  )
}
