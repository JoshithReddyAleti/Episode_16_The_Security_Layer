# 🎚️ Pillar 1 — AI Risk Assessment & Tiering

> *"Why did the marketing chatbot ship in two weeks and the loan-decisioning model take four months?"*
>
> *"Because one is Standard lane and one is Elevated Risk lane, here are the exact criteria that put each there, and here's the signed record of the decision."*
>
> That sentence — delivered calmly to an SVP — is the entire job.

The risk-assessment framework is the load-bearing wall of an AI security program. Everything else — guardrails, threat models, governance — hangs off it. Get it right and the program scales: hundreds of AI initiatives routed consistently, quickly, and defensibly. Get it wrong and you're either the bottleneck everyone routes around, or the rubber-stamp that lets a high-risk system ship uncontrolled.

This pillar is how to build that framework.

---

## The Core Idea — Proportionate Control

Treating every AI initiative as maximum-risk is as broken as treating every one as zero-risk. The framework's purpose is **proportionality**: match the weight of controls to the magnitude of risk, and make the matching *auditable*.

The output of the framework is a **delivery lane**:

| Lane | Risk profile | Control weight | Speed |
|---|---|---|---|
| **Standard** | Low risk, well-understood pattern | Lightweight, mostly automated | Fast — days to weeks |
| **Elevated Risk** | Material risk, sensitive data, or consequential decisions | Full threat model, human review, sign-off | Deliberate — weeks to months |
| **Experimentation** | Sandboxed, no production data, no real-world impact | Minimal, but bounded and monitored | Immediate — but caged |

The genius of the lane model is that it decouples *speed* from *risk* correctly: low-risk work is fast **because** it's low-risk, not because someone cut corners. And high-risk work is slow **because** it's high-risk, not because security is being obstructive. Everyone can see the logic.

---

## The Multi-Factor Risk Model

A single risk score is too blunt. Real risk is multi-dimensional, and the tiering model scores several factors, then combines them into a lane assignment.

### The factors that matter

