
import './globals.css';
import 'fomantic-ui-css/semantic.css';

export const metadata = {
  title: 'Auto Maksu Kalkulaator',
  description: 'Saa teada enda auto maks',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
