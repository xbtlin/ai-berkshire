import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "复利学堂 · 看懂一家公司",
  description: "12 章财报课程、互动实验室与出师挑战。从财务数字，走向独立判断。",
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-CN">
      <body className="antialiased">{children}</body>
    </html>
  );
}
