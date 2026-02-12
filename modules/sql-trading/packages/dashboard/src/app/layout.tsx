import type { Metadata, Viewport } from "next";
import { QueryProvider } from "@/lib/query-provider";
import { ThemeProvider } from "@/lib/theme-provider";
import { BottomNav } from "@/components/layout/BottomNav";
import { Header } from "@/components/layout/Header";
import "./globals.css";

export const metadata: Metadata = {
  title: "마켓브리핑 — 글로벌 금융 시장 대시보드",
  description: "매일 오전 9시, 오후 11시 AI가 최신 시장 데이터를 분석하여 업데이트합니다.",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#0f172a",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko" data-theme="dark" suppressHydrationWarning>
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
        />
      </head>
      <body className="antialiased">
        <ThemeProvider>
          <QueryProvider>
            <Header />
            <main className="max-w-[960px] mx-auto px-5 pt-4 pb-28">
              {children}
            </main>
            <BottomNav />
          </QueryProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}
