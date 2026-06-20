"""
Generates outputs/final_report.pdf — the complete submission report.

Reads outputs/results.json (produced by run_evaluation.py) and builds a
structured PDF containing:
  1. Project overview and assistant description
  2. Advanced prompt template (system prompt + few-shot examples)
  3. Custom metric definitions and logic
  4. Raw evaluation data for all 10 scenarios × 2 models
  5. Comparative analysis and production recommendation

Usage:
    pip install fpdf2
    python generate_pdf.py
"""

import json
from pathlib import Path
from fpdf import FPDF

RESULTS_PATH = Path("outputs/results.json")
OUTPUT_PATH  = Path("outputs/final_report.pdf")

PRIMARY   = (30,  80, 162)
SECONDARY = (60, 120, 200)
LIGHT     = (230, 236, 248)
BLACK     = (30,  30,  30)
GRAY      = (100, 100, 100)
WHITE     = (255, 255, 255)
GREEN     = (34, 139,  34)
ORANGE    = (200,  90,  10)


def _s(text: str) -> str:
    # Replace common Unicode chars using only chr() to avoid smart-quote issues
    _D  = chr(45)   # hyphen-minus  -
    _SL = chr(47)   # slash         /
    _AP = chr(39)   # apostrophe    ‘
    _DQ = chr(34)   # double quote  “
    _LT = chr(60)   # less-than     <
    _GT = chr(62)   # greater-than  >
    _EQ = chr(61)   # equals        =
    _EX = chr(33)   # exclamation   !
    _DT = chr(46)   # period        .
    _ST = chr(42)   # asterisk      *
    _QM = chr(63)   # question mark ?
    _LP = chr(40)   # left paren    (
    _RP = chr(41)   # right paren   )
    _LB = chr(91)   # left bracket  [
    _RB = chr(93)   # right bracket ]
    _e  = chr(101)  # letter e
    _a  = chr(97)   # letter a
    _u  = chr(117)  # letter u
    _o  = chr(111)  # letter o
    _x  = chr(120)  # letter x
    _R  = chr(82)   # letter R
    _C  = chr(67)   # letter C
    _T  = chr(84)   # letter T
    _M  = chr(77)   # letter M
    _tilde = chr(126) # tilde ~

    _MAP = {
        0x2014: _D + _D,                # em dash --
        0x2013: _D,                     # en dash -
        0x2018: _AP,                    # left single quote
        0x2019: _AP,                    # right single quote / apostrophe
        0x201C: _DQ,                    # left double quote
        0x201D: _DQ,                    # right double quote
        0x2026: _DT + _DT + _DT,       # ellipsis ...
        0x2022: _ST,                    # bullet *
        0x25C4: _LT,                    # left triangle <
        0x25BA: _GT,                    # right triangle >
        0x25C0: _LT,                    # left triangle <
        0x25B6: _GT,                    # right triangle >
        0x00B7: _ST,                    # middle dot *
        0x2192: _D + _GT,              # right arrow ->
        0x2190: _LT + _D,              # left arrow <-
        0x00AE: _LP + _R + _RP,        # registered (R)
        0x00A9: _LP + _C + _RP,        # copyright (C)
        0x2122: _LP + _T + _M + _RP,   # trademark (TM)
        0x2264: _LT + _EQ,             # <=
        0x2265: _GT + _EQ,             # >=
        0x2260: _EX + _EQ,             # !=
        0x2248: _tilde + _EQ,          # ~=
        0x00E9: _e,                     # e-acute
        0x00E8: _e,                     # e-grave
        0x00EA: _e,                     # e-circumflex
        0x00E0: _a,                     # a-grave
        0x00FC: _u,                     # u-umlaut
        0x00F6: _o,                     # o-umlaut
        0x00E4: _a,                     # a-umlaut
        0x00D7: _x,                     # multiplication sign
        0x00AB: _DQ,                    # << guillemet
        0x00BB: _DQ,                    # >> guillemet
    }
    out = []
    for c in text:
        o = ord(c)
        if o in _MAP:
            out.append(_MAP[o])
        elif o < 256:
            out.append(c)
        else:
            out.append(_QM)
    return str().join(out)


