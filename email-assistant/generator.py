"""
Email generation using two advanced prompting techniques:

1. Role-Playing: The system prompt casts the model as an expert professional
   email copywriter with a defined identity and track record. This primes the
   model to apply domain expertise rather than producing generic output.

2. Few-Shot Prompting: Two complete input→output examples are prepended to
   every user message. This anchors the model to the expected format (subject
   line, greeting, body, CTA, close) and demonstrates how facts should be
   woven into the narrative rather than listed.

3. Chain-of-Thought (embedded): The system prompt includes an explicit
   internal reasoning checklist the model should apply before drafting.
   This nudges the model to reason about goal, tone, fact integration, and
   CTA before generating — improving consistency on all three metrics.
"""

import os
import time
from mistralai.client import Mistral
from mistralai.client.errors.sdkerror import SDKError

_client = None

def _get_client():
    global _client
    if _client is None:
        _client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    return _client

# ── Prompts ────────────────────────────────────────────────────────────────────

SYSTEM_ADVANCED = """You are an expert professional email copywriter with 15+ years of experience crafting high-impact business communications across industries. Your writing is valued for precision, appropriate tone calibration, and seamless integration of facts into natural prose.

Before drafting any email, work through these steps internally:
1. What is the single goal this email must accomplish?
2. How does the requested tone shape word choice, sentence length, and the opening line?
3. How can each fact be woven naturally into the narrative — not listed, but integrated?
4. What is the one specific action the reader should take, and how do I make it easy?

Always produce: a subject line, greeting, body paragraphs, a clear call-to-action, and a professional closing."""

FEW_SHOT_PREFIX = """Here are two examples of the expected format:

--- EXAMPLE 1 ---
INPUT:
Intent: Introduce myself as the new account manager
Key Facts:
- My name is Alex Rivera
- Taking over from James Park who retired
- Have been briefed on their account: Northgate Healthcare, 3-year client
- First call scheduled for June 10 at 3pm EST
Tone: Warm, professional

OUTPUT:
Subject: Your New Account Manager – Let's Connect

Dear Northgate Healthcare Team,

I wanted to take a moment to introduce myself. My name is Alex Rivera, and I'll be your dedicated account manager going forward, stepping in for James Park, who has recently retired after a distinguished career.

I've already been fully briefed on your account and I'm genuinely excited to continue the strong partnership you've built over the past three years. My priority is making this transition completely seamless for your team.

I have a call scheduled for June 10 at 3:00 PM EST and look forward to connecting then. In the meantime, please don't hesitate to reach out with any questions or immediate needs.

Warm regards,
Alex Rivera
Account Manager

--- EXAMPLE 2 ---
INPUT:
Intent: Decline a vendor proposal
Key Facts:
- Vendor is Apex Supplies
- Pricing was 30% above our budget
- Proposed timeline of 6 months was too long for our needs
- We may revisit in Q1 next year
Tone: Respectful, direct

OUTPUT:
Subject: Re: Proposal from Apex Supplies

Dear Apex Supplies Team,

Thank you for the time and detail you invested in your proposal. After careful review, we've decided not to move forward at this time.

Two factors drove our decision: the proposed pricing came in approximately 30% above our current budget, and the 6-month delivery timeline doesn't align with our project schedule.

We genuinely appreciated the quality of your submission and would be open to revisiting this in Q1 of next year if circumstances allow. We'll be in touch if that opportunity arises.

Thank you again for your time.

Best regards,
[Your Name]

--- END EXAMPLES ---

Now generate an email for the following:

"""


def generate_email(intent: str, facts: list[str], tone: str, model: str) -> str:
    facts_str = "\n".join(f"- {f}" for f in facts)
    user_message = (
        FEW_SHOT_PREFIX
        + f"Intent: {intent}\nKey Facts:\n{facts_str}\nTone: {tone}\n\nOUTPUT:"
    )
    for attempt in range(3):
        try:
            response = _get_client().chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_ADVANCED},
                    {"role": "user", "content": user_message},
                ],
                max_tokens=900,
            )
            return response.choices[0].message.content.strip()
        except SDKError as e:
            if e.raw_response.status_code == 429 and attempt < 2:
                print(f" rate limit, waiting 60s...", end=" ", flush=True)
                time.sleep(60)
            else:
                raise
