import ChatWindow from "@/components/ChatWindow";

export default function ChatPage() {
  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <div className="flex flex-col lg:flex-row gap-8 items-start">
        {/* Sidebar Info */}
        <div className="w-full lg:w-80 space-y-6">
          <div className="bg-white/5 border border-white/10 p-6 rounded-3xl">
            <h3 className="font-bold mb-4">Chat Tips</h3>
            <ul className="space-y-4 text-sm text-slate-400">
              <li className="flex gap-2">
                <span>💡</span>
                <span>Ask "What's my spending summary?" to see where your money goes.</span>
              </li>
              <li className="flex gap-2">
                <span>⚠️</span>
                <span>"Detect any anomalies in my last statement."</span>
              </li>
              <li className="flex gap-2">
                <span>📈</span>
                <span>"Can you suggest a savings plan for me?"</span>
              </li>
            </ul>
          </div>

          <div className="bg-gradient-to-br from-indigo-600/20 to-blue-600/20 border border-white/10 p-6 rounded-3xl">
            <h3 className="font-bold mb-2">AI Memory</h3>
            <p className="text-xs text-slate-400 leading-relaxed mb-4">
              I remember your preferences and goals across sessions to provide more relevant advice.
            </p>
            <div className="flex items-center gap-2 text-xs font-medium text-blue-400 bg-blue-400/10 w-fit px-2 py-1 rounded-md">
              <span className="w-1 h-1 bg-blue-400 rounded-full animate-pulse" />
              Mem0 Persistent Cache
            </div>
          </div>
        </div>

        {/* Main Chat Area */}
        <div className="flex-1 w-full">
          <ChatWindow />
        </div>
      </div>
    </div>
  );
}