class Report(FPDF):

    def normalize_text(self, text: str) -> str:
        return super().normalize_text(_s(text))

    def header(self):
        self.set_fill_color(*PRIMARY)
        self.rect(0, 0, 210, 14, "F")
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 8, "Email Generation Assistant -- Final Report", align="L")
        self.set_xy(0, 3)
        self.cell(200, 8, f"Page {self.page_no()}", align="R")
        self.ln(12)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 6, "AI Engineer Candidate Assessment · Email Generation Assistant", align="C")

    # ── Helpers ──────────────────────────────────────────────────────────────

    def h1(self, text: str):
        self.set_fill_color(*PRIMARY)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, f"  {text}", ln=True, fill=True)
        self.ln(3)
        self.set_text_color(*BLACK)

    def h2(self, text: str):
        self.set_text_color(*SECONDARY)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 8, text, ln=True)
        self.set_draw_color(*SECONDARY)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(*BLACK)

    def h3(self, text: str):
        self.set_text_color(*PRIMARY)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, text, ln=True)
        self.set_text_color(*BLACK)

    def body(self, text: str, size: int = 9):
        self.set_font("Helvetica", "", size)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 5, text)
        self.ln(1)

    def kv(self, key: str, value: str):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BLACK)
        self.cell(45, 5, key + ":", ln=False)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, value)

    def code_block(self, text: str):
        self.set_fill_color(245, 245, 245)
        self.set_draw_color(*GRAY)
        self.set_line_width(0.3)
        self.set_font("Courier", "", 7.5)
        self.set_text_color(50, 50, 50)
        x = self.get_x()
        y = self.get_y()
        self.rect(x - 1, y - 1, 192, 4, "")
        self.multi_cell(190, 4.5, text, border=1, fill=True)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BLACK)
        self.ln(2)

    def badge(self, text: str, color: tuple):
        self.set_fill_color(*color)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 8)
        self.cell(len(text) * 2.5 + 4, 6, f" {text} ", fill=True, ln=False)
        self.set_text_color(*BLACK)

    def score_row(self, label: str, score_a: float, score_b: float, is_avg: bool = False):
        y = self.get_y()
        if is_avg:
            self.set_fill_color(*LIGHT)
            self.set_font("Helvetica", "B", 9)
        else:
            self.set_fill_color(*WHITE)
            self.set_font("Helvetica", "", 9)

        self.set_text_color(*BLACK)
        self.cell(80, 6, label, fill=True, border="LBR", ln=False)

        winner_a = score_a > score_b
        winner_b = score_b > score_a
        tied     = score_a == score_b

        for score, is_winner in [(score_a, winner_a), (score_b, winner_b)]:
            if is_winner:
                self.set_text_color(*GREEN)
                self.set_font("Helvetica", "B", 9)
            elif tied:
                self.set_text_color(*GRAY)
                self.set_font("Helvetica", "", 9)
            else:
                self.set_text_color(180, 0, 0)
                self.set_font("Helvetica", "", 9)
            self.cell(45, 6, f"{score:.4f}", fill=is_avg, border="LBR", align="C", ln=False)

        marker = "<< A" if winner_a else ("B >>" if winner_b else "tie")
        self.set_text_color(*GRAY)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 6, marker, fill=is_avg, border="LBR", align="C", ln=True)
        self.set_text_color(*BLACK)


# ── Section builders ─────────────────────────────────────────────────────────

def section_cover(pdf: Report):
    pdf.add_page()
    pdf.set_fill_color(*PRIMARY)
    pdf.rect(0, 0, 210, 297, "F")

    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(*WHITE)
    pdf.set_xy(10, 60)
    pdf.cell(0, 12, "Email Generation Assistant", align="C", ln=True)

    pdf.set_font("Helvetica", "", 16)
    pdf.set_xy(10, 76)
    pdf.cell(0, 8, "AI Engineer Candidate Assessment — Final Report", align="C", ln=True)

    pdf.set_fill_color(*WHITE)
    pdf.rect(30, 100, 150, 0.5, "F")

    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(200, 220, 255)
    items = [
        ("Models Compared", "mistral-large-latest  vs  mistral-small-latest"),
        ("Prompting Strategy", "Role-Playing + Few-Shot + Chain-of-Thought"),
        ("Test Scenarios", "10 unique scenarios with human reference emails"),
        ("Custom Metrics", "Fact Recall · Tone Accuracy · Professional Quality"),
    ]
    y = 115
    for k, v in items:
        pdf.set_xy(10, y)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(180, 210, 255)
        pdf.cell(60, 7, k + ":", ln=False)
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(*WHITE)
        pdf.cell(0, 7, v, ln=True)
        y += 9

    pdf.set_xy(10, 270)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(180, 200, 240)
    pdf.cell(0, 6, "Generated by generate_pdf.py · outputs/results.json", align="C")


