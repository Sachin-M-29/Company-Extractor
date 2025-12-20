'use client';

import { useState } from 'react';
import { Download } from 'lucide-react';

interface CompanyListProps {
  results: any[];
}

export default function CompanyList({ results }: CompanyListProps) {
  const [sortBy, setSortBy] = useState<'name' | 'confidence'>('name');

  const sortedResults = [...results].sort((a, b) => {
    if (sortBy === 'confidence') {
      return (b.confidence || 0) - (a.confidence || 0);
    }
    return (a.company_name || '').localeCompare(b.company_name || '');
  });

  const downloadJSON = () => {
    const data = JSON.stringify(results, null, 2);
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `companies_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
  };

  const downloadCSV = () => {
    const headers = ['Company Name', 'Website', 'Industry', 'Confidence'];
    const rows = results.map(r => [
      r.company_name || '',
      r.website || '',
      r.industry || '',
      r.confidence || '',
    ]);

    const csv = [
      headers.join(','),
      ...rows.map(r => r.map(cell => `"${cell}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `companies_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
  };

  return (
    <div className="panel-red-soft rounded-xl shadow-lg p-6 animate-scale-in transition-colors duration-300">
      <div className="flex justify-between items-center mb-6 animate-slide-down">
        <h2 className="text-2xl font-bold text-slate-100">
          Batch Results ({results.length})
        </h2>
        <div className="flex gap-2">
          <button
            onClick={downloadJSON}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 hover:from-red-700 hover:to-orange-500 text-white rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-red-900/40"
          >
            <Download size={18} />
            JSON
          </button>
          <button
            onClick={downloadCSV}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-orange-900/30"
          >
            <Download size={18} />
            CSV
          </button>
        </div>
      </div>

      {/* Sort Options */}
      <div className="mb-4 animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as 'name' | 'confidence')}
          className="px-4 py-2 border border-red-900/60 rounded-lg transition-all duration-300 hover:shadow-red-900/30 focus:ring-2 focus:ring-red-500 bg-[#0c0c0f] text-slate-100"
        >
          <option value="name">Sort by Name</option>
          <option value="confidence">Sort by Confidence</option>
        </select>
      </div>

      {/* Results Table */}
      <div className="overflow-x-auto animate-fade-in" style={{ animationDelay: '0.15s' }}>
        <table className="w-full">
          <thead className="bg-[#0e0e10]/90 border-b border-red-900/60 animate-slide-down backdrop-blur-sm">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-slate-100">Company</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-slate-100">Website</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-slate-100">Industry</th>
              <th className="px-6 py-3 text-left text-sm font-semibold text-slate-100">Confidence</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-red-900/40">
            {sortedResults.map((result, idx) => (
              <tr key={idx} className="border-b border-transparent hover:bg-[#111]/70 transition-all duration-300 animate-slide-up" style={{ animationDelay: `${0.05 * (idx % 10)}s` }}>
                <td className="px-6 py-4 text-sm text-slate-100">{result.company_name || 'N/A'}</td>
                <td className="px-6 py-4 text-sm text-red-300 truncate">
                  <a href={result.website} target="_blank" rel="noopener noreferrer" className="hover:underline hover:text-red-200 transition-colors">
                    {result.website || 'N/A'}
                  </a>
                </td>
                <td className="px-6 py-4 text-sm text-slate-300">{result.industry || 'N/A'}</td>
                <td className="px-6 py-4 text-sm">
                  <span className={`px-2 py-1 rounded text-xs font-semibold transition-all duration-300 ${
                    (result.confidence || 0) >= 0.8 ? 'bg-green-100 text-green-800 dark:bg-green-900/60 dark:text-green-100' :
                    (result.confidence || 0) >= 0.6 ? 'bg-yellow-100 text-yellow-800 dark:bg-amber-900/60 dark:text-amber-100' :
                    'bg-red-100 text-red-800 dark:bg-red-900/60 dark:text-red-100'
                  }`}>
                    {((result.confidence || 0) * 100).toFixed(0)}%
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
