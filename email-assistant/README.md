# Email Generation Assistant

An AI-powered email generation assistant with a FastAPI service and custom evaluation framework comparing two Mistral models.

## What This Does

1. **Generates** professional emails from three inputs: intent, key facts, and tone
2. **Evaluates** output quality using three custom metrics
3. **Compares** two models (`mistral-large-latest` vs `mistral-small-latest`) using the same prompt strategy
4. **Serves** email generation via a FastAPI REST API

---

## Setup

### 1. Set your API key

```bash
cp .env.example .env
# Edit .env and add your Mistral API key (get one free at console.mistral.ai)
```

### 2. Install dependencies

```bash
# Windows
py -m pip install -r requirements.txt

# macOS / Linux
pip install -r requirements.txt
```

---

## Running Options

### Option A — FastAPI Server (recommended for demo)

```bash
# Windows
py -m uvicorn api:app --reload

# macOS / Linux
uvicorn api:app --reload
```

Open **http://localhost:8000/docs** for the interactive Swagger UI.

**Endpoints:**
- `GET  /health` — liveness check
- `POST /generate` — generate one email
- `POST /evaluate` — generate + score with all 3 metrics

**Example request:**
```json
POST /generate
{
  "intent": "Follow up after a sales meeting",
  "facts": ["Met on June 15", "Demo scheduled June 28", "Contact is Sarah Chen"],
  "tone": "Professional, warm",
  "model": "mistral-large-latest"
}
```

---

### Option B — Batch Evaluation (generates report)

```bash
# Windows
py run_evaluation.py

# macOS / Linux
python run_evaluation.py
```

Runs all 10 test scenarios through both models, scores them, and saves results to `outputs/`.

**Expected runtime:** ~5–10 minutes (60 API calls: 20 generation + 40 judge calls).

---

### Option C — Generate PDF Report

```bash
# Install PDF dependency first
pip install fpdf2

# Windows
py generate_pdf.py

# macOS / Linux
python generate_pdf.py
```

Produces `outputs/final_report.pdf` from the existing `outputs/results.json`.

---

## Running with Docker

### API server

```bash
docker compose up api
```

Open **http://localhost:8000/docs**

### Batch evaluation

```bash
docker compose --profile evaluate run evaluate
```

Results land in `outputs/` on your local machine.

---

## Project Structure

```
email-assistant/
├── api.py                # FastAPI service (generate + evaluate endpoints)
├── generator.py          # Email generation with advanced prompting
├── evaluator.py          # 3 custom evaluation metrics
├── test_data.py          # 10 test scenarios with human reference emails
├── run_evaluation.py     # Batch runner — generates, evaluates, saves, reports
├── generate_pdf.py       # Produces outputs/final_report.pdf
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── outputs/
    ├── scores.csv        # Score table (one row per scenario × model)
    ├── results.json      # Full results including generated emails
    └── final_report.pdf  # Final submission report
```

---

## Advanced Prompting Technique

Three complementary techniques are applied together:

### 1. Role-Playing
The system prompt establishes the model as *"an expert professional email copywriter with 15+ years of experience."* This primes domain-specific vocabulary, structural conventions, and quality expectations rather than producing a generic completion.

### 2. Few-Shot Prompting
Two complete `INPUT → OUTPUT` examples are prepended to every user message. These anchor the expected format (subject line → greeting → body → CTA → close) and demonstrate how facts should be woven into narrative prose rather than bullet-listed.

### 3. Chain-of-Thought (embedded)
The system prompt includes an explicit four-step reasoning checklist the model applies *before* drafting:
1. What is the single goal?
2. How does the tone shape word choice?
3. How do I integrate each fact naturally?
4. What action do I want the reader to take?

---

## Custom Evaluation Metrics

### Metric 1: Fact Recall *(Automated)*

**Definition:** The fraction of provided key facts reflected in the generated email.

**Logic:**
- For each fact, extract content words (remove stopwords and words ≤2 characters)
- A fact is "recalled" if ≥50% of its content words appear in the email (case-insensitive)
- Score = recalled facts / total facts (range: 0.0–1.0)

**Why this matters:** An email that sounds polished but omits a key date, amount, or name fails its core purpose.

---

### Metric 2: Tone Accuracy *(LLM-as-Judge)*

**Definition:** How precisely the generated email matches the specified tone.

**Logic:**
- LLM judge (`mistral-small-latest`) rates 1–10 how well tone is executed, normalized to 0.0–1.0
- Tone is nuanced — "firm but polite" vs. "empathetic" vs. "enthusiastic" require genuinely different vocabulary and rhythm that keyword checks cannot capture

**Why this matters:** Wrong tone is a professional failure regardless of factual accuracy.

---

### Metric 3: Professional Quality *(LLM-as-Judge)*

**Definition:** Overall email craft independent of tone.

**Logic:**
- LLM judge evaluates: grammar, logical structure, subject line, appropriate length, clear CTA
- Rates 1–10, normalized to 0.0–1.0
- Scored separately from tone so a casual email can still score high here

**Why this matters:** Correct tone and facts don't save an email with poor grammar, no subject line, or no clear next step.

---

## Model Comparison

| | Model A | Model B |
|---|---|---|
| **Model** | `mistral-large-latest` | `mistral-small-latest` |
| **Prompting** | Advanced (same) | Advanced (same) |
| **Positioning** | Higher capability, higher cost | Faster, lower cost |

Both models use identical prompts — isolating model capability as the single variable.

---

## Output Files

**`outputs/scores.csv`** — One row per scenario × model. Use for the comparative analysis.

**`outputs/results.json`** — Full results: metric definitions, generated emails, per-scenario scores, and overall averages in `summary`.

**`outputs/final_report.pdf`** — Final submission report (run `generate_pdf.py` to produce).

---

## Comparative Analysis Results

After running the batch evaluation:

| Metric | Model A (large) | Model B (small) | Winner |
|---|---|---|---|
| Fact Recall | 0.9000 | 0.9350 | Model B |
| Tone Accuracy | 0.9300 | 0.9100 | Model A |
| Professional Quality | 0.9000 | 0.9000 | Tie |
| **Overall Average** | **0.9100** | **0.9150** | **Model B** |

See `outputs/final_report.pdf` for the full comparative analysis.
