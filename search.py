from __future__ import annotations
import os
import requests
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

def demo_sources(topic: str) -> list[dict]:
    path = ROOT / "data" / "demo_sources.json"
    sources = json.loads(path.read_text(encoding="utf-8"))
    # Explicitly label these as illustrative, not current real-world research.
    return [{**s, "title": s["title"].replace("{topic}", topic), "snippet": s["snippet"].replace("{topic}", topic), "url": "https://example.com/researchpilot-demo/" + s["id"].lower(), "demo": True} for s in sources]

def tavily_search(query: str, max_results: int = 6) -> list[dict]:
    api_key = os.getenv("TAVILY_API_KEY", "")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("TAVILY_API_KEY", "")
        except Exception:
            pass
    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is missing. Add it to your environment or Streamlit secrets.")
    response = requests.post("https://api.tavily.com/search", json={"api_key": api_key, "query": query, "search_depth": "advanced", "max_results": max_results, "include_answer": False}, timeout=30)
    response.raise_for_status()
    data = response.json()
    results = []
    for idx, item in enumerate(data.get("results", []), 1):
        results.append({"id": f"S{idx}", "title": item.get("title") or "Untitled source", "url": item.get("url") or "", "snippet": item.get("content") or "", "published_date": item.get("published_date"), "demo": False})
    return results