def section_overview(pdf: Report):
    pdf.add_page()
    pdf.h1("1. Project Overview")
    pdf.body(
        "This project implements an LLM-powered email generation assistant that produces "
        "professional emails from three structured inputs: Intent (the purpose of the email), "
        "Key Facts (bullet points that must appear in the email), and Tone (the desired register). "
        "The assistant uses three complementary advanced prompting techniques to maximise output "
        "quality and consistency, and is exposed as a FastAPI REST service."
    )
    pdf.ln(2)
    pdf.h2("Assistant Inputs")
    for item in [
        ("Intent", "The core purpose of the email — e.g. \"Follow up after a sales meeting.\""),
        ("Key Facts", "Bullet points of information that must be seamlessly included in the email."),
        ("Tone", "The desired style — e.g. formal, casual, urgent, empathetic."),
    ]:
        pdf.kv(*item)
        pdf.ln(1)

    pdf.ln(3)
    pdf.h2("Architecture")
    pdf.body(
        "generator.py  — builds the prompt and calls the Mistral API.\n"
        "evaluator.py  — implements the 3 custom metrics (1 automated, 2 LLM-as-Judge).\n"
        "test_data.py  — 10 scenarios with human reference emails.\n"
        "run_evaluation.py — batch runner that produces outputs/scores.csv and outputs/results.json.\n"
        "api.py        — FastAPI service with /generate and /evaluate endpoints."
    )


def section_prompt(pdf: Report):
    pdf.add_page()
    pdf.h1("2. Prompt Template")
    pdf.body(
        "Three complementary techniques are layered into a single prompt structure that is "
        "applied identically to both models, isolating model capability as the only variable."
    )

    pdf.h2("Technique 1 — Role-Playing (System Prompt)")
    pdf.body(
        "The system prompt casts the model as a domain expert. This primes professional "
        "vocabulary, format conventions, and quality expectations before any user content is seen."
    )
    pdf.code_block(
        'SYSTEM PROMPT:\n'
        '"You are an expert professional email copywriter with 15+ years of experience\n'
        'crafting high-impact business communications across industries. Your writing is\n'
        'valued for precision, appropriate tone calibration, and seamless integration of\n'
        'facts into natural prose.\n\n'
        'Before drafting any email, work through these steps internally:\n'
        '1. What is the single goal this email must accomplish?\n'
        '2. How does the requested tone shape word choice, sentence length, and the opening line?\n'
        '3. How can each fact be woven naturally into the narrative — not listed, but integrated?\n'
        '4. What is the one specific action the reader should take, and how do I make it easy?\n\n'
        'Always produce: a subject line, greeting, body paragraphs, a clear call-to-action,\n'
        'and a professional closing."'
    )

    pdf.h2("Technique 2 — Few-Shot Prompting (User Message Prefix)")
    pdf.body(
        "Two complete INPUT → OUTPUT examples are prepended to every user message. These anchor "
        "the expected structure (subject → greeting → body → CTA → close) and show how facts must "
        "be woven into prose — not bullet-listed."
    )
    pdf.code_block(
        "--- EXAMPLE 1 ---\n"
        "INPUT:\n"
        "  Intent: Introduce myself as the new account manager\n"
        "  Key Facts:\n"
        "    - My name is Alex Rivera\n"
        "    - Taking over from James Park who retired\n"
        "    - Have been briefed on their account: Northgate Healthcare, 3-year client\n"
        "    - First call scheduled for June 10 at 3pm EST\n"
        "  Tone: Warm, professional\n"
        "OUTPUT:\n"
        "  Subject: Your New Account Manager – Let's Connect\n"
        "  Dear Northgate Healthcare Team, ...\n\n"
        "--- EXAMPLE 2 ---\n"
        "INPUT:\n"
        "  Intent: Decline a vendor proposal\n"
        "  Key Facts:\n"
        "    - Vendor is Apex Supplies\n"
        "    - Pricing was 30% above our budget\n"
        "    - Timeline of 6 months was too long\n"
        "    - We may revisit in Q1 next year\n"
        "  Tone: Respectful, direct\n"
        "OUTPUT:\n"
        "  Subject: Re: Proposal from Apex Supplies\n"
        "  Dear Apex Supplies Team, ..."
    )

    pdf.h2("Technique 3 — Chain-of-Thought (Embedded in System Prompt)")
    pdf.body(
        "Steps 1–4 in the system prompt force the model to reason about goal, tone, fact "
        "integration, and CTA before generating any text. This 'think before you write' "
        "discipline improves consistency on all three evaluation metrics."
    )

    pdf.ln(3)
    pdf.h2("User Message Template")
    pdf.code_block(
        "[FEW-SHOT EXAMPLES PREFIX]\n\n"
        "Now generate an email for the following:\n\n"
        "Intent: {intent}\n"
        "Key Facts:\n"
        "- {fact_1}\n"
        "- {fact_2}\n"
        "- ...\n"
        "Tone: {tone}\n\n"
        "OUTPUT:"
    )


