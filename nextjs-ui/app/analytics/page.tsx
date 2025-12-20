'use client';

import { useState, useEffect } from 'react';
import Navigation from '@/components/navigation';
import { Download, FileJson, FileText } from 'lucide-react';

interface Company {
  company_name: string;
  website: string;
  industry?: string;
  confidence?: number;
  email?: string;
  phone?: string;
  address?: string;
  short_description?: string;
  [key: string]: any;
}

interface Stats {
  total: number;
  avg_confidence: number;
  industries_found: number;
}

export default function Analytics() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [stats, setStats] = useState<Stats>({ total: 0, avg_confidence: 0, industries_found: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/companies');
      const data = await response.json();

      const companiesData: Company[] = data.companies || data.results || [];

      if (data.error) {
        setError(data.error || 'Failed to load companies');
      }

      setCompanies(companiesData);

      const computedStats: Stats = data.stats || {
        total: companiesData.length,
        avg_confidence: companiesData.length
          ? companiesData.reduce((sum, c) => sum + (typeof c.confidence === 'number' ? c.confidence : 0), 0) / companiesData.length
          : 0,
        industries_found: new Set(companiesData.map(c => c.industry).filter(Boolean)).size,
      };

      setStats(computedStats);
    } catch (err: any) {
      setError(err.message || 'Error fetching companies');
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (companies.length === 0) {
      alert('No companies to download');
      return;
    }

    // Get all unique keys
    const allKeys = new Set<string>();
    companies.forEach(c => {
      Object.keys(c).forEach(key => allKeys.add(key));
    });
    const keys = Array.from(allKeys);

    // Create CSV header
    const header = keys.join(',');
    
    // Create CSV rows
    const rows = companies.map(company =>
      keys.map(key => {
        const value = company[key];
        // Escape quotes and wrap in quotes if contains comma or newline
        if (value === null || value === undefined) return '';
        const str = String(value);
        if (str.includes(',') || str.includes('\n') || str.includes('"')) {
          return `"${str.replace(/"/g, '""')}"`;
        }
        return str;
      }).join(',')
    );

    const csv = [header, ...rows].join('\n');
    downloadFile(csv, 'companies.csv', 'text/csv');
  };

  const downloadJSON = () => {
    if (companies.length === 0) {
      alert('No companies to download');
      return;
    }

    const json = JSON.stringify(companies, null, 2);
    downloadFile(json, 'companies.json', 'application/json');
  };

  const downloadFile = (content: string, filename: string, mimeType: string) => {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#050505] via-[#0b0b0b] to-[#050505] text-slate-100 transition-colors duration-500 aurora-grid">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-8 animate-slide-down">
          <h1 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 mb-2 animate-text-glow">
            📊 Analytics & Exports
          </h1>
          <p className="text-lg text-slate-300 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            View extracted company data and export as CSV or JSON
          </p>
        </div>

        {/* Download Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 animate-bounce-in" style={{ animationDelay: '0.2s' }}>
          <button
            onClick={downloadCSV}
            disabled={companies.length === 0}
            className="flex items-center justify-center gap-3 bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 hover:from-red-700 hover:to-orange-500 disabled:from-slate-700 disabled:to-slate-700 text-white font-bold py-4 px-6 rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-red-900/40 disabled:cursor-not-allowed disabled:shadow-none"
          >
            <FileText size={20} />
            Download as CSV ({companies.length} companies)
          </button>
          <button
            onClick={downloadJSON}
            disabled={companies.length === 0}
            className="flex items-center justify-center gap-3 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 disabled:from-slate-700 disabled:to-slate-700 text-white font-bold py-4 px-6 rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-orange-900/40 disabled:cursor-not-allowed disabled:shadow-none"
          >
            <FileJson size={20} />
            Download as JSON ({companies.length} companies)
          </button>
        </div>

        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="panel-red-strong rounded-lg p-6 border-l-4 border-red-600 animate-bounce-in hover-lift" style={{ animationDelay: '0.25s' }}>
            <p className="text-slate-300 text-sm font-bold mb-2 flex items-center">
              <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
              Total Companies
            </p>
            <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400">{stats.total}</p>
            <p className="text-xs text-slate-500 mt-3">Companies extracted</p>
          </div>
          <div className="panel-red-strong rounded-lg p-6 border-l-4 border-orange-500 animate-bounce-in hover-lift" style={{ animationDelay: '0.3s' }}>
            <p className="text-slate-300 text-sm font-bold mb-2 flex items-center">
              <span className="inline-block w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
              Average Confidence
            </p>
            <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-orange-400 via-amber-400 to-red-400">{(stats.avg_confidence * 100).toFixed(0)}%</p>
            <p className="text-xs text-slate-500 mt-3">Data quality score</p>
          </div>
          <div className="panel-red-strong rounded-lg p-6 border-l-4 border-red-400 animate-bounce-in hover-lift" style={{ animationDelay: '0.35s' }}>
            <p className="text-slate-300 text-sm font-bold mb-2 flex items-center">
              <span className="inline-block w-2 h-2 bg-red-400 rounded-full mr-2"></span>
              Industries Found
            </p>
            <p className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-400 via-rose-400 to-orange-300">{stats.industries_found}</p>
            <p className="text-xs text-slate-500 mt-3">Unique industries</p>
          </div>
        </div>

        {/* Main Content */}
          <div className="panel-red-soft rounded-xl shadow-lg overflow-hidden animate-fade-in border border-red-900/60 transition-colors duration-300" style={{ animationDelay: '0.35s' }}>
          {loading ? (
            <div className="p-12 text-center animate-fade-in">
              <div className="inline-block mb-6">
                <div className="w-12 h-12 border-4 border-red-900/60 border-t-red-400 rounded-full animate-spin"></div>
              </div>
              <p className="text-slate-200 font-semibold text-lg animate-glow-pulse">Loading companies from database...</p>
            </div>
          ) : error ? (
            <div className="p-12 text-center animate-slide-down">
              <p className="text-red-300 mb-6 font-semibold text-lg">❌ {error}</p>
              <button
                onClick={fetchCompanies}
                className="px-6 py-3 bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 text-white rounded-lg hover:from-red-700 hover:to-orange-500 transition-all duration-300 hover:scale-105 active:scale-95 font-semibold"
              >
                Retry
              </button>
            </div>
          ) : companies.length === 0 ? (
            <div className="p-12 text-center animate-float">
              <p className="text-slate-200 text-xl mb-2 font-bold">📭 No companies extracted yet</p>
              <p className="text-slate-400">Extract companies using the Single or Batch Extraction tools</p>
            </div>
          ) : (
            <>
              {/* Table */}
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-[#0e0e10]/90 border-b border-red-900/60 animate-slide-down backdrop-blur-sm">
                    <tr>
                      <th className="px-6 py-4 text-left text-sm font-bold text-slate-100">Company Name</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-slate-100">Website</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-slate-100">Industry</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-slate-100">Confidence</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-slate-100">Email</th>
                      <th className="px-6 py-4 text-left text-sm font-bold text-slate-100">Phone</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-red-900/40">
                    {companies.slice(0, 50).map((company, idx) => (
                      <tr key={idx} className="hover:bg-[#111]/70 transition-all duration-300 animate-slide-up" style={{ animationDelay: `${0.03 * (idx % 15)}s` }}>
                        <td className="px-6 py-4 text-sm font-semibold text-slate-100">{company.company_name}</td>
                        <td className="px-6 py-4 text-sm text-red-300 truncate">
                          {company.website ? (
                            <a href={company.website} target="_blank" rel="noopener noreferrer" className="hover:underline hover:text-red-200 transition-colors hover:font-semibold">
                              {company.website.replace(/^https?:\/\//, '')}
                            </a>
                          ) : '—'}
                        </td>
                        <td className="px-6 py-4 text-sm text-slate-300">{company.industry || '—'}</td>
                        <td className="px-6 py-4 text-sm">
                          {company.confidence ? (
                            <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold transition-all duration-300 ${
                              company.confidence >= 0.8 
                                ? 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 dark:from-green-900/60 dark:to-emerald-900/60 dark:text-green-100' 
                                : company.confidence >= 0.6 
                                ? 'bg-gradient-to-r from-yellow-100 to-amber-100 text-yellow-800 dark:from-amber-900/60 dark:to-yellow-900/60 dark:text-amber-100'
                                : 'bg-gradient-to-r from-red-100 to-orange-100 text-red-800 dark:from-red-900/60 dark:to-orange-900/60 dark:text-red-100'
                            }`}>
                              {(company.confidence * 100).toFixed(0)}%
                            </span>
                          ) : '—'}
                        </td>
                        <td className="px-6 py-4 text-sm text-slate-300">{company.email || '—'}</td>
                        <td className="px-6 py-4 text-sm text-slate-300">{company.phone || '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {companies.length > 50 && (
                <div className="px-6 py-4 bg-[#0f0f12] border-t border-red-900/60 text-center text-sm text-slate-300 font-semibold animate-fade-in">
                  ℹ️ Showing 50 of {companies.length} companies. Download as CSV or JSON to see all.
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </main>
  );
}
