from pathlib import Path
import sys
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.research_agents.pipeline import run_research
from src.research_agents.exporters import to_markdown

st.set_page_config(page_title="ResearchPilot | Multi-Agent Research", page_icon="🧭", layout="wide")
st.title("🧭 ResearchPilot")
st.caption("Multi-Agent Business Research & Report Generator")
st.write("Turn a business question into a structured, source-aware research brief with specialized research agents.")
with st.sidebar:
    st.header("Research settings")
    topic = st.text_input("Research topic", "AI-powered customer support software market")
    objective = st.text_area("Business objective", "Assess market opportunity, competitors, risks, and recommended next steps.", height=110)
    mode = st.selectbox("Research mode", ["Demo mode (no API key needed)", "Live web search (Tavily API)"])
    st.caption("Live mode requires TAVILY_API_KEY in your environment or Streamlit secrets.")
    run = st.button("Generate research report", type="primary", use_container_width=True)

if run:
    if not topic.strip():
        st.error("Enter a research topic first.")
    else:
        live = mode.startswith("Live")
        try:
            with st.spinner("Research agents are working: discovery → evidence review → synthesis → recommendations…"):
                report = run_research(topic.strip(), objective.strip(), live=live)
            st.session_state["report"] = report
        except Exception as exc:
            st.error(f"Research run failed: {exc}")

report = st.session_state.get("report")
if report:
    st.success(f"Report generated in {report['mode']} mode")
    metrics = st.columns(3)
    metrics[0].metric("Sources reviewed", len(report["sources"]))
    metrics[1].metric("Research agents", 4)
    metrics[2].metric("Evidence-backed findings", len(report["findings"]))
    tabs = st.tabs(["Executive summary", "Findings", "Competitor landscape", "Risks & recommendations", "Sources", "Full report"])
    with tabs[0]:
        st.subheader("Executive summary")
        st.write(report["executive_summary"])
        st.subheader("Key takeaways")
        for item in report["key_takeaways"]: st.markdown(f"- {item}")
    with tabs[1]:
        for i, item in enumerate(report["findings"], 1):
            with st.expander(f"{i}. {item['title']} · {item['confidence']} confidence", expanded=i == 1):
                st.write(item["detail"])
                st.caption(f"Evidence: {item['source_ids']}")
    with tabs[2]:
        st.dataframe(report["competitors"], use_container_width=True, hide_index=True)
    with tabs[3]:
        st.subheader("Risks")
        for item in report["risks"]: st.markdown(f"- **{item['risk']}** — {item['mitigation']}")
        st.subheader("Recommended next steps")
        for i, item in enumerate(report["recommendations"], 1): st.markdown(f"{i}. {item}")
    with tabs[4]:
        for src in report["sources"]:
            st.markdown(f"**[{src['id']}] [{src['title']}]({src['url']})**")
            st.caption(src.get("published_date") or "Publication date not provided")
            st.write(src["snippet"])
    with tabs[5]:
        md = to_markdown(report)
        st.markdown(md)
        st.download_button("Download Markdown report", md, file_name="researchpilot-report.md", mime="text/markdown")
        st.download_button("Download report data (JSON)", __import__("json").dumps(report, indent=2), file_name="researchpilot-report.json", mime="application/json")
else:
    st.info("Choose a topic and generate a report. Demo mode works without API keys and clearly labels illustrative evidence.")
    st.markdown("""**Agent workflow**

1. **Discovery Agent** — gathers relevant sources.
2. **Evidence Analyst** — extracts themes and evidence.
3. **Competitive Intelligence Agent** — structures competitor signals.
4. **Report Strategist** — creates an executive brief and actions.
""")