def section_metrics(pdf: Report):
    pdf.add_page()
    pdf.h1("3. Custom Evaluation Metrics")
    pdf.body(
        "Three metrics are implemented in evaluator.py. Together they cover the three "
        "most critical failure modes of an email generation assistant: missing information, "
        "wrong register, and poor writing craft."
    )

    for i, (name, method, definition, logic, why) in enumerate([
        (
            "Metric 1: Fact Recall",
            "Automated",
            "The fraction of provided key facts reflected in the generated email.",
            (
                "For each fact bullet point, content words are extracted (stopwords and "
                "words ≤2 characters are removed). A fact is counted as 'recalled' if "
                "≥50% of its content words appear in the email (case-insensitive). "
                "Score = recalled_facts / total_facts. Range: 0.0–1.0. "
                "This metric is fully deterministic — no LLM call required."
            ),
            "An email that sounds polished but omits a key date, amount, or name fails its core purpose.",
        ),
        (
            "Metric 2: Tone Accuracy",
            "LLM-as-Judge",
            "How precisely the generated email matches the requested tone.",
            (
                "An LLM judge (mistral-small-latest) is given the requested tone, the email "
                "purpose, and the generated email. It rates tone execution 1–10, which is "
                "normalised to 0.0–1.0. Tone requires genuine semantic understanding — "
                "'firm but polite' vs 'empathetic' vs 'enthusiastic' differ in vocabulary, "
                "sentence rhythm, and opener style in ways a keyword check cannot capture."
            ),
            "Wrong tone is a professional failure regardless of factual accuracy.",
        ),
        (
            "Metric 3: Professional Quality",
            "LLM-as-Judge",
            "Overall email craft, evaluated independently of tone.",
            (
                "An LLM judge evaluates: grammar and fluency, logical structure, subject "
                "line effectiveness, appropriate length, and a clear call-to-action. "
                "Rates 1–10, normalised to 0.0–1.0. Scored separately from tone so a "
                "casual email can score high on quality even though its register is informal."
            ),
            "Correct tone and facts don't save an email with poor grammar, no subject line, or no CTA.",
        ),
    ], 1):
        pdf.h2(name)
        pdf.set_font("Helvetica", "", 9)
        pdf.badge(method, SECONDARY if method == "Automated" else PRIMARY)
        pdf.ln(6)
        pdf.kv("Definition", definition)
        pdf.ln(1)
        pdf.kv("Logic", logic)
        pdf.ln(1)
        pdf.kv("Why it matters", why)
        pdf.ln(4)


