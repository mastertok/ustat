import type { Metadata } from 'next';
import { Geist } from 'next/font/google';
import { Providers } from '@/components/providers';
import './globals.css';

const geist = Geist({
  subsets: ['latin'],
  variable: '--font-geist',
});

export const metadata: Metadata = {
  title: 'Устат - Онлайн обучение',
  description: 'Устат - платформа для онлайн обучения. Учитесь у лучших преподавателей и получайте новые навыки.',
  keywords: ['онлайн обучение', 'курсы', 'образование', 'репетиторы', 'преподаватели'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru" suppressHydrationWarning>
      <body className={`${geist.variable} font-sans antialiased`}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
