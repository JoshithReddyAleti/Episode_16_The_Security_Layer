# 🎯 Pillar 2 — Threat Modeling for AI Systems

> *"Where's your threat model?"*
>
> The question a regulator or a serious internal auditor asks first. Not "is it secure" — "show me you systematically thought about how it could be attacked." A program without threat models is a program that got lucky, and luck is not a control.

Threat modeling is the discipline of systematically finding how a system can be attacked *before* an attacker does. AI systems have a threat surface that classical threat modeling only partially covers, so the senior AI security architect must be fluent in both the classical taxonomies (STRIDE) and the AI-specific ones (MITRE ATLAS, OWASP LLM Top 10, MAESTRO) — and must produce the Architecture Decision Records that make the whole analysis defensible.

This pillar is that fluency.

---

## Why AI Needs Its Own Threat Modeling

Classical systems have classical threats: someone breaks authentication, injects SQL, floods the service. AI systems have all of those **plus** a category that didn't exist before: **the model itself is an attack surface.**

- The input can *reprogram the system's behavior* (prompt injection) in a way SQL injection never could — because the instruction and the data share a channel.
- The model can *leak its training data* or *memorize secrets*.
- The model can be *poisoned* during training so it behaves maliciously on a trigger.
- The model can be *stolen* by querying it enough to clone its behavior.
- The model can be *manipulated into harmful outputs* that then flow downstream into actions.

No amount of classical network security addresses these. You need threat models built for the AI-specific surface. The mature approach uses **multiple lenses layered together** — each catches what the others miss.

---

## Lens 1: STRIDE — The Classical Foundation, Applied to AI

STRIDE is Microsoft's classical threat taxonomy. It still applies — AI systems are still systems — but each category takes on AI-specific forms.

| STRIDE category | Classical meaning | AI-specific manifestation |
|---|---|---|
| **S**poofing | Pretending to be someone else | Impersonating a user to an agent; forging identity in tool calls; deepfake-based auth bypass |
| **T**ampering | Unauthorized modification | Training-data poisoning; prompt injection altering behavior; modifying the vector index; tampering with model weights |
| **R**epudiation | Denying an action | An agent takes an action with no audit trail tying it to the authorizing user; non-reproducible model decisions |
| **I**nformation disclosure | Leaking data | Model leaking training data / PII; RAG surfacing unauthorized documents; reasoning traces exposing secrets; membership inference |
| **D**enial of service | Making it unavailable | Model-DoS via expensive queries; unbounded reasoning-token consumption; adversarial inputs that trigger runaway loops |
| **E**levation of privilege | Gaining unauthorized capability | Prompt injection escalating an agent's authority; jailbreaks bypassing guardrails; excessive agency letting a tool do more than intended |

**How to use it:** walk every component of your AI system (the model, the retrieval layer, the tool interface, the agent loop, the data pipeline) against all six categories. For each cell that's plausible, you have a threat to mitigate or accept. STRIDE's value is *completeness* — it forces you to consider categories you'd otherwise skip.

---

## Lens 2: OWASP LLM Top 10 — The Application-Risk Checklist

The OWASP Top 10 for Large Language Model Applications is the industry's consensus list of the most critical LLM risks. It's the checklist every LLM app should be measured against.

> ⚠️ OWASP revised this list for 2025; the ordering and some names changed from the original 2023 version. Verify current numbering against owasp.org before citing specific IDs. The concepts below are stable even where the numbers shifted.

**The canonical risks (2023 framing, with 2025 notes):**

- **LLM01 · Prompt Injection** — attacker-controlled input overrides intended instructions. Direct (user does it) and indirect (malicious content in a retrieved document / webpage does it). *The number-one risk, and the one that makes agents dangerous.*
- **LLM02 · Insecure Output Handling** — downstream systems trust model output blindly (model output flows into a shell, SQL, or HTML without sanitization → RCE, XSS, SQLi). *2025 reframed sensitive-info disclosure prominently here.*
- **LLM03 · Training Data Poisoning** — corrupted training/fine-tuning data introduces backdoors or bias.
- **LLM04 · Model Denial of Service** — expensive queries exhaust resources. *2025 broadened toward "unbounded consumption."*
- **LLM05 · Supply Chain Vulnerabilities** — compromised models, datasets, or dependencies (a poisoned model from a public hub, a malicious pip package).
- **LLM06 · Sensitive Information Disclosure** — model reveals PII, secrets, or proprietary data in its outputs.
- **LLM07 · Insecure Plugin/Tool Design** — tools/plugins with excessive permissions or poor input validation become an attack path.
- **LLM08 · Excessive Agency** — the system can do more than it should (too many permissions, too much autonomy, no human gate). *Directly relevant to Pillar 6 and the 2027 series.*
- **LLM09 · Overreliance** — humans trust model output more than they should, acting on hallucinations.
- **LLM10 · Model Theft** — the model itself is exfiltrated or cloned via query access.

