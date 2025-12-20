export default function Navigation() {
  return (
    <nav className="bg-[#080808]/95 border-b border-red-900/60 sticky top-0 z-50 shadow-lg shadow-red-900/30 animate-slide-down backdrop-blur-md transition-colors duration-300">
      <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3 group cursor-pointer hover:scale-110 transition-transform duration-300">
          <span className="text-3xl group-hover:rotate-12 group-hover:animate-bounce transition-transform duration-300">🔍</span>
          <h1 className="text-2xl font-black bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 bg-clip-text text-transparent">
            CompanyExtractor
          </h1>
        </div>
        
        <div className="flex gap-8 items-center">
          <a href="/" className="text-slate-200 hover:text-red-300 font-semibold transition-all duration-300 relative group hover:scale-110">
            <span className="relative">
              Home
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 group-hover:w-full transition-all duration-300"></span>
            </span>
          </a>
          <a href="/contact" className="text-slate-200 hover:text-red-300 font-semibold transition-all duration-300 relative group hover:scale-110">
            <span className="relative">
              Contact Us
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 group-hover:w-full transition-all duration-300"></span>
            </span>
          </a>
          <a href="/about" className="text-slate-200 hover:text-red-300 font-semibold transition-all duration-300 relative group hover:scale-110">
            <span className="relative">
              About
              <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-red-500 via-rose-500 to-orange-400 group-hover:w-full transition-all duration-300"></span>
            </span>
          </a>
        </div>
      </div>
    </nav>
  );
}
