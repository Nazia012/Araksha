import type { Metadata } from 'next';
import './globals.css';
import Link from 'next/link';
import ThemeToggle from './ThemeToggle';

export const metadata: Metadata = {
  title: 'Araksha | Prescription & Drug Safety Inspector',
  description: 'Araksha: Simple, safe prescription scanner verifying drug interactions and translating into plain English with Google Gemma 4.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <header className="site-header">
          <div className="nav-container">
            <div className="brand-wrapper">
              <Link href="/" className="brand-wrapper">
                <div className="brand-icon">℞</div>
                <div>
                  <span className="brand-title">Araksha</span>
                  <span className="brand-pill">Gemma 4</span>
                </div>
              </Link>
            </div>

            <nav className="nav-links">
              <Link href="/" className="nav-item">Check Prescription</Link>
              <Link href="/pipeline" className="nav-item">How It Works</Link>
              <Link href="/drugs" className="nav-item">Medicine Catalog</Link>
            </nav>

            <div className="header-actions">
              <ThemeToggle />
              <div className="badge-status">
                <span className="status-dot"></span>
                <span>Active</span>
              </div>
            </div>
          </div>
        </header>

        <main>{children}</main>

        <footer className="site-footer">
          <p>
            Araksha • Real Doctor Handwriting Testing (RxHandBD) + Verified Medical Database + Google Gemma 4 Plain Language
          </p>
          <p style={{ marginTop: '6px', fontSize: '0.72rem', opacity: 0.7 }}>
            This tool is for informational reference and does not replace the judgment of your pharmacist or physician.
          </p>
        </footer>
      </body>
    </html>
  );
}
