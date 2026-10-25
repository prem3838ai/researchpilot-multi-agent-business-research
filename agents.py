from __future__ import annotations
import re
from collections import Counter

STOPWORDS = {"about", "their", "there", "which", "would", "could", "should", "these", "those", "with", "from", "into", "that", "this", "have", "will", "your", "than", "then", "them", "they", "what", "when", "where", "while", "also", "more", "most", "some", "such", "over", "under", "based", "business", "research", "market"}

def discovery_agent(topic: str, sources: list[dict]) -> dict:
    return {"agent": "Discovery Agent", "goal": f"Collect sources relevant to: {topic}", "sources_found": len(sources), "source_ids": [s["id"] for s in sources]}

def evidence_analyst(topic: str, sources: list[dict]) -> list[dict]:
    findings = []
    patterns = [
        ("Market and demand signals", r"market|demand|growth|adoption|customer|buyer|trend"),
        ("Product and technology signals", r"technology|platform|product|automation|AI|software|integration"),
        ("Competition and positioning", r"competitor|competition|pricing|differenti|vendor|alternative"),
        ("Risks and constraints", r"risk|privacy|security|cost|regulation|challenge|limitation"),
    ]
    for title, pattern in patterns:
        matches = [s for s in sources if re.search(pattern, s.get("snippet", "") + " " + s.get("title", ""), re.I)]
        if matches:
            details = " ".join(f"{s['snippet']} [{s['id']}]" for s in matches[:3])
            findings.append({"title": title, "detail": details, "source_ids": ", ".join(s["id"] for s in matches[:3]), "confidence": "Medium" if len(matches) > 1 else "Low"})
    if not findings:
        findings.append({"title": "Initial research coverage", "detail": f"The available sources mention {topic}, but more targeted sources are needed to validate specific claims.", "source_ids": ", ".join(s["id"] for s in sources[:2]), "confidence": "Low"})
    return findings

def competitive_intelligence_agent(topic: str, sources: list[dict]) -> list[dict]:
    rows = []
    for s in sources[:6]:
        title = s.get("title", "Source")
        rows.append({"Organization / source": title[:80], "Signal": s.get("snippet", "")[:220], "Evidence ID": s.get("id", ""), "Source type": "Illustrative demo" if s.get("demo") else "Web result"})
    return rows

def report_strategist(topic: str, objective: str, findings: list[dict], sources: list[dict]) -> dict:
    if sources and all(s.get("demo") for s in sources):
        caveat = "This report uses illustrative demo material, not verified live research. Replace it with live web results before making business decisions."
    else:
        caveat = "Search snippets are starting points, not proof. Verify source quality, dates, and underlying claims before making business decisions."
    summary = f"This initial brief examines {topic} against the objective: {objective or 'understand the business opportunity and risks'}. It organizes available evidence into market, product, competitive, and risk themes. Treat conclusions as directional until claims are independently validated. {caveat}"
    risks = [
        {"risk": "Evidence may be incomplete or outdated", "mitigation": "Prioritize primary sources, record publication dates, and validate important claims independently."},
        {"risk": "Search snippets can omit context", "mitigation": "Open and read the full source before using a claim in a decision or client report."},
        {"risk": "Competitive claims may be biased", "mitigation": "Compare vendor claims with customer reviews, pricing pages, and independent analysis."},
    ]
    recommendations = [
        f"Define measurable success criteria for the research question: {objective or topic}.",
        "Validate the two or three most decision-critical findings using primary sources and recent publications.",
        "Build a competitor comparison using consistent criteria such as target customer, capabilities, pricing model, integrations, and proof points.",
        "Convert the strongest validated evidence into a 30-day experiment with an owner, metric, and review date.",
    ]
    takeaways = [f"The research is structured around {len(findings)} evidence themes.", "Source quality and recency should be checked before relying on any conclusion.", "Use the recommendations as a validation plan, not as a substitute for due diligence."]
    return {"executive_summary": summary, "key_takeaways": takeaways, "risks": risks, "recommendations": recommendations}
