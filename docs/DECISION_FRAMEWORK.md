# 🧭 AI Security Program Decision Framework

The drop-in decision doc for standing up and running an AI security program.

## Step 1: Tier The Initiative (Pillar 1)

Score seven factors: data sensitivity, decision consequence, autonomy level, population scale, model provenance, regulatory exposure, reversibility.

Combine with dominant-factor logic:
- Any single **critical** factor -> Elevated Risk
- Two or more **high** factors -> Elevated Risk
- Regulatory high-risk category -> Elevated Risk (hard escalator)
- No production data and no real-world impact -> Experimentation
- Otherwise -> Standard

Produce a Risk Decision Record: factor scores, dominant factor, rationale, required controls, sign-off, review date.

## Step 2: Threat Model (Pillar 2)

Layer the lenses:
- **STRIDE** for component completeness
- **OWASP LLM Top 10** for the application-risk checklist
- **MITRE ATLAS** for the adversary's perspective
- **MAESTRO** for agentic / multi-agent / emergent surface

Consolidate into a threat register. Capture significant decisions as ADRs.

## Step 3: Define Controls & Thresholds (Pillar 3)

For each applicable risk, define the guardrail and its threshold:
- Hallucination -> faithfulness score threshold, tied to lane
- PII/PHI -> detection confidence + zero-tolerance categories
- Prompt injection -> detection threshold + architectural blast-radius bounding
- Toxicity -> category-specific thresholds, context-aware
- Data access -> runtime authorization enforcement

Tie every threshold to the risk lane. Document each as an ADR.

## Step 4: Make Controls Enforceable (Pillar 4)

Translate policy to policy-as-code:
- Decompose policy into decidable predicates
- Choose enforcement point (deploy / runtime / config)
- Choose enforcement level (advisory / soft / hard mandatory) mapped to lane
- Test and version the policy
- Generate evidence on every evaluation

## Step 5: Govern It (Pillar 5)

- Represent security in the AI Center of Excellence
- Map controls to EU AI Act / ISO 42001 / SR 11-7
- Choose the operating model (federated is usually right)
- Pre-approve patterns to scale
- Lead through influence; communicate risk to executives in business terms

## Step 6: Get Ahead Of Agents (Pillar 6)

- Evaluate agentic frameworks across six risk dimensions before production
- Define secure defaults on the blessed agentic platform
- Design the automation layer with the same discipline it enforces

## Build vs Buy Quick Reference

**Buy** commoditized detectors (toxicity, PII, injection classification, observability) — Arize, Fiddler, Varonis, and equivalents.

**Build** the policy orchestration that combines detectors with your risk lanes and data-access rules.

**Usual answer:** hybrid. Own the decision logic; rent the detectors. Bring a recommendation with reasoning to security leadership, not a menu.