**How to use it:** for each item, document whether it applies to your system, what the mitigation is, and what residual risk you accept. This becomes a section of your threat model and a direct answer to "did you consider the standard LLM risks?"

---

## Lens 3: MITRE ATLAS — The Adversary's Playbook

MITRE ATLAS (Adversarial Threat Landscape for Artificial-Intelligence Systems) is the AI analog of the famous MITRE ATT&CK framework. Where ATT&CK catalogs how adversaries attack IT systems, **ATLAS catalogs how adversaries attack AI/ML systems** — organized as tactics (the adversary's goals) and techniques (how they achieve them).

**The tactics (the adversary's kill chain for AI):**
- **Reconnaissance** — researching the target model
- **Resource Development** — building attack capabilities (adversarial datasets, proxy models)
- **Initial Access** — getting to the AI system
- **ML Model Access** — gaining query or white-box access
- **Execution** — running the attack
- **Persistence** — maintaining access (e.g., a backdoor in a fine-tuned model)
- **Defense Evasion** — evading detection (adversarial examples that bypass filters)
- **Discovery** — learning about the model's properties
- **Collection** — gathering data (e.g., extracting training data)
- **Exfiltration** — stealing the model or data
- **Impact** — the ultimate goal (degrade, deny, manipulate)

**Real ATLAS techniques worth knowing:**
- **Model evasion** — crafting inputs that cause misclassification (adversarial examples)
- **Model extraction / stealing** — querying to clone the model
- **Membership inference** — determining whether specific data was in the training set
- **Data poisoning** — corrupting training data
- **Prompt injection** — (ATLAS has adopted LLM-specific techniques)

> ⚠️ ATLAS technique IDs (like `AML.T####`) and the exact tactic list evolve. Pull current IDs from atlas.mitre.org before putting them in a formal threat model.

**How to use it:** ATLAS gives you the *adversary's perspective*. For your system, walk the tactics and ask "how would an attacker accomplish this against us?" It's especially strong for maturity beyond the checklist — it makes you think like the attacker, not just tick boxes. It also gives you a shared vocabulary with the broader security community (your SOC already knows ATT&CK; ATLAS extends that mental model to AI).

---

## Lens 4: MAESTRO — Threat Modeling for Agentic Systems

As AI moves from single-model apps to **multi-agent systems**, the classical lenses strain. STRIDE wasn't built for autonomous agents coordinating with each other; OWASP LLM Top 10 is app-centric. MAESTRO is an emerging framework built specifically for **agentic and multi-agent AI threat modeling.**

> ⚠️ MAESTRO is a newer framework (from the Cloud Security Alliance's agentic-security work). Its exact structure and the expansion of the acronym should be verified against the CSA primary source — I may not have the current definition precisely. What follows is the concept as I understand it; confirm specifics before formal use.

The core idea of MAESTRO is a **layered analysis of the agentic stack** — it recognizes that an agentic system has multiple layers (the foundation model, the agent's reasoning/planning, its memory, its tools, the orchestration between agents, the deployment environment, and the ecosystem it operates in), and that **each layer has its own threat surface** and threats can **cross layers.**

The kinds of threats MAESTRO-style analysis surfaces that the other lenses miss:
- **Inter-agent threats** — one agent manipulating another; a compromised agent poisoning shared state; trust exploitation between agents
- **Orchestration threats** — the coordination layer itself being attacked; message tampering between agents
- **Emergent threats** — behavior arising from agent interaction that no single agent exhibits
- **Memory-layer threats** — an agent's accumulated memory being poisoned so future behavior is compromised
- **Goal/planning threats** — an agent's objective being subverted, causing it to pursue an attacker's goal while appearing to work normally

**How to use it:** for any multi-agent or autonomous system, layer MAESTRO on top of the others. STRIDE/OWASP/ATLAS cover the components; MAESTRO covers the *emergent, cross-layer, and inter-agent* surface that only exists when agents act and coordinate. This is the lens that carries directly into the 2027 series (see Pillar 6).

---

## Layering the Lenses — The Complete Threat Model

No single lens is sufficient. The mature practice layers them:

```
For a given AI system:

1. STRIDE          → component-by-component completeness
                     (walk every component × 6 categories)

2. OWASP LLM Top 10 → application-risk checklist
                     (which of the 10 apply, mitigations, residual)

3. MITRE ATLAS     → adversary's perspective
                     (how would an attacker accomplish each tactic)

4. MAESTRO         → agentic / multi-agent / emergent surface
                     (layer-by-layer + inter-agent + emergent)

→ Consolidated threat register:
   [threat | lens | likelihood | impact | mitigation | residual | owner]
```

The consolidated register is the artifact. Each row: the threat, which lens surfaced it, likelihood and impact, the mitigation (control), the residual risk after mitigation, and who owns it. That register, kept current, *is* your threat model.

---

## Architecture Decision Records — Making It Defensible

A threat model is a point-in-time analysis. An AI system evolves. What keeps the program defensible over time is the **Architecture Decision Record (ADR)** — a lightweight, versioned document capturing *why* a security-relevant architectural decision was made.

**An ADR captures:**
- **Context** — the situation and forces at play
- **Decision** — what was decided
- **Alternatives considered** — what else was on the table and why it was rejected
- **Consequences** — the tradeoffs accepted, including residual risk
- **Status** — proposed / accepted / superseded

**Why ADRs are the auditor's best friend:**
When an auditor or regulator asks "why did you allow this agent to call external tools without human approval?", the answer isn't a defensive scramble — it's *"ADR-014, here it is: we considered three options, here's the risk analysis, here's why we chose bounded autonomy with these specific guardrails, here's the residual risk we accepted and who signed off."* That transforms an interrogation into a review of a documented, reasoned decision. **ADRs are how a program proves it was thinking, not just reacting.**

A worked ADR template is in [`docs/ADR_TEMPLATE.md`](../docs/ADR_TEMPLATE.md).

---

## Files In This Pillar

| File | Concept |
|---|---|
| [`stride_for_ai.py`](stride_for_ai.py) | STRIDE categories mapped to AI-specific threats |
| [`owasp_llm_top10.py`](owasp_llm_top10.py) | The Top 10 with mitigations and applicability check |
| [`mitre_atlas_tactics.py`](mitre_atlas_tactics.py) | ATLAS tactics and adversary-perspective analysis |
| [`maestro_agentic_layers.py`](maestro_agentic_layers.py) | Layered agentic threat analysis |
| [`threat_register.py`](threat_register.py) | Consolidated multi-lens threat register |
| [`adr_workflow.py`](adr_workflow.py) | Architecture Decision Record lifecycle |

---

## The Interview Question

*"How would you threat model a new AI system pattern — say, a customer-facing agent that can look up account data and take limited actions?"*

**The wrong answer:** "I'd run STRIDE on it."

**The right answer:**
*"I'd layer multiple lenses because no single one is complete for AI. Start with STRIDE for component completeness — walk the model, the retrieval layer, the tool interface, the agent loop, and the data pipeline against spoofing, tampering, repudiation, info disclosure, DoS, and elevation of privilege. For this system, tampering and elevation jump out immediately — prompt injection is the vector, because the agent takes actions. Then the OWASP LLM Top 10 as the application checklist — LLM01 prompt injection and LLM08 excessive agency are the critical ones here given it can act on accounts. Then MITRE ATLAS for the adversary's perspective — how would an attacker actually accomplish model extraction, evasion, or injection against us, using ATLAS's tactic taxonomy so it's shared vocabulary with our SOC. And because there's an agent taking actions, I'd add MAESTRO-style layered analysis for the agentic surface — inter-component threats, the memory layer being poisoned, the goal being subverted. That all consolidates into a threat register: each threat, which lens found it, likelihood, impact, mitigation, residual risk, owner. And critically — every significant architectural decision gets an ADR: why we allowed the agent to take actions, what alternatives we rejected, what residual risk we accepted, who signed off. That's what makes it defensible when a regulator asks 'why is this designed this way' six months from now. The threat model isn't a document you write once — it's a living register plus a trail of reasoned decisions."*

That's the senior answer.

---

*Previous: [← AI Risk Assessment & Tiering](../01_ai_risk_assessment_and_tiering/README.md) · Return to [episode README](../README.md) · Next: [Guardrails & Control Thresholds →](../03_guardrails_and_control_thresholds/README.md)*
