import type { Metadata } from 'next';
import { Space_Grotesk } from 'next/font/google';
import './globals.css';

const display = Space_Grotesk({ subsets: ['latin'], variable: '--font-display' });

export const metadata: Metadata = {
  title: 'Company Information Extractor',
  description: 'Extract and organize company data using web scraping + AI',
  icons: {
    icon: '🔍',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`antialiased ${display.variable} bg-[#040404] text-slate-100`}>
        <div className="min-h-screen bg-gradient-to-br from-[#050505] via-[#0a0a0a] to-[#050505]">
          {children}
        </div>
      </body>
    </html>
  );
}
