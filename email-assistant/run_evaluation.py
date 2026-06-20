"""
Runs the full evaluation pipeline:
  - Generates emails for all 10 scenarios using two models
  - Scores each email on 3 custom metrics
  - Saves detailed results to outputs/results.json
  - Saves scores table to outputs/scores.csv
  - Prints a comparative summary report to the console

Usage:
    python run_evaluation.py

Models compared:
    Model A: mistral-large-latest   (higher capability)
    Model B: mistral-small-latest   (faster, lower cost)
Both use the same advanced prompting strategy (role-play + few-shot + CoT).
"""

import csv
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("MISTRAL_API_KEY"):
    sys.exit(
        "Error: MISTRAL_API_KEY is not set.\n"
        "Copy .env.example to .env and add your Mistral API key."
    )

from test_data import SCENARIOS
from generator import generate_email
from evaluator import evaluate_email, JUDGE_MODEL

MODEL_A = "mistral-large-latest"
MODEL_B = "mistral-small-latest"

OUTPUTS_DIR = Path("outputs")
OUTPUTS_DIR.mkdir(exist_ok=True)


def run() -> None:
    results = []
    total = len(SCENARIOS)

    print(f"Running evaluation: {total} scenarios × 2 models")
    print(f"  Model A: {MODEL_A}")
    print(f"  Model B: {MODEL_B}")
    print(f"  Judge:   {JUDGE_MODEL}\n")

    for i, scenario in enumerate(SCENARIOS, 1):
        print(f"[{i}/{total}] Scenario {scenario['id']}: {scenario['intent'][:60]}...")

        print(f"  Generating with Model A...", end=" ", flush=True)
        email_a = generate_email(scenario["intent"], scenario["facts"], scenario["tone"], MODEL_A)
        print("done")

        print(f"  Generating with Model B...", end=" ", flush=True)
        email_b = generate_email(scenario["intent"], scenario["facts"], scenario["tone"], MODEL_B)
        print("done")

        print(f"  Evaluating Model A...", end=" ", flush=True)
        scores_a = evaluate_email(scenario, email_a)
        print("done")

        print(f"  Evaluating Model B...", end=" ", flush=True)
        scores_b = evaluate_email(scenario, email_b)
        print("done\n")

        results.append({
            "scenario_id": scenario["id"],
            "intent": scenario["intent"],
            "tone": scenario["tone"],
            "model_a": {"generated_email": email_a, "scores": scores_a},
            "model_b": {"generated_email": email_b, "scores": scores_b},
        })

    _save_json(results)
    _save_csv(results)
    _print_summary(results)


def _save_json(results: list[dict]) -> None:
    output = {
        "metadata": {
            "model_a": MODEL_A,
            "model_b": MODEL_B,
            "prompting_strategy": "Advanced: Role-Playing + Few-Shot + Chain-of-Thought",
            "judge_model": JUDGE_MODEL,
            "metrics": {
                "fact_recall": (
                    "Automated keyword matching. For each fact, content words are extracted "
                    "and checked against the email text. Score = fraction of facts where "
                    ">=50% of their content words appear in the email. Range: 0.0–1.0."
                ),
                "tone_accuracy": (
                    "LLM-as-Judge. The judge model rates (1–10) how well the email matches "
                    "the requested tone, normalised to 0.0–1.0."
                ),
                "professional_quality": (
                    "LLM-as-Judge. The judge model rates (1–10) overall email craft: "
                    "grammar, structure, subject line, length, and call-to-action, "
                    "normalised to 0.0–1.0."
                ),
            },
        },
        "results": results,
        "summary": _compute_summary(results),
    }
    path = OUTPUTS_DIR / "results.json"
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(f"Saved: {path}")


def _save_csv(results: list[dict]) -> None:
    path = OUTPUTS_DIR / "scores.csv"
    rows = []
    for r in results:
        for label, model_key in [("model_a", "model_a"), ("model_b", "model_b")]:
            s = r[model_key]["scores"]
            rows.append({
                "scenario_id": r["scenario_id"],
                "model": MODEL_A if model_key == "model_a" else MODEL_B,
                "intent": r["intent"],
                "tone": r["tone"],
                "fact_recall": s["fact_recall"],
                "tone_accuracy": s["tone_accuracy"],
                "professional_quality": s["professional_quality"],
                "average": s["average"],
            })
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved: {path}")


def _compute_summary(results: list[dict]) -> dict:
    def avg_metric(model_key: str, metric: str) -> float:
        vals = [r[model_key]["scores"][metric] for r in results]
        return round(sum(vals) / len(vals), 4)

    summary = {}
    for label, key in [("model_a", "model_a"), ("model_b", "model_b")]:
        fr = avg_metric(key, "fact_recall")
        ta = avg_metric(key, "tone_accuracy")
        pq = avg_metric(key, "professional_quality")
        summary[label] = {
            "avg_fact_recall": fr,
            "avg_tone_accuracy": ta,
            "avg_professional_quality": pq,
            "overall_average": round((fr + ta + pq) / 3, 4),
        }
    return summary


def _print_summary(results: list[dict]) -> None:
    summary = _compute_summary(results)
    sa = summary["model_a"]
    sb = summary["model_b"]

    print("\n" + "=" * 64)
    print("EVALUATION SUMMARY")
    print("=" * 64)
    print(f"{'Metric':<28} {'Model A (large)':>16} {'Model B (small)':>16}")
    print("-" * 64)
    metrics = [
        ("Fact Recall", "avg_fact_recall"),
        ("Tone Accuracy", "avg_tone_accuracy"),
        ("Professional Quality", "avg_professional_quality"),
        ("OVERALL AVERAGE", "overall_average"),
    ]
    for label, key in metrics:
        va = sa[key]
        vb = sb[key]
        winner = "◀" if va > vb else ("▶" if vb > va else "=")
        print(f"{label:<28} {va:>16.4f} {vb:>16.4f}  {winner}")
    print("=" * 64)

    winner_label = "Model A (mistral-large-latest)" if sa["overall_average"] > sb["overall_average"] else "Model B (mistral-small-latest)"
    print(f"\nOverall winner: {winner_label}")
    print("\nPer-scenario breakdown:")
    print(f"{'ID':<4} {'Model A avg':>12} {'Model B avg':>12} {'Winner'}")
    print("-" * 40)
    for r in results:
        avg_a = r["model_a"]["scores"]["average"]
        avg_b = r["model_b"]["scores"]["average"]
        w = "A" if avg_a > avg_b else ("B" if avg_b > avg_a else "tie")
        print(f"{r['scenario_id']:<4} {avg_a:>12.4f} {avg_b:>12.4f} {w}")
    print("=" * 64)
    print(f"\nFull results: {OUTPUTS_DIR / 'results.json'}")
    print(f"Score table:  {OUTPUTS_DIR / 'scores.csv'}")


if __name__ == "__main__":
    run()
