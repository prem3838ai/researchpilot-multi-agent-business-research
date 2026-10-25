def to_markdown(report: dict) -> str:
    lines = [f"# {report['title']}", "", f"- **Generated:** {report['generated_at']}", f"- **Mode:** {report['mode']}", f"- **Objective:** {report.get('objective') or 'Not specified'}", "", "> Verify claims against the original sources. Demo-mode sources are illustrative and are not real citations.", "", "## Executive summary", report["executive_summary"], "", "## Key takeaways"]
    lines += [f"- {x}" for x in report["key_takeaways"]]
    lines += ["", "## Findings"]
    for item in report["findings"]:
        lines += [f"### {item['title']}", f"**Confidence:** {item['confidence']}  ", f"**Evidence IDs:** {item['source_ids']}", "", item["detail"], ""]
    lines += ["## Competitive landscape", "| Organization / source | Signal | Evidence ID | Source type |", "|---|---|---|---|"]
    for row in report["competitors"]:
        vals = [str(row[k]).replace("|", "\\|").replace("\n", " ") for k in ["Organization / source", "Signal", "Evidence ID", "Source type"]]
        lines.append("| " + " | ".join(vals) + " |")
    lines += ["", "## Risks and mitigations"]
    lines += [f"- **{r['risk']}** — {r['mitigation']}" for r in report["risks"]]
    lines += ["", "## Recommendations"]
    lines += [f"{i}. {r}" for i, r in enumerate(report["recommendations"], 1)]
    lines += ["", "## Sources"]
    lines += [f"- **[{s['id']}] {s['title']}** — {s['url']}\n  - {s['snippet']}" for s in report["sources"]]
    return "\n".join(lines) + "\n"
