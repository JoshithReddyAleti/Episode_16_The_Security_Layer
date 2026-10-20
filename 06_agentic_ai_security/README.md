# 🤖 Pillar 6 — Agentic AI Security

> *Everything in the first five pillars gets harder the moment the AI stops answering and starts acting. A model that hallucinates gives you a wrong answer. An agent that hallucinates takes a wrong action — on a real system, with your credentials, while you're asleep.*

This is the pillar where the 2026 security layer meets the 2027 agentic series. Agentic AI — multi-agent orchestration, LLM tool-calling, autonomous workflows — is arriving in production faster than most security programs are ready for. The senior architect's job is to evaluate these frameworks for architectural risk *before* they reach production and define the secure defaults that partner teams build on. This pillar is that evaluation, and it's the on-ramp to everything the 2027 series covers in depth.

---

## Why Agentic AI Breaks the Existing Model

Every control in Pillars 1-5 was designed for AI that *responds*. Agentic AI *acts*, and that single shift breaks assumptions everywhere:

**The blast radius changes category.** A non-agentic LLM's worst case is a bad output a human might act on. An agent's worst case is the agent *itself* acting — sending the email, running the code, moving the money, deleting the data. The harm is direct and often irreversible.

**Prompt injection becomes privilege escalation.** In a non-agentic system, a successful injection produces bad text. In an agentic system, a successful injection *commands the agent to take actions* — the attacker's instructions become the agent's actions, executed with the agent's authority. Indirect injection (malicious content in a webpage or document the agent reads) turns any untrusted content the agent touches into a potential attack vector. This is the single most important agentic security fact.

**Authorization must be continuous, not one-time.** A non-agentic call checks authorization once. An agent takes many actions over a long horizon, each of which may need its own authorization check — and the agent's context (what it's seen, what it's been told) changes between actions.

**Observability requirements explode.** A non-agentic call has one input and one output to log. An agent has a trajectory — dozens of reasoning steps, tool calls, and decisions — each a potential point of failure or compromise, each needing to be logged, traced, and made auditable (this is a full episode in the 2027 series).

**The failure modes multiply.** An agent can get stuck, loop, hallucinate progress, take a wrong irreversible action, or be manipulated mid-trajectory. Each is a security-relevant failure that the non-agentic model never had to consider.

---

## Evaluating Agentic Frameworks for Architectural Risk

The role calls for evaluating *"emerging agentic AI frameworks (multi-agent orchestration, LLM tool-calling, autonomous workflows) for architectural risk."* When a partner team wants to adopt LangGraph, AutoGen, CrewAI, or similar, the security architect assesses the framework's architectural risk *before* it reaches production. The evaluation framework:

### The evaluation dimensions

**1. Authority & action model.** How does the framework bound what agents can do?
- Can you constrain which tools an agent can call?
- Can you require human approval for specific actions?
- Is there a permission model, or can any agent do anything its tools allow?
- *Red flag:* frameworks where agents have unbounded tool access by default.

**2. Trust boundaries between components.** In multi-agent systems, how is trust handled between agents?
- Can a compromised agent manipulate others?
- Is shared state (memory, message bus) protected from poisoning?
- Are inter-agent messages authenticated?
- *Red flag:* frameworks where all agents implicitly trust each other and shared state.

**3. Injection resistance.** How does the framework handle untrusted content?
- Is there separation between trusted instructions and untrusted data?
- When an agent reads external content (web, documents, tool results), can that content hijack it?
- *Red flag:* frameworks that feed untrusted content directly into the instruction context with no isolation.

**4. Observability & auditability.** Can you see what the agents did?
- Does the framework produce traceable, auditable logs of every action and decision?
- Can you replay a trajectory to debug or investigate?
- Can you tie every action to an authorizing identity?
- *Red flag:* frameworks that are black boxes at runtime.

**5. Failure handling.** What happens when things go wrong?
- Can you interrupt a running agent?
- Are there timeouts, loop detection, spend caps?
- Can actions be rolled back or compensated?
- *Red flag:* frameworks with no kill switch and no bounds on execution.

