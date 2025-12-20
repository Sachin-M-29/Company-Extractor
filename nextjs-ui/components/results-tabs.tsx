'use client';

import { useState } from 'react';
import { Download, Mail, Phone, Briefcase, Award, Users } from 'lucide-react';

interface ResultsTabsProps {
  data: any;
}

export default function ResultsTabs({ data }: ResultsTabsProps) {
  const [activeTab, setActiveTab] = useState<'company' | 'contact' | 'products' | 'team' | 'certs' | 'raw'>('company');

  // Prefer richer descriptions when short/long variants exist
  const description = data.description || data.short_description || data.long_description;
  const longDescription = data.long_description && data.long_description !== description ? data.long_description : null;

  const saveCompany = () => {
    const history = JSON.parse(localStorage.getItem('company_history') || '[]');
    const entry = {
      id: `${data.company_name}-${Date.now()}`,
      timestamp: new Date().toISOString(),
      data,
    };
    // Keep last 50 searches
    history.unshift(entry);
    localStorage.setItem('company_history', JSON.stringify(history.slice(0, 50)));
    alert(`✓ Saved: ${data.company_name}`);
  };

  const downloadJSON = () => {
    const json = JSON.stringify(data, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${data.company_name || 'company'}_${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
  };

  const tabs = [
    { id: 'company', label: 'Company Info', icon: Briefcase },
    { id: 'contact', label: 'Contact & Social', icon: Mail },
    { id: 'products', label: 'Products & Services', icon: Award },
    { id: 'team', label: 'Team', icon: Users },
    { id: 'certs', label: 'Certifications', icon: Award },
    { id: 'raw', label: 'Raw Data', icon: null },
  ];

  return (
    <div className="panel-red-strong rounded-xl shadow-lg p-6 animate-scale-in transition-colors duration-300">
      {/* Header */}
      <div className="flex justify-between items-start mb-6 animate-slide-down">
        <div>
          <h2 className="text-3xl font-bold text-slate-100">{data.company_name || 'Company'}</h2>
          {data.website && (
            <a href={data.website} target="_blank" rel="noopener noreferrer" className="text-red-300 hover:underline hover:text-red-200 transition-colors">
              {data.website}
            </a>
          )}
        </div>
        <div className="flex gap-2">
          <button
            onClick={saveCompany}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-green-900/40 font-semibold"
          >
            ★ Save
          </button>
          <button
            onClick={downloadJSON}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 hover:from-red-700 hover:to-orange-500 text-white rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-red-900/40"
          >
            <Download size={18} />
            Export
          </button>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 animate-fade-in" style={{ animationDelay: '0.1s' }}>
        {[
          { label: 'Industry', value: data.industry || 'N/A' },
          { label: 'Confidence', value: data.confidence ? `${(data.confidence * 100).toFixed(0)}%` : 'N/A' },
          { label: 'Sector', value: data.sector || 'N/A' },
          { label: 'Sub-Industry', value: data.sub_industry || 'N/A' },
        ].map((metric, idx) => (
          <div
            key={idx}
            className="bg-[#0f0f12] border border-red-900/50 p-4 rounded-lg animate-scale-in hover:shadow-red-900/30 transition-all duration-300 hover:translate-y-[-2px]"
            style={{ animationDelay: `${0.05 * (idx + 1)}s` }}
          >
            <p className="text-xs font-semibold text-slate-400 mb-1">{metric.label}</p>
            <p className="text-lg font-bold text-slate-100">{metric.value}</p>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="border-b border-red-900/60 mb-6 animate-slide-down" style={{ animationDelay: '0.2s' }}>
        <div className="flex gap-2 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-4 py-3 font-semibold whitespace-nowrap transition-all duration-300 border-b-2 hover:scale-105 ${
                activeTab === tab.id
                  ? 'border-red-500 text-red-300'
                  : 'border-transparent text-slate-400 hover:text-slate-100'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="space-y-6 animate-fade-in">
        {activeTab === 'company' && (
          <div className="animate-fade-in">
            <h3 className="text-xl font-bold text-slate-100 mb-4">Company Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { label: 'Company Name', value: data.company_name },
                { label: 'Website', value: data.website },
                { label: 'Industry', value: data.industry },
                { label: 'Sector', value: data.sector },
                { label: 'Sub-Industry', value: data.sub_industry },
                { label: 'Address', value: data.address },
                { label: 'Description', value: description },
                { label: 'Long Description', value: longDescription },
                { label: 'Confidence', value: data.confidence ? `${(data.confidence * 100).toFixed(0)}%` : 'N/A' },
              ].map((field, idx) => (
                field.value && (
                  <div key={idx} className="bg-[#0f0f12] border border-red-900/50 p-4 rounded-lg">
                    <p className="text-xs font-semibold text-slate-400 mb-1">{field.label}</p>
                    <p className="text-slate-100">{field.value}</p>
                  </div>
                )
              ))}
            </div>
          </div>
        )}

        {activeTab === 'contact' && (
          <div>
            <h3 className="text-xl font-bold text-slate-100 mb-4">Contact & Social Media</h3>
            <div className="space-y-3">
              {[
                { icon: Mail, label: 'Email', value: data.email },
                { icon: Phone, label: 'Phone', value: data.phone },
                { label: 'LinkedIn', value: data.linkedin },
                { label: 'Facebook', value: data.facebook },
                { label: 'Twitter', value: data.twitter },
                { label: 'Instagram', value: data.instagram },
                { label: 'YouTube', value: data.youtube },
                { label: 'Blog', value: data.blog },
              ].map((contact, idx) => {
                const cleanValue = String(contact.value || '').replace(/^[<\s]+|[>\s]+$/g, '');
                return contact.value ? (
                  <div key={idx} className="flex items-start gap-3 p-3 bg-[#0f0f12] border border-red-900/50 rounded-lg">
                    <span className="font-semibold text-slate-300 min-w-24">{contact.label}</span>
                    {cleanValue.startsWith('http') ? (
                      <a href={cleanValue} target="_blank" rel="noopener noreferrer" className="text-red-300 hover:underline hover:text-red-200 transition-colors break-all">
                        {cleanValue}
                      </a>
                    ) : (
                      <span className="text-slate-100">{contact.value}</span>
                    )}
                  </div>
                ) : null;
              })}
            </div>
          </div>
        )}

        {activeTab === 'products' && (
          <div>
            <h3 className="text-xl font-bold text-slate-100 mb-4">Products & Services</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {data.products && Array.isArray(data.products) && (
                <div>
                  <h4 className="font-semibold text-slate-100 mb-3">Products</h4>
                  <ul className="space-y-2">
                    {data.products.map((product: string, idx: number) => (
                      <li key={idx} className="flex gap-2 text-slate-300">
                        <span className="text-red-400">•</span>
                        {product}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {data.services && Array.isArray(data.services) && (
                <div>
                  <h4 className="font-semibold text-slate-100 mb-3">Services</h4>
                  <ul className="space-y-2">
                    {data.services.map((service: string, idx: number) => (
                      <li key={idx} className="flex gap-2 text-slate-300">
                        <span className="text-orange-400">•</span>
                        {service}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'team' && (
          <div>
            <h3 className="text-xl font-bold text-slate-100 mb-4">Team Members</h3>
            {data.people && Array.isArray(data.people) && data.people.length > 0 ? (
              <div className="space-y-3">
                {data.people.map((person: any, idx: number) => (
                  <div key={idx} className="p-4 bg-[#0f0f12] border border-red-900/50 rounded-lg">
                    <p className="font-semibold text-slate-100">{person.name}</p>
                    {person.title && <p className="text-sm text-slate-400">{person.title}</p>}
                    {person.email && <p className="text-sm text-red-300">{person.email}</p>}
                    {person.profile_url && (
                      <a href={person.profile_url} target="_blank" rel="noopener noreferrer" className="text-sm text-red-300 hover:underline">
                        Profile
                      </a>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-400">No team members found</p>
            )}
          </div>
        )}

        {activeTab === 'certs' && (
          <div>
            <h3 className="text-xl font-bold text-slate-100 mb-4">Certifications</h3>
            {data.certifications && Array.isArray(data.certifications) && data.certifications.length > 0 ? (
              <div className="flex flex-wrap gap-3">
                {data.certifications.map((cert: string, idx: number) => (
                  <span key={idx} className="px-4 py-2 bg-[#1a0b0b] border border-red-900/50 text-red-200 rounded-full font-semibold text-sm">
                    {cert}
                  </span>
                ))}
              </div>
            ) : (
              <p className="text-slate-400">No certifications found</p>
            )}
          </div>
        )}

        {activeTab === 'raw' && (
          <div>
            <h3 className="text-xl font-bold text-slate-100 mb-4">Raw Data</h3>
            <pre className="bg-black text-red-100 p-4 rounded-lg overflow-auto max-h-96 text-xs border border-red-900/60">
              {JSON.stringify(data, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