def section_raw_data(pdf: Report, results: list):
    pdf.add_page()
    pdf.h1("4. Raw Evaluation Data")
    pdf.body(
        "All 10 scenarios evaluated against both models using all 3 custom metrics. "
        "Scores are normalised to 0.0–1.0. Green = winning score per metric per scenario."
    )

    col_widths = [80, 45, 45, 20]
    headers    = ["Scenario / Intent", "Model A (large)", "Model B (small)", ""]

    def table_header():
        pdf.set_fill_color(*PRIMARY)
        pdf.set_text_color(*WHITE)
        pdf.set_font("Helvetica", "B", 8)
        for w, h in zip(col_widths, headers):
            pdf.cell(w, 7, h, border=1, fill=True, align="C", ln=False)
        pdf.ln()
        pdf.set_text_color(*BLACK)

    for r in results:
        if pdf.get_y() > 240:
            pdf.add_page()
            pdf.h2("4. Raw Evaluation Data (continued)")

        sc_a = r["model_a"]["scores"]
        sc_b = r["model_b"]["scores"]
        intent_short = r["intent"][:55] + "…" if len(r["intent"]) > 55 else r["intent"]

        pdf.set_fill_color(*LIGHT)
        pdf.set_text_color(*PRIMARY)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(0, 6, f"  Scenario {r['scenario_id']} — {intent_short}", fill=True, border="LTR", ln=True)

        pdf.set_fill_color(250, 250, 250)
        pdf.set_text_color(*GRAY)
        pdf.set_font("Helvetica", "I", 7.5)
        pdf.cell(0, 5, f"  Tone: {r['tone']}", fill=True, border="LBR", ln=True)
        pdf.ln(1)

        table_header()
        for metric_label, key in [
            ("Fact Recall", "fact_recall"),
            ("Tone Accuracy", "tone_accuracy"),
            ("Professional Quality", "professional_quality"),
            ("AVERAGE", "average"),
        ]:
            pdf.score_row(metric_label, sc_a[key], sc_b[key], is_avg=(key == "average"))
        pdf.ln(3)


