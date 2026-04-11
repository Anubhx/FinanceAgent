"use client";

import React, { useState } from "react";
import axios from "axios";
import { useAuth } from "@clerk/nextjs";

export default function UploadDropzone() {
  const { userId } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [password, setPassword] = useState("");
  const [isPasswordRequired, setIsPasswordRequired] = useState(false);
  const [status, setStatus] = useState<"idle" | "uploading" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      // Check if it's a PDF to potentially show password field
      setIsPasswordRequired(selectedFile.type === "application/pdf");
      setStatus("idle");
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file || !userId) return;

    setStatus("uploading");
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_id", userId);
    formData.append("password", password);

    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/upload`,
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      if (response.data.success) {
        setStatus("success");
        setMessage(response.data.message);
        setFile(null);
        setPassword("");
      }
    } catch (error: any) {
      setStatus("error");
      const serverError = error.response?.data?.detail;
      setMessage(serverError || "Upload failed. Please check the file and password.");
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      <div className="bg-white/5 border-2 border-dashed border-white/10 rounded-3xl p-12 transition-all hover:border-blue-500/50 group text-center">
        {!file ? (
          <label className="cursor-pointer">
            <div className="text-5xl mb-4 group-hover:scale-110 transition-transform">📂</div>
            <h3 className="text-xl font-bold mb-2">Click to upload statement</h3>
            <p className="text-slate-400 text-sm">PDF or CSV files supported</p>
            <input 
              type="file" 
              className="hidden" 
              accept=".pdf,.csv" 
              onChange={handleFileChange} 
            />
          </label>
        ) : (
          <div className="space-y-6">
            <div className="flex items-center justify-between bg-white/5 p-4 rounded-2xl border border-white/10">
              <div className="flex items-center gap-3">
                <span className="text-2xl">📄</span>
                <div className="text-left">
                  <p className="font-medium truncate max-w-[200px]">{file.name}</p>
                  <p className="text-xs text-slate-500">{(file.size / 1024).toFixed(1)} KB</p>
                </div>
              </div>
              <button 
                onClick={() => setFile(null)}
                className="text-slate-500 hover:text-white transition-colors"
              >
                ✕
              </button>
            </div>

            {isPasswordRequired && (
              <div className="text-left space-y-2">
                <label className="text-sm font-medium text-slate-400">PDF Password (if protected)</label>
                <input 
                  type="password" 
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password..."
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-blue-500 transition-colors"
                />
                <p className="text-xs text-slate-500 italic">Passwords are never stored on our servers.</p>
              </div>
            )}

            <button 
              onClick={handleUpload}
              disabled={status === "uploading"}
              className={`w-full py-4 rounded-xl font-bold transition-all active:scale-95 ${
                status === "uploading" 
                ? "bg-slate-700 cursor-not-allowed" 
                : "bg-blue-600 hover:bg-blue-500 shadow-lg shadow-blue-500/20"
              }`}
            >
              {status === "uploading" ? "Parsing Statement..." : "Confirm & Parse"}
            </button>
          </div>
        )}
      </div>

      {status === "success" && (
        <div className="mt-6 bg-green-500/10 border border-green-500/20 text-green-400 p-4 rounded-2xl text-center text-sm font-medium">
          ✅ {message}
        </div>
      )}

      {status === "error" && (
        <div className="mt-6 bg-red-500/10 border border-red-500/20 text-red-400 p-4 rounded-2xl text-center text-sm font-medium">
          ❌ {message}
        </div>
      )}
    </div>
  );
}
