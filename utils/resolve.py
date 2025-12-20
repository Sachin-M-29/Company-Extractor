"""
Resolve a company's official website from a name or loose input.
- If input already looks like a domain/URL, normalize and return it.
- Otherwise, query DuckDuckGo HTML results and pick the most likely official site.
"""
from __future__ import annotations

import re
import logging
from typing import Optional
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_DOMAIN_RE = re.compile(r"^(?:https?://)?[a-z0-9.-]+\.[a-z]{2,}(?:/.*)?$", re.IGNORECASE)
_SOCIAL_HOSTS = {
    "linkedin.com", "lnkd.in", "facebook.com", "x.com", "twitter.com",
    "instagram.com", "youtube.com", "youtu.be", "medium.com", "github.com",
    "gitlab.com", "crunchbase.com", "wikipedia.org", "bloomberg.com",
}


def _normalize_url(url: str) -> str:
    u = (url or "").strip()
    if not u:
        return u
    if u.lower().startswith(("http://", "https://")):
        return u
    return f"https://{u}"


def _is_domain_like(text: str) -> bool:
    return bool(_DOMAIN_RE.match((text or "").strip()))


def resolve_company_website(query: str, timeout: int = 10) -> Optional[str]:
    """
    Return a best-guess official website URL for a company name or domain-ish input.
    """
    q = (query or "").strip()
    if not q:
        return None

    # If it already looks like a domain/URL, just normalize.
    if _is_domain_like(q):
        return _normalize_url(q)

    # Search DuckDuckGo HTML (no API key required)
    search_url = f"https://duckduckgo.com/html/?q={quote_plus(q + ' official site')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(search_url, headers=headers, timeout=timeout)
        resp.raise_for_status()
    except Exception as e:
        logger.warning(f"Resolve search failed: {e}")
        return None

    soup = BeautifulSoup(resp.text, "html.parser")

    # DuckDuckGo classic HTML results: links with class 'result__a'
    links = soup.select("a.result__a") or soup.find_all("a", href=True)
    candidates: list[str] = []
    for a in links:
        href = a.get("href") or ""
        if href.startswith("/") or not href.startswith("http"):
            continue
        host = urlparse(href).netloc.lower()
        # Strip www.
        host = host[4:] if host.startswith("www.") else host
        if any(host.endswith(bad) for bad in _SOCIAL_HOSTS):
            continue
        # Prefer homepages (no long paths)
        path = (urlparse(href).path or "/").strip()
        if path not in ("/", "") and path.count("/") > 2:
            continue
        candidates.append(href)

    # Return first acceptable candidate
    if candidates:
        return _normalize_url(candidates[0])
    return None
