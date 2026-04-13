import { ClerkProvider, SignInButton, Show, UserButton } from "@clerk/nextjs";
import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Kuber AI — Your Personal Finance AI",
  description: "AI-powered agent for bank statement analysis and financial advice.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en" className="dark">
        <body className={`${inter.className} bg-slate-950 text-slate-50 min-h-screen antialiased`}>
          <header className="fixed top-0 w-full z-50 bg-slate-950/80 backdrop-blur-md border-b border-white/10 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold text-white shadow-lg shadow-blue-500/20">
                K
              </div>
              <span className="text-xl font-bold tracking-tight">Kuber AI</span>
            </div>
            <nav className="flex items-center gap-6">
              <Show when="signed-in">
                <div className="flex gap-6 mr-6">
                  <a href="/dashboard" className="text-sm font-medium text-slate-400 hover:text-white transition-colors">Dashboard</a>
                  <a href="/chat" className="text-sm font-medium text-slate-400 hover:text-white transition-colors">Chat</a>
                  <a href="/upload" className="text-sm font-medium text-slate-400 hover:text-white transition-colors">Upload</a>
                </div>
                <UserButton />
              </Show>
              <Show when="signed-out">
                <SignInButton mode="modal">
                  <button className="bg-white text-slate-950 px-4 py-2 rounded-full text-sm font-semibold hover:bg-slate-200 transition-all active:scale-95">
                    Sign In
                  </button>
                </SignInButton>
              </Show>
            </nav>
          </header>
          <main className="pt-20">
            {children}
          </main>
        </body>
      </html>
    </ClerkProvider>
  );
}