# 📚 The Frameworks Reference — Every Framework, In Depth

This is the detailed companion to the pillar READMEs. Where the pillars *use* the frameworks in context, this document *explains each one fully* — structure, internals, AI application, and how to use it in practice.

> ⚠️ **Read this first.** My knowledge has a cutoff and these frameworks evolve — especially the regulatory ones (EU AI Act dates), the newest ones (MAESTRO), and anything with numbered identifiers (ATLAS technique IDs, ISO clause numbers, OWASP numbering, EU AI Act article numbers). Treat the **concepts and structure** here as reliable and every **specific number, date, and identifier** as *verify against the primary source before it goes in front of an auditor, a regulator, or a C-suite deck.* Where I'm genuinely uncertain, I say so explicitly.

**Contents**
- Part A — Risk & Governance Frameworks: [NIST AI RMF](#1-nist-ai-rmf) · [ISO/IEC 42001](#2-isoiec-42001) · [SR 11-7](#3-sr-11-7) · [EU AI Act](#4-eu-ai-act)
- Part B — Threat Modeling Frameworks: [STRIDE](#5-stride) · [OWASP LLM Top 10](#6-owasp-llm-top-10) · [MITRE ATLAS](#7-mitre-atlas) · [MAESTRO](#8-maestro)
- Part C — Enforcement & Credentials: [Sentinel / OPA](#9-sentinel--opa-rego) · [CISSP / CISM](#10-cissp--cism)

---

# Part A — Risk & Governance Frameworks

---

## 1. NIST AI RMF

**Full name:** NIST Artificial Intelligence Risk Management Framework (AI RMF 1.0)
**Author:** US National Institute of Standards and Technology
**Released:** January 2023 (voluntary, non-regulatory)
**Companion:** a Generative AI Profile was added later (NIST AI 600-1) to address GenAI-specific risks; there is also an AI RMF Playbook with actionable guidance.

### What it is and why it exists

The AI RMF is a **voluntary framework for managing risks across the AI lifecycle.** It's non-prescriptive — it doesn't tell you "do X" — it gives you a structured way to think about, identify, and manage AI risk that's flexible across industries and use cases. It's become the US reference point the way ISO 27001 is for infosec, and it's the framework most US enterprises anchor their AI governance to.

### The structure — two halves

**Half 1: The characteristics of trustworthy AI.** The framework defines what "trustworthy AI" means across a set of characteristics. A trustworthy AI system should be:
- **Valid and reliable** — it works and keeps working
- **Safe** — it doesn't endanger life, health, property, environment
- **Secure and resilient** — it withstands attack and recovers
- **Accountable and transparent** — you can trace who's responsible and what it did
- **Explainable and interpretable** — you can understand its outputs
- **Privacy-enhanced** — it protects personal data
- **Fair, with harmful bias managed** — it doesn't produce unjust outcomes

These are the *properties you're managing toward*. Every risk decision trades off against these.

**Half 2: The four core functions.** This is the operational heart — the AI RMF organizes risk work into four functions, each broken into **categories** and **subcategories** (the granular, actionable items):

**GOVERN** *(cross-cutting — it wraps the other three)*
The culture, structures, processes, and accountability for managing AI risk across the organization. This is where policies, roles, risk tolerance, and oversight live. Your risk-tiering framework (Pillar 1), your CoE (Pillar 5), and your policies (Pillar 4) are all GOVERN artifacts. GOVERN is not a phase — it's continuous and it surrounds Map/Measure/Manage.

**MAP**
Establish the context and identify risks. What is the system, what's its purpose, who are the stakeholders, what could go wrong? This is where you frame the problem and enumerate risks *before* measuring them. Your factor assessment (Pillar 1) and threat modeling (Pillar 2) are MAP activities.

**MEASURE**
Analyze, assess, benchmark, and monitor the risks identified in MAP. Use quantitative and qualitative methods to track them. Your guardrail metrics, evaluation scores, and monitoring (Pillar 3) are MEASURE activities. You can't manage what you don't measure.

**MANAGE**
Allocate resources to the mapped-and-measured risks. Prioritize, respond, recover, communicate. This is where you actually act — apply controls, accept residual risk, escalate. Your lane routing and control application (Pillars 1, 3, 4) are MANAGE activities.

### How you use it for AI security

The AI RMF is your **program's backbone vocabulary.** You map every activity you do to a function: "our risk tiering is a GOVERN + MAP activity; our guardrail monitoring is MEASURE; our lane-based controls are MANAGE." When a regulator or auditor asks "how do you manage AI risk," you answer in RMF terms and show the artifacts under each function. It makes an otherwise ad-hoc program *legible* to outsiders.

For generative AI specifically, the GenAI Profile adds risk categories unique to LLMs — things like confabulation/hallucination, dangerous or harmful content, data privacy leakage, and information integrity — and suggests actions against each. If you're doing GenAI, use the profile, not just the base framework.

### Verify

The four functions and the trustworthy-AI characteristics are stable. The exact category/subcategory identifiers and the GenAI Profile's specific content should be pulled from the current NIST publications before you cite them precisely.

---

## 2. ISO/IEC 42001

**Full name:** ISO/IEC 42001 — Information technology, Artificial intelligence, Management system
**Authors:** ISO and IEC (international standards bodies)
**Published:** December 2023
**Nature:** the world's first **certifiable AI management system standard.** Unlike NIST AI RMF (voluntary, self-assessed), you can be **audited and certified** against ISO 42001 by an accredited body — which is why it matters for enterprise credibility and customer trust.

### What it is and why it exists

ISO 42001 specifies requirements for an **AI Management System (AIMS)** — the organizational system for governing how you develop, deploy, and operate AI responsibly. It's the AI-specific sibling of ISO 27001 (information security management) and ISO 9001 (quality management), and it shares their structure. If NIST AI RMF is "how to think about AI risk," ISO 42001 is "how to run a certifiable, auditable AI governance program."

### The structure — harmonized management-system clauses

ISO 42001 follows the standard ISO "harmonized structure" (the same skeleton as ISO 27001), which is why organizations with existing ISO certifications adopt it readily. The requirement clauses are roughly:

- **Clause 4 — Context of the organization:** understand your organization, interested parties, and the scope of the AIMS.
- **Clause 5 — Leadership:** top-management commitment, an AI policy, roles and responsibilities.
- **Clause 6 — Planning:** risk assessment and risk treatment, AI objectives, and — critically for AI — **AI system impact assessments.**
- **Clause 7 — Support:** resources, competence, awareness, communication, documented information.
- **Clause 8 — Operation:** operational planning and control; carrying out the risk treatments and impact assessments.
- **Clause 9 — Performance evaluation:** monitoring, measurement, internal audit, management review.
- **Clause 10 — Improvement:** nonconformity handling, corrective action, continual improvement.

Running through it is the **PDCA cycle** (Plan-Do-Check-Act) — plan the AIMS, implement it, check it works, improve it. Continual improvement is a core requirement, not a nice-to-have.

**The controls.** ISO 42001 includes an **Annex of controls** (analogous to ISO 27001's Annex A) — a reference set of AI-specific controls and implementation guidance covering areas like AI policies, internal organization, resources for AI systems, impact assessment, the AI system lifecycle, data management, information for interested parties, use of AI systems, and third-party relationships. You select applicable controls (a "Statement of Applicability") based on your risk assessment.

> ⚠️ The exact annex letters (which annex holds the controls vs implementation guidance vs domain considerations) and the precise control list should be checked against the published standard — I'm confident the harmonized clause structure (4-10) and the existence of an annexed control set are correct, but don't quote specific annex letters or control numbers without verifying.

### How you use it for AI security

Two modes:
1. **As a structure** — even without pursuing certification, ISO 42001 gives your program a recognized skeleton. Organize your CoE, policies, risk process, and controls to conform, and you have a defensible, complete governance program.
2. **As a certification** — pursue formal certification when enterprise customers or regulators expect independent attestation. The certification is external evidence your AI governance is real and disciplined, which shortens procurement and builds trust. Your risk-tiering framework, threat models, ADRs, and control records become the audit evidence.

**NIST AI RMF vs ISO 42001** — the common question: NIST is a *voluntary US framework for thinking about risk*; ISO 42001 is an *international, certifiable management-system standard*. They're complementary — many programs use NIST AI RMF for the risk-thinking vocabulary and ISO 42001 for the certifiable management structure. Neither replaces the other.

---

## 3. SR 11-7

**Full name:** Supervisory Guidance on Model Risk Management (Federal Reserve SR 11-7 / OCC Bulletin 2011-12)
**Authors:** US Federal Reserve and Office of the Comptroller of the Currency
**Issued:** April 2011
**Nature:** supervisory guidance for regulated financial institutions. Originally about quantitative financial models; now the de facto reference for **AI/ML model risk in regulated industries.**

### What it is and why it exists

SR 11-7 exists because banks make consequential decisions using models, and models can be wrong or misused. It defines **model risk** and prescribes how institutions must manage it. For AI in banking, insurance, and other regulated sectors, SR 11-7 is frequently the *binding* constraint — stricter and more specific than the voluntary frameworks.

### The core definitions

**Model** — SR 11-7 defines a model broadly: a quantitative method, system, or approach that applies statistical, economic, financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates. **An ML/AI model squarely qualifies** — which is why the guidance applies to AI.

**Model risk** — the potential for adverse consequences from decisions based on incorrect or misused model outputs. It has **two primary sources:**
1. **Fundamental errors** — the model produces inaccurate outputs (bad data, flawed design, implementation bugs).
2. **Incorrect or inappropriate use** — the model is used outside its intended purpose or its limitations are misunderstood.

### The three components of model risk management

**1. Robust model development, implementation, and use.** Sound design, documented assumptions, appropriate data, and testing. The people who build the model must document *what it does, what it assumes, and where it breaks.*

**2. Effective challenge.** This is the heart of SR 11-7. **Effective challenge** = critical analysis by objective, informed parties who can identify model limitations and produce appropriate changes. It requires competence, influence, and *independence* — the challenger can't be the person who built the model. This is what forces real scrutiny rather than rubber-stamping.

**3. Governance, policies, and controls.** The organizational framework — model risk policies, roles, and the **model inventory** (you must maintain a complete inventory of all models in use; you can't manage models you don't know you have).

### Model validation — the deep requirement

SR 11-7 requires **independent validation** of models, typically covering three elements:
- **Evaluation of conceptual soundness** — is the model well-designed for its purpose? Are assumptions and methodology sound?
- **Ongoing monitoring** — does it still work in production? (Process verification and benchmarking.)
- **Outcomes analysis** — do the model's outputs match reality? (Including **back-testing** — comparing predictions to actual outcomes.)

The "three lines of defense" model is commonly used to operationalize this: first line = model owners/developers; second line = independent model risk management/validation; third line = internal audit. *(SR 11-7 itself emphasizes independence and roles; the explicit "three lines" phrasing is a broader risk-governance convention often layered on top — accurate in spirit, verify if quoting SR 11-7 directly.)*

### How you use it for AI security

If your AI touches a regulated financial decision, your **Elevated Risk lane must incorporate SR 11-7's requirements:** independent validation, effective challenge, conceptual-soundness review, ongoing monitoring with outcomes analysis, and inclusion in the model inventory. Practically, this means your governance can't let the team that builds a consequential model be the only one that blesses it — you need an independent validation function. This shapes org structure, not just process.

The modern challenge: SR 11-7 predates deep learning. Applying "evaluate conceptual soundness" to a billion-parameter model whose internal logic isn't human-interpretable is genuinely hard, and supervisors have issued follow-on guidance and interpretations. Treat SR 11-7's *principles* as binding and its *application to modern AI* as an evolving area — verify current supervisory expectations.

---

## 4. EU AI Act

**Full name:** Regulation (EU) 2024/1689 — the Artificial Intelligence Act
**Author:** European Union
**Status:** entered into force in 2024, with obligations **phasing in over roughly 2025–2027.**
**Nature:** the world's first comprehensive, **binding** AI regulation. Unlike everything else in Part A, this is *law*, with penalties — and it has extraterritorial reach (it applies to AI systems placed on the EU market or affecting EU persons, regardless of where the provider sits).

### What it is and why it exists

The EU AI Act regulates AI by **risk tier** — the higher the risk to health, safety, and fundamental rights, the heavier the obligations. It's the AI analog of GDPR in ambition and reach, and like GDPR it's likely to set a de facto global baseline because compliance is easier to do uniformly than regionally.

### The structure — four risk tiers

**Tier 1 — Unacceptable risk (Prohibited).**
Certain AI practices are banned outright. These include things like government social scoring, certain manipulative or exploitative techniques that cause harm, untargeted scraping of facial images to build recognition databases, and (with narrow law-enforcement exceptions) real-time remote biometric identification in public spaces. If your system falls here, it can't be deployed in the EU — full stop.

**Tier 2 — High risk.**
The core of the Act. AI used in sensitive domains — biometrics, critical infrastructure, education, employment, access to essential services (including creditworthiness/insurance), law enforcement, migration, justice — plus AI that is a safety component of a regulated product. High-risk systems carry substantial obligations: a **risk management system, data governance, technical documentation, record-keeping/logging, transparency to users, human oversight, and accuracy/robustness/cybersecurity** — plus conformity assessment before market and post-market monitoring after.

**Tier 3 — Limited risk (Transparency obligations).**
Systems like chatbots and generative AI that interact with people or produce synthetic content carry **transparency** duties — users must be told they're interacting with AI, and AI-generated content (deepfakes) must be disclosed/labeled.

**Tier 4 — Minimal risk.**
Everything else (spam filters, AI in video games). No specific obligations; voluntary codes of conduct encouraged.

### General-Purpose AI (GPAI) models

The Act has a **separate regime for general-purpose AI models** (foundation models). GPAI providers face transparency and documentation obligations (technical documentation, information for downstream deployers, a copyright policy, and a summary of training data). GPAI models deemed to pose **systemic risk** (above a compute/capability threshold) face additional obligations — model evaluation, adversarial testing, systemic-risk assessment and mitigation, and incident reporting.

### Timeline and penalties

**Timeline (phased):** prohibitions on unacceptable-risk practices apply first (earliest), GPAI obligations follow, and the bulk of high-risk obligations apply later (the longest lead time). The phase-in runs across roughly 2025–2027.

**Penalties:** tiered and severe — the top tier (for prohibited-practice violations) reaches into the tens of millions of euros or a percentage of global annual turnover, whichever is higher, with lower bands for other violations.

> ⚠️ **Verify all specifics here.** Exact prohibited-practice lists, the high-risk annex contents, the GPAI systemic-risk compute threshold, the precise application dates, and the exact penalty figures are all things I'd confirm against the current official text before putting them in a compliance document. The *four-tier structure and the GPAI regime* are the stable, load-bearing concepts.

### How you use it for AI security

**Map your risk-tiering framework (Pillar 1) to the Act's tiers.** A system that's high-risk under the EU AI Act should automatically route to your Elevated Risk lane, and the Act's high-risk obligations (risk management, data governance, human oversight, logging, accuracy/robustness) become *required controls* in that lane. The Act's transparency duties become guardrail/UX requirements. For GPAI, if you host or fine-tune foundation models, the documentation and (if applicable) systemic-risk obligations attach. The Act is where "governance" stops being best-practice and becomes legally mandatory for the EU market.

---

# Part B — Threat Modeling Frameworks

*(These are covered in applied form in Pillar 2; here is the fuller standalone explanation of each.)*

---

## 5. STRIDE

**Full name:** STRIDE (an acronym — see below)
**Authors:** developed at Microsoft (Loren Kohnfelder and Praerit Garg, late 1990s)
**Nature:** the classic, general-purpose threat-modeling taxonomy. Not AI-specific, but foundational — it gives you *completeness*.

### What it is

STRIDE is a mnemonic for six categories of security threat. You threat-model by taking each component of a system and asking, "how is this component vulnerable to each of the six?" It's valued because it's *systematic* — it forces you to consider categories you'd otherwise skip.

### The six categories (and their security-property opposites)

| Letter | Threat | Violates | Plain meaning |
|---|---|---|---|
| **S** | **Spoofing** | Authentication | Pretending to be someone/something you're not |
| **T** | **Tampering** | Integrity | Unauthorized modification of data or code |
| **R** | **Repudiation** | Non-repudiation | Denying you did something, with no proof otherwise |
| **I** | **Information disclosure** | Confidentiality | Exposing data to those not authorized |
| **D** | **Denial of service** | Availability | Making the system unavailable |
| **E** | **Elevation of privilege** | Authorization | Gaining capabilities you shouldn't have |

Each threat maps to a security property it violates — Spoofing breaks authentication, Tampering breaks integrity, and so on. The defense for each is the corresponding property (authentication, integrity controls, logging/audit, encryption/access control, rate-limiting/redundancy, authorization).

### The methodology

Classic STRIDE threat modeling: (1) build a **data flow diagram** of the system — its processes, data stores, data flows, and trust boundaries; (2) for each element, enumerate which of the six threats apply; (3) for each applicable threat, decide to mitigate, eliminate, transfer, or accept; (4) document. The **trust boundary** — where data crosses from less-trusted to more-trusted — is where threats concentrate.

### Why it still matters for AI

AI systems are still systems — they have processes, data stores, and trust boundaries. STRIDE catches the "classical" threats that AI-specific frameworks assume away. Its unique value in an AI context is *completeness*: layered under OWASP/ATLAS/MAESTRO, it ensures you didn't forget that your vector database can be tampered with, your model endpoint can be DoS'd, or your agent's actions can be repudiated. Pillar 2 has the full STRIDE-for-AI grid mapping each category to AI-specific manifestations.

---

## 6. OWASP LLM Top 10

**Full name:** OWASP Top 10 for Large Language Model Applications
**Author:** OWASP (Open Worldwide Application Security Project) — the same body behind the famous OWASP Web Top 10
**Nature:** the community-consensus list of the most critical security risks specific to LLM applications. Updated periodically.

### What it is

Where STRIDE is a general taxonomy, the OWASP LLM Top 10 is a **concrete checklist of the actual, observed, high-impact risks in real LLM applications.** It's the fastest way to answer "did you consider the standard LLM risks?" — you go down the list and document applicability, mitigation, and residual risk for each.

### The ten (2023/2024 framing, with 2025-revision notes)

> ⚠️ OWASP revised this list for 2025; some names, ordering, and emphases changed. The concepts below are stable; verify current IDs/names against owasp.org before quoting numbers.

- **LLM01 · Prompt Injection** — attacker input overrides intended instructions. **Direct** (the user injects) and **indirect** (malicious instructions hidden in retrieved content, a webpage, a document, a tool result the model ingests). The #1 risk, and the one that makes agents dangerous, because the instruction and the data share one channel with no clean separation.
- **LLM02 · Insecure Output Handling** — downstream systems trust model output blindly. If model output flows unsanitized into a shell, SQL query, or web page, you get command injection, SQLi, or XSS *via the model*. (The 2025 revision elevates sensitive-information handling around here.)
- **LLM03 · Training Data Poisoning** — corrupted training or fine-tuning data introduces backdoors, biases, or vulnerabilities that surface later, sometimes only on a trigger.
- **LLM04 · Model Denial of Service** — crafted inputs cause disproportionate resource consumption (expensive queries, unbounded generation). The 2025 revision broadens this toward "unbounded consumption," including cost/economic exhaustion.
- **LLM05 · Supply Chain Vulnerabilities** — compromised third-party models, datasets, or dependencies. A poisoned model from a public hub, a malicious package, a tampered dataset.
- **LLM06 · Sensitive Information Disclosure** — the model reveals PII, secrets, proprietary data, or other sensitive content in its outputs (via memorization, context leakage, or manipulation).
- **LLM07 · Insecure Plugin/Tool Design** — plugins or tools with excessive permissions, poor input validation, or insufficient access control become an attack path into connected systems.
- **LLM08 · Excessive Agency** — the system can *do too much*: too many permissions, too much autonomy, too little human oversight. When an LLM can take consequential actions, excessive agency turns any other exploit (like injection) into real-world harm. Directly relevant to agentic systems (Pillar 6) and the whole 2027 series.
- **LLM09 · Overreliance** — humans (or systems) trust model output more than warranted, acting on hallucinations or errors without verification. A socio-technical risk as much as a technical one.
- **LLM10 · Model Theft** — the model itself is exfiltrated, or cloned via extensive querying (model extraction), stealing the intellectual property and enabling offline attack development.

### How you use it

For each LLM application, walk all ten: does it apply, what's the mitigation, what's the residual risk? That becomes a section of your threat model and a direct, checkable answer to security review. The Top 10 pairs naturally with the risk lanes — LLM01 (injection) and LLM08 (excessive agency) dominate for anything agentic, pushing it toward Elevated Risk. Pillar 3's guardrails are, in large part, the mitigations for the content-related items (injection, sensitive-info disclosure, toxicity-adjacent output handling).

---

## 7. MITRE ATLAS

**Full name:** MITRE ATLAS — Adversarial Threat Landscape for Artificial-Intelligence Systems
**Author:** MITRE (the organization behind MITRE ATT&CK), with community contribution
**Nature:** a knowledge base of adversary **tactics and techniques against AI/ML systems**, deliberately modeled on — and complementary to — MITRE ATT&CK.

### What it is and why it exists

MITRE ATT&CK catalogs how real adversaries attack IT systems, organized as a matrix of tactics (the adversary's *goals*) and techniques (the *how*). ATLAS does the same thing **for AI/ML systems.** Its value is the **adversary's perspective** — where OWASP is a defender's checklist, ATLAS makes you think like the attacker, walking their kill chain against your model. It also gives you shared vocabulary with your existing security team (your SOC already knows ATT&CK; ATLAS extends that mental model to AI). ATLAS includes **real-world case studies** of AI attacks, which make it concrete rather than theoretical.

### The structure — tactics and techniques

**Tactics** are the adversary's objectives, arranged roughly as a kill chain. They mirror ATT&CK's tactics and add AI-specific ones. The tactic set includes (approximately):
- **Reconnaissance** — researching the target AI system
- **Resource Development** — building attack capabilities (proxy models, adversarial datasets)
- **Initial Access** — getting into the environment / reaching the AI system
- **ML Model Access** — gaining query access or white-box access to the model itself
- **Execution** — running malicious code/inputs
- **Persistence** — maintaining a foothold (e.g., a backdoor planted via poisoning)
- **Defense Evasion** — evading detection (adversarial examples that slip past filters)
- **Discovery** — learning the model's properties and environment
- **Collection** — gathering data for the attack
- **ML Attack Staging** — preparing the actual model attack
- **Exfiltration** — stealing the model or its data
- **Impact** — the end goal: degrade, deny, manipulate, or erode trust

**Techniques** are the specific methods under each tactic, with identifiers of the form **`AML.T####`**. Well-known technique families include:
- **Model evasion** — crafting adversarial inputs that cause misclassification
- **Model extraction / stealing** — querying to reconstruct or clone the model
- **Membership inference** — determining whether specific data was in the training set (a privacy attack)
- **Data poisoning** — corrupting training data to implant behavior
- **Prompt injection and LLM-specific techniques** — ATLAS has incorporated LLM-era attacks
- **Model/ML supply chain compromise**

> ⚠️ The exact tactic list, the technique IDs (`AML.T####`), and the case-study catalog evolve as MITRE updates ATLAS. Pull current IDs from atlas.mitre.org before putting them in a formal threat model — the *structure and the adversary-perspective methodology* are the durable parts.

### How you use it

For a given AI system, **walk the tactics and ask "how would an attacker accomplish this against us?"** For each, assess your exposure, your detection capability, and your mitigation. ATLAS is especially strong for maturity *beyond the checklist* — it pushes you past "did we handle the known risks" into "how would a determined adversary actually chain an attack." Because it shares ATT&CK's structure, it plugs into your existing threat-intel and detection-engineering workflows. Pillar 2 shows the adversary-walk template.

---

## 8. MAESTRO

**Full name:** MAESTRO — a threat-modeling framework for **agentic / multi-agent AI**, associated with the Cloud Security Alliance's agentic-security work
**Nature:** an emerging, agent-focused framework built because the older lenses (STRIDE, OWASP, ATLAS) weren't designed for autonomous, multi-agent systems.

> ⚠️ **Strongest caveat in this document.** MAESTRO is new and I have lower confidence in its exact definition than in the other frameworks here. I believe the acronym expands to something along the lines of *Multi-Agent Environment, Security, Threat, Risk, and Outcome* and that it uses a **layered (roughly seven-layer) reference architecture** for analyzing agentic systems — but treat the specific acronym expansion, the exact number of layers, and the precise layer names as **unverified.** Confirm against the Cloud Security Alliance's primary source before any formal or external use. What I'm confident about is the *problem it addresses and the style of analysis*, described below.

### Why it exists — the gap it fills

The moment AI systems become **agentic** (they plan, use tools, act, and coordinate with other agents), the older threat-modeling lenses strain:
- STRIDE is component-oriented and wasn't built for autonomous agents pursuing goals.
- OWASP LLM Top 10 is application-centric, not agent-coordination-centric.
- ATLAS is adversary-oriented but not specifically about emergent, multi-agent behavior.

MAESTRO exists to model the surface that *only appears when agents act and coordinate* — the inter-agent, cross-layer, and emergent risks.

### The style of analysis — layered + cross-layer

MAESTRO's core idea is a **layered analysis of the agentic stack.** An agentic system isn't one thing; it's a stack of layers, and each layer has its own threat surface, *and threats cross layers.* The layers (as I understand them, conceptually) span roughly: the **foundation model**, the agent's **reasoning/planning**, its **memory**, its **tools/plugins**, the **orchestration** between agents, the **deployment environment/infrastructure**, and the broader **ecosystem** it operates in.

The threats MAESTRO-style analysis surfaces that the other lenses miss:
- **Inter-agent threats** — one agent manipulating another; a compromised agent poisoning shared state; trust exploitation between agents that implicitly trust each other.
- **Orchestration threats** — the coordination layer itself attacked; message tampering or spoofing between agents.
- **Cross-layer threats** — an attack at one layer propagating to another (e.g., a poisoned memory corrupting the planning layer).
- **Memory-layer threats** — an agent's accumulated memory poisoned so future behavior is compromised long after the initial injection.
- **Goal/planning threats** — an agent's objective subverted so it pursues an attacker's goal while appearing to function normally.
- **Emergent threats** — harmful behavior arising from agent *interaction* that no single agent exhibits alone.

### How you use it

For any **multi-agent or autonomous system**, layer MAESTRO on top of STRIDE/OWASP/ATLAS: the classical lenses cover the components; MAESTRO covers the emergent, cross-layer, and inter-agent surface. This is the lens that carries directly into the 2027 agentic series — every one of the five agentic architectural gaps has a MAESTRO-style threat dimension. Pillar 6 develops the agentic-security application in depth; Pillar 2 has the layer-analysis template.

---

# Part C — Enforcement & Credentials

---

## 9. Sentinel / OPA (Rego)

These are the two dominant **policy-as-code** tools — the mechanism for turning written policy into automatically enforced, testable controls (Pillar 4).

### HashiCorp Sentinel

**What it is:** a policy-as-code framework embedded in HashiCorp's enterprise products (notably Terraform Cloud/Enterprise, Vault, etc.). Policies are written in the **Sentinel policy language** and evaluated against a proposed change *before* it's applied — a deployment gate.

**The defining feature — enforcement levels:**
- **Advisory** — policy failure produces a *warning* but does not block. (Maps to your Experimentation lane.)
- **Soft-mandatory** — policy failure *blocks*, but an authorized user can **override** with a recorded justification. (Maps to your Standard lane.)
- **Hard-mandatory** — policy failure *blocks* with **no override possible.** (Maps to your non-negotiable controls — "no PHI to a provider without a BAA.")

This three-level model maps almost perfectly onto risk lanes, which is why Sentinel is called out for AI governance: you express your policy as code once, tag each policy with the right enforcement level, and the platform enforces it consistently and automatically. Sentinel also supports **testing** (you write tests for your policies) and **mocking** (evaluate against sample data), so policies are trustworthy code, not untested scripts.

### Open Policy Agent (OPA) and Rego

**What it is:** OPA is the **open-source, CNCF-graduated** general-purpose policy engine; **Rego** is its declarative policy language. OPA decouples policy decision-making from your application — your service asks OPA "is this allowed?" and OPA evaluates the request against Rego policies and returns a decision. It's especially dominant in **cloud-native / Kubernetes** environments (e.g., admission control) but is general-purpose (API authorization, CI/CD gates, data filtering).

**Sentinel vs OPA — when each:**
- **Sentinel** — HashiCorp-centric shops; deep Terraform/Vault integration; the built-in advisory/soft/hard enforcement levels are a natural fit for risk lanes.
- **OPA/Rego** — cloud-native/Kubernetes shops; open-source and vendor-neutral; broader ecosystem; you implement enforcement-level semantics yourself.

A senior architect should be conversant in both and choose based on the existing platform. Either way, the *method* (Pillar 4) is the same: decompose prose policy into decidable predicates, choose the enforcement point and level, test and version, and generate evidence on every evaluation.

> ⚠️ Exact Sentinel/Rego syntax evolves; the runnable demo in `code_examples/policy_as_code_demo.py` is deliberately syntax-agnostic pseudo-policy that demonstrates the *semantics* (advisory/soft/hard, decidable predicates, evidence). Verify current syntax against HashiCorp/OPA docs before implementing for real.

---

## 10. CISSP / CISM

The two credentials most associated with the senior AI-security-architect role. Neither is AI-specific — they certify the **security and security-management foundation** the role is built on, which AI-specific knowledge then extends.

### CISSP — Certified Information Systems Security Professional

**Body:** (ISC)²
**What it certifies:** broad, deep technical-and-managerial security competence across the field. It's the widely-recognized "senior security practitioner" credential.
**Structure:** the CISSP Common Body of Knowledge is organized into **eight domains:**
1. Security and Risk Management
2. Asset Security
3. Security Architecture and Engineering
4. Communication and Network Security
5. Identity and Access Management (IAM)
6. Security Assessment and Testing
7. Security Operations
8. Software Development Security

**Requirements:** passing the exam plus (typically) several years of cumulative paid work experience across the domains, and endorsement.
**Why it matters for the role:** it signals you understand the *full* security landscape — risk management, architecture, IAM, assessment — into which AI security fits. The AI-specific work (this whole episode) sits *on top of* this foundation.

### CISM — Certified Information Security Manager

**Body:** ISACA
**What it certifies:** security **management and governance** — more managerial/strategic than CISSP's technical breadth. Oriented toward those who *run* security programs and align them with business.
**Structure:** organized around four domains (approximately):
1. Information Security Governance
2. Information Security Risk Management
3. Information Security Program (development and management)
4. Incident Management (and response)

**Why it matters for the role:** CISM's governance-and-management emphasis maps directly to the role's Pillar 5 work — running an AI security program, governance, aligning security with business, communicating to leadership. Where CISSP says "you know security," CISM says "you can *manage a security program*."

**CISSP vs CISM for this role:** CISSP is the broad technical-and-managerial foundation; CISM is the governance-and-management specialization. Many senior architects hold both. The role also values **advanced credentials in AI, cloud, or zero-trust** as differentiators on top of the foundation — and genuine AI-security depth (the content of this episode) is increasingly what distinguishes candidates, since the certs predate the AI-security discipline.

> ⚠️ Domain names/counts for both certifications are periodically updated by (ISC)² and ISACA. Verify the current domain structure and experience requirements against the official sources.

---

## Summary — Which Framework For What

| Need | Reach for |
|---|---|
| A vocabulary for AI risk management (US) | **NIST AI RMF** |
| A certifiable AI governance management system | **ISO/IEC 42001** |
| Model risk in regulated finance | **SR 11-7** |
| Legal compliance for the EU market | **EU AI Act** |
| Systematic component threat completeness | **STRIDE** |
| The LLM-specific risk checklist | **OWASP LLM Top 10** |
| The adversary's perspective on AI attacks | **MITRE ATLAS** |
| Agentic / multi-agent threat modeling | **MAESTRO** |
| Turning policy into enforced controls | **Sentinel / OPA** |
| The security foundation credential | **CISSP** |
| The security-management credential | **CISM** |

The senior architect doesn't pick one — they **layer** them. NIST/ISO/SR 11-7/EU AI Act govern *how you decide and prove*; STRIDE/OWASP/ATLAS/MAESTRO govern *how you find the threats*; Sentinel/OPA govern *how you enforce*; CISSP/CISM certify *that you can do all of it.*

---

*Return to [episode README](../README.md) · This reference complements the applied treatment in [Pillar 1](../01_ai_risk_assessment_and_tiering/README.md), [Pillar 2](../02_threat_modeling_for_ai/README.md), [Pillar 4](../04_policy_as_code_and_enforcement/README.md), and [Pillar 5](../05_governance_and_operating_models/README.md).*
