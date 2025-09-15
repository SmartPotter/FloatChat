import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'FloatChat - ARGO Float Data Explorer',
  description: 'AI-powered conversational interface for ARGO float oceanographic data',
  keywords: 'oceanography, ARGO, float, data, analysis, AI, chat',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-ocean-50">
          {children}
        </div>
      </body>
    </html>
  )
}