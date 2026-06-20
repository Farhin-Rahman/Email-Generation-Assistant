SCENARIOS = [
    {
        "id": 1,
        "intent": "Follow up on a sales meeting with a potential enterprise client",
        "facts": [
            "Met with Acme Corp on June 15",
            "Discussed upgrading their legacy CRM system",
            "Demo scheduled for June 28 at 10am",
            "Primary contact is Sarah Chen, VP of Operations",
            "Their budget cycle closes at end of Q3",
        ],
        "tone": "Professional, warm",
        "human_reference": """Subject: Great Meeting – Looking Forward to the Demo on June 28

Dear Sarah,

Thank you for taking the time to meet with us on June 15. It was a genuine pleasure discussing how a CRM upgrade could benefit Acme Corp's operations.

I'm looking forward to the demo on June 28 at 10:00 AM, where I'll be able to show you exactly how the platform addresses the friction points we talked about. With your Q3 budget cycle closing soon, I want to make sure you have everything you need to evaluate this comfortably ahead of that deadline.

If there's anything useful I can send over before the 28th — case studies, technical specs, pricing breakdowns — just say the word.

Looking forward to connecting again.

Best regards,
[Your Name]""",
    },
    {
        "id": 2,
        "intent": "Apply for a Senior Data Scientist position",
        "facts": [
            "Position ID: DS-2024-089",
            "5 years of ML/AI experience at fintech companies",
            "Built a fraud detection model that saved $2.1M annually",
            "Proficient in Python, PyTorch, and AWS SageMaker",
            "Available to start July 14",
        ],
        "tone": "Confident, formal",
        "human_reference": """Subject: Application for Senior Data Scientist – DS-2024-089

Dear Hiring Team,

I am writing to apply for the Senior Data Scientist position (DS-2024-089). With five years of machine learning experience at fintech companies, I am confident I can contribute meaningfully from day one.

In my most recent role, I designed and deployed a fraud detection model that reduced annual losses by $2.1 million — a result achieved by combining rigorous feature engineering with real-time production constraints. I work primarily in Python with PyTorch and AWS SageMaker and am comfortable owning the full pipeline from experimentation through to deployment.

I am available to start July 14 and would welcome the opportunity to discuss how my background aligns with your team's goals.

Thank you for your time and consideration.

Sincerely,
[Your Name]""",
    },
    {
        "id": 3,
        "intent": "Respond to a customer complaint about a delayed shipment",
        "facts": [
            "Customer name: Mr. David Park",
            "Order number: #45892",
            "Shipment delayed due to warehouse flooding",
            "New estimated delivery date: June 30",
            "Offering 20% discount on next order as compensation",
        ],
        "tone": "Empathetic, apologetic",
        "human_reference": """Subject: Our Sincere Apologies Regarding Order #45892

Dear Mr. Park,

I want to personally apologize for the delay with your order #45892. This is not the experience we aim to provide, and I completely understand your frustration.

The delay was caused by unexpected flooding at our fulfillment warehouse, which disrupted our shipping operations. I can confirm that your order is now on track, with a revised delivery date of June 30.

To acknowledge the inconvenience this has caused you, we'd like to offer a 20% discount on your next order — a small gesture, but one we hope shows how seriously we take this.

Thank you for your patience, Mr. Park. Please don't hesitate to reach out if you have any questions in the meantime.

Sincerely,
[Your Name]
Customer Support""",
    },
    {
        "id": 4,
        "intent": "Send a weekly project status update to stakeholders",
        "facts": [
            "Project: Website Redesign for GlobalBank",
            "Overall progress: 60% complete",
            "Completed: Homepage, About, and Services pages",
            "In progress: Blog section and Contact form",
            "Launch target: August 1",
            "Blocker: Need final copy from marketing team by July 5",
        ],
        "tone": "Professional, clear, informative",
        "human_reference": """Subject: Website Redesign – Weekly Status Update

Hi Team,

Here's this week's update on the GlobalBank website redesign.

We are currently at 60% completion. The homepage, About, and Services pages have been finalized and approved. The development team is now focused on the blog section and contact form.

We remain on track for an August 1 launch, with one key dependency: final copy from the marketing team is needed by July 5. A delay past that date would put the launch timeline at risk.

Please flag any concerns or questions and I'll address them before the next update.

Best,
[Your Name]""",
    },
    {
        "id": 5,
        "intent": "Request a meeting to get budget approval for software licenses",
        "facts": [
            "Three pending software licenses need sign-off: Salesforce, Figma Enterprise, DataDog",
            "Total budget request: $48,000",
            "Commitment deadline with vendors: June 25",
            "Requesting a 30-minute meeting on June 22 or 23 at 2:00 PM",
        ],
        "tone": "Direct, professional, concise",
        "human_reference": """Subject: 30-Min Budget Approval Needed Before June 25 – Software Licenses

Hi [Name],

I need your sign-off on three software licenses — Salesforce, Figma Enterprise, and DataDog — before our vendor commitment deadline of June 25. The total ask is $48,000.

Could we find 30 minutes on June 22 or 23 at 2:00 PM? I'll have the full breakdown and business case ready and can walk you through everything quickly.

Let me know which day works.

Thank you,
[Your Name]""",
    },
    {
        "id": 6,
        "intent": "Announce a new product launch to existing customers",
        "facts": [
            "Product name: DataPulse Pro",
            "Launch date: July 1",
            "Key new features: AI-powered analytics dashboard, real-time alerts, team collaboration workspace",
            "Existing customers get 40% early-bird discount, expires June 28",
            "Sign-up link: datapulse.io/pro",
        ],
        "tone": "Enthusiastic, exciting, friendly",
        "human_reference": """Subject: You're First in Line for DataPulse Pro – 40% Off Inside

Hi [First Name],

We've been working on something big, and we're excited to share it with you first.

DataPulse Pro launches on July 1, and it's our most powerful product to date. Here's what's new:

• AI-powered analytics dashboard
• Real-time alerts and monitoring
• Team collaboration workspace

As one of our existing customers, you get exclusive early-bird pricing: 40% off — but only until June 28.

Claim your discount now at datapulse.io/pro.

We can't wait for you to try it.

The DataPulse Team""",
    },
    {
        "id": 7,
        "intent": "Send a first payment reminder for an overdue invoice",
        "facts": [
            "Invoice number: INV-2024-089",
            "Amount due: $4,750.00",
            "Original due date: June 1 (now 20 days overdue)",
            "Payment accepted via bank transfer or online portal",
            "Payment portal: payments.ourcompany.com",
        ],
        "tone": "Firm but polite, professional",
        "human_reference": """Subject: Payment Reminder – Invoice INV-2024-089 ($4,750.00 Overdue)

Dear [Name],

I'm following up on invoice INV-2024-089 for $4,750.00, which was due on June 1 and remains outstanding — now 20 days past due.

If payment has already been sent, please disregard this message. If not, we'd appreciate settlement at your earliest convenience.

You can pay securely via bank transfer or through our online portal at payments.ourcompany.com.

Please reach out if you have any questions about the invoice or would like to discuss payment arrangements.

Best regards,
[Your Name]
Accounts Receivable""",
    },
    {
        "id": 8,
        "intent": "Send a thank you email after a job interview",
        "facts": [
            "Interviewed for: Senior Product Manager role",
            "Interviewer: Jennifer Walsh, Head of Product",
            "Key discussion: 2025 mobile app roadmap",
            "I proposed the 'progressive onboarding' feature concept during the interview",
            "Interview took place today, June 20",
        ],
        "tone": "Warm, enthusiastic, professional",
        "human_reference": """Subject: Thank You – Senior Product Manager Interview

Dear Jennifer,

Thank you for meeting with me today to discuss the Senior Product Manager role. I came away from our conversation genuinely energized about the opportunity.

I particularly enjoyed our discussion around the 2025 mobile app roadmap — it gave me a clear picture of the challenges ahead and how much impact this role can have. I hope the progressive onboarding concept I proposed sparked some useful thinking; I'd be happy to elaborate further if it would be helpful.

The culture you described came through clearly in our conversation, and it's exactly the kind of environment where I do my best work.

Thank you again for your time, Jennifer. I look forward to hearing about next steps.

Warm regards,
[Your Name]""",
    },
    {
        "id": 9,
        "intent": "Propose a co-marketing partnership to a complementary business",
        "facts": [
            "Target company: GreenTech Solutions",
            "Proposing a joint 3-part webinar series on sustainable enterprise technology",
            "Both companies target mid-market B2B clients with significant audience overlap",
            "Lead sharing model: 50/50 split",
            "Proposing a 90-day pilot program starting in August",
        ],
        "tone": "Persuasive, professional, collaborative",
        "human_reference": """Subject: Partnership Opportunity: Joint Webinar Series on Sustainable Enterprise Tech

Dear GreenTech Solutions Team,

I'm reaching out because I see a strong opportunity for our two companies to create something meaningful together.

We serve many of the same mid-market B2B clients, and there's clear alignment in how we approach the sustainable technology conversation. I'd like to propose a joint 3-part webinar series on sustainable enterprise tech — a topic our shared audiences are actively seeking guidance on.

My suggested structure: co-host three sessions over 90 days beginning in August, with a 50/50 lead-sharing model. A defined pilot keeps the commitment manageable and gives us both a chance to measure ROI before deciding on next steps.

I'd love to connect for 20 minutes to explore whether this fits your goals. Would any time next week work?

Looking forward to hearing your thoughts.

Best,
[Your Name]""",
    },
    {
        "id": 10,
        "intent": "Apologize to enterprise clients for an unexpected platform outage",
        "facts": [
            "Outage duration: 4 hours (2:00 AM to 6:00 AM EST, June 18)",
            "Root cause: failed database migration script",
            "All services fully restored at 6:00 AM EST",
            "Preventive measures taken: automated rollback and enhanced monitoring implemented",
            "Compensation: one month of service credit applied to all affected accounts",
        ],
        "tone": "Apologetic, accountable, transparent",
        "human_reference": """Subject: Apology and Full Transparency on Yesterday's Service Interruption

Dear [Client Name],

I want to personally apologize for the service interruption our platform experienced on June 18, from 2:00 AM to 6:00 AM EST.

The outage was caused by a failed database migration script. Our engineering team identified and resolved the issue within four hours, and all services were fully restored by 6:00 AM EST. I want to be transparent: this was an error on our end, and we own it.

In response, we have implemented automated rollback procedures and significantly enhanced our monitoring to prevent a recurrence. We have also applied one full month of service credit to your account.

A complete root cause analysis report is available on request if you would like the full technical detail.

You expect consistent, reliable service from us — this incident fell short of that standard, and we are committed to earning back your confidence.

Sincerely,
[Your Name]""",
    },
]
