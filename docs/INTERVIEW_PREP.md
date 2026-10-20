# 🎯 Interview Prep — AI Security Architect / AI Risk Lead

Calibrated to the senior AI-security-architect archetype: builds risk frameworks, defines guardrail thresholds, owns threat models and ADRs, represents security in AI governance, evaluates agentic frameworks, presents to SVP/C-suite.

## The Universal Opener

For any "how would you secure AI at scale" question:

*"Security's job here isn't to say no — it's to make yes safe, fast, and repeatable. That means proportionate control: a risk-tiering framework that routes low-risk work through lightweight automated controls and high-risk work through proportionate scrutiny, all of it auditable. Everything else — threat models, guardrails, policy-as-code, governance — hangs off that framework."*

## Question Bank

### "Design an AI risk-assessment framework." -> Pillar 1
Multi-factor tiering (seven factors), dominant-factor combination with escalation, three delivery lanes, auditable Risk Decision Records, grounded in NIST AI RMF / ISO 42001 / SR 11-7. Framework-as-product with calibration metrics.

### "How do you threat model an AI system?" -> Pillar 2
Layer STRIDE + OWASP LLM Top 10 + MITRE ATLAS + MAESTRO. Consolidated threat register. ADRs for defensibility.

### "How do you set a guardrail threshold?" -> Pillar 3
Tie to risk lane. Measure the confusion matrix. Bias toward recall where false negatives are catastrophic (PHI, child-safety), toward precision where false positives are very costly. Monitor and tune. Document as ADR. Be honest that injection detection reduces but doesn't solve — real defense is architectural.

### "Build vs buy for AI protection tooling?" -> Pillar 3
Buy commoditized detectors (Arize, Fiddler for observability/guardrails; Varonis for data-access/DSPM). Build the policy orchestration that encodes your business logic. Hybrid. Bring a recommendation to security leadership.

### "Translate a security policy into an enforced control." -> Pillar 4
Decompose into decidable predicates, choose enforcement point and level (Sentinel/OPA), test and version, generate evidence. This is what makes the Standard lane genuinely fast.

### "You found a risk in a high-profile initiative that doesn't report to you." -> Pillar 5
Influence not authority. Partner not gate. Bring a solution. If it's a real tradeoff, bring it to the CoE as an informed decision with a recommendation. Document the decision in an ADR either way.

### "Present an AI risk to the C-suite." -> Pillar 5
Business terms not technology. Quantify and compare. Give a decision, not a lecture. Be honest about uncertainty. One slide, ninety seconds.

### "Evaluate an agentic framework for production." -> Pillar 6
Six dimensions: authority/action model, trust boundaries, injection resistance, observability, failure handling, human oversight. Output: architectural risk assessment + required controls + secure defaults. Injection becomes privilege escalation — the critical agentic fact.

### "How does security change with agents?" -> Pillar 6
Blast radius becomes direct action. Injection becomes privilege escalation. Authorization must be continuous. Observability explodes to trajectory level. Failure modes multiply. Maps to the five agentic gaps of the 2027 series.

## Certifications Worth Naming

CISSP, CISM for security foundation; advanced AI / cloud / zero-trust credentials as differentiators. The role values the security-governance foundation plus AI-specific depth.

## The Framework To Remember

1. **Risk tiering** — proportionate control into delivery lanes
2. **Threat modeling** — STRIDE / OWASP / ATLAS / MAESTRO layered
3. **Guardrails** — thresholds tied to lanes, build-vs-buy
4. **Policy-as-code** — enforceable, testable, versioned
5. **Governance** — CoE, regulation, influence, executive communication
6. **Agentic security** — evaluate frameworks, secure defaults, the bridge to 2027

Know these six and you're ready for the role and the interview.
