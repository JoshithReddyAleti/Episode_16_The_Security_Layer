# 🚧 Pillar 3 — Guardrails & Control Thresholds

> *"What's your threshold for blocking a response as a prompt-injection attempt?"*
>
> If the answer is "we use the vendor's default," you don't own your controls — the vendor does. And when the auditor asks why that threshold, "the vendor picked it" is not an answer.

Guardrails are the automated controls that enforce your security policy at runtime — catching hallucinations, PII leaks, prompt injections, and toxic outputs before they cause harm. But a guardrail is only as good as its *threshold*, and setting defensible thresholds is a genuine engineering and risk discipline. This pillar is how to define the controls, set the thresholds, and make the build-vs-buy call on the tooling that enforces them.

---

## What Guardrails Actually Are

A guardrail is a control that sits in the request/response path and evaluates content against a policy, taking action (allow, block, redact, flag, escalate) based on a threshold.

Guardrails operate at three points:
- **Input guardrails** — evaluate the user's request before it reaches the model (catch prompt injection, PII in the query, policy violations)
- **Retrieval guardrails** — evaluate retrieved context before it reaches the model (catch unauthorized documents, injected instructions in retrieved content)
- **Output guardrails** — evaluate the model's response before it reaches the user or a downstream system (catch hallucinations, PII leakage, toxicity, unsafe outputs)

The four control categories the role explicitly calls out — hallucination, PII/PHI exposure, prompt injection, toxicity — plus data-access policy, are the core of what the guardrail layer enforces.

---

## Control 1: Hallucination

**What it is:** the model states something false with confidence — fabricated facts, invented citations, incorrect figures.

**Why it's hard to guardrail:** hallucination isn't a pattern you can regex. It's a *semantic* problem — the output is fluent and well-formed but *wrong*. Detection requires either grounding verification or a separate judgment.

**Detection approaches:**
- **Grounding / faithfulness checks** — does the output's claims trace to the retrieved source context? (For RAG, this is the strongest signal: if a claim isn't supported by retrieved docs, flag it.)
- **Self-consistency** — sample multiple responses; high variance signals low confidence / likely hallucination.
- **LLM-judge faithfulness** — a separate model evaluates whether the response is supported by the source.
- **Citation verification** — if the model cites sources, verify the citations exist and support the claim.
- **Uncertainty estimation** — token-level confidence / entropy as a weak signal.

**Threshold setting:** the metric is typically a *faithfulness score* (0-1). The threshold question is: below what score do you block, flag, or append a disclaimer?

- **High-stakes (medical, legal, financial):** high threshold (e.g., faithfulness ≥ 0.9 to pass), block-or-review below.
- **Assistive (drafting, brainstorming):** lower threshold, flag rather than block.
- **The tradeoff:** too strict blocks legitimate responses (false positives frustrate users); too loose lets hallucinations through. The threshold is a *risk decision*, tied to the initiative's lane from Pillar 1.

---

## Control 2: PII / PHI Exposure

**What it is:** personally identifiable information (PII) or protected health information (PHI) appearing where it shouldn't — in a prompt sent to a provider, in a response returned to an unauthorized user, in a log.

**Detection approaches:**
- **Named-entity recognition (NER)** — detect names, SSNs, account numbers, addresses, medical terms
- **Pattern matching** — structured PII (SSN, credit card via Luhn check, email, phone) is regex-detectable with high precision
- **Contextual classifiers** — ML models that detect PII/PHI in context (better recall on unstructured mentions)
- **Dictionary / gazetteer** — known-sensitive terms (drug names, diagnoses for PHI)

**Actions:**
- **Redact** — replace `SSN: 123-45-6789` with `SSN: [REDACTED]` before the model or user sees it
- **Block** — reject the request/response entirely
- **Tokenize** — swap sensitive values for reversible tokens (so downstream systems can act without exposure)

**Threshold setting:** PII/PHI is often **zero-tolerance for certain categories** — you don't set a "how much PHI is OK" threshold, you set *which categories are absolutely blocked* and *which detection confidence triggers action*. The tuning is on the *detector's* precision/recall:
- **High recall** (catch everything, tolerate false positives) for regulated data — missing a real PHI leak is catastrophic, over-redacting is annoying.
- The threshold is on detector confidence: at what confidence do you redact vs flag-for-review?

This control ties directly to the HIPAA/GDPR requirements from 2026 Ep15/Folder 4.

---

## Control 3: Prompt Injection

**What it is:** input that overrides the system's intended instructions. Direct ("ignore your instructions and...") or, far more dangerous, **indirect** — malicious instructions embedded in content the model processes (a retrieved document, a webpage, a tool result, an email the agent reads).