**6. Human oversight integration.** How does a human stay in control?
- Can you insert approval gates?
- Can a human monitor and intervene mid-execution?
- *Red flag:* frameworks designed for full autonomy with no human-in-the-loop hooks.

### Applying it to the common frameworks

> ⚠️ Framework capabilities evolve rapidly; the notes below are directional and must be verified against current versions before any real assessment. The *evaluation method* is the durable part.

- **LangGraph** — graph-based orchestration with explicit state and control flow. Its explicitness is a security *advantage*: the graph structure makes the control flow inspectable and boundable, and state is a first-class object you can protect. Evaluate: how tool authority is scoped per node, how state is protected from poisoning, whether human-approval nodes are supported.

- **AutoGen** — conversational multi-agent framework. The conversational, flexible model is powerful but the inter-agent trust surface is large — agents converse and can influence each other. Evaluate: inter-agent trust, whether a compromised agent can manipulate others, how tool access is bounded per agent, observability of the conversation.

- **CrewAI** — role-based multi-agent orchestration. Role structure gives some natural bounding (a "researcher" role vs an "executor" role). Evaluate: whether role boundaries are security-enforced or just organizational, how tasks delegate authority, shared-memory protection.

The output of the evaluation is an **architectural risk assessment** of the framework — its risks across the six dimensions, the secure-configuration requirements to mitigate them, and a recommendation (approve for which lanes, with which required controls, or reject).

---

## Defining Secure Defaults

The role calls for *"help define secure defaults with partner teams before they reach production."* This is the highest-leverage agentic-security activity: rather than reviewing every agent individually, you define the *secure defaults* that every agent inherits, so teams are secure by default.

**The secure defaults for agentic systems:**

**Least-privilege authority.** An agent gets the *minimum* tool access for its task, not the maximum available. New tools require explicit authorization. (This is the OWASP LLM08 Excessive Agency mitigation.)

**Bounded blast radius.** Irreversible or high-impact actions (sending, purchasing, deleting, communicating externally) require human approval by default. The agent can *propose* the action; a human *confirms* it. Autonomy is earned per action-type, not granted wholesale.

**Injection-resistant architecture.** Untrusted content (web, documents, tool results) is isolated from the instruction context. The dual-LLM pattern where feasible — a quarantined agent processes untrusted content and cannot take actions; a privileged agent takes actions but never sees raw untrusted content.

**Continuous authorization.** Every action re-checks authorization against the current identity and policy — not a one-time check at session start.

**Full observability by default.** Every agent action, decision, and tool call is traced and auditable, tied to the authorizing identity. Nothing the agent does is invisible.

**Bounded execution.** Every agent has timeouts, loop detection, and spend caps. A stuck, looping, or runaway agent is stopped automatically.

**A kill switch.** Every agent can be interrupted and halted by a human, immediately, at any point.

**These defaults are the paved road.** Partner teams that build on the blessed agentic platform inherit them automatically — secure by default, without having to be security experts. That's the Pillar 5 influence principle (make the secure path the easy path) applied to agents.

---

## The Bridge to the 2027 Series

Every secure default above is a preview of a full episode in the Agentic AI Roadmap 2027, and every one maps to one of the five agentic architectural gaps:

| This pillar's concern | 2027 gap | 2027 episode |
|---|---|---|
| Bounded execution, kill switch | Gap 1 · The Control Loop | Ep 3 |
| Injection-resistant context, memory poisoning | Gap 2 · Context & State Over Horizons | Ep 7 |
| Least-privilege authority, bounded blast radius | Gap 3 · The Authority Model | Ep 10 |
| Loop detection, stuck-agent handling, rollback | Gap 4 · Failure & Recovery Semantics | Ep 11 |
| Verifying the agent actually did the right thing | Gap 5 · Ground Truth & Verification | Ep 13 |
| Full observability of trajectories | (cross-cutting) | Ep 14 (Observability) |
| Evaluating frameworks, secure defaults | (cross-cutting) | Ep 16 (Safety), Ep 20 (Enterprise) |

