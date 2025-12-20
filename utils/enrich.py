from __future__ import annotations

import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

PEOPLE_CONTAINER_HINTS = (
    "team",
    "leadership",
    "management",
    "board",
    "people",
    "our-team",
    "staff",
    "employees",
)
PRODUCTS_HINTS = ("products", "solutions", "offerings")
SERVICES_HINTS = ("services", "capabilities")
ADDRESS_HINTS = ("contact", "locations", "find us")

NAME_RE = re.compile(r"\b([A-Z][a-z]+\s+[A-Z][a-zA-Z\-']+)\b")
CERT_RE = re.compile(r"ISO\s*\d{4,5}|SOC\s*\d|SOC\s*Type\s*II|GDPR|HIPAA|FedRAMP|PCI\s*DSS|CSA\s*STAR|Cyber\s*Essentials|CE\s*Mark|FDA", re.IGNORECASE)
POSTAL_RE = re.compile(r"\b(\d+\s+[A-Za-z][A-Za-z\s]+\b|[A-Za-z]+\s+(Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Boulevard|Blvd))\b.*", re.IGNORECASE)
COUNTRY_RE = re.compile(r"United\s*Kingdom|UK|England|Scotland|Wales|Northern\s*Ireland|United\s*States|USA|Canada|India|Germany|France", re.IGNORECASE)

INDUSTRY_KEYWORDS = {
    "Information Technology": ["software", "saas", "platform", "cloud", "api", "ai", "data", "development", "tech"],
    "Manufacturing": ["manufacturing", "factory", "production", "barcode", "label", "packaging", "industrial"],
    "Consulting": ["consulting", "advisory", "expert", "services", "consulting services"],
    "Healthcare": ["medical", "health", "patient", "clinical", "pharma", "healthcare"],
    "Information Security": ["security", "cybersecurity", "compliance", "security solutions", "penetration", "audit"],
    "Financial Services": ["finance", "banking", "investment", "fintech", "payments"],
    "E-commerce": ["e-commerce", "retail", "store", "shop", "marketplace"],
    "Business Services": ["outsourcing", "staffing", "recruitment", "hr solutions"],
    "Real Estate": ["property", "real estate", "real-estate", "realty", "development"],
    "Education": ["education", "training", "learning", "academy", "university", "school"],
}
SUB_INDUSTRY_KEYWORDS = {
    "AI Services": ["annotation", "labeling", "machine learning", "ml", "training data", "computer vision", "ai data"],
    "Cloud Infrastructure": ["cloud", "infrastructure", "aws", "azure", "hosting"],
    "Cybersecurity": ["security", "penetration", "audit", "threat", "vulnerability"],
    "Data Analytics": ["analytics", "business intelligence", "bi", "data science"],
    "E-commerce": ["store", "shop", "retail", "checkout", "cart", "marketplace"],
    "Consulting": ["consulting", "advisory", "management consulting"],
}
SECTOR_KEYWORDS = {
    "Technology": ["software", "ai", "cloud", "data", "platform", "tech", "development", "it"],
    "Industrial": ["manufacturing", "plant", "factory", "production", "industrial"],
    "Services": ["services", "consulting", "advisory"],
    "Financial": ["finance", "banking", "fintech", "payment"],
}


def _fetch(url: str, timeout: int) -> Optional[str]:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def _soup(html: Optional[str]) -> Optional[BeautifulSoup]:
    if not html:
        return None
    return BeautifulSoup(html, "html.parser")


def _candidate_paths(base: str, fast_mode: bool = False) -> List[str]:
    paths = [
        "/about",
        "/company",
        "/team",
        "/leadership",
        "/management",
        "/contact",
        "/products",
        "/services",
        "/solutions",
    ]
    if fast_mode:
        paths = ["/about", "/contact", "/services", "/products"]
    return [urljoin(base, p) for p in paths]


def _extract_people(soup: BeautifulSoup) -> List[Dict[str, Optional[str]]]:
    people: List[Dict[str, Optional[str]]] = []
    if not soup:
        return people
    containers = []
    for hint in PEOPLE_CONTAINER_HINTS:
        containers.extend(soup.find_all(class_=lambda c: c and hint in str(c).lower()))
        containers.extend(soup.find_all(id=lambda i: i and hint in str(i).lower()))
    if not containers:
        containers = [soup]
    seen_names = set()
    for cont in containers:
        for tag in cont.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            text = (tag.get_text(" ") or "").strip()
            m = NAME_RE.search(text)
            if m:
                name = m.group(1)
                if name in seen_names:
                    continue
                seen_names.add(name)
                title = None
                for t in ("CEO", "CTO", "COO", "Founder", "Director", "Manager", "Engineer", "Lead", "Head"):
                    if t.lower() in text.lower():
                        title = t
                        break
                email = None
                link = None
                a = tag.find("a", href=True)
                if a:
                    link = a["href"]
                people.append({"name": name, "title": title, "email": email, "profile_url": link})
    return people


