"""
Heuristic extraction of contacts, social links, and certifications directly from a website.
Lightweight and fast: fetches homepage HTML and uses regex/BeautifulSoup parsing.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\+?\d{1,3}[\s\(\).\-]?\d{1,4}[\s\(\).\-]?\d{1,4}[\s\(\).\-]?\d{1,9}")

SOCIAL_HOSTS = {
    "linkedin": ("linkedin.com", "lnkd.in"),
    "facebook": ("facebook.com", "fb.com"),
    "twitter": ("twitter.com", "x.com", "t.co"),
    "instagram": ("instagram.com", "insta.com"),
    "youtube": ("youtube.com", "youtu.be"),
    "github": ("github.com",),
    "gitlab": ("gitlab.com",),
}

CERT_PATTERNS = [
    r"ISO\s*9001", r"ISO\s*27001", r"ISO\s*27017", r"ISO\s*27018", r"ISO\s*13485",
    r"ISO\s*14001", r"ISO\s*22301", r"ISO\s*20000",
    r"SOC\s*2", r"SOC\s*1", r"SOC\s*Type\s*II", r"SOC\s*Type\s*2",
    r"GDPR", r"HIPAA", r"FedRAMP", r"PCI\s*DSS", r"CSA\s*STAR",
    r"Cyber\s*Essentials", r"CE\s*Mark", r"FDA",
]
CERT_RE = re.compile("|".join(CERT_PATTERNS), re.IGNORECASE)


def fetch_homepage_html(url: str, timeout: int = 10) -> Optional[str]:
    if not url:
        return None
    u = url
    if not u.lower().startswith(("http://", "https://")):
        u = "https://" + u
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
        r = requests.get(u, headers=headers, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception:
        return None


def extract_all(url: str, timeout: int = 10) -> Dict[str, object]:
    html = fetch_homepage_html(url, timeout=timeout) or ""
    emails = list(dict.fromkeys(EMAIL_RE.findall(html)))
    phones = list(dict.fromkeys(PHONE_RE.findall(html)))

    soup = BeautifulSoup(html, "html.parser") if html else None

    links = {k: None for k in ("linkedin", "facebook", "twitter", "instagram", "youtube", "github", "gitlab", "blog")}
    if soup:
        for a in soup.find_all("a", href=True):
            href = a.get("href") or ""
            if href.startswith("#"):
                continue
            full = urljoin(url, href)
            host = urlparse(full).netloc.lower()
            
            # Match social hosts
            for key, hosts in SOCIAL_HOSTS.items():
                if any(h in host for h in hosts):
                    if not links[key]:
                        links[key] = full
                        break
            
            # Detect blog
            path = urlparse(full).path or ""
            text = (a.get_text(" ") or "").lower()
            if not links["blog"] and ("/blog" in path or host.startswith("blog.") or "blog" in text):
                links["blog"] = full

    certs = []
    if html:
        certs = list(dict.fromkeys(CERT_RE.findall(html)))

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        **links,
        "certifications": certs,
    }
