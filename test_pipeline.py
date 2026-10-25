import unittest
from src.research_agents.pipeline import run_research
from src.research_agents.exporters import to_markdown

class PipelineTests(unittest.TestCase):
    def test_demo_pipeline_returns_expected_sections(self):
        report = run_research("AI customer support", "Assess opportunity", live=False)
        for key in ["executive_summary", "key_takeaways", "sources", "findings", "competitors", "risks", "recommendations", "agents"]:
            self.assertIn(key, report)
        self.assertGreaterEqual(len(report["sources"]), 3)
        self.assertEqual(len(report["agents"]), 4)
    def test_demo_mode_is_disclosed(self):
        report = run_research("CRM analytics", live=False)
        self.assertIn("Demo", report["mode"])
        self.assertTrue(all(s["demo"] for s in report["sources"]))
    def test_blank_topic_raises(self):
        with self.assertRaises(ValueError):
            run_research("   ")
    def test_markdown_export(self):
        report = run_research("Retail analytics", live=False)
        md = to_markdown(report)
        self.assertIn("## Executive summary", md)
        self.assertIn("## Sources", md)
        self.assertIn("Illustrative", md)

if __name__ == "__main__": unittest.main()
