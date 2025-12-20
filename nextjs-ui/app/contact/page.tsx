'use client';

import { useState } from 'react';
import Navigation from '@/components/navigation';
import { Mail, Send, MessageCircle, MapPin, Phone } from 'lucide-react';

export default function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send to your backend
    console.log('Form submitted:', formData);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setFormData({ name: '', email: '', subject: '', message: '' });
    }, 3000);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-[#050505] via-[#0b0b0b] to-[#050505] text-slate-100 transition-colors duration-500 aurora-grid">
      <Navigation />
      
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="mb-12 animate-slide-down text-center">
          <h1 className="text-5xl font-black text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 mb-4 animate-text-glow">
            📬 Get In Touch
          </h1>
          <p className="text-lg text-slate-300 animate-fade-in" style={{ animationDelay: '0.2s' }}>
            Have questions about our company extraction service? We'd love to hear from you!
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Contact Info Cards */}
          <div className="lg:col-span-1 space-y-6 animate-slide-left">
            <div className="panel-red-strong rounded-lg p-6 hover-lift border border-red-900/60 animate-bounce-in">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-red-600/20 rounded-lg">
                  <Mail className="text-red-400" size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-slate-100 mb-1">Email Us</h3>
                  <a href="mailto:support@companyextractor.com" className="text-sm text-red-300 hover:underline hover:text-red-200 transition-colors">
                    support@companyextractor.com
                  </a>
                </div>
              </div>
            </div>

            <div className="panel-red-strong rounded-lg p-6 hover-lift border border-red-900/60 animate-bounce-in" style={{ animationDelay: '0.1s' }}>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-orange-600/20 rounded-lg">
                  <Phone className="text-orange-400" size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-slate-100 mb-1">Call Us</h3>
                  <a href="tel:+1234567890" className="text-sm text-red-300 hover:underline hover:text-red-200 transition-colors">
                    +1 (234) 567-890
                  </a>
                </div>
              </div>
            </div>

            <div className="panel-red-strong rounded-lg p-6 hover-lift border border-red-900/60 animate-bounce-in" style={{ animationDelay: '0.2s' }}>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-rose-600/20 rounded-lg">
                  <MapPin className="text-rose-400" size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-slate-100 mb-1">Visit Us</h3>
                  <p className="text-sm text-slate-300">
                    123 Tech Street<br />
                    San Francisco, CA 94102<br />
                    United States
                  </p>
                </div>
              </div>
            </div>

            <div className="panel-red-strong rounded-lg p-6 hover-lift border border-red-900/60 animate-bounce-in" style={{ animationDelay: '0.3s' }}>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-amber-600/20 rounded-lg">
                  <MessageCircle className="text-amber-400" size={24} />
                </div>
                <div>
                  <h3 className="font-bold text-slate-100 mb-1">Live Chat</h3>
                  <p className="text-sm text-slate-300">
                    Available Mon-Fri<br />
                    9:00 AM - 6:00 PM PST
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="lg:col-span-2 animate-slide-right">
            <div className="panel-red-soft rounded-xl p-8 border border-red-900/60">
              <h2 className="text-2xl font-bold text-slate-100 mb-6 flex items-center gap-2">
                <Send size={24} className="text-red-400" />
                Send us a message
              </h2>

              {submitted ? (
                <div className="bg-green-900/20 border border-green-500/50 text-green-300 p-6 rounded-lg text-center animate-bounce-in">
                  <p className="text-xl font-bold mb-2">✓ Message Sent!</p>
                  <p className="text-sm">Thank you for contacting us. We'll get back to you soon.</p>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-bold text-slate-200 mb-2">
                        Your Name *
                      </label>
                      <input
                        type="text"
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-3 border-2 border-red-900/60 bg-[#0c0c0f] text-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300 hover:border-red-600/60"
                        placeholder="John Doe"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-bold text-slate-200 mb-2">
                        Email Address *
                      </label>
                      <input
                        type="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                        className="w-full px-4 py-3 border-2 border-red-900/60 bg-[#0c0c0f] text-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300 hover:border-red-600/60"
                        placeholder="john@example.com"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-bold text-slate-200 mb-2">
                      Subject *
                    </label>
                    <input
                      type="text"
                      name="subject"
                      value={formData.subject}
                      onChange={handleChange}
                      required
                      className="w-full px-4 py-3 border-2 border-red-900/60 bg-[#0c0c0f] text-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300 hover:border-red-600/60"
                      placeholder="How can we help?"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-bold text-slate-200 mb-2">
                      Message *
                    </label>
                    <textarea
                      name="message"
                      value={formData.message}
                      onChange={handleChange}
                      required
                      rows={6}
                      className="w-full px-4 py-3 border-2 border-red-900/60 bg-[#0c0c0f] text-slate-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300 hover:border-red-600/60 resize-none"
                      placeholder="Tell us more about your inquiry..."
                    />
                  </div>

                  <button
                    type="submit"
                    className="w-full bg-gradient-to-r from-red-600 via-rose-600 to-orange-500 hover:from-red-700 hover:to-orange-600 text-white font-bold py-4 px-6 rounded-lg transition-all duration-300 hover:scale-105 active:scale-95 hover:shadow-xl shadow-red-900/40 flex items-center justify-center gap-2"
                  >
                    <Send size={20} />
                    Send Message
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-16 animate-fade-in" style={{ animationDelay: '0.5s' }}>
          <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 mb-8 text-center">
            Frequently Asked Questions
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="panel-red-strong rounded-lg p-6 border border-red-900/60 hover-lift">
              <h3 className="font-bold text-slate-100 mb-2">What data do you extract?</h3>
              <p className="text-sm text-slate-300">
                We extract comprehensive company information including name, industry, contact details, social media, team members, products, services, and certifications.
              </p>
            </div>

            <div className="panel-red-strong rounded-lg p-6 border border-red-900/60 hover-lift">
              <h3 className="font-bold text-slate-100 mb-2">How accurate is the extraction?</h3>
              <p className="text-sm text-slate-300">
                Our AI-powered system achieves 85-95% accuracy. Each extraction includes a confidence score to help you assess data quality.
              </p>
            </div>

            <div className="panel-red-strong rounded-lg p-6 border border-red-900/60 hover-lift">
              <h3 className="font-bold text-slate-100 mb-2">Can I export the data?</h3>
              <p className="text-sm text-slate-300">
                Yes! You can export data in JSON or CSV formats for easy integration with your existing tools and workflows.
              </p>
            </div>

            <div className="panel-red-strong rounded-lg p-6 border border-red-900/60 hover-lift">
              <h3 className="font-bold text-slate-100 mb-2">What about batch processing?</h3>
              <p className="text-sm text-slate-300">
                Our batch extraction feature allows you to process multiple companies simultaneously with parallel processing for maximum efficiency.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
