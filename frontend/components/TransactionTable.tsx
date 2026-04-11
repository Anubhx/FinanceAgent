"use client";

import React from "react";

interface Transaction {
  date: string;
  name: string;
  amount: number;
  category: string;
}

export default function TransactionTable({ transactions }: { transactions: Transaction[] }) {
  if (!transactions || transactions.length === 0) {
    return (
      <div className="text-center py-20 bg-white/5 border border-white/10 rounded-3xl">
        <p className="text-slate-400">No transactions found. Upload a statement to get started.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto bg-white/5 border border-white/10 rounded-3xl backdrop-blur-md">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-white/10 text-xs font-bold uppercase tracking-wider text-slate-500">
            <th className="px-6 py-4">Date</th>
            <th className="px-6 py-4">Description</th>
            <th className="px-6 py-4 text-right">Amount (₹)</th>
            <th className="px-6 py-4">Category</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-white/5">
          {transactions.map((t, i) => (
            <tr key={i} className="hover:bg-white/5 transition-colors group">
              <td className="px-6 py-4 text-sm text-slate-400 font-mono italic">{t.date}</td>
              <td className="px-6 py-4 text-sm font-medium group-hover:text-blue-400 transition-colors uppercase">{t.name}</td>
              <td className={`px-6 py-4 text-sm font-bold text-right ${t.amount < 0 ? 'text-red-400' : 'text-green-400'}`}>
                {t.amount.toLocaleString()}
              </td>
              <td className="px-6 py-4">
                <span className="text-[10px] font-bold uppercase px-2 py-1 rounded-md bg-white/10 text-slate-300 border border-white/10">
                  {t.category}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
