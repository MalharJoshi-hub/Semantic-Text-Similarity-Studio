"""
Curated Multi-Domain Datasets for Semantic Similarity & FAISS Retrieval.
Covers 4 critical enterprise domains:
1. Healthcare & Biomedicine
2. Legal & Compliance
3. Finance & FinTech
4. Software Engineering & Cloud Infrastructure
"""

DOMAIN_PACKS = {
    "healthcare": {
        "title": "Healthcare & Biomedicine",
        "badge_color": "#10b981",
        "document": {
            "label": "Clinical Cardiology & Pharmacotherapy Guidelines",
            "content": """# Overview of Hypertension and Cardiovascular Risk
Essential hypertension is a chronic elevation of systemic arterial pressure leading to increased risk of myocardial infarction, stroke, heart failure, and renal insufficiency.

# First-Line Pharmacotherapy: ACE Inhibitors and ARBs
Angiotensin-converting enzyme (ACE) inhibitors, such as lisinopril and enalapril, inhibit the conversion of angiotensin I to angiotensin II, reducing peripheral vascular resistance.
A hallmark adverse effect of ACE inhibitors is a persistent dry cough caused by the accumulation of bradykinin in the upper respiratory tract.
In patients experiencing bradykinin-mediated cough, Angiotensin Receptor Blockers (ARBs), such as losartan and valsartan, are recommended as first-line alternatives.

# Beta-Blockers and Calcium Channel Blockers
Beta-1 adrenergic receptor antagonists, such as metoprolol and carvedilol, reduce myocardial oxygen demand by decreasing heart rate and contractility.
Dihydropyridine calcium channel blockers, such as amlodipine, selectively relax vascular smooth muscle to induce systemic vasodilation."""
        },
        "presets": [
            {
                "name": "Clinical Paraphrase",
                "text1": "Myocardial infarction secondary to acute coronary artery thrombosis.",
                "text2": "Heart attack caused by sudden blood clot occlusion in the coronary vessel.",
                "expected": "Extremely High (>= 0.80)"
            },
            {
                "name": "Drug & Side Effect Correlation",
                "text1": "Patients taking lisinopril frequently report an intractable dry respiratory cough.",
                "text2": "ACE inhibitor therapy commonly induces dry cough due to bradykinin peptide accumulation.",
                "expected": "High (>= 0.70)"
            },
            {
                "name": "Contrasting Pharmacology",
                "text1": "Beta-blockers decrease myocardial oxygen demand by slowing heart rate and contractility.",
                "text2": "Inotropic sympathomimetics like epinephrine increase cardiac output and accelerate heart rate.",
                "expected": "Moderate / Divergent (0.45 - 0.65)"
            },
            {
                "name": "Cross-Domain Unrelated",
                "text1": "Dihydropyridine calcium channel blockers induce peripheral arterial vasodilation.",
                "text2": "The Kubernetes ingress controller routes external HTTP traffic to cluster service endpoints.",
                "expected": "Unrelated (< 0.25)"
            }
        ],
        "queries": [
            "ACE inhibitors adverse dry cough and bradykinin",
            "beta blockers reducing myocardial oxygen consumption",
            "essential hypertension cardiovascular risk and stroke"
        ]
    },

    "legal": {
        "title": "Legal & Compliance",
        "badge_color": "#818cf8",
        "document": {
            "label": "Master Cloud SaaS Agreement & Mutual NDA",
            "content": """# Confidentiality and Proprietary Information
Each party agrees that all code, trade secrets, business strategies, and technical architectures disclosed shall be held in strict confidence.
Neither party shall disclose Proprietary Information to third parties without prior written authorization from the disclosing party.
Confidentiality obligations shall survive termination of this Agreement for a period of five (5) consecutive years.

# Limitation of Liability and Consequential Damages
Except for gross negligence or willful misconduct, neither party shall be liable for indirect, incidental, special, or consequential damages.
The aggregate cumulative liability of either party arising out of or related to this Agreement shall not exceed the total fees paid during the preceding twelve months.

# Intellectual Property and Non-Assertion
Customer retains all right, title, and ownership in and to Customer Data uploaded to the hosted service.
Vendor retains all proprietary rights, copyright, and patent claims in the underlying software, APIs, and algorithmic documentation."""
        },
        "presets": [
            {
                "name": "Contractual Paraphrase",
                "text1": "Neither party shall disclose Proprietary Information without prior written authorization.",
                "text2": "Strict confidentiality must be maintained for proprietary materials absent express written consent.",
                "expected": "Extremely High (>= 0.80)"
            },
            {
                "name": "Liability Cap Agreement",
                "text1": "Total aggregate liability is strictly capped at the fees paid in the preceding twelve months.",
                "text2": "Damages recovered under this contract cannot exceed the cumulative subscription fees of the prior year.",
                "expected": "Extremely High (>= 0.80)"
            },
            {
                "name": "Uncapped vs Capped Liability",
                "text1": "Total liability is capped at the annual subscription amount paid by the customer.",
                "text2": "The supplier accepts unlimited, uncapped indemnification liability for all third-party intellectual property claims.",
                "expected": "Moderate / Opposing (0.45 - 0.65)"
            },
            {
                "name": "Cross-Domain Unrelated",
                "text1": "Confidentiality obligations shall survive contract termination for five consecutive years.",
                "text2": "Baking sourdough bread with steam maximizes oven spring and gelatinizes crust starches.",
                "expected": "Unrelated (< 0.25)"
            }
        ],
        "queries": [
            "limitation of aggregate liability and consequential damages",
            "confidentiality survival obligations after agreement termination",
            "customer data ownership and vendor intellectual property"
        ]
    },

    "finance": {
        "title": "Finance & FinTech",
        "badge_color": "#f59e0b",
        "document": {
            "label": "Central Banking, Monetary Policy & Inflation Dynamics",
            "content": """# Central Bank Mandate and Headline Inflation
The Federal Open Market Committee (FOMC) operates under a dual mandate to foster maximum employment and long-term price stability.
The benchmark inflation gauge is the Personal Consumption Expenditures (PCE) price index, with an annualized target of 2.0 percent.

# Interest Rate Decisions and Monetary Transmission
When core inflation exceeds sustainable thresholds, the central bank enacts benchmark interest rate increases to tighten credit conditions.
Higher policy rates increase the borrowing costs for commercial banks, cooling consumer discretionary demand and slowing business capital expenditures.

# Quantitative Tightening and Balance Sheet Normalization
In addition to policy rate adjustments, central banks utilize quantitative tightening (QT) by allowing maturing Treasury securities and mortgage-backed securities to roll off the balance sheet without reinvestment.
Quantitative tightening reduces excess reserves in the banking system, reinforcing the restrictive policy stance."""
        },
        "presets": [
            {
                "name": "Monetary Paraphrase",
                "text1": "The central bank enacted a 50 bps reduction in the federal funds rate.",
                "text2": "The monetary policy committee lowered the benchmark lending rate by half a percentage point.",
                "expected": "Extremely High (>= 0.80)"
            },
            {
                "name": "Inflation & Rate Hike",
                "text1": "Elevated core inflation compelled policymakers to raise benchmark borrowing costs.",
                "text2": "Rising consumer prices forced the central bank to tighten monetary policy via interest rate increases.",
                "expected": "High (>= 0.75)"
            },
            {
                "name": "Hawkish vs Dovish Divergence",
                "text1": "The committee aggressively raised interest rates to combat runaway consumer price inflation.",
                "text2": "The central bank expanded its quantitative easing purchases and slashed interest rates to zero.",
                "expected": "Moderate / Directional Contrast (0.50 - 0.68)"
            },
            {
                "name": "Cross-Domain Unrelated",
                "text1": "Quantitative tightening allows maturing Treasury securities to roll off the central bank balance sheet.",
                "text2": "Acute myocardial infarction requires emergency coronary angioplasty or thrombolytic therapy.",
                "expected": "Unrelated (< 0.25)"
            }
        ],
        "queries": [
            "interest rate hikes to combat headline PCE inflation",
            "quantitative tightening balance sheet asset runoff",
            "dual mandate price stability and maximum employment"
        ]
    },

    "software": {
        "title": "Software Engineering & DevOps",
        "badge_color": "#06b6d4",
        "document": {
            "label": "Kubernetes Cluster Architecture & Container Orchestration",
            "content": """# Kubernetes Control Plane Architecture
The Kubernetes control plane manages the global state of the cluster, detecting and responding to cluster events.
Key control plane components include the kube-apiserver, etcd, kube-scheduler, and kube-controller-manager.
The etcd database is a consistent, highly available distributed key-value store holding the complete declarative state of all cluster resources.

# Worker Node Architecture and Kubelet
Each worker node runs a container runtime, the kubelet agent, and kube-proxy.
The kubelet is the primary node agent that registers the node with the apiserver and ensures containers described in PodSpecs are running and healthy.

# Services, Ingress, and Network Routing
ClusterIP exposes the Service on a cluster-internal IP, making the service reachable only from within the cluster.
The Ingress controller provides application-layer (L7) HTTP and HTTPS routing from external traffic to internal services using host and path rules."""
        },
        "presets": [
            {
                "name": "DevOps Paraphrase",
                "text1": "The ingress controller routes external HTTP traffic to internal ClusterIP services.",
                "text2": "External web requests are directed to internal service endpoints by the cluster ingress gateway.",
                "expected": "Extremely High (>= 0.80)"
            },
            {
                "name": "Etcd & State Management",
                "text1": "Etcd serves as the distributed key-value store holding declarative cluster state.",
                "text2": "The complete configuration and state of the cluster is persisted in a distributed key-value datastore.",
                "expected": "High (>= 0.75)"
            },
            {
                "name": "Stateless vs Stateful Architecture",
                "text1": "Stateless microservices scale horizontally across worker nodes using Deployments and HPA.",
                "text2": "Stateful database clusters require dedicated persistent volume claims and stable network identities via StatefulSets.",
                "expected": "Moderate / Conceptual Contrast (0.50 - 0.68)"
            },
            {
                "name": "Cross-Domain Unrelated",
                "text1": "The kubelet monitors PodSpecs to ensure container runtimes maintain healthy workloads.",
                "text2": "The aggregate liability under this cloud contract shall not exceed fees paid in the prior twelve months.",
                "expected": "Unrelated (< 0.25)"
            }
        ],
        "queries": [
            "etcd distributed key-value store holding cluster state",
            "kubelet node agent ensuring pod container health",
            "ingress controller application layer L7 HTTP routing"
        ]
    }
}