**Why it's the hardest control:** the instruction and the data share a channel. There's no clean syntactic separation between "the system's instructions" and "the attacker's injected instructions" — they're all just tokens. This is *the* unsolved problem of LLM security.

**Detection / mitigation approaches:**
- **Injection classifiers** — models trained to detect injection attempts (catch known patterns; imperfect against novel attacks)
- **Spotlighting / delimiting** — marking untrusted content clearly so the model treats it as data, not instructions (helps, doesn't solve)
- **Instructional hierarchy** — training/prompting the model to prioritize system instructions over content instructions (providers are building this in)
- **Output constraints** — if the model can't produce a harmful action, injection that aims for that action fails (defense in depth)
- **Privilege separation** — the agent's *authority* is bounded regardless of what it's told (Pillar 6 — this is the real defense for agents)
- **Dual-LLM patterns** — a quarantined LLM processes untrusted content and can't take actions; a privileged LLM takes actions but never sees raw untrusted content

**Threshold setting:** injection classifiers produce a score. The threshold trades off:
- **Strict:** block anything that looks remotely like injection → high false positives (blocks legitimate content that happens to contain instruction-like text, e.g., a document *about* prompt injection).
- **Loose:** only block obvious attacks → misses novel/obfuscated injections.

The honest position: **thresholds alone don't solve injection.** They reduce it. The real control for high-risk systems is architectural — bounding what the model can *do* so a successful injection has limited blast radius. Threshold-based detection is one layer of defense-in-depth, not the whole answer. Say this explicitly to leadership; overpromising on injection detection is a credibility risk.

---

## Control 4: Toxicity

**What it is:** the model produces harmful, hateful, harassing, or otherwise unacceptable content — either unprompted or when manipulated.

**Detection approaches:**
- **Toxicity classifiers** — well-established models scoring content across categories (hate, harassment, violence, self-harm, sexual content)
- **Category-specific thresholds** — different thresholds for different harm categories
- **Provider moderation APIs** — most providers offer a moderation endpoint

**Threshold setting:** toxicity classifiers score per-category (0-1). Thresholds are set per category based on:
- **Audience** — a mental-health support product needs different self-harm handling than a coding assistant
- **Context** — content *about* a sensitive topic vs content *promoting* harm (a classifier must distinguish "discussing violence in a news summary" from "inciting violence")
- **Category severity** — child-safety and self-harm categories are typically zero-tolerance; mild profanity may be tolerated depending on product

The nuance that separates senior from junior: **toxicity thresholds must account for false positives that harm legitimate use.** A cancer-support forum's AI that blocks all mentions of death is broken. The threshold is contextual, not a global constant.

---

## Control 5: Data-Access Policy

Beyond content controls, the guardrail layer enforces **who can access what** — the runtime enforcement of the RLS and identity work from 2026 Ep15/Folder 4.

- **Every request carries identity** (Pillar from Ep15/Folder 4 §01)
- **Retrieval is pre-filtered** by the requesting user's permissions (Ep15/Folder 4 §02)
- **The guardrail layer verifies** that no response contains data the requesting identity isn't authorized to see
- **Cross-tenant / cross-classification access attempts** are blocked and alerted as critical events

Data-access policy is where content guardrails meet authorization — a response can be non-toxic, PII-free, and faithful, yet still be a violation if it contains data *this user* shouldn't see.

---

## Setting Thresholds — The Meta-Discipline

Across all controls, threshold-setting follows the same discipline:

**1. Tie the threshold to the risk lane.** An Elevated Risk initiative (Pillar 1) gets stricter thresholds than a Standard one. The threshold is a risk decision, and the lane already encodes the risk.

**2. Measure the confusion matrix.** For each threshold, you have false positives (legitimate content blocked) and false negatives (harmful content passed). You cannot minimize both — you choose where to sit based on the relative cost.
- Where a false negative is catastrophic (PHI leak, child-safety) → bias toward recall, tolerate false positives.
- Where a false positive is very costly (blocking legitimate high-value responses) and the false-negative cost is bounded → bias toward precision.

**3. Make it measurable and monitored.** A threshold you set once and never measure is a liability. Track: block rate, false-positive rate (from user appeals / review), incident rate (harms that got through). Tune continuously.

**4. Document the decision.** Every threshold is an ADR-worthy decision: why this number, what tradeoff it encodes, what the residual risk is. When the auditor asks "why 0.85 and not 0.95," you have an answer.

---

## Build vs Buy — The Tooling Landscape

You will not build all of this from scratch. A mature AI protection layer combines your own policy logic with commercial tooling. The senior architect's job is the **build-vs-buy call**, made with security leadership.

### The landscape (representative, verify current capabilities)

**AI Observability & Guardrails:**
- **Arize** (and its open-source Phoenix) — ML/LLM observability, evaluation, drift and hallucination monitoring, guardrails.
- **Fiddler AI** — model monitoring, explainability, LLM observability, safety metrics.
- **Others in the space** — Guardrails AI (open-source guardrail framework), Lakera (prompt-injection focus), Protect AI, WhyLabs, Robust Intelligence.

**Data Security Posture Management (DSPM) / Data Access:**
- **Varonis** — data access governance, DSPM, monitoring who-can-access-what and detecting anomalous access — directly relevant to the data-access-policy control.
- **Others** — Cyera, BigID, Securiti in the data-security-posture space.

> ⚠️ Vendor capabilities change fast; treat specific feature claims as "verify against current product docs before recommending." The categories are stable; the feature boundaries move.

### The build-vs-buy decision logic

**Buy when:**
- The capability is commoditized (toxicity classification, standard PII detection, model monitoring) — vendors do it better than you will.
- Time-to-value matters and the capability isn't a differentiator.
- The vendor's coverage of evolving threats (new injection patterns) exceeds what you'd maintain.
- Compliance benefits from a third-party attestation (an independent guardrail vendor is evidence of due diligence).

**Build when:**
- The control encodes *your specific policy* (your risk lanes, your data-access rules) — no vendor knows your business logic.
- The integration with your identity and authorization layer is deep and custom.
- You need full control of thresholds and their evolution for defensibility.
- Data-residency or contractual constraints prevent sending content to a third-party guardrail service.

**The usual answer is hybrid:** buy the commoditized detectors (toxicity, PII, injection classification, observability), build the policy orchestration that combines them with your risk lanes and data-access rules. You own the *decision logic*; you rent the *detectors*.

**Bringing security leadership to the decision** (an explicit responsibility of the role): the build-vs-buy call isn't purely technical — it's a spend decision, a risk decision, and a strategic one. The senior architect frames the options, quantifies the tradeoffs (cost, coverage, control, time-to-value, defensibility), and brings a *recommendation with reasoning* to security leadership — not a menu, a position.

---

## Files In This Pillar

| File | Concept |
|---|---|
| [`hallucination_control.py`](hallucination_control.py) | Faithfulness scoring and threshold logic |
| [`pii_phi_control.py`](pii_phi_control.py) | Detection, redaction, tokenization patterns |
| [`prompt_injection_control.py`](prompt_injection_control.py) | Injection detection + defense-in-depth |
| [`toxicity_control.py`](toxicity_control.py) | Category-specific toxicity thresholds |
| [`data_access_control.py`](data_access_control.py) | Runtime authorization enforcement |
| [`threshold_tuning.py`](threshold_tuning.py) | Confusion-matrix-driven threshold calibration |
| [`build_vs_buy_matrix.py`](build_vs_buy_matrix.py) | Decision logic for tooling selection |

---

## The Interview Question

*"How would you set the threshold for a prompt-injection guardrail, and what would you tell leadership about its effectiveness?"*

**The wrong answer:** "I'd set it high to catch all injections."

**The right answer:**
*"First, honesty about what threshold-based injection detection can and can't do — because overpromising here is a credibility risk. Detection reduces injection; it doesn't solve it, because the instruction and the data share a channel and novel attacks evade classifiers. So I'd set the threshold as one layer of defense-in-depth, not the whole defense. For the threshold itself: the classifier produces a score, and I'd calibrate it against a labeled set measuring the confusion matrix — false positives are legitimate content blocked, like a document that's *about* prompt injection, and false negatives are real attacks that pass. Where I sit depends on the risk lane from our tiering framework: a high-risk system that can take actions gets a strict threshold biased toward recall, because a missed injection there could trigger a real action; a low-risk read-only assistant gets a looser threshold to avoid frustrating users. Then I monitor block rate, false-positive rate from appeals, and any injection incidents that get through, and tune continuously. But the message to leadership is the important part: the *real* control for our high-risk agents isn't the detector threshold — it's architectural. We bound what the agent can *do*, so even a successful injection has limited blast radius. The threshold reduces the attack surface; privilege separation contains the damage. I'd present both, and I'd document the threshold choice as an ADR so when an auditor asks why 0.8, we have the reasoning and the residual-risk acceptance on record."*

That's the answer that shows you own your controls.

---

*Previous: [← Threat Modeling for AI](../02_threat_modeling_for_ai/README.md) · Return to [episode README](../README.md) · Next: [Policy-as-Code & Enforcement →](../04_policy_as_code_and_enforcement/README.md)*
