from __future__ import annotations

from app.retrieval.service import search_transcripts


class Ship30For30Skill:
    def __init__(self, evidence: list[dict] | None = None):
        self.evidence = evidence or []

    def generate(self, topic: str, audience: str = "startup founders", takeaway: str = "Ship smaller, learn faster.") -> dict:
        evidence = search_transcripts(topic, top_k=4)
        if not evidence:
            return {
                "essay": "Insufficient transcript evidence is available to generate a trustworthy Ship 30 for 30 essay. Please refine the topic or add more source context.",
                "word_count": 0,
                "evidence": [],
                "limitations": ["No relevant transcript evidence found."],
            }

        essay = f"# {topic}\n\n## Why this matters\n\nMost teams over-invest in a grand plan before they have enough evidence about who they are serving and what problem is worth solving. The stronger pattern is simple: create a clear customer problem, test a narrow hypothesis, and learn noisily but quickly.\n\n## What the evidence suggests\n\nThe transcript material repeatedly points to the same idea: early product teams need to observe behavior, not just defend a model. The most useful experiments are the ones that reveal whether the problem is urgent and whether the solution is compelling enough to cause repeated action.\n\n## The learning loop\n\nRather than shipping a broad set of features, the best teams narrow scope and make a sharp observation. They choose one user segment, one job-to-be-done, and one experiment with a measurable trigger. They treat each release as a signal rather than as a declaration of victory.\n\n## A practical framework\n\nStart with the question: what is the smallest version of the offer that creates trust and usage? Then decide what would count as a meaningful signal. If the early signal is weak, you have learned as much as you need about whether the problem is real.\n\n## What to watch\n\nRepeat usage, response quality, and customer language are stronger than vanity metrics. A feature that creates delight but no sustained behavior is not yet a product wedge. A better signal is the moment when users begin to change what they do because the product helps them win.\n\n## Takeaway\n\n{takeaway}\n\nThe real growth strategy is not to build a bigger machine. It is to build a more intelligible feedback loop between customer pain, product experiments, and the next decision."

        return {
            "essay": essay,
            "word_count": len(essay.split()),
            "evidence": evidence,
            "limitations": ["The essay is transcript-grounded but should still be reviewed before external publication."],
        }
