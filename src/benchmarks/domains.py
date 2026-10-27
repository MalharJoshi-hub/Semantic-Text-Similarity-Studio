"""Enterprise multi-domain taxonomy, ground truth pairs, and benchmark suites."""

from typing import Dict, Any, List

ALL_DOMAINS: Dict[str, Dict[str, Any]] = {
    "legal": {
        "name": "Legal & Contract Law",
        "description": "Commercial liability, indemnification, and dispute resolution.",
        "pairs": [
            {
                "t1": "The contractor shall indemnify and hold harmless the client from third-party liabilities.",
                "t2": "The vendor agrees to defend and compensate the customer against all third-party damages and legal claims.",
                "expected_min": 0.50,
                "label": "Paraphrase: Indemnification"
            },
            {
                "t1": "Either party may terminate this agreement with thirty days written notice.",
                "t2": "This contract remains irrevocable and perpetual for five calendar years.",
                "expected_max": 0.45,
                "label": "Contradiction: Termination rights"
            }
        ],
        "queries": [
            "indemnity clauses and supplier legal liability",
            "jurisdiction and governing law arbitration rules"
        ]
    },
    "healthcare": {
        "name": "Healthcare & Clinical Medicine",
        "description": "Cardiology, diagnostics, pharmacology, and clinical treatment.",
        "pairs": [
            {
                "t1": "The patient exhibits acute myocardial infarction secondary to coronary artery thrombosis.",
                "t2": "The individual suffered a severe heart attack caused by a blood clot obstructing coronary blood flow.",
                "expected_min": 0.50,
                "label": "Paraphrase: Myocardial infarction"
            },
            {
                "t1": "Administer 500mg oral amoxicillin twice daily for bacterial pharyngitis.",
                "t2": "Surgical excision of the lumbar herniated disc was completed under general anesthesia.",
                "expected_max": 0.40,
                "label": "Distinct: Antibiotic therapy vs Spine surgery"
            }
        ],
        "queries": [
            "hypertension management and beta blocker dosing",
            "early symptoms of diabetic ketoacidosis in adults"
        ]
    },
    "finance": {
        "name": "Finance & Capital Markets",
        "description": "Equities, central bank monetary policy, hedging, and balance sheets.",
        "pairs": [
            {
                "t1": "The Federal Reserve elevated interest rates by 25 basis points to temper inflationary pressures.",
                "t2": "The US central bank raised its benchmark lending rate by a quarter point to counter rising prices.",
                "expected_min": 0.48,
                "label": "Paraphrase: Rate hike"
            },
            {
                "t1": "The hedge fund bought long call options to speculate on equity price appreciation.",
                "t2": "The company reported a severe net loss driven by write-downs of intangible goodwill.",
                "expected_max": 0.40,
                "label": "Divergent: Derivatives trading vs Earnings impairment"
            }
        ],
        "queries": [
            "treasury yield curve inversion and recession probability",
            "credit default swap pricing models and counterparty risk"
        ]
    },
    "cybersecurity": {
        "name": "Cybersecurity & Threat Intelligence",
        "description": "Vulnerability assessment, exploit vectors, cryptography, and zero-day defense.",
        "pairs": [
            {
                "t1": "An unauthenticated remote code execution vulnerability was discovered in the HTTP daemon.",
                "t2": "Attackers can execute arbitrary instructions without credentials via a flaw in the web server process.",
                "expected_min": 0.55,
                "label": "Paraphrase: RCE Vulnerability"
            },
            {
                "t1": "Enforce mandatory multi-factor authentication with hardware security keys.",
                "t2": "Database query optimization reduced p99 latency by fifty percent.",
                "expected_max": 0.35,
                "label": "Unrelated: MFA vs DB optimization"
            }
        ],
        "queries": [
            "mitigating cross-site request forgery in REST APIs",
            "zero trust architecture identity segmentation"
        ]
    },
    "devops": {
        "name": "Cloud Architecture & DevOps",
        "description": "Container orchestration, CI/CD pipelines, autoscaling, and telemetry.",
        "pairs": [
            {
                "t1": "The Kubernetes cluster autoscaler provisions additional compute worker nodes when CPU requests exceed limits.",
                "t2": "When cluster node resource utilization spikes, Kubernetes automatically scales out cloud virtual machines.",
                "expected_min": 0.60,
                "label": "Paraphrase: K8s autoscaling"
            },
            {
                "t1": "Deploy Docker container images to Amazon Elastic Container Registry via GitHub Actions.",
                "t2": "Employees must submit expense reimbursement forms prior to end of month.",
                "expected_max": 0.30,
                "label": "Unrelated: CI/CD vs Expense policy"
            }
        ],
        "queries": [
            "blue green deployment strategy on cloud platforms",
            "prometheus metric scraping intervals and alertmanager rules"
        ]
    },
    "academic": {
        "name": "Academic & Scientific Publishing",
        "description": "Peer review, experimental methodology, and statistical validation.",
        "pairs": [
            {
                "t1": "Empirical results demonstrate a statistically significant reduction in latency (p < 0.001).",
                "t2": "Experimental measurements confirm a significant drop in response delay with high statistical confidence.",
                "expected_min": 0.55,
                "label": "Paraphrase: Statistical significance"
            },
            {
                "t1": "The double-blind clinical trial randomized participants into four parallel cohorts.",
                "t2": "The quarterly marketing campaign launched across social media channels.",
                "expected_max": 0.30,
                "label": "Unrelated: Trial design vs Marketing campaign"
            }
        ],
        "queries": [
            "methodology section sample size determination",
            "literature review citation formatting and bibliography"
        ]
    },
    "customer_support": {
        "name": "Customer Support & Service Desk",
        "description": "Troubleshooting, refunds, SLA management, and ticket escalation.",
        "pairs": [
            {
                "t1": "My account was billed twice for the annual subscription; please issue a refund.",
                "t2": "I was charged duplicate amounts for my yearly membership and need reimbursement.",
                "expected_min": 0.60,
                "label": "Paraphrase: Duplicate charge refund"
            },
            {
                "t1": "How do I reset my password if I lost access to my recovery email?",
                "t2": "Our enterprise sales team offers custom volume discount agreements.",
                "expected_max": 0.35,
                "label": "Unrelated: Password reset vs Enterprise sales"
            }
        ],
        "queries": [
            "return merchandise authorization procedure",
            "troubleshooting mobile app login connection failures"
        ]
    },
    "ecommerce": {
        "name": "E-Commerce & Digital Retail",
        "description": "Product catalogs, fulfillment, cart checkout, and payment gateways.",
        "pairs": [
            {
                "t1": "Customers who spend over fifty dollars qualify for complimentary two-day expedited shipping.",
                "t2": "Free two-day delivery is automatically applied to orders with a subtotal exceeding $50.",
                "expected_min": 0.60,
                "label": "Paraphrase: Free shipping threshold"
            },
            {
                "t1": "Add item to shopping bag and proceed to secure credit card payment.",
                "t2": "The factory installed a new hydraulic cooling pump on assembly line 3.",
                "expected_max": 0.25,
                "label": "Unrelated: Checkout vs Factory maintenance"
            }
        ],
        "queries": [
            "inventory tracking and low stock reorder thresholds",
            "stripe payment gateway webhook error codes"
        ]
    },
    "aerospace": {
        "name": "Aerospace & Avionics",
        "description": "Propulsion, flight control systems, orbital mechanics, and aerodynamics.",
        "pairs": [
            {
                "t1": "The fly-by-wire flight control system utilizes triple-redundant hydraulic actuators.",
                "t2": "Aircraft control surfaces are managed by three backup hydraulic systems coordinated via fly-by-wire.",
                "expected_min": 0.60,
                "label": "Paraphrase: Flight controls"
            },
            {
                "t1": "Specific impulse of the liquid rocket engine exceeds 450 seconds in vacuum.",
                "t2": "Retail store employees must wear name badges during customer facing shifts.",
                "expected_max": 0.20,
                "label": "Unrelated: Rocket engine vs Retail dress code"
            }
        ],
        "queries": [
            "wing tip vortex drag reduction winglet designs",
            "geostationary transfer orbit apogee burn velocity delta"
        ]
    },
    "biotech": {
        "name": "Biotechnology & Genetics",
        "description": "CRISPR gene editing, recombinant DNA, proteomics, and monoclonal antibodies.",
        "pairs": [
            {
                "t1": "CRISPR-Cas9 endonuclease creates targeted double-stranded breaks in the genomic DNA.",
                "t2": "The Cas9 enzyme induces precise double-strand DNA cleavage at specific sequence loci.",
                "expected_min": 0.55,
                "label": "Paraphrase: CRISPR DNA cleavage"
            },
            {
                "t1": "Purification of the recombinant human monoclonal antibody was performed using protein A chromatography.",
                "t2": "The corporate treasury invested cash balances in short term commercial paper.",
                "expected_max": 0.20,
                "label": "Unrelated: Protein purification vs Commercial paper"
            }
        ],
        "queries": [
            "messenger RNA vaccine lipid nanoparticle formulation",
            "polymerase chain reaction thermal cycling denaturation steps"
        ]
    },
    "human_resources": {
        "name": "Human Resources & Talent Acquisition",
        "description": "Employee benefits, talent recruitment, onboarding, and performance appraisal.",
        "pairs": [
            {
                "t1": "Full-time team members receive four weeks of paid vacation and comprehensive medical insurance.",
                "t2": "Permanent staff members are entitled to twenty days paid annual leave plus healthcare benefits.",
                "expected_min": 0.48,
                "label": "Paraphrase: Employee benefits"
            },
            {
                "t1": "Conduct annual 360-degree performance reviews for engineering department managers.",
                "t2": "Configure network subnet routing tables on the gateway router.",
                "expected_max": 0.25,
                "label": "Unrelated: Performance review vs Router subnet"
            }
        ],
        "queries": [
            "standard operating procedure for employee voluntary resignation",
            "diversity equity and inclusion workplace training programs"
        ]
    },
    "education": {
        "name": "Education & Pedagogical Technology",
        "description": "Curriculum design, formative assessment, learning management, and student outcomes.",
        "pairs": [
            {
                "t1": "Formative assessments throughout the semester assist instructors in adjusting pedagogical approaches.",
                "t2": "Continuous ongoing quizzes allow teachers to identify student learning deficits and modify lesson plans.",
                "expected_min": 0.42,
                "label": "Paraphrase: Formative assessment"
            },
            {
                "t1": "Students enrolled in introductory calculus completed problem sets on integration.",
                "t2": "The offshore oil drilling platform initiated deep water extraction operations.",
                "expected_max": 0.20,
                "label": "Unrelated: Calculus vs Oil drilling"
            }
        ],
        "queries": [
            "blended asynchronous classroom engagement methodologies",
            "rubrics for assessing peer evaluated collaborative research projects"
        ]
    },
    "patents": {
        "name": "Patents & Intellectual Property",
        "description": "Prior art search, patent claims, patentability, and infringement.",
        "pairs": [
            {
                "t1": "The independent claim specifies an apparatus comprising a sensor array coupled to an embedded controller.",
                "t2": "Claim 1 recites a device containing multiple sensor units communicating with an on-board microprocessor.",
                "expected_min": 0.55,
                "label": "Paraphrase: Patent independent claim"
            },
            {
                "t1": "A patent search revealed invalidating prior art published three years before the priority date.",
                "t2": "The school cafeteria menu features vegetarian lasagna every Tuesday.",
                "expected_max": 0.20,
                "label": "Unrelated: Prior art vs Cafeteria menu"
            }
        ],
        "queries": [
            "doctrine of equivalents in patent infringement litigation",
            "patent cooperation treaty international filing phase deadlines"
        ]
    },
    "philosophy": {
        "name": "Philosophy & Epistemology",
        "description": "Logic, metaphysics, ethics, epistemology, and phenomenology.",
        "pairs": [
            {
                "t1": "Epistemological skepticism questions whether justified true belief is achievable by human cognition.",
                "t2": "Skeptical philosophy doubts whether humanity can ever attain certain, verifiable knowledge of reality.",
                "expected_min": 0.60,
                "label": "Paraphrase: Epistemic skepticism"
            },
            {
                "t1": "Utilitarian ethics asserts that moral goodness is defined by maximizing aggregate happiness.",
                "t2": "Replace worn brake pads on the front rotor assembly of the vehicle.",
                "expected_max": 0.20,
                "label": "Unrelated: Utilitarianism vs Brake pad replacement"
            }
        ],
        "queries": [
            "kantian categorical imperative versus consequentialist ethical frameworks",
            "mind body dualism and the hard problem of consciousness"
        ]
    },
    "news": {
        "name": "Journalism & Media",
        "description": "Editorial standards, investigative reporting, headline synthesis, and news feeds.",
        "pairs": [
            {
                "t1": "Heavy precipitation caused widespread river flooding and prompted mandatory municipal evacuations.",
                "t2": "Torrential downpours led rivers to breach their banks, forcing city authorities to order evacuations.",
                "expected_min": 0.60,
                "label": "Paraphrase: Flood evacuations"
            },
            {
                "t1": "The foreign minister delivered a televised address discussing bilateral trade agreements.",
                "t2": "Mix two cups of flour with baking powder and room temperature butter.",
                "expected_max": 0.20,
                "label": "Unrelated: Foreign policy vs Baking recipe"
            }
        ],
        "queries": [
            "investigative reporting guidelines for protecting anonymous sources",
            "breaking news coverage verification protocols during natural disasters"
        ]
    }
}


def get_domain_definition(domain_key: str) -> Dict[str, Any]:
    """Retrieve domain configuration by key."""
    if domain_key not in ALL_DOMAINS:
        raise KeyError(f"Domain '{domain_key}' is not defined. Available: {list(ALL_DOMAINS.keys())}")
    return ALL_DOMAINS[domain_key]