**The security architect who masters this pillar is already thinking in the 2027 series' terms.** Agentic security isn't a separate discipline bolted onto agent engineering — it *is* agent engineering done responsibly. The five gaps are simultaneously the architecture challenges and the security challenges. That's why the 2027 series treats security as structural (Gap 3, the Authority Model, is a full episode) rather than as an afterthought.

---

## The Automation Layer, Revisited

Pillar 4 introduced designing controls so they can be *progressively operated by AI agents.* Pillar 6 closes the loop on why that's both powerful and delicate:

**An AI agent operating your security controls is itself an autonomous agent** — and therefore subject to every risk in this pillar. If you build an agent that assesses risk, assigns lanes, and configures guardrails, that agent needs:
- Least-privilege authority (it can configure controls, not disable them)
- Bounded blast radius (its high-impact decisions — like approving an Elevated Risk system — require human confirmation)
- Full observability (every decision it makes is traced and auditable)
- A kill switch (a human can stop it)
- Continuous verification (is it actually making good decisions, or has it drifted?)

**The security automation layer must be built with the same security discipline it enforces.** This is the elegant, slightly vertiginous truth of mature AI security: the controls, the agents that operate the controls, and the agents being controlled are all subject to the same principles. Getting this right is the frontier — and it's exactly where the 2027 series is heading.

---

## Files In This Pillar

| File | Concept |
|---|---|
| [`framework_risk_evaluation.py`](framework_risk_evaluation.py) | The six-dimension framework assessment |
| [`langgraph_autogen_crewai.py`](langgraph_autogen_crewai.py) | Applying the evaluation to common frameworks |
| [`secure_defaults.py`](secure_defaults.py) | The secure-default configuration for agents |
| [`injection_resistant_patterns.py`](injection_resistant_patterns.py) | Dual-LLM and isolation patterns |
| [`agentic_authority_model.py`](agentic_authority_model.py) | Least-privilege and bounded blast radius |
| [`bridge_to_2027.py`](bridge_to_2027.py) | Mapping to the five agentic gaps |

---

## The Interview Question

*"A partner team wants to build an autonomous agent using AutoGen that can access customer data and take actions on their behalf. How do you evaluate and secure it before it reaches production?"*

**The wrong answer:** "I'd review the code for vulnerabilities."

**The right answer:**
*"I'd evaluate the framework and the specific design across six architectural risk dimensions, then define secure defaults. First, the authority and action model — what can the agent actually do, and is it least-privilege? An agent that can 'take actions on a customer's behalf' needs its action set bounded to the minimum, with irreversible or high-impact actions gated behind human approval by default. Second, injection resistance — this is the critical one, because the agent accesses customer data and takes actions, so a successful prompt injection becomes privilege escalation: the attacker's instructions become the agent's actions. If the agent reads any untrusted content, I'd require isolation — ideally a dual-LLM pattern where a quarantined agent handles untrusted content and can't act, while the privileged agent that acts never sees raw untrusted input. Third, trust boundaries — AutoGen is multi-agent and conversational, so I'd assess whether a compromised agent can manipulate the others and whether shared state can be poisoned. Fourth, observability — every action and decision must be traced, auditable, and tied to the authorizing customer identity. Fifth, failure handling — timeouts, loop detection, spend caps, and a kill switch, non-negotiable. Sixth, human oversight — approval gates for high-impact actions and the ability to intervene mid-trajectory. The output is an architectural risk assessment and a set of required controls — which, given this touches customer data and takes actions, puts it squarely in the Elevated Risk lane with full threat modeling and sign-off. And I wouldn't do this as a one-off review — I'd define these as secure defaults on our blessed agentic platform, so this team and every future team inherits them automatically. That's the difference between reviewing agents one at a time and making the secure path the default path. This is also exactly where the whole discipline is heading — bounding authority, isolating untrusted input, verifying the agent did the right thing — so getting the defaults right now is what lets us scale agentic AI safely."*

That's the answer that shows you're ready for where AI security is going — and ready for the 2027 series.

---

*Previous: [← Governance & Operating Models](../05_governance_and_operating_models/README.md) · Return to [episode README](../README.md)*

*This is the final pillar of Episode 16 — and the bridge into the Agentic AI Roadmap 2027. The security layer is complete. The next series begins where this pillar points.*
