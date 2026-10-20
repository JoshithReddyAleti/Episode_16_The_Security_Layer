"""
risk_tiering_engine.py — Multi-factor AI risk tiering into delivery lanes.

Demonstrates:
- Seven-factor risk scoring
- Dominant-factor combination with escalation
- Delivery lane routing (Standard / Elevated Risk / Experimentation)
- Auditable Risk Decision Records
- Framework calibration metrics

Run:
    python risk_tiering_engine.py
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import IntEnum


class Level(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Lane:
    EXPERIMENTATION = "Experimentation"
    STANDARD = "Standard"
    ELEVATED = "Elevated Risk"


FACTORS = [
    "data_sensitivity",
    "decision_consequence",
    "autonomy_level",
    "population_scale",
    "model_provenance",
    "regulatory_exposure",
    "reversibility",
]


@dataclass
class Initiative:
    name: str
    data_sensitivity: Level
    decision_consequence: Level
    autonomy_level: Level
    population_scale: Level
    model_provenance: Level
    regulatory_exposure: Level
    reversibility: Level
    # Sandbox flags
    uses_production_data: bool = True
    has_real_world_impact: bool = True
    # Hard regulatory escalator
    regulatory_high_risk_category: bool = False

    def factor_scores(self) -> dict:
        return {f: getattr(self, f) for f in FACTORS}


@dataclass
class RiskDecision:
    initiative: str
    lane: str
    factor_scores: dict
    dominant_factor: str
    rationale: str
    required_controls: list = field(default_factory=list)


def route(initiative: Initiative) -> RiskDecision:
    scores = initiative.factor_scores()

    # Experimentation override: no prod data, no real-world impact
    if not initiative.uses_production_data and not initiative.has_real_world_impact:
        return RiskDecision(
            initiative=initiative.name,
            lane=Lane.EXPERIMENTATION,
            factor_scores=scores,
            dominant_factor="sandbox",
            rationale="No production data and no real-world impact; sandboxed. "
                      "Minimal but bounded controls; caged environment.",
            required_controls=["sandbox_isolation", "no_prod_data_egress", "usage_monitoring"],
        )

    # Determine dominant factor and escalation
    lane = Lane.STANDARD
    high_factors = [f for f, v in scores.items() if v == Level.HIGH]
    critical_factors = [f for f, v in scores.items() if v == Level.CRITICAL]

    dominant = max(scores, key=lambda f: scores[f])
    reasons = []

    if critical_factors:
        lane = Lane.ELEVATED
        reasons.append(f"critical factor(s): {', '.join(critical_factors)}")
    elif len(high_factors) >= 2:
        lane = Lane.ELEVATED
        reasons.append(f"multiple high factors: {', '.join(high_factors)}")
    elif len(high_factors) == 1:
        reasons.append(f"single high factor ({high_factors[0]}), no escalation")
    else:
        reasons.append("no high or critical factors")

    # Regulatory hard escalator
    if initiative.regulatory_high_risk_category:
        lane = Lane.ELEVATED
        reasons.append("regulatory high-risk category (hard escalator)")

    # Required controls scale with lane
    if lane == Lane.ELEVATED:
        controls = ["full_threat_model", "human_signoff", "all_guardrails",
                    "independent_validation", "quarterly_review", "adr_required"]
    else:
        controls = ["standard_guardrails", "output_logging", "automated_policy_checks",
                    "annual_review"]

    return RiskDecision(
        initiative=initiative.name,
        lane=lane,
        factor_scores=scores,
        dominant_factor=dominant,
        rationale="; ".join(reasons),
        required_controls=controls,
    )


def print_decision(d: RiskDecision):
    print(f"\n{'='*64}")
    print(f"  Initiative: {d.initiative}")
    print(f"{'='*64}")
    print(f"  Factor scores:")
    for f, v in d.factor_scores.items():
        bar = "#" * int(v)
        print(f"    {f:24s} {v.name:9s} {bar}")
    print(f"  Dominant factor: {d.dominant_factor}")
    print(f"  --> LANE: {d.lane}")
    print(f"  Rationale: {d.rationale}")
    print(f"  Required controls: {', '.join(d.required_controls)}")


def main():
    initiatives = [
        # Marketing chatbot — low risk, should be Standard
        Initiative(
            name="Marketing FAQ chatbot",
            data_sensitivity=Level.LOW,
            decision_consequence=Level.LOW,
            autonomy_level=Level.LOW,
            population_scale=Level.HIGH,      # public-facing
            model_provenance=Level.LOW,
            regulatory_exposure=Level.LOW,
            reversibility=Level.LOW,
        ),
        # Loan decisioning — critical, should be Elevated
        Initiative(
            name="Loan decisioning model",
            data_sensitivity=Level.CRITICAL,   # financial PII
            decision_consequence=Level.CRITICAL,  # affects access to money
            autonomy_level=Level.HIGH,
            population_scale=Level.HIGH,
            model_provenance=Level.MEDIUM,
            regulatory_exposure=Level.CRITICAL,   # SR 11-7, fair lending
            reversibility=Level.HIGH,
            regulatory_high_risk_category=True,
        ),
        # Internal RAG assistant — medium, should be Standard
        Initiative(
            name="Internal engineering RAG",
            data_sensitivity=Level.MEDIUM,
            decision_consequence=Level.MEDIUM,
            autonomy_level=Level.LOW,
            population_scale=Level.MEDIUM,
            model_provenance=Level.LOW,
            regulatory_exposure=Level.LOW,
            reversibility=Level.LOW,
        ),
        # Autonomous agent prototype — sandboxed, should be Experimentation
        Initiative(
            name="Autonomous ops agent (prototype)",
            data_sensitivity=Level.HIGH,
            decision_consequence=Level.HIGH,
            autonomy_level=Level.CRITICAL,
            population_scale=Level.LOW,
            model_provenance=Level.MEDIUM,
            regulatory_exposure=Level.MEDIUM,
            reversibility=Level.HIGH,
            uses_production_data=False,
            has_real_world_impact=False,
        ),
        # Customer support agent that acts — two high factors, Elevated
        Initiative(
            name="Customer support agent (acts on accounts)",
            data_sensitivity=Level.HIGH,       # customer data
            decision_consequence=Level.HIGH,   # takes account actions
            autonomy_level=Level.MEDIUM,
            population_scale=Level.HIGH,
            model_provenance=Level.LOW,
            regulatory_exposure=Level.MEDIUM,
            reversibility=Level.MEDIUM,
        ),
    ]

    print("AI Risk Tiering Engine — Routing Initiatives Into Delivery Lanes")

    decisions = [route(i) for i in initiatives]
    for d in decisions:
        print_decision(d)

    # Calibration metrics
    print(f"\n{'='*64}")
    print("  Framework Calibration Metrics")
    print(f"{'='*64}")
    from collections import Counter
    lane_dist = Counter(d.lane for d in decisions)
    total = len(decisions)
    for lane in [Lane.STANDARD, Lane.ELEVATED, Lane.EXPERIMENTATION]:
        count = lane_dist.get(lane, 0)
        pct = count / total * 100
        print(f"    {lane:16s}: {count}/{total} ({pct:.0f}%)")
    elevated_pct = lane_dist.get(Lane.ELEVATED, 0) / total * 100
    print()
    if elevated_pct > 60:
        print("    ⚠️  >60% in Elevated — factors may be too conservative (bottleneck risk)")
    elif elevated_pct < 10:
        print("    ⚠️  <10% in Elevated — factors may be too loose (exposure risk)")
    else:
        print(f"    ✓ Elevated at {elevated_pct:.0f}% — healthy discrimination between lanes")

    print()
    print("Reading the result: the worst single factor drives the lane, regulation")
    print("is a hard escalator, and sandboxed work is caged into Experimentation.")
    print("The same initiative always gets the same lane — that is auditability.")


if __name__ == "__main__":
    main()
