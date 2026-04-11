"use client";

import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { useAuth, useUser } from "@clerk/nextjs";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatWindow() {
  const { userId } = useAuth();
  const { user } = useUser();
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Hi! I'm your FinanceAgent. Have you uploaded your bank statement yet? I can help you analyze your spending, detect anomalies, or create a savings plan." }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !userId) return;

    const userMessage = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/chat`,
        { user_id: userId, message: userMessage }
      );

      setMessages(prev => [...prev, { role: "assistant", content: response.data.reply }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: "assistant", content: "Sorry, I encountered an error. Please try again later." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[70vh] w-full max-w-4xl mx-auto bg-white/5 border border-white/10 rounded-3xl overflow-hidden backdrop-blur-md">
      {/* Chat Header */}
      <div className="p-6 border-b border-white/10 bg-white/5 flex items-center gap-3">
        <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center shadow-lg shadow-blue-500/20">
          🤖
        </div>
        <div>
          <h3 className="font-bold">Finance Agent</h3>
          <p className="text-xs text-green-400 flex items-center gap-1">
            <span className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
            Online & Ready
          </p>
        </div>
      </div>

      {/* Messages */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[80%] p-4 rounded-2xl ${
              msg.role === "user" 
              ? "bg-blue-600 text-white shadow-lg shadow-blue-500/10 rounded-tr-none" 
              : "bg-white/10 text-slate-100 rounded-tl-none border border-white/5"
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white/10 p-4 rounded-2xl rounded-tl-none border border-white/5 flex gap-1">
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" />
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.2s]" />
              <span className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce [animation-delay:0.4s]" />
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-6 border-t border-white/10 bg-white/5">
        <div className="flex gap-4">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask anything about your finances..."
            className="flex-1 bg-white/5 border border-white/10 rounded-2xl px-6 py-4 focus:outline-none focus:border-blue-500 transition-colors"
          />
          <button 
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed text-white w-14 h-14 rounded-2xl flex items-center justify-center shadow-lg shadow-blue-500/20 transition-all active:scale-95"
          >
            <span className="text-xl">↗️</span>
          </button>
        </div>
      </div>
    </div>
  );
}
