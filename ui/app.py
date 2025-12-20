"""
Streamlit UI for Web Scraper + LLM Information Extractor
"""

import streamlit as st
import json
import time
import io
import re
import csv
from datetime import datetime
import sys
import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper import WebScraper, chunk_text
from utils.resolve import resolve_company_website
from utils.heuristics import extract_all as heuristic_extract
from utils.enrich import enrich_company_details
from llm.extractor import LLMExtractor
from llm.cli_extractor import CLIExtractor
from database.db import CompanyDatabase


# Page configuration
st.set_page_config(
    page_title="Company Info Extractor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styling
st.markdown("""
<style>
    .main-header {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 5px solid #17a2b8;
        padding: 15px;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None
if "processing" not in st.session_state:
    st.session_state.processing = False
if "batch_results" not in st.session_state:
    st.session_state.batch_results = []
if "batch_failures" not in st.session_state:
    st.session_state.batch_failures = []

# Header
st.markdown("# 🔍 Company Information Extractor")
st.markdown("Extract and organize company data using web scraping + AI")

# Sidebar configuration
st.sidebar.header("⚙️ Configuration")

with st.sidebar:
    st.subheader("LLM Settings")
    
    llm_backend = st.radio(
        "LLM Backend",
        ["Ollama (Recommended)", "Hugging Face"]
    )
    
    if llm_backend == "Ollama (Recommended)":
        st.caption("Using local Ollama via CLI (offline). No HTTP connectivity required.")
        model_name = st.selectbox(
            "Model",
            [
                "mistral:7b-instruct-q4_0",
                "phi3:3.8b-mini-4k-instruct-q4_0",
                "neural-chat:7b-v3-q4",
                "orca2:7b-q4"
            ]
        )
        ollama_host = None
    else:
        model_name = st.selectbox(
            "HF Model",
            [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "microsoft/phi-3"
            ]
        )
        ollama_host = None
    
    st.subheader("Scraping Settings")
    scrape_method = st.radio(
        "Scraping Method",
        ["Static HTML Only", "Auto (Smart)", "Playwright Only"],
        index=0
    )
    
    timeout = st.slider("Timeout (seconds)", 5, 60, 10)
    
    st.subheader("Enrichment")
    enable_enrich = st.checkbox(
        "Enable enrichment (people/products/services)",
        value=False,
        help="Crawls a few extra pages like About/Team/Contact to improve completeness. Turn off for fastest runs."
    )
    
    st.subheader("Batch Speed")
    batch_fast_mode = st.checkbox(
        "⚡ Fast mode (batch only)",
        value=True,
        help="For batch extraction: limits to 2 pages & 5s timeout. Single extraction unaffected."
    )
    batch_max_workers = st.slider(
        "Parallel workers (batch only)",
        min_value=1,
        max_value=10,
        value=3,
        help="Higher = faster but more system load. 3-5 recommended."
    )
    
    st.subheader("Database")
    show_saved = st.checkbox("Show Saved Companies", value=False)

# Main content area
col1 = st.container()

with col1:
    st.subheader("📥 Input")
    
    input_type = st.radio(
        "Input Type",
        ["URL", "Company Name"],
        horizontal=True
    )
    
    if input_type == "URL":
        url_input = st.text_input(
            "Enter Website URL",
            placeholder="https://example.com or example.com",
            help="Full URL or domain (auto-adds https://)"
        )
        company_url = url_input
        # Auto-add https:// if missing
        if company_url and not company_url.lower().startswith(("http://", "https://")):
            company_url = f"https://{company_url}"
    else:
        company_name = st.text_input(
            "Enter Company Name",
            placeholder="e.g., TechCorp Inc.",
            help="Will search for official website"
        )
        company_url = company_name

# Processing section
st.markdown("---")

if st.button("🚀 Extract Information", use_container_width=True, type="primary"):
    if not company_url:
        st.error("❌ Please enter a URL or company name")
    else:
        st.session_state.processing = True
        
        with st.spinner("🔄 Processing... This may take a minute"):
            try:
                start_time = time.time()
                # Detect multiple URLs pasted into the single URL box
                multi_urls = []
                if input_type == "URL":
                    tokens = [t.strip() for t in re.split(r"[\s,;]+", company_url or "") if t.strip()]
                    for t in tokens:
                        if t.lower().startswith("http://") or t.lower().startswith("https://") or "." in t:
                            u = t if t.lower().startswith(("http://", "https://")) else f"https://{t}"
                            multi_urls.append(u)
                    # Keep unique order
                    seen = set()
                    uniq_urls = []
                    for u in multi_urls:
                        if u not in seen:
                            seen.add(u)
                            uniq_urls.append(u)
                    multi_urls = uniq_urls

                if input_type == "URL" and len(multi_urls) > 1:
                    # Run inline batch extraction with parallel processing
                    st.info(f"Detected {len(multi_urls)} URLs. Running batch extraction ({batch_max_workers} workers)…")
                    st.session_state.batch_results = []
                    st.session_state.batch_failures = []
                    progress = st.progress(0)
                    status = st.empty()

                    # Batch-optimized timeout (faster fail)
                    batch_timeout = min(timeout, 5) if batch_fast_mode else timeout

                    def process_url(url: str):
                        """Process single URL for batch extraction"""
                        try:
                            scraper = WebScraper(timeout=batch_timeout)
                            if llm_backend == "Ollama (Recommended)":
                                extractor = CLIExtractor(model=model_name)
                            else:
                                from llm.extractor import HFExtractor
                                extractor = HFExtractor(model_name=model_name)

                            if scrape_method == "Auto (Smart)":
                                scraped_text = scraper.auto_scrape(url)
                            elif scrape_method == "Static HTML Only":
                                scraped_text = scraper.scrape_static_html(url)
                            else:
                                import asyncio
                                scraped_text = asyncio.run(scraper.scrape_js_heavy_page(url))

                            if not scraped_text:
                                raise RuntimeError("Scrape failed")

                            chunks = chunk_text(scraped_text, chunk_size=500, overlap=50)
                            text_to_extract = chunks[0] if chunks else scraped_text

                            data = extractor.extract_from_text(text_to_extract, url)
                            if not data:
                                raise RuntimeError("LLM extraction failed")
                            if not data.get("website"):
                                data["website"] = url

                            # Heuristic merge for contacts/social/certs
                            try:
                                hints = heuristic_extract(url, timeout=batch_timeout) or {}
                            except Exception:
                                hints = {}
                            for k in ["email", "phone", "linkedin", "facebook", "twitter", "instagram", "youtube", "blog"]:
                                if not data.get(k) and hints.get(k):
                                    data[k] = hints[k]
                            if hints.get("certifications"):
                                cur = data.get("certifications") or []
                                if not isinstance(cur, list):
                                    cur = [cur]
                                data["certifications"] = list(dict.fromkeys([*cur, *hints["certifications"]]))

                            return ("success", data)
                        except Exception as e:
                            return ("error", {"url": url, "error": str(e)})

                    # Parallel processing with ThreadPoolExecutor
                    total = len(multi_urls)
                    processed_count = [0]  # Use list to track in nested scope
                    
                    def update_progress():
                        processed_count[0] += 1
                        progress.progress(min(1.0, processed_count[0] / total))

                    with ThreadPoolExecutor(max_workers=batch_max_workers) as executor:
                        futures = {executor.submit(process_url, url): url for url in multi_urls}
                        
                        for future in as_completed(futures):
                            url = futures[future]
                            status.info(f"Processing: {url} ({processed_count[0]}/{total})")
                            
                            try:
                                result_type, result_data = future.result()
                                if result_type == "success":
                                    st.session_state.batch_results.append(result_data)
                                else:
                                    st.session_state.batch_failures.append(result_data)
                            except Exception as e:
                                st.session_state.batch_failures.append({"url": url, "error": str(e)})
                            finally:
                                update_progress()

                    status.success(
                        f"✅ Completed. OK: {len(st.session_state.batch_results)} | Failures: {len(st.session_state.batch_failures)}"
                    )
                    st.session_state.processing = False
                    
                    # Display batch results immediately
                    if st.session_state.batch_results:
                        st.markdown("---")
                        st.subheader("📊 Batch Results")
                        
                        def _row(d: dict) -> dict:
                            return {
                                "company_name": d.get("company_name"),
                                "website": d.get("website"),
                                "industry": d.get("industry"),
                                "confidence": d.get("confidence"),
                            }
                        
                        rows = [_row(d) for d in st.session_state.batch_results]
                        st.dataframe(rows, use_container_width=True, hide_index=True)
                        
                        # Downloads
                        ndjson_str = "\n".join(json.dumps(obj, ensure_ascii=False) for obj in st.session_state.batch_results)
                        
                        csv_buf = io.StringIO()
                        writer = csv.DictWriter(csv_buf, fieldnames=["company_name", "website", "industry", "confidence"])
                        writer.writeheader()
                        for r in rows:
                            writer.writerow(r)
                        csv_bytes = csv_buf.getvalue().encode("utf-8")
                        
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button(
                                label="📥 Download NDJSON",
                                data=ndjson_str.encode("utf-8"),
                                file_name=f"companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ndjson",
                                mime="application/x-ndjson",
                                use_container_width=True,
                            )
                        with col_dl2:
                            st.download_button(
                                label="📥 Download CSV",
                                data=csv_bytes,
                                file_name=f"companies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True,
                            )
                        
                        if st.session_state.batch_failures:
                            with st.expander("⚠️ Failures"):
                                for f in st.session_state.batch_failures:
                                    st.write(f"- {f['url']}: {f['error']}")
                    
                    st.stop()
                
                # If input was a company name, resolve website first
                resolved_note = None
                if input_type == "Company Name":
                    resolved = resolve_company_website(company_url, timeout=timeout)
                    if not resolved:
                        st.error("❌ Couldn't find an official website for that company name.")
                        st.session_state.processing = False
                        st.stop()
                    resolved_note = f"Resolved website: {resolved}"
                    company_url = resolved

                # Step 1: Scraping
                st.info("📡 Step 1/3: Scraping website content...")
                scraper = WebScraper(timeout=timeout)
                
                try:
                    if scrape_method == "Static HTML Only":
                        scraped_text = scraper.scrape_static_html(company_url)
                    elif scrape_method == "Auto (Smart)":
                        try:
                            scraped_text = scraper.auto_scrape(company_url)
                        except Exception:
                            st.warning("⚠️ Auto-scrape failed, falling back to static HTML...")
                            scraped_text = scraper.scrape_static_html(company_url)
                    else:  # Playwright
                        try:
                            import asyncio
                            scraped_text = asyncio.run(scraper.scrape_js_heavy_page(company_url))
                        except Exception as e:
                            st.warning(f"⚠️ Playwright failed ({str(e)[:50]}), falling back to static HTML...")
                            scraped_text = scraper.scrape_static_html(company_url)
                except Exception as e:
                    st.error(f"❌ All scraping methods failed: {str(e)}")
                    st.session_state.processing = False
                    st.stop()
                
                if not scraped_text:
                    st.error("❌ Failed to scrape website. Check URL and try again.")
                    st.session_state.processing = False
                    st.stop()
                
                scraped_length = len(scraped_text)

                # Quick heuristics from homepage for contacts/social/certs
                hints = {}
                try:
                    hints = heuristic_extract(company_url, timeout=timeout) or {}
                except Exception:
                    hints = {}
                
                # Step 2: Chunking
                st.info("✂️ Step 2/3: Processing content...")
                chunks = chunk_text(scraped_text, chunk_size=500, overlap=50)
                
                # Use first chunk for extraction (most relevant info usually at top)
                text_to_extract = chunks[0] if chunks else scraped_text
                
                # Step 3: LLM Extraction
                st.info("🤖 Step 3/3: Extracting information with AI...")
                
                if llm_backend == "Ollama (Recommended)":
                    # Use CLI extractor (more reliable on Windows)
                    extractor = CLIExtractor(model=model_name)
                else:
                    from llm.extractor import HFExtractor
                    extractor = HFExtractor(model_name=model_name)
                
                extracted_data = extractor.extract_from_text(text_to_extract, company_url)
                
                if not extracted_data:
                    st.error("❌ LLM extraction failed. Check Ollama is running: `ollama serve`")
                    st.session_state.processing = False
                    st.stop()

                # Merge heuristic hints into LLM result (fill missing)
                for k in ["email", "phone", "linkedin", "facebook", "twitter", "instagram", "youtube", "blog"]:
                    if not extracted_data.get(k) and hints.get(k):
                        extracted_data[k] = hints[k]
                if hints.get("certifications"):
                    llm_certs = extracted_data.get("certifications") or []
                    if not isinstance(llm_certs, list):
                        llm_certs = [llm_certs]
                    merged = list(dict.fromkeys([*llm_certs, *hints["certifications"]]))
                    extracted_data["certifications"] = merged

                # Optional enrichment crawl for people, products/services, industry/sub-industry/sector, address
                if enable_enrich:
                    st.info("🔎 Enriching details from more pages…")
                    try:
                        # Use fast mode and fewer pages for better performance
                        enrich_fast = batch_fast_mode if batch_fast_mode else False
                        enrich_pages = 2 if enrich_fast else 6
                        enrich = enrich_company_details(company_url, timeout=timeout, fast_mode=enrich_fast, max_pages=enrich_pages)
                    except Exception:
                        enrich = {}
                    for k in ["people", "products", "services", "address", "industry", "sub_industry", "sector"]:
                        if not extracted_data.get(k) and enrich.get(k):
                            extracted_data[k] = enrich[k]
                    if enrich.get("enrichment_notes"):
                        notes = extracted_data.get("extraction_notes")
                        base = []
                        if isinstance(notes, list):
                            base = notes
                        elif isinstance(notes, str) and notes:
                            base = [notes]
                        extracted_data["extraction_notes"] = list(dict.fromkeys([*base, *enrich["enrichment_notes"]]))
                
                # Store for display
                st.session_state.extracted_data = extracted_data
                extraction_time = time.time() - start_time
                
                # Store in database
                db = CompanyDatabase()
                db.insert_company(
                    extracted_data,
                    scrape_url=company_url,
                    scrape_method=scrape_method,
                    content_length=scraped_length,
                    processing_time=extraction_time * 1000,
                    raw_content=text_to_extract[:1000]  # Store first 1000 chars
                )
                
                st.session_state.processing = False
                if resolved_note:
                    st.success(f"✅ Completed in {extraction_time:.2f}s — {resolved_note}")
                else:
                    st.success(f"✅ Completed in {extraction_time:.2f}s")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.processing = False

# Display Results
if st.session_state.extracted_data:
    st.markdown("---")
    st.subheader("📋 Extracted Information")
    
    data = st.session_state.extracted_data
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if data.get("company_name"):
            st.metric("Company", data["company_name"][:20] + "..." 
                     if len(str(data.get("company_name", ""))) > 20 else data["company_name"])
        else:
            st.metric("Company", "N/A")
    
    with col2:
        if data.get("industry"):
            st.metric("Industry", data["industry"][:15] + "..." 
                     if len(str(data.get("industry", ""))) > 15 else data["industry"])
        else:
            st.metric("Industry", "N/A")
    
    with col3:
        conf_raw = data.get("confidence")
        if conf_raw is None:
            st.metric("Confidence", "N/A")
        else:
            try:
                conf_val = float(conf_raw)
                # Clamp between 0 and 1 for percentage display
                if conf_val < 0:
                    conf_val = 0.0
                if conf_val > 1:
                    conf_val = 1.0
                st.metric("Confidence", f"{conf_val:.0%}")
            except Exception:
                st.metric("Confidence", "N/A")
    
    with col4:
        st.metric("Fields Found", len([v for v in data.values() if v is not None]))
    
    # Detailed information in tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📌 Company Info", 
        "📞 Contact & Social", 
        "🛍️ Products & Services",
        "👥 Team",
        "🏆 Certifications",
        "📄 Raw Data"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Information")
            if data.get("logo_url"):
                st.image(data["logo_url"], width=150)
            
            basic_fields = {
                "Company Name": data.get("company_name"),
                "Website": data.get("website"),
                "Industry": data.get("industry"),
                "Sub-Industry": data.get("sub_industry"),
                "Sector": data.get("sector")
            }
            
            for key, value in basic_fields.items():
                if value:
                    st.write(f"**{key}:** {value}")
                else:
                    st.write(f"**{key}:** *Not found*")
        
        with col2:
            st.subheader("Description")
            if data.get("short_description"):
                st.markdown(f"**Short:** {data['short_description']}")
            if data.get("long_description"):
                st.markdown(f"**Detailed:** {data['long_description']}")
            
            if data.get("sic_code") or data.get("sic_text"):
                st.markdown("**Classification:**")
                if data.get("sic_code"):
                    st.write(f"SIC Code: {data['sic_code']}")
                if data.get("sic_text"):
                    st.write(f"SIC Text: {data['sic_text']}")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Contact Information")
            contact_fields = {
                "Email": data.get("email"),
                "Phone": data.get("phone"),
                "Address": data.get("address")
            }
            
            for key, value in contact_fields.items():
                if value:
                    st.write(f"**{key}:** {value}")
                else:
                    st.write(f"**{key}:** *Not found*")
        
        with col2:
            st.subheader("Social Media & Links")
            social_fields = {
                "LinkedIn": data.get("linkedin"),
                "Facebook": data.get("facebook"),
                "Twitter": data.get("twitter"),
                "Instagram": data.get("instagram"),
                "YouTube": data.get("youtube"),
                "Blog": data.get("blog"),
                "Articles": data.get("articles")
            }
            
            found_social = False
            for key, value in social_fields.items():
                if value:
                    found_social = True
                    st.markdown(f"**{key}:** [{value}]({value if value.startswith('http') else 'https://' + value})")
            
            if not found_social:
                st.write("*No social media links found*")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Products")
            if data.get("products"):
                for i, product in enumerate(data["products"], 1):
                    st.write(f"{i}. {product}")
            else:
                st.write("*No products found*")
        
        with col2:
            st.subheader("Services")
            if data.get("services"):
                for i, service in enumerate(data["services"], 1):
                    st.write(f"{i}. {service}")
            else:
                st.write("*No services found*")
    
    with tab4:
        st.subheader("Key People")
        if data.get("people"):
            for person in data["people"]:
                with st.expander(f"👤 {person.get('name', 'Unknown')} - {person.get('title', 'N/A')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Name:** {person.get('name', 'N/A')}")
                        st.write(f"**Title:** {person.get('title', 'N/A')}")
                    with col2:
                        if person.get('email'):
                            st.write(f"**Email:** {person['email']}")
                        if person.get('profile_url'):
                            st.markdown(f"**Profile:** [{person['profile_url']}]({person['profile_url']})")
        else:
            st.write("*No team information found*")
    
    with tab5:
        st.subheader("Certifications & Compliance")
        if data.get("certifications"):
            # Display as badges
            cert_html = " ".join([
                f'<span style="background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; margin: 5px; display: inline-block;">{cert}</span>'
                for cert in data["certifications"]
            ])
            st.markdown(cert_html, unsafe_allow_html=True)
        else:
            st.write("*No certifications found*")
    
    with tab6:
        st.subheader("Raw JSON Data")
        st.json(data)
    
    # Notes at bottom (sanitize HTML and format nicely)
    def _strip_tags(val: str) -> str:
        try:
            return re.sub(r"<[^>]+>", "", val or "").strip()
        except Exception:
            return str(val)

    notes_val = data.get("extraction_notes")
    if notes_val:
        st.markdown("**Extraction Notes:**")
        if isinstance(notes_val, list):
            cleaned = [_strip_tags(str(n)) for n in notes_val if n]
            if cleaned:
                for n in cleaned:
                    st.write(f"- {n}")
            else:
                st.write("- (none)")
        else:
            st.write(_strip_tags(str(notes_val)))
    
    # Download option
    st.download_button(
        label="📥 Download as JSON",
        data=json.dumps(data, indent=2),
        file_name=f"company_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json",
        use_container_width=True
    )

# Show saved companies
if show_saved:
    st.markdown("---")
    st.subheader("💾 Saved Companies")
    
    try:
        db = CompanyDatabase()
        companies = db.get_all_companies(limit=10)
        
        if companies:
            for i, company in enumerate(companies, 1):
                with st.expander(f"{i}. {company.get('company_name', 'Unknown')} - {company.get('industry', 'N/A')}"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write(f"**Email:** {company.get('email', 'N/A')}")
                        st.write(f"**Phone:** {company.get('phone', 'N/A')}")
                    
                    with col2:
                        st.write(f"**Address:** {company.get('address', 'N/A')}")
                        st.write(f"**Website:** {company.get('website', 'N/A')}")
                    
                    with col3:
                        st.write(f"**Confidence:** {company.get('confidence', 0):.0%}")
                        st.write(f"**Added:** {company.get('created_at', 'N/A')}")
                    
                    if company.get('products'):
                        st.write(f"**Products:** {', '.join(company['products'])}")
        else:
            st.info("No companies saved yet. Extract information to get started!")
            
    except Exception as e:
        st.error(f"Error loading companies: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
### ℹ️ How to Use
1. Enter a company website URL or name
2. Select scraping method (Auto recommended)
3. Click "Extract Information"
4. Review extracted data and download as JSON

### 🔧 Setup Instructions
1. Install Ollama: https://ollama.ai
2. Run: `ollama pull mistral:7b-instruct-q4_0`
3. Start Ollama: `ollama serve`
4. Run Streamlit: `streamlit run ui/app.py`

### 📊 Supported LLM Models
- **Mistral-7B** (Recommended, best balance)
- **Phi-3-mini** (Smallest, fastest)
- **Neural-Chat-7B** (Good quality)
- **Orca-2-7B** (Best reasoning)
""")
