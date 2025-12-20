'use client';

import { useState } from 'react';
import axios from 'axios';

interface CompanySearchProps {
  view: 'search' | 'batch';
  onProcessing: (state: boolean) => void;
  onExtractedData: (data: any) => void;
  onBatchResults: (results: any[]) => void;
}

export default function CompanySearch({
  view,
  onProcessing,
  onExtractedData,
  onBatchResults,
}: CompanySearchProps) {
  const [input, setInput] = useState('');
  const [inputType, setInputType] = useState<'url' | 'company'>('url');
  const [scrapeMethod, setScrapeMethod] = useState('Static HTML Only');
  const [timeout, setTimeout] = useState(10);
  const [enableEnrich, setEnableEnrich] = useState(false);
  const [fastMode, setFastMode] = useState(true);
  const [workers, setWorkers] = useState(3);
  const [error, setError] = useState('');

  const handleExtract = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!input.trim()) {
      setError('Please enter a URL or company name');
      return;
    }

    onProcessing(true);

    try {
      if (view === 'search') {
        // Single extraction
        const response = await axios.post('/api/extract', {
          input: input.trim(),
          input_type: inputType,
          scrape_method: scrapeMethod,
          timeout,
          enable_enrich: enableEnrich,
        });
        onExtractedData(response.data);
      } else {
        // Batch extraction
        const urls = input
          .split(/[\n,\s]+/)
          .map(u => u.trim())
          .filter(u => u.length > 0);

        const response = await axios.post('/api/batch-extract', {
          urls,
          scrape_method: scrapeMethod,
          timeout,
          fast_mode: fastMode,
          max_workers: workers,
        });
        onBatchResults(response.data.results);
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Extraction failed. Please try again.');
    } finally {
      onProcessing(false);
    }
  };

  return (
    <div className="panel-red-soft rounded-lg shadow-lg p-6 h-fit sticky top-24 animate-bounce-in hover-lift border border-red-900/60 text-slate-100 transition-colors duration-300">
      <h2 className="text-2xl font-bold bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 bg-clip-text text-transparent mb-6 animate-slide-down">
        {view === 'search' ? 'Single Extraction' : 'Batch Extraction'}
      </h2>

      <form onSubmit={handleExtract} className="space-y-6">
        {/* Input Type */}
        <div className="animate-fade-in transition-smooth" style={{ animationDelay: '0.1s' }}>
          <label className="block text-sm font-bold text-slate-200 mb-3 flex items-center">
            <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
            Input Type
          </label>
          <div className="flex gap-4 p-3 bg-[#0f0f0f]/80 rounded-lg border border-red-900/60">
            <label className="flex items-center gap-2 cursor-pointer hover:text-red-300 transition-colors">
              <input
                type="radio"
                name="inputType"
                value="url"
                checked={inputType === 'url'}
                onChange={(e) => setInputType(e.target.value as 'url')}
                className="w-4 h-4 accent-red-500"
              />
              <span className="text-sm font-medium">URL</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer hover:text-red-300 transition-colors">
              <input
                type="radio"
                name="inputType"
                value="company"
                checked={inputType === 'company'}
                onChange={(e) => setInputType(e.target.value as 'company')}
                className="w-4 h-4 accent-red-500"
              />
              <span className="text-sm font-medium">Company Name</span>
            </label>
          </div>
        </div>

        {/* Input Field */}
        <div className="animate-fade-in transition-smooth" style={{ animationDelay: '0.15s' }}>
          <label className="block text-sm font-bold text-slate-200 mb-3 flex items-center">
            <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
            {view === 'search'
              ? inputType === 'url'
                ? 'Website URL'
                : 'Company Name'
              : 'URLs or Company Names'}
          </label>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={
              view === 'search'
                ? inputType === 'url'
                  ? 'https://example.com or example.com'
                  : 'e.g., TechCorp Inc.'
                : 'example.com\ngoogle.com\nmicrosoft.com'
            }
            rows={view === 'search' ? 3 : 6}
            className="w-full px-4 py-3 border-2 border-red-900/60 bg-[#0c0c0f] text-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300 hover:shadow-red-900/40 hover:border-red-600/60 resize-none"
          />
        </div>

        {/* Scraping Settings */}
        <div className="animate-fade-in transition-smooth" style={{ animationDelay: '0.2s' }}>
          <label className="block text-sm font-bold text-slate-200 mb-3 flex items-center">
            <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
            Scraping Method
          </label>
          <select
            value={scrapeMethod}
            onChange={(e) => setScrapeMethod(e.target.value)}
            className="w-full px-4 py-3 border-2 border-red-900/60 bg-[#0c0c0f] text-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300 hover:shadow-red-900/40 hover:border-red-600/60"
          >
            <option>Static HTML Only</option>
            <option>Auto (Smart)</option>
            <option>Playwright Only</option>
          </select>
        </div>

        {/* Timeout */}
        <div className="animate-fade-in transition-smooth" style={{ animationDelay: '0.25s' }}>
          <label className="block text-sm font-bold text-slate-200 mb-3 flex items-center">
            <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
            Timeout: <span className="ml-2 font-black text-red-400">{timeout}s</span>
          </label>
          <input
            type="range"
            min="5"
            max="60"
            value={timeout}
            onChange={(e) => setTimeout(parseInt(e.target.value))}
            className="w-full h-2 bg-[#1a1a1a] rounded-lg appearance-none cursor-pointer accent-red-500"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-2">
            <span>5s</span>
            <span>60s</span>
          </div>
        </div>

        {/* Enrichment */}
        <div className="bg-gradient-to-r from-[#140606] via-[#1d0a0a] to-[#140606] border-2 border-red-900/60 rounded-lg p-4 animate-pulse-glow transition-all duration-300 hover:shadow-red-900/30">
          <label className="flex items-start gap-3 cursor-pointer">
            <input
              type="checkbox"
              checked={enableEnrich}
              onChange={(e) => setEnableEnrich(e.target.checked)}
              className="w-4 h-4 mt-1 cursor-pointer accent-red-500"
            />
            <div>
              <span className="font-bold text-slate-100 block">Enable Enrichment</span>
              <p className="text-sm text-slate-300 mt-1">
                {enableEnrich 
                  ? '⏱️ SLOW: Takes 60-180 seconds (multi-page crawl + analysis)'
                  : 'Adds company details like address, people, industry (slow)'}
              </p>
            </div>
          </label>
        </div>

        {/* Batch-specific settings */}
        {view === 'batch' && (
          <>
            <div className="animate-fade-in transition-smooth" style={{ animationDelay: '0.3s' }}>
              <label className="flex items-center gap-2 cursor-pointer hover:text-red-300 transition-colors p-3 rounded-lg hover:bg-[#111]">
                <input
                  type="checkbox"
                  checked={fastMode}
                  onChange={(e) => setFastMode(e.target.checked)}
                  className="w-4 h-4 cursor-pointer accent-red-500"
                />
                <span className="text-sm font-bold text-slate-200">⚡ Fast mode (2x faster)</span>
              </label>
            </div>
            <div className="animate-fade-in transition-smooth" style={{ animationDelay: '0.35s' }}>
              <label className="block text-sm font-bold text-slate-200 mb-3 flex items-center">
                <span className="inline-block w-2 h-2 bg-red-500 rounded-full mr-2"></span>
                Parallel workers: <span className="ml-2 font-black text-red-400">{workers}</span>
              </label>
              <input
                type="range"
                min="1"
                max="10"
                value={workers}
                className="w-full h-2 bg-[#1a1a1a] rounded-lg appearance-none cursor-pointer accent-red-500"
              />
              <div className="flex justify-between text-xs text-slate-400 mt-2">
                <span>1 (slow)</span>
                <span>10 (fastest)</span>
              </div>
            </div>
          </>
        )}

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-2 border-red-300 text-red-700 px-4 py-3 rounded-lg text-sm animate-slide-down font-medium">
            ❌ {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 hover:from-red-700 hover:via-rose-600 hover:to-orange-500 text-white font-bold py-3 rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-xl shadow-red-800/40 animate-fade-in"
          style={{ animationDelay: '0.4s' }}
        >
          {view === 'search' ? '🔍 Extract Info' : '⚡ Extract Batch'}
        </button>
      </form>
    </div>
  );
}
