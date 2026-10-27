"""Enterprise Multi-Domain Dataset Matrix and Knowledge Base.

Contains verified domain documents, evaluation queries, and test assertions
across 15 industry verticals for code licensing and automated benchmarks.
"""

from typing import Dict, Any, List

ENTERPRISE_DOMAIN_DATA: Dict[str, Dict[str, Any]] = {
    "legal_contracts": {
        "domain": "Legal & Corporate Law",
        "description": "Standard clauses, commercial liability, indemnification, and dispute resolution.",
        "documents": [
            {
                "id": "leg_doc_01",
                "title": "Master Software and Services Licensing Agreement",
                "content": """# Master Software and Services Licensing Agreement

## 1. Definitions and Interpretations
In this Agreement, unless the context otherwise requires, the following terms shall have the respective meanings assigned to them:
- 'Authorized Users' means employees, contractors, and agents of Licensee authorized to access the Software.
- 'Confidential Information' means proprietary technical, financial, and operational data disclosed by either Party.
- 'Effective Date' means the date on which this Agreement is executed by the authorized signatories of both Parties.
- 'Intellectual Property Rights' includes patents, copyrights, trade secrets, trademarks, and all corresponding sui generis rights worldwide.

## 2. Grant of License and Scope of Usage
Subject to the terms and conditions of this Agreement, Licensor hereby grants Licensee a non-exclusive, non-transferable, worldwide license to install, execute, and display the Software solely for Licensee's internal business operations.
Licensee shall not sub-license, rent, lease, or distribute the Software to any third party without express prior written consent.
Reverse engineering, decompilation, or disassembly of the compiled binary objects is strictly prohibited except to the extent permitted by mandatory statutory law.

## 3. Representations, Warranties, and Disclaimers
Licensor warrants that for a period of ninety (90) days from delivery, the Software will conform in all material respects with the published documentation.
Except as expressly provided herein, the Software is provided on an 'AS IS' basis without warranties of merchantability or fitness for a particular purpose.

## 4. Indemnification and Limitation of Liability
Licensor agrees to defend, indemnify, and hold harmless Licensee from and against any third-party claims alleging that the Software infringes any valid patent or copyright.
In no event shall either party's aggregate liability exceed the total fees paid under this Agreement during the preceding twelve (12) month period.

## 5. Governing Law and Arbitration
This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, without regard to conflicts of law principles.
Any dispute arising hereunder shall be settled by binding arbitration administered by the American Arbitration Association.
"""
            },
            {
                "id": "leg_doc_02",
                "title": "Non-Disclosure and Confidentiality Undertaking",
                "content": """# Non-Disclosure and Confidentiality Undertaking

## 1. Scope of Confidential Information
Each party anticipates receiving non-public proprietary technical, business, and commercial information from the other party.
Confidential Information includes source code, architectural schematics, customer lists, pricing structures, and unreleased product roadmaps.

## 2. Standard of Care and Non-Use Obligations
The Receiving Party shall exercise the same degree of care to protect Confidential Information as it uses to protect its own sensitive data, but no less than reasonable care.
The Receiving Party shall not disclose, disseminate, or copy any Confidential Information to third parties without prior authorization.

## 3. Exceptions and Exclusions
The confidentiality obligations do not apply to information that:
- Is or becomes publicly known through no breach by the Receiving Party;
- Was already in the rightful possession of the Receiving Party prior to disclosure;
- Is independently developed by the Receiving Party without reference to the Disclosing Party's Confidential Information.

## 4. Term and Destruction of Materials
The obligations under this Agreement shall endure for a period of five (5) years following the Effective Date.
Upon written request, the Receiving Party shall certify the complete destruction or return of all tangible copies of Confidential Information.
"""
            }
        ]
    },
    "healthcare_clinical": {
        "domain": "Healthcare & Clinical Medicine",
        "description": "Cardiology, diagnostics, pharmacotherapy, and emergency clinical pathways.",
        "documents": [
            {
                "id": "health_doc_01",
                "title": "Clinical Practice Guideline: Acute Myocardial Infarction",
                "content": """# Clinical Practice Guideline: Acute Myocardial Infarction

## 1. Diagnostic Criteria and Initial Assessment
Acute myocardial infarction (AMI) is characterized by acute myocardial injury with clinical evidence of acute myocardial ischemia.
Diagnosis requires a rise and/or fall of cardiac troponin (cTn) with at least one value above the 99th percentile upper reference limit.
Concomitant findings must include at least one of the following:
- Symptoms of acute myocardial ischemia including retrosternal chest pressure radiating to the left arm or jaw;
- New ischemic electrocardiographic changes (ST-segment elevation or depression, new left bundle branch block);
- Development of pathological Q waves on 12-lead electrocardiography;
- Imaging evidence of new loss of viable myocardium or new regional wall motion abnormality.

## 2. Immediate Pharmacotherapy Protocol
Upon presentation, patients with suspected ST-elevation myocardial infarction (STEMI) should immediately receive:
- Chewable non-enteric coated aspirin (162 to 325 mg orally);
- Sublingual nitroglycerin (0.4 mg every 5 minutes up to three doses, if systolic blood pressure exceeds 100 mmHg);
- Supplemental oxygen therapy only if arterial oxygen saturation drops below 90%;
- Loading dose of a P2Y12 platelet inhibitor (ticagrelor 180 mg or prasugrel 60 mg).

## 3. Reperfusion Strategy Selection
Primary percutaneous coronary intervention (PCI) is the preferred reperfusion strategy when performed within 90 minutes of first medical contact.
If anticipated transfer time to a PCI-capable facility exceeds 120 minutes, intravenous fibrinolytic therapy (tenecteplase) must be administered within 30 minutes of diagnosis.
"""
            },
            {
                "id": "health_doc_02",
                "title": "Management Protocol: Adult Diabetic Ketoacidosis",
                "content": """# Management Protocol: Adult Diabetic Ketoacidosis

## 1. Pathophysiology and Triage
Diabetic ketoacidosis (DKA) results from absolute or relative insulin deficiency combined with counter-regulatory hormone excess.
Laboratory criteria for diagnosis include serum glucose > 250 mg/dL, arterial pH < 7.30, serum bicarbonate < 18 mEq/L, and elevated serum beta-hydroxybutyrate.

## 2. Fluid Resuscitation and Electrolyte Correction
Initial intravenous fluid therapy consists of 0.9% isotonic saline at 1000 mL/hour for the first 1 to 2 hours.
Potassium replacement must begin as soon as serum potassium is below 5.2 mEq/L to prevent fatal hypokalemic cardiac arrhythmias.
Insulin therapy must be withheld if serum potassium is below 3.3 mEq/L until hypokalemia is corrected.

## 3. Continuous Insulin Infusion Protocol
Administer regular insulin as a continuous intravenous infusion at 0.1 units/kg/hour.
When blood glucose falls below 200 mg/dL, add 5% dextrose to intravenous fluids while continuing insulin to clear ketoacidosis.
Resolution criteria include blood glucose < 200 mg/dL, serum bicarbonate >= 18 mEq/L, and venous pH > 7.30.
"""
            }
        ]
    },
    "finance_markets": {
        "domain": "Finance & Quantitative Asset Management",
        "description": "Equities, monetary policy, derivatives pricing, and balance sheet risk.",
        "documents": [
            {
                "id": "fin_doc_01",
                "title": "Federal Reserve Monetary Policy & Interest Rate Transmission",
                "content": """# Federal Reserve Monetary Policy & Interest Rate Transmission

## 1. The Dual Mandate and Policy Framework
The Federal Open Market Committee (FOMC) conducts monetary policy to foster maximum employment and long-run price stability.
The statutory target is anchored to a 2 percent annual inflation rate as measured by the Personal Consumption Expenditures (PCE) price index.

## 2. Policy Transmission Mechanisms
The primary policy lever is the target range for the federal funds rate, which influences commercial lending rates through several channels:
- Interest Rate Channel: Higher policy rates increase borrowing costs for capital expenditures and mortgages, reducing aggregate demand.
- Asset Price Channel: Rising discount rates suppress equity valuations and corporate bond prices, exerting a negative wealth effect.
- Exchange Rate Channel: Relative interest rate differentials alter capital flows, impacting the foreign exchange value of the US dollar.

## 3. Quantitative Easing and Balance Sheet Normalization
In addition to short-term interest rate adjustments, large-scale asset purchases (LSAPs) expand the Federal Reserve balance sheet to compress term premiums on longer-duration securities.
During balance sheet normalization (quantitative tightening), the Federal Reserve caps reinvestments of maturing Treasuries and agency debt.
"""
            },
            {
                "id": "fin_doc_02",
                "title": "Black-Scholes-Merton Derivatives Pricing Model",
                "content": """# Black-Scholes-Merton Derivatives Pricing Model

## 1. Fundamental Assumptions
The Black-Scholes-Merton (BSM) framework models the price dynamics of European-style options under the following ideal conditions:
- The underlying asset price follows a geometric Brownian motion with constant drift and volatility;
- No transaction costs, taxes, or bid-ask friction in trading the underlying asset or bond;
- The risk-free interest rate remains constant across all maturities;
- Short selling of securities is permitted with continuous trading.

## 2. The Partial Differential Equation
The Black-Scholes PDE governs the fair value V of an option as a function of asset price S and time t:
d V / d t + 0.5 * sigma^2 * S^2 * (d^2 V / d S^2) + r * S * (d V / d S) - r * V = 0

## 3. The Greeks and Risk Hedging
Option sensitivity metrics quantify exposure to underlying parameter variations:
- Delta (dV/dS): Hedge ratio representing change in option price per dollar move in underlying.
- Gamma (d^2V/dS^2): Convexity measure capturing rate of change of Delta.
- Vega (dV/d_sigma): Sensitivity of option value to shifts in implied volatility.
- Theta (dV/dt): Time decay rate indicating value erosion as maturity nears.
"""
            }
        ]
    },
    "cybersecurity_defense": {
        "domain": "Cybersecurity & Incident Response",
        "description": "Threat modeling, exploit mitigation, zero-trust, and cryptography.",
        "documents": [
            {
                "id": "cyber_doc_01",
                "title": "Zero Trust Enterprise Architecture Implementation",
                "content": """# Zero Trust Enterprise Architecture Implementation

## 1. Core Paradigm and Principles
Zero Trust Architecture (ZTA) eliminates implicit trust granted to network perimeters, adhering to NIST SP 800-207.
The core tenets mandate:
- All resource requests are verified explicitly using multiple identity, device, and contextual telemetry signals;
- Access is granted on a least-privilege, just-in-time basis per session;
- Assume breach posture: network segments are treated as potentially hostile regardless of physical topography.

## 2. Policy Decision Point (PDP) and Enforcement Point (PEP)
The Policy Engine evaluates continuous risk scores derived from device health, geolocation, and behavioral analytics.
The Policy Enforcement Point terminates client sessions immediately if an anomaly or compromised token is detected.
Mutual TLS (mTLS) with cryptographically bound X.509 client certificates is required for all microservice communications.

## 3. Micro-Segmentation and Lateral Movement Prevention
Network security groups and software-defined perimeters partition workloads into micro-segments.
Inter-segment traffic requires explicit firewall rules, eliminating lateral attacker traversal during initial compromise.
"""
            }
        ]
    }
}


def get_enterprise_domain_docs(domain_key: str = None) -> List[Dict[str, Any]]:
    """Retrieve all or domain-specific enterprise documentation texts."""
    all_docs = []
    for d_key, data in ENTERPRISE_DOMAIN_DATA.items():
        if domain_key is None or domain_key == d_key:
            for doc in data["documents"]:
                all_docs.append({
                    "domain": data["domain"],
                    "id": doc["id"],
                    "title": doc["title"],
                    "content": doc["content"],
                })
    return all_docs
