from __future__ import annotations
from datetime import datetime, timezone
from .search import demo_sources, tavily_search
from .agents import discovery_agent, evidence_analyst, competitive_intelligence_agent, report_strategist

def run_research(topic: str, objective: str = "", live: bool = False) -> dict:
    if not topic or not topic.strip():
        raise ValueError("topic must not be empty")
    sources = tavily_search(f"{topic} {objective}".strip()) if live else demo_sources(topic)
    if not sources:
        raise RuntimeError("No sources returned. Try a broader topic or check your search API configuration.")
    discovery = discovery_agent(topic, sources)
    findings = evidence_analyst(topic, sources)
    competitors = competitive_intelligence_agent(topic, sources)
    strategy = report_strategist(topic, objective, findings, sources)
    return {"title": f"Business Research Brief: {topic}", "topic": topic, "objective": objective, "generated_at": datetime.now(timezone.utc).isoformat(), "mode": "Live web search" if live else "Demo (illustrative data)", "agents": [discovery, {"agent": "Evidence Analyst", "findings_created": len(findings)}, {"agent": "Competitive Intelligence Agent", "rows_created": len(competitors)}, {"agent": "Report Strategist", "recommendations_created": len(strategy["recommendations"])}], "sources": sources, "findings": findings, "competitors": competitors, **strategy}
