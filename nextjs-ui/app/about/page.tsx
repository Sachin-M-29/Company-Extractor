import Navigation from '@/components/navigation';

export default function About() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-[#050505] via-[#0b0b0b] to-[#050505] text-slate-100 aurora-grid">
      <Navigation />
      
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 mb-6">About Company Extractor</h1>
        
        <div className="panel-red-soft rounded-lg shadow-lg p-8 space-y-6 border border-red-900/60">
          <section>
            <h2 className="text-2xl font-bold text-slate-100 mb-3">Overview</h2>
            <p className="text-slate-300">
              Company Extractor is an intelligent data extraction system that combines web scraping with AI to automatically extract and organize detailed company information from websites.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-100 mb-3">How It Works</h2>
            <ol className="list-decimal list-inside space-y-2 text-slate-300">
              <li><strong>Web Scraping:</strong> Fetches website content using static HTML or JavaScript rendering</li>
              <li><strong>AI Extraction:</strong> Uses local LLM (Ollama) to intelligently extract structured data</li>
              <li><strong>Heuristic Merge:</strong> Combines LLM results with regex-based pattern matching for reliability</li>
              <li><strong>Enrichment:</strong> Optional crawling of multiple pages for people, products, and industry classification</li>
              <li><strong>Database Storage:</strong> Saves all extractions to SQLite for future reference</li>
            </ol>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-100 mb-3">Extracted Data</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { title: 'Company Info', items: ['Name', 'Website', 'Industry', 'Sector', 'Description'] },
                { title: 'Contact', items: ['Email', 'Phone', 'Address', 'Social media'] },
                { title: 'Details', items: ['Team members', 'Products', 'Services', 'Certifications'] },
                { title: 'Classification', items: ['Industry', 'Sub-industry', 'Sector', 'Confidence score'] },
              ].map((category, idx) => (
                <div key={idx} className="bg-[#0f0f12] border border-red-900/50 p-4 rounded-lg">
                  <h3 className="font-bold text-slate-100 mb-2">{category.title}</h3>
                  <ul className="text-sm text-slate-300 space-y-1">
                    {category.items.map((item, i) => (
                      <li key={i}>✓ {item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-100 mb-3">Key Features</h2>
            <ul className="space-y-2 text-slate-300">
              <li>✨ <strong>Single & Batch Extraction:</strong> Extract from one or thousands of companies</li>
              <li>⚡ <strong>Fast Mode:</strong> Optimized settings for rapid batch processing</li>
              <li>🔄 <strong>Parallel Processing:</strong> Process multiple companies simultaneously</li>
              <li>📥 <strong>Multiple Formats:</strong> Export results as JSON or CSV</li>
              <li>🤖 <strong>AI-Powered:</strong> Uses local Ollama LLM for offline extraction</li>
              <li>🛡️ <strong>Reliable:</strong> Combines multiple extraction methods for accuracy</li>
              <li>💾 <strong>Persistent Storage:</strong> All data saved to local database</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-bold text-slate-100 mb-3">Technology Stack</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { name: 'Frontend', tech: ['Next.js', 'React', 'TypeScript', 'Tailwind CSS'] },
                { name: 'Backend', tech: ['Python', 'Flask', 'Ollama', 'SQLite'] },
                { name: 'Scraping', tech: ['BeautifulSoup', 'Requests', 'Playwright', 'Async/Await'] },
              ].map((stack, idx) => (
                <div key={idx} className="bg-[#0f0f12] border border-red-900/50 p-4 rounded-lg">
                  <h3 className="font-bold text-slate-100 mb-2">{stack.name}</h3>
                  <ul className="text-sm text-slate-300 space-y-1">
                    {stack.tech.map((t, i) => (
                      <li key={i}>{t}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          <section className="bg-[#0f0f12] border border-red-900/60 p-6 rounded-lg">
            <h2 className="text-xl font-bold text-red-200 mb-2">Getting Started</h2>
            <ol className="list-decimal list-inside space-y-1 text-slate-300">
              <li>Enter a company website URL or name</li>
              <li>Click "Extract Info" to see the results</li>
              <li>For batch mode, paste multiple URLs separated by newlines</li>
              <li>Download your results in JSON or CSV format</li>
            </ol>
          </section>
        </div>
      </div>
    </main>
  );
}
