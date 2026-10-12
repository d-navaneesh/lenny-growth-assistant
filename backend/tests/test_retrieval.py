from __future__ import annotations

from app.retrieval.service import search_transcripts
from app.skills.ship_30_for_30.skill import Ship30For30Skill


def test_search_returns_grounded_evidence():
    results = search_transcripts("product-market fit", top_k=2)
    assert len(results) >= 1
    assert results[0]["source_title"]
    assert "excerpt" in results[0]


def test_ship_30_skill_has_structure():
    skill = Ship30For30Skill()
    generated = skill.generate("How to choose a wedge in early-stage SaaS")
    assert generated["word_count"] > 150
    assert "# " in generated["essay"]
    assert "Takeaway" in generated["essay"]