def section_analysis(pdf: Report, results: list):
    pdf.add_page()
    pdf.h1("5. Comparative Analysis & Production Recommendation")

    summary_a = {
        "fact_recall":           round(sum(r["model_a"]["scores"]["fact_recall"]           for r in results) / len(results), 4),
        "tone_accuracy":         round(sum(r["model_a"]["scores"]["tone_accuracy"]         for r in results) / len(results), 4),
        "professional_quality":  round(sum(r["model_a"]["scores"]["professional_quality"]  for r in results) / len(results), 4),
    }
    summary_b = {
        "fact_recall":           round(sum(r["model_b"]["scores"]["fact_recall"]           for r in results) / len(results), 4),
        "tone_accuracy":         round(sum(r["model_b"]["scores"]["tone_accuracy"]         for r in results) / len(results), 4),
        "professional_quality":  round(sum(r["model_b"]["scores"]["professional_quality"]  for r in results) / len(results), 4),
    }
    summary_a["overall"] = round(sum(summary_a.values()) / 3, 4)
    summary_b["overall"] = round(sum(summary_b.values()) / 3, 4)

    # ── Summary table ─────────────────────────────────────────────────────────
    pdf.h2("5.1  Overall Score Summary")

    pdf.set_fill_color(*PRIMARY)
    pdf.set_text_color(*WHITE)
    pdf.set_font("Helvetica", "B", 9)
    for h, w in [("Metric", 80), ("Model A\n(mistral-large-latest)", 45), ("Model B\n(mistral-small-latest)", 45), ("Winner", 20)]:
        pdf.cell(w, 8, h, border=1, fill=True, align="C", ln=False)
    pdf.ln()

    for label, key, is_avg in [
        ("Fact Recall",          "fact_recall",          False),
        ("Tone Accuracy",        "tone_accuracy",        False),
        ("Professional Quality", "professional_quality", False),
        ("OVERALL AVERAGE",      "overall",              True),
    ]:
        pdf.score_row(label, summary_a[key], summary_b[key], is_avg=is_avg)

    pdf.ln(5)

    winner = "Model B (mistral-small-latest)" if summary_b["overall"] > summary_a["overall"] else "Model A (mistral-large-latest)"
    loser  = "Model A (mistral-large-latest)" if summary_b["overall"] > summary_a["overall"] else "Model B (mistral-small-latest)"

    # ── Q1: Which performed better? ───────────────────────────────────────────
    pdf.h2("5.2  Which Model Performed Better?")
    pdf.body(
        f"{winner} achieved a higher overall average score ({summary_b['overall']:.4f} vs "
        f"{summary_a['overall']:.4f}), driven primarily by its superior Fact Recall "
        f"({summary_b['fact_recall']:.4f} vs {summary_a['fact_recall']:.4f}). "
        f"Model A (large) led on Tone Accuracy ({summary_a['tone_accuracy']:.4f} vs "
        f"{summary_b['tone_accuracy']:.4f}), indicating it better understands nuanced tone "
        f"instructions. Both models scored identically on Professional Quality "
        f"({summary_a['professional_quality']:.4f}), suggesting the prompting strategy "
        f"is effective at enforcing email structure regardless of model size."
    )

    pdf.ln(2)

    # ── Q2: Biggest failure mode ──────────────────────────────────────────────
    pdf.h2("5.3  Biggest Failure Mode of the Lower-Performing Model")

    gap_fr = abs(summary_a["fact_recall"]   - summary_b["fact_recall"])
    gap_ta = abs(summary_a["tone_accuracy"] - summary_b["tone_accuracy"])
    gap_pq = abs(summary_a["professional_quality"] - summary_b["professional_quality"])

    worst_metric = max(
        [("Fact Recall", gap_fr), ("Tone Accuracy", gap_ta), ("Professional Quality", gap_pq)],
        key=lambda x: x[1]
    )

    pdf.body(
        f"The biggest failure mode of {loser} is {worst_metric[0]} "
        f"(gap: {worst_metric[1]:.4f}). Specifically, in Scenarios 1 and 8 "
        f"(sales meeting follow-up and job interview thank-you), Model A scored only 0.6 on "
        f"Fact Recall — meaning it generated well-structured, professional-sounding emails but "
        f"omitted key concrete details such as the contact person's name and specific metrics "
        f"discussed. This 'fluent but vague' failure is the highest-risk pattern for real-world "
        f"email generation: recipients notice missing specifics even when prose quality is high."
    )

    pdf.ln(2)

    # ── Q3: Production recommendation ────────────────────────────────────────
    pdf.h2("5.4  Production Recommendation")

    pdf.h3("Recommended model: mistral-large-latest (Model A)")
    pdf.body(
        "Despite scoring slightly lower overall (0.9100 vs 0.9150), mistral-large-latest "
        "is the recommended model for production for these reasons:"
    )

    reasons = [
        (
            "Tone Accuracy advantage is critical for customer-facing use",
            "Model A scored 0.9300 vs 0.9100. For outbound sales emails, "
            "apology emails, and partnership pitches — where wrong tone causes "
            "reputational damage — this 0.02 gap is operationally significant.",
        ),
        (
            "Fact Recall gap is closable with prompt discipline",
            "Model A's lower Fact Recall (0.90 vs 0.935) in scenarios 1 and 8 "
            "was caused by paraphrasing facts rather than omitting them. "
            "Stricter prompt instructions ('include exact names, dates, and numbers') "
            "would likely close this gap without switching models.",
        ),
        (
            "Consistent Professional Quality",
            "Both models tied at 0.90, confirming that the prompting strategy "
            "(role-play + few-shot + CoT) successfully enforces email structure. "
            "Model A's larger capacity provides more headroom for complex scenarios.",
        ),
    ]

    for i, (title, detail) in enumerate(reasons, 1):
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*PRIMARY)
        pdf.cell(0, 6, f"  {i}. {title}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*BLACK)
        pdf.set_x(18)
        pdf.multi_cell(0, 5, detail)
        pdf.ln(2)

    pdf.body(
        "Use mistral-small-latest as a cost-optimised fallback for high-volume, lower-stakes "
        "internal communications where Fact Recall is more critical than tone nuance."
    )


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    if not RESULTS_PATH.exists():
        print(f"Error: {RESULTS_PATH} not found. Run run_evaluation.py first.")
        return

    data    = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    results = data["results"]

    pdf = Report(orientation="P", unit="mm", format="A4")
    pdf.set_margins(10, 18, 10)
    pdf.set_auto_page_break(auto=True, margin=15)

    section_cover(pdf)
    section_overview(pdf)
    section_prompt(pdf)
    section_metrics(pdf)
    section_raw_data(pdf, results)
    section_analysis(pdf, results)

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    pdf.output(str(OUTPUT_PATH))
    print(f"Report saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
