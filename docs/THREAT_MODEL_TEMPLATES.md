# 🎯 Threat Model Templates — STRIDE / MITRE ATLAS / MAESTRO

Drop-in templates for threat modeling an AI system. Fill per system.

> Verify all framework specifics (ATLAS technique IDs, OWASP numbering, MAESTRO structure) against primary sources before formal use.

## Template 1: STRIDE-for-AI Worked Grid

For each component (model, retrieval, tools, agent loop, data pipeline), assess each STRIDE category.

| Component | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation |
|---|---|---|---|---|---|---|
| Model | Impersonated caller | Weight tampering / poisoning | Non-reproducible output | Training-data leak / memorization | Expensive-query DoS | Jailbreak bypass |
| Retrieval | — | Index tampering / injection in docs | Unlogged retrieval | Unauthorized doc surfaced | Retrieval flooding | Cross-tenant retrieval |
| Tools | Forged tool identity | Tampered tool result | Unattributed tool action | Tool leaking data | Tool abuse DoS | Excessive tool permission |
| Agent loop | Impersonated user to agent | Injected instructions | Unlogged agent action | Reasoning-trace leak | Runaway loop | Injection -> privilege escalation |
| Data pipeline | — | Poisoned training data | Untracked data lineage | Pipeline data leak | Pipeline overload | Pipeline access escalation |

For each plausible cell: document the threat, likelihood, impact, mitigation, residual, owner.

## Template 2: OWASP LLM Top 10 Applicability

| # | Risk | Applies? | Mitigation | Residual |
|---|---|---|---|---|
| LLM01 | Prompt Injection | | | |
| LLM02 | Insecure Output Handling | | | |
| LLM03 | Training Data Poisoning | | | |
| LLM04 | Model Denial of Service | | | |
| LLM05 | Supply Chain | | | |
| LLM06 | Sensitive Info Disclosure | | | |
| LLM07 | Insecure Plugin/Tool Design | | | |
| LLM08 | Excessive Agency | | | |
| LLM09 | Overreliance | | | |
| LLM10 | Model Theft | | | |

## Template 3: MITRE ATLAS Adversary Walk

For each tactic, ask "how would an attacker accomplish this against us?"

| Tactic | Attacker goal | Our exposure | Detection | Mitigation |
|---|---|---|---|---|
| Reconnaissance | Research our model | | | |
| ML Model Access | Gain query/white-box access | | | |
| Execution | Run the attack | | | |
| Persistence | Maintain access (backdoor) | | | |
| Defense Evasion | Bypass our filters | | | |
| Exfiltration | Steal model/data | | | |
| Impact | Degrade/deny/manipulate | | | |

## Template 4: MAESTRO Agentic Layer Analysis

For agentic systems, assess each layer and cross-layer threats.

| Layer | Threats | Inter-layer risk | Mitigation |
|---|---|---|---|
| Foundation model | Jailbreak, poisoning | | |
| Reasoning / planning | Goal subversion | Planning poisoned by memory | |
| Memory | Memory poisoning | Poisoned memory -> bad planning | |
| Tools | Excessive agency, tool abuse | Tool result -> injection | |
| Orchestration | Message tampering, agent spoofing | Compromised agent -> others | |
| Deployment env | Standard infra threats | | |
| Ecosystem | Supply chain, external content | External content -> injection | |

Plus: emergent threats (behavior from interaction no single agent shows), inter-agent trust exploitation.

## Consolidated Threat Register

| ID | Threat | Lens | Likelihood | Impact | Mitigation | Residual | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| T-001 | | STRIDE | | | | | | |
| T-002 | | OWASP | | | | | | |
| T-003 | | ATLAS | | | | | | |
| T-004 | | MAESTRO | | | | | | |
