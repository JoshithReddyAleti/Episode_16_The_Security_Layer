# 📐 Architecture Decision Record (ADR) Template

ADRs keep an AI security program defensible. When an auditor or regulator asks "why is this designed this way," the ADR is the reasoned, documented answer.

## Format

```
# ADR-NNNN: [Short title of the decision]

## Status
[Proposed | Accepted | Superseded by ADR-XXXX | Deprecated]

## Date
YYYY-MM-DD

## Context
What is the situation? What forces are at play — technical, business,
regulatory, risk? What problem are we deciding about? Include the risk
lane (from Pillar 1) and relevant threats (from the threat register).

## Decision
What did we decide? State it clearly and specifically.

## Alternatives Considered
What other options were on the table?
- Option A: [description] — rejected because [reason]
- Option B: [description] — rejected because [reason]
- Option C (chosen): [description]

## Consequences
What are the tradeoffs of this decision?
- Positive: [what this buys us]
- Negative: [what this costs us]
- Residual risk accepted: [the risk we are consciously accepting]

## Controls & Enforcement
What controls implement or bound this decision?
- Guardrails: [which, thresholds]
- Policy-as-code: [which policies enforce this]
- Monitoring: [what we watch]

## Sign-off
- Decision owner: [name, role]
- Security review: [name, role]
- Risk acceptance (if residual risk): [name, role, date]

## Review
Next review date: [YYYY-MM-DD or trigger condition]
```

## Worked Example

```
# ADR-014: Bounded autonomy for the customer-support agent

## Status
Accepted

## Date
2026-08-14

## Context
The customer-support agent (Elevated Risk lane) needs to take actions
on customer accounts (issue refunds, update details). Threat register
T-023 (injection -> privilege escalation) and OWASP LLM08 (excessive
agency) are the driving risks. The business wants low-friction resolution;
security needs bounded blast radius.

## Decision
The agent may autonomously take reversible, low-value actions (update
non-sensitive details, issue refunds under $50). Irreversible or
high-value actions (refunds over $50, account closure, PII changes)
require human agent approval via an in-flow gate.

## Alternatives Considered
- Full autonomy — rejected: unbounded blast radius on injection.
- No autonomy (all actions human-approved) — rejected: defeats the
  purpose, no efficiency gain, high friction.
- Bounded autonomy (chosen): efficiency for the safe majority, human
  gate for the risky minority.

## Consequences
- Positive: fast resolution for most cases; bounded injection blast radius.
- Negative: some latency on high-value actions awaiting approval.
- Residual risk accepted: a successful injection could trigger a
  sub-$50 refund autonomously. Bounded and monitored; accepted.

## Controls & Enforcement
- Guardrails: prompt-injection detection (threshold tied to Elevated lane);
  action-value check before autonomous execution.
- Policy-as-code: hard-mandatory gate on actions above thresholds.
- Monitoring: all agent actions traced and tied to authorizing identity;
  alert on anomalous action patterns.

## Sign-off
- Decision owner: [product lead]
- Security review: [security architect]
- Risk acceptance: [risk lead], 2026-08-14

## Review
Next review: 2027-02-14 or on any expansion of the agent's action set.
```
