"""
Three custom evaluation metrics for the email generation assistant.

Metric 1 — Fact Recall (Automated)
    Measures whether the generated email actually includes the information it
    was given. For each fact bullet point, key content words are extracted and
    checked against the email text. A fact is counted as "recalled" if at least
    50% of its content words appear in the email. Score = recalled / total.
    This is fully automated (no LLM call) and deterministic.

Metric 2 — Tone Accuracy (LLM-as-Judge)
    Measures how precisely the generated email matches the requested tone.
    An LLM judge rates the email 1–10, which is normalized to 0–1. Tone is
    nuanced — "firm but polite" vs. "empathetic" vs. "enthusiastic" require
    genuinely different vocabulary, sentence rhythms, and openers. A keyword
    check cannot capture this; LLM judgment is the appropriate tool.

Metric 3 — Professional Quality (LLM-as-Judge)
    Measures overall email craft: grammar and fluency, logical structure,
    subject line effectiveness, appropriate length, and clear call-to-action.
    Score 1–10, normalized to 0–1. Rated independently of tone so a casual
    email can score high on quality even though its register is informal.
"""

import os
import re
import time
from mistralai.client import Mistral
from mistralai.client.errors.sdkerror import SDKError

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    return _client

JUDGE_MODEL = "mistral-small-latest"

STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "that", "this", "these", "those",
    "i", "we", "you", "he", "she", "they", "it", "our", "your", "their",
    "its", "my", "his", "her", "as", "if", "so", "no", "not", "up", "out",
}


# ── Metric 1: Fact Recall (automated) ─────────────────────────────────────────

def fact_recall_score(generated_email: str, facts: list[str]) -> float:
    email_lower = generated_email.lower()
    recalled = 0
    for fact in facts:
        words = re.findall(r"[a-zA-Z0-9]+", fact.lower())
        keywords = [w for w in words if w not in STOPWORDS and len(w) > 2]
        if not keywords:
            recalled += 1
            continue
        matched = sum(1 for k in keywords if k in email_lower)
        if matched / len(keywords) >= 0.5:
            recalled += 1
    return round(recalled / len(facts), 4) if facts else 0.0


# ── Metric 2: Tone Accuracy (LLM-as-judge) ────────────────────────────────────

def tone_accuracy_score(generated_email: str, tone: str, intent: str) -> float:
    prompt = (
        f"Rate how accurately the following email matches the requested tone.\n\n"
        f"Requested tone: {tone}\n"
        f"Email purpose: {intent}\n\n"
        f"Email:\n{generated_email}\n\n"
        f"Rate from 1 (tone completely mismatched) to 10 (tone perfectly executed). "
        f"Respond with only a single integer."
    )
    return _llm_score(prompt)


# ── Metric 3: Professional Quality (LLM-as-judge) ─────────────────────────────

def professional_quality_score(generated_email: str, intent: str) -> float:
    prompt = (
        f"Rate the overall professional quality of this email.\n\n"
        f"Email purpose: {intent}\n\n"
        f"Email:\n{generated_email}\n\n"
        f"Evaluate on: grammar and fluency, logical structure, subject line "
        f"effectiveness, appropriate length, and a clear call-to-action. "
        f"Rate from 1 (very poor) to 10 (excellent). Respond with only a single integer."
    )
    return _llm_score(prompt)


# ── Shared LLM judge helper ────────────────────────────────────────────────────

def _llm_score(prompt: str) -> float:
    for attempt in range(3):
        try:
            response = _get_client().chat.complete(
                model=JUDGE_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=10,
            )
            text = response.choices[0].message.content.strip()
            match = re.search(r"\d+", text)
            if match:
                return round(max(1, min(10, int(match.group()))) / 10.0, 4)
            return 0.5
        except SDKError as e:
            if e.raw_response.status_code == 429 and attempt < 2:
                time.sleep(60)
            else:
                raise


# ── Convenience wrapper ────────────────────────────────────────────────────────

def evaluate_email(scenario: dict, generated_email: str) -> dict:
    fr = fact_recall_score(generated_email, scenario["facts"])
    ta = tone_accuracy_score(generated_email, scenario["tone"], scenario["intent"])
    pq = professional_quality_score(generated_email, scenario["intent"])
    avg = round((fr + ta + pq) / 3, 4)
    return {"fact_recall": fr, "tone_accuracy": ta, "professional_quality": pq, "average": avg}
