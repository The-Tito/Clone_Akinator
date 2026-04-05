"use client";

import Image from "next/image";
import { useJuego } from "@/lib/useJuego";
import { TarjetaPregunta } from "@/components/TarjetaPregunta";
import { Resultado } from "@/components/Resultado";
import { BarraConfianza } from "@/components/BarraConfianza";

const PUG_IMG = "/puginator.png";

export default function JuegoPage() {
  const { estado, cargando, error, iniciarJuego, responder, reiniciar } =
    useJuego();

  return (
    <>
      {/* Fondo estrellado */}
      <div className="starfield" />

      <main
        style={{
          position: "relative",
          zIndex: 1,
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "24px 16px",
          gap: 0,
        }}
      >
        {/* ── PANTALLA DE INICIO ───────────────────────────────────────── */}
        {estado.fase === "inicio" && (
          <div
            className="fade-up flex flex-col items-center gap-8"
            style={{ maxWidth: 480, width: "100%", textAlign: "center" }}
          >
            <div>
              <p
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: "0.7rem",
                  letterSpacing: "0.25em",
                  color: "var(--cyan-glow)",
                  textTransform: "uppercase",
                  marginBottom: 12,
                }}
              >
                El Oráculo de los Pugs
              </p>
              <h1
                className="font-display"
                style={{
                  fontSize: "clamp(2.5rem, 8vw, 4rem)",
                  fontWeight: 900,
                  color: "var(--text-primary)",
                  lineHeight: 1,
                }}
              >
                Puginator
              </h1>
            </div>

            {/* Pug con aura */}
            <div style={{ position: "relative" }}>
              <div
                className="aura-ring pug-float"
                style={{
                  borderRadius: "50%",
                  padding: 6,
                  background:
                    "linear-gradient(135deg, #f97316, #a855f7, #06b6d4)",
                }}
              >
                <div
                  style={{
                    width: 200,
                    height: 200,
                    borderRadius: "50%",
                    overflow: "hidden",
                    position: "relative",
                    background: "#0f1535",
                  }}
                >
                  <Image
                    src={PUG_IMG}
                    alt="Pug Oráculo"
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
              </div>
            </div>

            <p
              style={{
                color: "var(--text-muted)",
                fontSize: "1rem",
                lineHeight: 1.6,
                fontWeight: 600,
              }}
            >
              Piensa en un personaje famoso.
              <br />
              El Pug Oráculo lo adivinará con unas pocas preguntas.
            </p>

            {error && (
              <p
                style={{
                  color: "#f87171",
                  background: "rgba(239,68,68,0.1)",
                  padding: "12px 20px",
                  borderRadius: 12,
                  fontSize: "0.85rem",
                }}
              >
                {error}
              </p>
            )}

            <button
              onClick={iniciarJuego}
              disabled={cargando}
              style={{
                padding: "18px 56px",
                borderRadius: 20,
                border: "1px solid rgba(249,115,22,0.4)",
                background:
                  "linear-gradient(135deg, rgba(249,115,22,0.2), rgba(168,85,247,0.2))",
                color: "var(--text-primary)",
                fontFamily: "var(--font-display)",
                fontSize: "0.9rem",
                letterSpacing: "0.15em",
                cursor: cargando ? "not-allowed" : "pointer",
                opacity: cargando ? 0.5 : 1,
                transition: "all 0.3s ease",
                backdropFilter: "blur(12px)",
              }}
            >
              {cargando ? "Invocando al Pug..." : "✦ Comenzar ✦"}
            </button>
          </div>
        )}

        {/* ── PANTALLA DE JUEGO ────────────────────────────────────────── */}
        {estado.fase === "jugando" && (
          <div
            className="flex flex-col items-center fade-up"
            style={{ width: "100%", maxWidth: 560, gap: 0 }}
          >
            {/* Título pequeño */}
            <p
              className="font-display"
              style={{
                fontSize: "0.65rem",
                letterSpacing: "0.2em",
                color: "var(--text-muted)",
                textTransform: "uppercase",
                marginBottom: 32,
              }}
            >
              Puginator · El Oráculo
            </p>

            {/* Pregunta (burbuja) */}
            <div style={{ width: "100%", marginBottom: 32 }}>
              {cargando && !estado.preguntaActual ? (
                <div className="speech-bubble" style={{ textAlign: "center" }}>
                  <p style={{ color: "var(--text-muted)", fontWeight: 700 }}>
                    El Pug está meditando…
                  </p>
                </div>
              ) : estado.preguntaActual ? (
                <TarjetaPregunta
                  pregunta={estado.preguntaActual}
                  cargando={cargando}
                  onResponder={responder}
                />
              ) : null}
            </div>

            {/* Pug oráculo */}
            <div style={{ position: "relative", marginBottom: 32 }}>
              <div
                className={`aura-ring pug-float`}
                style={{
                  borderRadius: "50%",
                  padding: 5,
                  background:
                    "linear-gradient(135deg, #f97316, #a855f7, #06b6d4)",
                }}
              >
                <div
                  style={{
                    width: 160,
                    height: 160,
                    borderRadius: "50%",
                    overflow: "hidden",
                    position: "relative",
                    background: "#0f1535",
                  }}
                >
                  <Image
                    src={PUG_IMG}
                    alt="Pug Oráculo"
                    fill
                    className="object-cover"
                    unoptimized
                  />
                </div>
              </div>
              {/* Orb decorativo */}
              <div
                style={{
                  position: "absolute",
                  bottom: -8,
                  right: -8,
                  width: 36,
                  height: 36,
                  borderRadius: "50%",
                  background: "linear-gradient(135deg, #a855f7, #06b6d4)",
                  opacity: 0.8,
                  boxShadow: "0 0 16px #a855f7",
                }}
              />
            </div>

            {/* Barra de aura */}
            <BarraConfianza confianza={estado.confianza} turno={estado.turno} />

            {/* Error */}
            {error && (
              <p
                style={{
                  marginTop: 16,
                  color: "#f87171",
                  background: "rgba(239,68,68,0.1)",
                  padding: "10px 18px",
                  borderRadius: 10,
                  fontSize: "0.8rem",
                  textAlign: "center",
                }}
              >
                {error}
              </p>
            )}
          </div>
        )}

        {/* ── PANTALLA DE FIN ──────────────────────────────────────────── */}
        {estado.fase === "fin" && (
          <div
            className="flex flex-col items-center"
            style={{ width: "100%", maxWidth: 480 }}
          >
            <Resultado
              adivinanza={estado.adivinanza}
              confianza={estado.confianza}
              turno={estado.turno}
              onReiniciar={reiniciar}
            />
          </div>
        )}
      </main>
    </>
  );
}
