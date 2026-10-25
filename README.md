# ResearchPilot — Multi-Agent Business Research & Report Generator

A portfolio-ready Streamlit app that orchestrates four specialized agents to turn a business question into a structured research brief. Includes demo mode, optional live search via Tavily, evidence IDs, competitor signal table, risks, recommendations, and Markdown/JSON export.

> **Important:** Demo mode uses illustrative sample material and placeholder `example.com` URLs. It is for testing the workflow only, not real-world research. Use Live web search and verify original sources before citing claims in a business decision.

## Features
- Four-agent workflow: Discovery, Evidence Analyst, Competitive Intelligence, Report Strategist
- Topic and business-objective inputs
- Optional Tavily-powered live web search
- Evidence IDs and source list for traceability
- Executive summary, key takeaways, findings, competitor landscape, risk register, recommendations
- Download report as Markdown or JSON
- Unit tests and GitHub Actions CI

## Project structure
```text
researchpilot/
├── app/streamlit_app.py
├── src/research_agents/  # agent logic, search, pipeline, exports
├── data/demo_sources.json
├── tests/test_pipeline.py
├── .github/workflows/tests.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run locally
Python 3.10+ recommended.

```bash
python -m venv .venv
```
Activate it:
- Windows PowerShell: `.venv\\Scripts\\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then:
```bash
python -m pip install -r requirements.txt
streamlit run app/streamlit_app.py
```
Open the local URL shown by Streamlit, usually `http://localhost:8501`.

## Enable live web research (optional)
1. Create a Tavily API key from https://tavily.com/.
2. Set environment variable `TAVILY_API_KEY` before launching Streamlit, or add it to Streamlit Community Cloud secrets.
3. Select **Live web search (Tavily API)** in the app.

Never commit API keys to GitHub. `.env.example` is a template only; `.env` and `.streamlit/secrets.toml` are ignored.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Deploy free on Streamlit Community Cloud
1. Create a GitHub repository, e.g. `researchpilot-multi-agent-research`.
2. Upload the extracted **contents** of this folder (not only the ZIP file).
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Create an app and choose your repository/branch.
5. Set **Main file path** to `app/streamlit_app.py` and deploy.
6. For live mode, open app settings → Secrets and add `TAVILY_API_KEY = "your_key"`. Demo mode works without a key.

## Agent architecture
```text
Business question
       ↓
Discovery Agent → gather source material
       ↓
Evidence Analyst → group source snippets into themes
       ↓
Competitive Intelligence Agent → structure source/vendor signals
       ↓
Report Strategist → executive summary, risks, recommendations
       ↓
Markdown / JSON report
```

## Limitations and responsible use
- This is a lightweight agent workflow, not an autonomous fact-checker or a substitute for professional market research.
- Live mode uses search results/snippets; open the original pages and verify date, authorship, methodology, and claims.
- Confidence labels are heuristic and indicate source coverage, not statistical certainty.
- Demo-mode sources are fictional illustrative content with placeholder URLs.

## Suggested next improvements
- Add an LLM provider for evidence extraction and synthesis with strict citation checks.
- Persist research runs in SQLite/PostgreSQL.
- Add source-quality scoring, deduplication, and PDF export.
- Add a review screen to approve claims before report export.

## License
MIT — see `LICENSE`.
