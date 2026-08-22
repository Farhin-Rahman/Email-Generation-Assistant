# Email Generation Assistant

An LLM-powered assistant for generating professional emails from structured inputs (intent, facts, tone) and for evaluating outputs with custom metrics. The project provides a FastAPI service for on-demand generation and a batch evaluation pipeline that compares two Mistral models using identical prompts and evaluation logic.

Project description
This repository demonstrates how to pair advanced prompting techniques (role-playing, few-shot examples, and an embedded chain-of-thought checklist) with deterministic and LLM-based evaluation metrics to produce and measure high-quality professional emails. It supports interactive use via a FastAPI server, batch evaluation across test scenarios, and a PDF report generator for summarizing results.
Environment
bash
cp .env.example .env
# Edit .env and set:
# MISTRAL_API_KEY=your_api_key_here
Install
bash
pip install -r requirements.txt
Run the API (development)

bash
uvicorn api:app --reload
Open the interactive docs: http://localhost:8000/docs

API endpoints

GET /health — liveness
POST /generate — generate an email
POST /evaluate — generate + score with all 3 metrics
Example: generate (curl)

bash
curl -s -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Follow up after sales meeting",
    "facts": ["Met on June 15", "Demo scheduled June 28", "Contact is Sarah Chen"],
    "tone": "Professional, warm",
    "model": "mistral-large-latest"
  }'
Example: evaluate (curl)

bash
curl -s -X POST "http://localhost:8000/evaluate" \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Follow up after sales meeting",
    "facts": ["Met on June 15", "Demo scheduled June 28", "Contact is Sarah Chen"],
    "tone": "Professional, warm",
    "model": "mistral-small-latest"
  }'
Batch evaluation

run_evaluation.py runs the provided scenarios in test_data.py against both models and writes results to outputs/.
bash
python run_evaluation.py
Expected runtime: several minutes (depends on API latency).

PDF report

Install fpdf2, then:
bash
pip install fpdf2
python generate_pdf.py
Generates outputs/final_report.pdf from results.

Docker

Start API:
bash
docker compose up api
Run batch evaluation:
bash
docker compose --profile evaluate run evaluate
Project layout

Code
email-assistant/
├── api.py                # FastAPI service (generate + evaluate endpoints)
├── generator.py          # Email generation with advanced prompting
├── evaluator.py          # 3 custom evaluation metrics and wrappers
├── test_data.py          # Test scenarios and human references
├── run_evaluation.py     # Batch runner — generates & evaluates scenarios
├── generate_pdf.py       # Produces outputs/final_report.pdf
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── outputs/              # Results, scores, and generated report
How it works (brief)

generator.py: Constructs a sophisticated system prompt that includes role-playing, few-shot examples, and an internal reasoning checklist; then calls the Mistral chat API to produce the email.
evaluator.py: Computes Fact Recall deterministically (keyword matching) and uses a smaller Mistral model as a judge for Tone Accuracy and Professional Quality; aggregates scores.
run_evaluation.py: Drives batch runs for model comparison and saves the results.
Configuration

MISTRAL_API_KEY (required)
All other configuration is environment-driven or in the scripts; see .env.example.
Extending & Development

Add more test scenarios in test_data.py to expand evaluation coverage.
Add alternative judge prompts or additional metrics (e.g., readability, sentiment).
Add CI workflows to run static checks and small smoke tests against a mocked client or in a staging environment.
Troubleshooting

Rate limits: code retries on 429 and waits — still expect long batch runtimes if throttled.
Missing API key: ensure MISTRAL_API_KEY is set in environment or .env.
Docker volumes: outputs are bind-mounted; ensure permission/ownership matches your host.
Contributing Contributions welcome. 

Acknowledgements

Built with Mistral LLMs and inspired by practical prompt-engineering and LLM evaluation best practices.
Author / Contact

Farhin Rahman — https://github.com/Farhin-Rahman
