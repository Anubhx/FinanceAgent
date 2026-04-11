"use client";

import React, { useEffect, useState } from "react";
import TransactionTable from "@/components/TransactionTable";
import axios from "axios";
import { useAuth } from "@clerk/nextjs";

interface Transaction {
  date: string;
  name: string;
  amount: number;
  category: string;
}

export default function DashboardPage() {
  const { userId } = useAuth();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      fetchData();
    }
  }, [userId]);

  const fetchData = async () => {
    try {
      const response = await axios.get(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/transactions?user_id=${userId}`);
      setTransactions(response.data);
    } catch (error) {
      console.error("Failed to fetch transactions:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const totalExpense = transactions
    .filter(t => t.amount < 0)
    .reduce((acc, t) => acc + Math.abs(t.amount), 0);
    
  const totalIncome = transactions
    .filter(t => t.amount > 0)
    .reduce((acc, t) => acc + t.amount, 0);

  return (
    <div className="max-w-7xl mx-auto px-6 py-12">
      <div className="flex flex-col sm:flex-row justify-between items-end mb-12 gap-6">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight mb-2">Dashboard</h1>
          <p className="text-slate-400">Your financial overview and recent transactions.</p>
        </div>
        <div className="flex gap-4">
          <div className="bg-white/5 border border-white/10 px-6 py-3 rounded-2xl backdrop-blur-md">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Total Spending</p>
            <p className="text-2xl font-bold text-red-400">₹{totalExpense.toLocaleString()}</p>
          </div>
          <div className="bg-white/5 border border-white/10 px-6 py-3 rounded-2xl backdrop-blur-md">
            <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-1">Total Income</p>
            <p className="text-2xl font-bold text-green-400">₹{totalIncome.toLocaleString()}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold">Recent Transactions</h2>
            <button 
              onClick={fetchData}
              className="text-sm font-medium text-blue-400 hover:text-blue-300 transition-colors"
            >
              Refresh
            </button>
          </div>
          {isLoading ? (
            <div className="h-64 bg-white/5 animate-pulse rounded-3xl" />
          ) : (
            <TransactionTable transactions={transactions} />
          )}
        </div>

        <div className="space-y-6">
          <h2 className="text-xl font-bold">Spending by Category</h2>
          <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-md">
            {/* Logic for category distribution visualization could go here */}
            {transactions.length > 0 ? (
              <ul className="space-y-4">
                {Array.from(new Set(transactions.map(t => t.category))).map(cat => {
                  const amount = transactions
                    .filter(t => t.category === cat && t.amount < 0)
                    .reduce((acc, t) => acc + Math.abs(t.amount), 0);
                  if (amount === 0) return null;
                  const percentage = (amount / totalExpense) * 100;
                  return (
                    <li key={cat} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-slate-300 font-medium">{cat}</span>
                        <span className="font-bold text-slate-100">₹{amount.toLocaleString()}</span>
                      </div>
                      <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-blue-500 rounded-full" 
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </li>
                  );
                })}
              </ul>
            ) : (
              <p className="text-sm text-slate-400">No data available.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
