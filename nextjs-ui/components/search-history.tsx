'use client';

import { useState, useEffect } from 'react';
import { Trash2, RotateCcw } from 'lucide-react';

interface HistoryEntry {
  id: string;
  timestamp: string;
  data: any;
}

interface SearchHistoryProps {
  onSelect: (company: any) => void;
}

export default function SearchHistory({ onSelect }: SearchHistoryProps) {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem('company_history') || '[]');
    setHistory(stored);
  }, []);

  const deleteEntry = (id: string) => {
    const updated = history.filter(h => h.id !== id);
    setHistory(updated);
    localStorage.setItem('company_history', JSON.stringify(updated));
  };

  const clearAll = () => {
    if (confirm('Clear all search history?')) {
      setHistory([]);
      localStorage.removeItem('company_history');
    }
  };

  const loadCompany = (company: any) => {
    onSelect(company);
  };

  if (!expanded && history.length === 0) return null;

  return (
    <div className="bg-[#0b0b0f]/80 border border-red-900/60 rounded-lg p-4 mt-6 animate-fade-in">
      <div className="flex items-center justify-between mb-4 cursor-pointer" onClick={() => setExpanded(!expanded)}>
        <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <RotateCcw size={18} className="text-red-400" />
          Search History ({history.length})
        </h3>
        <span className="text-slate-400 text-sm">{expanded ? '▼' : '▶'}</span>
      </div>

      {expanded && (
        <div className="space-y-2">
          {history.length === 0 ? (
            <p className="text-slate-400 text-sm">No history yet. Start extracting companies to build your history.</p>
          ) : (
            <>
              {history.map((entry, idx) => (
                <div key={entry.id} className="flex items-center justify-between p-3 bg-[#0f0f12] border border-red-900/30 rounded-lg hover:border-red-600/60 transition-colors">
                  <div className="flex-1 cursor-pointer" onClick={() => loadCompany(entry.data)}>
                    <p className="font-semibold text-slate-100 hover:text-red-300">{entry.data.company_name}</p>
                    <p className="text-xs text-slate-400">
                      {new Date(entry.timestamp).toLocaleString()} • {entry.data.industry || 'N/A'}
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteEntry(entry.id);
                    }}
                    className="ml-2 p-1 text-slate-400 hover:text-red-400 transition-colors"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              ))}
              {history.length > 0 && (
                <button
                  onClick={clearAll}
                  className="w-full mt-3 px-3 py-2 text-sm bg-red-900/30 hover:bg-red-900/50 text-red-300 rounded-lg transition-colors font-semibold"
                >
                  Clear All History
                </button>
              )}
            </>
          )}
        </div>
      )}
    </div>
  );
}
