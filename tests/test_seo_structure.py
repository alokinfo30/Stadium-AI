import os
import json


def test_robots_txt_exists_and_allows_ai_bots():
    robots_path = os.path.join(os.path.dirname(__file__), "..", "public", "robots.txt")
    assert os.path.exists(robots_path)
    with open(robots_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "User-agent: *" in content
    assert "Allow: /" in content
    assert "GPTBot" in content
    assert "PerplexityBot" in content
    assert "ClaudeBot" in content


def test_sitemap_xml_exists_and_contains_urls():
    sitemap_path = os.path.join(os.path.dirname(__file__), "..", "public", "sitemap.xml")
    assert os.path.exists(sitemap_path)
    with open(sitemap_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "<urlset" in content
    assert "<loc>" in content
    assert "llms.txt" in content


def test_llms_txt_exists_and_valid():
    llms_path = os.path.join(os.path.dirname(__file__), "..", "public", "llms.txt")
    assert os.path.exists(llms_path)
    with open(llms_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "FIFA World Cup 2026" in content
    assert "7 Autonomous AI Agents" in content
    assert "Alok Srivastava" in content


def test_index_html_contains_schema_org_json_ld():
    html_path = os.path.join(os.path.dirname(__file__), "..", "public", "index.html")
    assert os.path.exists(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "application/ld+json" in content
    assert "SoftwareApplication" in content
    assert "SportsEvent" in content
    assert "FAQPage" in content
