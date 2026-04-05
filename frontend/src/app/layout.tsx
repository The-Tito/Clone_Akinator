import type { Metadata } from "next"
import { Cinzel, Nunito } from "next/font/google"
import "./globals.css"

const cinzel = Cinzel({
  subsets: ["latin"],
  variable: "--font-cinzel",
  weight: ["400", "700", "900"],
})

const nunito = Nunito({
  subsets: ["latin"],
  variable: "--font-nunito",
  weight: ["400", "600", "700", "800"],
})

export const metadata: Metadata = {
  title: "Puginator — El Pug Oráculo",
  description: "Piensa en un personaje famoso. El Pug Oráculo lo adivinará.",
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className={`${cinzel.variable} ${nunito.variable}`}>
      <body className="antialiased">{children}</body>
    </html>
  )
}
