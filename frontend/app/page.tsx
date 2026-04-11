import Link from "next/link";

export default function HomePage() {
  return (
    <div className="relative overflow-hidden">
      {/* Background Orbs */}
      <div className="absolute top-0 right-0 -translate-y-1/2 translate-x-1/2 w-[600px] h-[600px] bg-blue-600/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-0 left-0 translate-y-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-indigo-600/20 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-6 py-24 sm:py-32 flex flex-col items-center text-center relative z-10">
        <div className="inline-flex items-center gap-2 bg-white/5 border border-white/10 px-4 py-2 rounded-full mb-8 backdrop-blur-sm">
          <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-sm font-medium text-slate-400">Powered by Gemini 1.5 Flash</span>
        </div>
        
        <h1 className="text-5xl sm:text-7xl font-extrabold tracking-tight mb-8">
          Your personal finance, <br />
          <span className="bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
            powered by AI.
          </span>
        </h1>
        
        <p className="text-lg text-slate-400 max-w-2xl mb-12 leading-relaxed">
          FinanceAgent parses your password-protected bank statements, extracts every transaction, 
          and provides agentic advice tailored to your spending habits and financial goals.
        </p>

        <div className="flex flex-col sm:flex-row gap-4">
          <Link 
            href="/chat" 
            className="bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-2xl font-bold text-lg transition-all shadow-xl shadow-blue-500/20 active:scale-95"
          >
            Start Chatting
          </Link>
          <Link 
            href="/upload" 
            className="bg-white/5 hover:bg-white/10 border border-white/10 text-white px-8 py-4 rounded-2xl font-bold text-lg transition-all backdrop-blur-sm active:scale-95"
          >
            Upload Statement
          </Link>
        </div>

        <div className="mt-24 grid grid-cols-1 sm:grid-cols-3 gap-8 w-full max-w-5xl">
          {[
            {
              title: "Smart Parsing",
              desc: "Upload PDFs (even password-protected ones) and CSVs. Our AI does the rest.",
              icon: "📄"
            },
            {
              title: "Persistent Memory",
              desc: "Our agent remembers your goals across sessions for truly personalized advice.",
              icon: "🧠"
            },
            {
              title: "Deep Analysis",
              desc: "Detect anomalies, categorize spending, and generate actionable savings plans.",
              icon: "📊"
            }
          ].map((feature, i) => (
            <div key={i} className="bg-white/5 border border-white/10 p-8 rounded-3xl text-left backdrop-blur-sm">
              <div className="text-3xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
              <p className="text-slate-400 leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
