# 📖 The Security Layer Glossary

**ADR (Architecture Decision Record)** — a versioned document capturing the context, decision, alternatives, and consequences of a security-relevant architectural choice.

**AI Center of Excellence (CoE)** — cross-functional governance body that sets AI standards and makes key decisions across an enterprise.

**AIMS** — AI Management System, the governance structure specified by ISO/IEC 42001.

**Advisory / Soft-mandatory / Hard-mandatory** — policy-as-code enforcement levels: warn / block-with-override / block-no-override.

**Arize** — AI/ML observability and guardrails platform (open-source: Phoenix).

**Build-vs-buy** — the decision of whether to build a control in-house or buy commercial tooling.

**Confusion matrix** — the true/false positive/negative breakdown used to calibrate a threshold.

**Data-access policy** — runtime enforcement of who can access what data through the AI system.

**Delivery lane** — the routing output of the risk framework: Standard, Elevated Risk, or Experimentation.

**Dominant-factor logic** — combining risk factors by letting the worst single factor drive the lane, with escalation rules.

**DSPM (Data Security Posture Management)** — tooling that discovers, classifies, and monitors sensitive data and access (e.g., Varonis).

**Effective challenge** — SR 11-7 principle of critical, independent review of models.

**Elevated Risk lane** — the delivery lane for material-risk initiatives requiring full threat modeling and sign-off.

**EU AI Act** — EU regulation tiering AI by risk with obligations scaling to risk.

**Experimentation lane** — the sandboxed delivery lane: no production data, no real-world impact, minimal but bounded controls.

**Faithfulness score** — a measure of whether model output is supported by its source context; the primary hallucination signal in RAG.

**Fiddler** — AI observability, explainability, and safety-monitoring platform.

**Guardrail** — an automated control in the request/response path that evaluates content against policy and takes action.

**Hard escalator** — a factor (like regulatory high-risk classification) that forces a lane regardless of other factors.

**Hallucination** — model output that is fluent but false.

**Indirect prompt injection** — injection via malicious instructions embedded in content the model processes (documents, web pages, tool results).

**ISO/IEC 42001** — international, certifiable standard for an AI management system.

**MAESTRO** — an emerging threat-modeling framework for agentic / multi-agent AI systems (Cloud Security Alliance).

**MITRE ATLAS** — Adversarial Threat Landscape for AI Systems; the AI analog of MITRE ATT&CK.

**Model provenance** — the origin and controllability of a model, a risk factor.

**NIST AI RMF** — US AI Risk Management Framework (Govern, Map, Measure, Manage).

**OPA / Rego** — Open Policy Agent and its policy language; open-source policy-as-code.

**OWASP LLM Top 10** — the consensus list of the most critical LLM application risks.

**PHI** — Protected Health Information.

**PII** — Personally Identifiable Information.

**Policy-as-code** — expressing security/governance policy as executable, testable, versioned code.

**Prompt injection** — input that overrides the system's intended instructions; the top LLM risk.

**Proportionate control** — matching control weight to risk magnitude; the core principle of the risk framework.

**Risk Decision Record** — the auditable output of a tiering decision.

**Sentinel** — HashiCorp's policy-as-code framework.

**Shadow AI** — ungoverned AI built by teams routing around a too-heavy security process; the signal of a failed operating model.

**SR 11-7** — US model risk management supervisory guidance.

**Standard lane** — the fast delivery lane for low-risk, well-understood patterns with lightweight automated controls.

**STRIDE** — classical threat taxonomy: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege.

**Three lines of defense** — SR 11-7 structure: model owners, independent validation, audit.

**Toxicity** — harmful, hateful, or harassing model output.

**Varonis** — data security and access governance / DSPM platform.

**Secure defaults** — the safe-by-default configuration that every agent or system inherits from the blessed platform.

**Threat register** — the consolidated list of threats from all modeling lenses, with mitigations and owners.
