import UploadDropzone from "@/components/UploadDropzone";

export default function UploadPage() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-12 sm:py-24">
      <div className="text-center mb-12">
        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight mb-4">
          Upload your statement
        </h1>
        <p className="text-lg text-slate-400 max-w-xl mx-auto">
          We support PDF and CSV formats from most major Indian banks. 
          If your PDF is password-protected, we'll ask for it securely.
        </p>
      </div>

      <UploadDropzone />

      <div className="mt-24 grid grid-cols-1 sm:grid-cols-2 gap-8">
        <div className="flex gap-4 p-6 rounded-3xl bg-white/5 border border-white/10">
          <div className="text-2xl">🔒</div>
          <div>
            <h4 className="font-bold mb-1">Privacy First</h4>
            <p className="text-sm text-slate-400">Passwords are used in-memory only and never stored. Your data stays yours.</p>
          </div>
        </div>
        <div className="flex gap-4 p-6 rounded-3xl bg-white/5 border border-white/10">
          <div className="text-2xl">⚡</div>
          <div>
            <h4 className="font-bold mb-1">Fast Processing</h4>
            <p className="text-sm text-slate-400">Our parser extracts transactions in seconds, including merchant normalization.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