def _extract_list_by_heading(soup: BeautifulSoup, hints: List[str]) -> List[str]:
    items: List[str] = []
    if not soup:
        return items
    # First: look for headings with hints
    for h in soup.find_all(["h2", "h3", "h4", "h5"]):
        ht = (h.get_text(" ") or "").lower()
        if any(k in ht for k in hints):
            # Look for lists after this heading
            next_el = h.find_next(["ul", "ol"])
            if next_el:
                for li in next_el.find_all("li", recursive=False):
                    val = (li.get_text(" ") or "").strip()
                    if val and 3 < len(val) < 200:
                        items.append(val)
            # Also check for next few paragraphs
            for p in h.find_next_siblings(["p", "div"], limit=5):
                txt = (p.get_text(" ") or "").strip()
                if 10 < len(txt) < 500 and not any(ch in txt for ch in "{}[]<>"):
                    if len(items) < 15:
                        items.append(txt[:100])
    # Second: if nothing found, try generic lists
    if not items:
        for li in soup.find_all("li"):
            val = (li.get_text(" ") or "").strip()
            if 3 < len(val) < 100 and not any(ch in val for ch in "{}[]<>"):
                if len(items) < 20:
                    items.append(val)
    return list(dict.fromkeys(items))[:25]


def _extract_address(soup: BeautifulSoup) -> Optional[str]:
    if not soup:
        return None
    for tag in soup.find_all(attrs={"itemtype": lambda v: v and "PostalAddress" in v}):
        text = (tag.get_text(" ") or "").strip()
        if text:
            return text
    # fallback regex scan
    text = soup.get_text(" ")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in lines:
        if POSTAL_RE.search(l) or COUNTRY_RE.search(l):
            return l
    return None


def _classify(text: str) -> Dict[str, Optional[str]]:
    industry = None
    sub_industry = None
    sector = None
    lt = text.lower()
    for key, kws in INDUSTRY_KEYWORDS.items():
        if any(k in lt for k in kws):
            industry = key
            break
    for key, kws in SUB_INDUSTRY_KEYWORDS.items():
        if any(k in lt for k in kws):
            sub_industry = key
            break
    for key, kws in SECTOR_KEYWORDS.items():
        if any(k in lt for k in kws):
            sector = key
            break
    return {"industry": industry, "sub_industry": sub_industry, "sector": sector}


def enrich_company_details(base_url: str, timeout: int = 10, fast_mode: bool = False, max_pages: int = 5) -> Dict[str, object]:
    url = base_url if base_url.startswith(("http://", "https://")) else "https://" + base_url
    pages = [url] + _candidate_paths(url, fast_mode)
    pages = pages[:max_pages]
    notes: List[str] = []

    people: List[Dict[str, Optional[str]]] = []
    products: List[str] = []
    services: List[str] = []
    address: Optional[str] = None
    industry: Optional[str] = None
    sub_industry: Optional[str] = None
    sector: Optional[str] = None

    for p in pages:
        html = _fetch(p, timeout)
        if not html:
            continue
        soup = _soup(html)
        text = soup.get_text(" ") if soup else ""
        
        # Classify on every page and keep non-None results
        cls = _classify(text)
        if cls.get("industry") and not industry:
            industry = cls.get("industry")
            notes.append(f"Industry '{industry}' found on {p}")
        if cls.get("sub_industry") and not sub_industry:
            sub_industry = cls.get("sub_industry")
            notes.append(f"Sub-industry '{sub_industry}' found on {p}")
        if cls.get("sector") and not sector:
            sector = cls.get("sector")
            notes.append(f"Sector '{sector}' found on {p}")
        
        if not people or len(people) < 5:
            ppl = _extract_people(soup)
            if ppl and len(ppl) > len(people):
                people = ppl
                notes.append(f"Found {len(ppl)} people on {p}")
        
        if not address:
            addr = _extract_address(soup)
            if addr:
                address = addr
                notes.append(f"Found address on {p}")
        
        if not products or len(products) < 5:
            prods = _extract_list_by_heading(soup, list(PRODUCTS_HINTS))
            if prods and len(prods) > len(products):
                products = prods
                notes.append(f"Found {len(prods)} products on {p}")
        
        if not services or len(services) < 5:
            servs = _extract_list_by_heading(soup, list(SERVICES_HINTS))
            if servs and len(servs) > len(services):
                services = servs
                notes.append(f"Found {len(servs)} services on {p}")

    return {
        "people": people or None,
        "products": products or None,
        "services": services or None,
        "address": address,
        "industry": industry,
        "sub_industry": sub_industry,
        "sector": sector,
        "enrichment_notes": notes,
    }
