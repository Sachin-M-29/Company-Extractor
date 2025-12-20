'use client';

import { useState } from 'react';
import Navigation from '@/components/navigation';
import CompanySearch from '@/components/company-search';
import CompanyList from '@/components/company-list';
import ResultsTabs from '@/components/results-tabs';
import SearchHistory from '@/components/search-history';

export default function Home() {
  const [activeView, setActiveView] = useState<'search' | 'batch'>('search');
  const [extractedData, setExtractedData] = useState(null);
  const [batchResults, setBatchResults] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handleDownload = async (format: 'json' | 'csv') => {
    const payload = activeView === 'search'
      ? (extractedData ? [extractedData] : [])
      : batchResults;

    if (!payload || payload.length === 0) return;

    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ format, data: payload }),
    });

    if (!res.ok) return;

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `companies_${new Date().toISOString().slice(0, 10)}.${format}`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <main className="relative min-h-screen overflow-hidden bg-gradient-to-br from-[#050505] via-[#0b0b0b] to-[#050505] text-slate-100 transition-colors duration-500 aurora-grid">
      {/* Ambient background orbs */}
      <div className="pointer-events-none absolute inset-0 -z-10 opacity-70 blur-3xl">
        <div className="absolute -top-24 -left-16 h-72 w-72 rounded-full bg-gradient-to-br from-red-600/35 via-rose-500/30 to-orange-500/25 animate-blob" />
        <div className="absolute top-32 -right-24 h-80 w-80 rounded-full bg-gradient-to-br from-rose-600/30 via-red-500/25 to-amber-500/25 animate-blob" style={{ animationDelay: '2s' }} />
        <div className="absolute bottom-0 left-1/3 h-64 w-64 rounded-full bg-gradient-to-br from-orange-500/25 via-amber-400/25 to-red-500/25 animate-blob" style={{ animationDelay: '4s' }} />
      </div>

      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 py-8 relative">
        {/* Header with glow effect */}
        <div className="mb-12 animate-slide-down">
          <h1 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 mb-2 animate-text-glow">
            Company Information Extractor
          </h1>
          <p className="text-lg text-slate-300 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            Extract and organize company data using web scraping + AI
          </p>
        </div>

        {/* View Toggle with enhanced hover */}
        <div className="mb-8 flex flex-wrap gap-4 items-center animate-bounce-in" style={{ animationDelay: '0.15s' }}>
          <button
            onClick={() => setActiveView('search')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 hover:scale-110 active:scale-95 hover-lift ${
              activeView === 'search'
                ? 'bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 text-white shadow-xl shadow-red-600/30'
                : 'bg-[#0b0b0f]/80 text-slate-200 border border-red-900/60 hover:border-red-500/60'
            }`}
          >
            Single Extraction
          </button>
          <button
            onClick={() => setActiveView('batch')}
            className={`px-6 py-3 rounded-lg font-semibold transition-all duration-300 hover:scale-110 active:scale-95 hover-lift ${
              activeView === 'batch'
                ? 'bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 text-white shadow-xl shadow-red-600/30'
                : 'bg-[#0b0b0f]/80 text-slate-200 border border-red-900/60 hover:border-red-500/60'
            }`}
          >
            Batch Extraction
          </button>

          {(!!extractedData || batchResults.length > 0) && (
            <div className="ml-auto flex gap-2 animate-fade-in" style={{ animationDelay: '0.2s' }}>
              <button
                onClick={() => handleDownload('json')}
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 text-white font-semibold hover:scale-105 active:scale-95 transition-all duration-300 shadow-red-900/40 shadow-lg"
              >
                Download JSON
              </button>
              <button
                onClick={() => handleDownload('csv')}
                className="px-4 py-2 rounded-lg bg-gradient-to-r from-amber-500 to-orange-500 text-white font-semibold hover:scale-105 active:scale-95 transition-all duration-300 shadow-orange-900/40 shadow-lg"
              >
                Download CSV
              </button>
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 animate-fade-in" style={{ animationDelay: '0.3s' }}>
          {/* Search Section */}
          <div className="lg:col-span-1 animate-slide-left" style={{ animationDelay: '0.4s' }}>
            <CompanySearch 
              view={activeView}
              onProcessing={setIsProcessing}
              onExtractedData={setExtractedData}
              onBatchResults={setBatchResults}
            />
            <SearchHistory onSelect={setExtractedData} />
          </div>

          {/* Results Section */}
          <div className="lg:col-span-2 animate-slide-right" style={{ animationDelay: '0.4s' }}>
            {isProcessing && (
              <div className="panel-red-soft rounded-xl p-8 text-center animate-bounce-in">
                <div className="inline-block">
                  <div className="w-16 h-16 border-4 border-red-900/60 border-t-red-400 rounded-full animate-spin"></div>
                </div>
                <p className="mt-6 text-slate-100 font-bold text-lg animate-glow-pulse">Extracting company information...</p>
                <p className="mt-3 text-sm text-slate-400">
                  This may take 30-60 seconds<br />
                  <span className="text-xs">Ollama is analyzing the website content</span>
                </p>
              </div>
            )}

            {!isProcessing && activeView === 'search' && extractedData && (
              <div className="animate-scale-in" style={{ animationDelay: '0.2s' }}>
                <ResultsTabs data={extractedData} />
              </div>
            )}

            {!isProcessing && activeView === 'batch' && batchResults.length > 0 && (
              <div className="animate-scale-in" style={{ animationDelay: '0.2s' }}>
                <CompanyList results={batchResults} />
              </div>
            )}

            {!isProcessing && !extractedData && batchResults.length === 0 && (
              <div className="panel-red-soft rounded-xl shadow-lg p-12 text-center animate-float">
                <div className="text-5xl mb-4 animate-bounce-in" style={{ animationDelay: '0.1s' }}>🚀</div>
                <p className="text-slate-100 text-lg font-medium">Enter a company URL or name to get started</p>
                <p className="text-slate-400 mt-2">Powered by AI-driven web scraping</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}