**1. Data sensitivity.** What data does the system touch?
- Public / synthetic → low
- Internal business → medium
- PII → high
- PHI / financial / regulated → critical
- Special categories (biometric, children's data) → critical+

**2. Decision consequence.** What happens when the system is wrong?
- Informational only (suggestions a human ignores freely) → low
- Assistive (human reviews before acting) → medium
- Consequential (affects a person's access, money, opportunity) → high
- Autonomous action (system acts without human in the loop) → critical

**3. Autonomy level.** How much does the system act on its own?
- Read-only / generate-only → low
- Human-approved actions → medium
- Bounded autonomous actions → high
- Open-ended autonomous actions → critical (and this is the 2027 series' whole domain)

**4. Population scale & exposure.** Who and how many are affected?
- Internal, small team → low
- Internal, org-wide → medium
- External customers → high
- Public / vulnerable populations → critical

**5. Model provenance & control.** How well do you understand and control the model?
- Well-understood API from a vetted provider with a contract → lower
- Open-weights model you host and evaluate → medium
- Fine-tuned model with unclear training data → higher
- Third-party model with opaque provenance → higher

**6. Regulatory exposure.** What rules apply?
- No specific regulation → low
- General privacy (GDPR/CCPA) → medium
- Sector regulation (HIPAA, SR 11-7 model risk, GLBA) → high
- EU AI Act high-risk category → critical

**7. Reversibility.** Can a bad outcome be undone?
- Fully reversible → low
- Reversible with effort → medium
- Hard to reverse → high
- Irreversible (money moved, message sent, decision communicated) → critical

### Combining factors into a lane

The naive approach — average the factors — is wrong, because risk doesn't average. A system with critical data sensitivity is high-risk *even if every other factor is low*. The correct combination logic is **dominant-factor with escalation**:

```
lane = Standard
for each factor:
    if factor == critical:
        lane = Elevated Risk   # any single critical factor escalates
    if factor == high and (count of high factors >= 2):
        lane = Elevated Risk   # multiple high factors escalate
if no production data and no real-world impact:
    lane = Experimentation     # sandbox overrides (but stays caged)
if any factor triggers a regulatory high-risk category:
    lane = Elevated Risk       # regulation is a hard escalator
```

This captures the real intuition: **the worst single dimension usually determines the lane, and regulation is never negotiable.** A working implementation is in [`code_examples/risk_tiering_engine.py`](../code_examples/risk_tiering_engine.py).

---

## Making It Auditable

A tiering decision that can't be explained is worse than no tiering, because it creates the *illusion* of governance. Every lane assignment must produce an auditable record:

```
Risk Decision Record
─────────────────────
Initiative: Customer support chatbot v2
Assessed: 2026-08-14 by [assessor]
Factors:
  data_sensitivity:     medium  (internal KB + customer names)
  decision_consequence: medium  (assistive, human agents review)
  autonomy_level:       low     (generate-only, no actions)
  population_scale:     high    (all external customers)
  model_provenance:     low     (vetted provider, contract in place)
  regulatory_exposure:  medium  (GDPR — EU customers)
  reversibility:        medium  (responses editable before send)
Dominant factor: population_scale = high (single high, no escalation)
Assigned lane: STANDARD
Rationale: Single high factor (scale) without critical data or
           consequence; assistive with human review; established
           pattern. Standard controls sufficient.
Required controls: [PII guardrail, prompt-injection guardrail,
                    output logging, quarterly review]
Sign-off: [name], [role], [date]
Next review: 2027-02-14 or on material change
```

**The three properties an auditor checks:**
1. **Consistency** — would the same initiative get the same lane if assessed by a different person? (This is why the factors and combination logic must be explicit, not judgment calls.)
2. **Traceability** — can you show *why* this lane, with the factor scores and rationale?
3. **Currency** — is the decision still valid, or has the system changed since assessment?

---

## Grounding in the Frameworks

The tiering model isn't invented from nothing — it operationalizes established risk frameworks.

### NIST AI RMF

The US National Institute of Standards and Technology's AI Risk Management Framework organizes AI risk work into four functions: **Govern, Map, Measure, Manage.**

- **Govern** — the culture and structures for managing risk (your tiering framework *is* a Govern artifact)
- **Map** — establish context and identify risks (your factor assessment is the Map step)
- **Measure** — analyze and track risks (your guardrail metrics from Pillar 3)
- **Manage** — allocate resources to risks and act (your lane routing and controls)

The tiering framework is how you make NIST AI RMF concrete rather than aspirational. *(Verify current RMF structure against the NIST primary source — it has companion profiles and a Generative AI profile that evolve.)*

### ISO/IEC 42001

The international standard for an **AI Management System (AIMS)** — the AI analog of ISO 27001 for information security. Certifiable, which matters for enterprise credibility. It requires a systematic, documented approach to AI risk: policy, roles, risk assessment, controls, continual improvement.

Your tiering framework is a central control in an ISO 42001-conformant AIMS. If you're pursuing certification, the framework, its records, and its review cadence are direct evidence. *(Clause numbers evolve; check the published standard before citing specifics.)*

### SR 11-7 — Model Risk Management

US Federal Reserve / OCC supervisory guidance on **model risk management**, originally aimed at financial models but now the reference point for AI/ML model risk in regulated industries. Its core tenets:

- **Model risk = risk of adverse consequences from decisions based on incorrect or misused model output**
- **Effective challenge** — critical, independent review of models
- **Three lines of defense** — model owners, independent validation, audit
- **Model inventory** — you must know every model in production

For AI in financial services, SR 11-7 is often the binding constraint. Your tiering framework's Elevated Risk lane should map to SR 11-7's validation and effective-challenge requirements for consequential models. *(SR 11-7 is a 2011 document; interpretation for modern AI is evolving through subsequent guidance — verify current supervisory expectations.)*

---

## The Speed-vs-Assurance Balance

The hardest part of the job, and the part that distinguishes senior from junior, is calibrating the framework so it delivers *both* assurance and speed.

**Signs the framework is too heavy (strangling delivery):**
- Most initiatives land in Elevated Risk (the lanes aren't discriminating)
- Standard-lane work still takes weeks (the "lightweight" controls aren't lightweight)
- Teams are building shadow AI to avoid the process (the loudest signal of failure)
- The security team is a named bottleneck in every retro

**Signs the framework is too light (creating exposure):**
- Consequential systems slipping into Standard lane
- No initiative has ever been stopped or materially changed by the process
- Auditors find risk decisions that don't match the actual risk
- Guardrail incidents in production that the assessment should have caught

**The calibration levers:**
- **Tune the escalation thresholds** — if too much lands in Elevated, your factor definitions are too conservative.
- **Automate Standard-lane controls fully** — Standard should be nearly frictionless *because* the controls are policy-as-code (Pillar 4), not human review.
- **Pre-approve patterns** — if "internal RAG over public docs" is assessed once and blessed as a pattern, every future instance skips reassessment.
- **Make Experimentation genuinely fast** — a well-caged sandbox lane relieves pressure on the production lanes.

The senior move is treating the framework itself as a product with metrics: lane distribution, time-in-lane, shadow-AI incidence, and caught-vs-missed risk. You tune it continuously.

---

## Files In This Pillar

| File | Concept |
|---|---|
| [`multi_factor_model.py`](multi_factor_model.py) | The seven factors and their scoring |
| [`lane_routing_logic.py`](lane_routing_logic.py) | Dominant-factor combination with escalation |
| [`risk_decision_record.py`](risk_decision_record.py) | The auditable record schema |
| [`framework_mapping.py`](framework_mapping.py) | Mapping lanes to NIST/ISO 42001/SR 11-7 requirements |
| [`framework_calibration.py`](framework_calibration.py) | Metrics for tuning speed vs assurance |

---

## The Interview Question

*"Design a risk-assessment framework for AI initiatives at a large enterprise. It needs to move fast for low-risk work and rigorously for high-risk work, and it needs to be defensible to auditors."*

**The wrong answer:** "We'd review each project and assign a risk level."

**The right answer:**
*"Multi-factor tiering routing into delivery lanes. First, the factors — I'd score each initiative on data sensitivity, decision consequence, autonomy level, population scale, model provenance, regulatory exposure, and reversibility. Not averaged — combined with dominant-factor logic, because any single critical dimension escalates the whole thing and regulation is a hard escalator. That produces one of three lanes: Standard for low-risk well-understood patterns with lightweight automated controls, Elevated Risk for material risk with full threat modeling and sign-off, Experimentation for sandboxed work with no production data. The auditability comes from a Risk Decision Record per initiative — factor scores, the dominant factor, the rationale, required controls, sign-off, and a review date. That gives an auditor the three things they check: consistency, traceability, currency. I'd ground it in NIST AI RMF's Govern-Map-Measure-Manage, map the Elevated lane to SR 11-7 effective-challenge for consequential models, and structure the whole thing as evidence for ISO 42001 if we're pursuing certification. And critically — I'd treat the framework as a product with metrics: lane distribution, time-in-lane, and shadow-AI incidence. If most things land in Elevated, my factors are miscalibrated. If teams are routing around me, I'm the bottleneck. The framework only works if low-risk work is genuinely fast *because* the Standard-lane controls are policy-as-code, not human review. Speed and assurance aren't a tradeoff if the framework is designed right — they're both outputs of proportionate control."*

That's the answer that gets the senior role.

---

*Return to [episode README](../README.md) · Next: [Threat Modeling for AI →](../02_threat_modeling_for_ai/README.md)*
