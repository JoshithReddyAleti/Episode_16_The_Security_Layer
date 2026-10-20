"""
policy_as_code_demo.py — Policy-as-code enforcement (Sentinel/OPA-style).

Demonstrates:
- Decomposing prose policy into decidable predicates
- Enforcement levels (advisory / soft-mandatory / hard-mandatory)
- Enforcement mapped to risk lanes
- Deployment-gate evaluation with pass/block/override
- Evidence generation for the audit trail

Run:
    python policy_as_code_demo.py
"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class Enforcement(Enum):
    ADVISORY = "advisory"            # warn, never block
    SOFT_MANDATORY = "soft"          # block, overridable with approval
    HARD_MANDATORY = "hard"          # block, never overridable


@dataclass
class Deployment:
    """The AI deployment being evaluated against policy."""
    name: str
    lane: str
    handles_pii: bool
    data_classification: str          # 'general' | 'pii' | 'phi'
    guardrails: list
    provider_baa_signed: bool
    has_signoff: bool
    provider_region: str
    tenant_required_region: str
    takes_actions: bool
    has_authority_policy: bool


@dataclass
class PolicyResult:
    policy_name: str
    passed: bool
    enforcement: Enforcement
    message: str


@dataclass
class Verdict:
    deployment: str
    allowed: bool
    overridable: bool
    results: list = field(default_factory=list)
    evidence: dict = field(default_factory=dict)


# --- Policies as decidable predicates ---

def policy_pii_guardrail(d: Deployment) -> PolicyResult:
    """PII-handling systems must have PII + output guardrails. (hard)"""
    if d.handles_pii:
        ok = "pii_detection" in d.guardrails and "output_filtering" in d.guardrails
    else:
        ok = True
    return PolicyResult(
        "requires_pii_guardrail", ok, Enforcement.HARD_MANDATORY,
        "PII guardrails present" if ok else "PII handled but PII/output guardrails missing",
    )


def policy_phi_baa(d: Deployment) -> PolicyResult:
    """PHI requires a signed provider BAA. (hard)"""
    if d.data_classification == "phi":
        ok = d.provider_baa_signed
    else:
        ok = True
    return PolicyResult(
        "requires_baa_for_phi", ok, Enforcement.HARD_MANDATORY,
        "BAA present or not PHI" if ok else "PHI processed without signed provider BAA",
    )


def policy_elevated_signoff(d: Deployment) -> PolicyResult:
    """Elevated Risk requires sign-off. (soft — overridable by approver)"""
    if d.lane == "Elevated Risk":
        ok = d.has_signoff
    else:
        ok = True
    return PolicyResult(
        "requires_elevated_signoff", ok, Enforcement.SOFT_MANDATORY,
        "Sign-off present or not Elevated" if ok else "Elevated Risk without recorded sign-off",
    )


def policy_residency(d: Deployment) -> PolicyResult:
    """Provider region must match tenant's required region. (hard)"""
    ok = d.provider_region == d.tenant_required_region
    return PolicyResult(
        "residency_match", ok, Enforcement.HARD_MANDATORY,
        f"Region {d.provider_region} matches requirement" if ok
        else f"Region {d.provider_region} != required {d.tenant_required_region}",
    )


def policy_action_authority(d: Deployment) -> PolicyResult:
    """Systems that take actions must declare an authority policy. (soft)"""
    if d.takes_actions:
        ok = d.has_authority_policy
    else:
        ok = True
    return PolicyResult(
        "requires_authority_policy", ok, Enforcement.SOFT_MANDATORY,
        "Authority policy present or no actions" if ok
        else "Takes actions without a declared authority policy",
    )


def policy_advisory_review_date(d: Deployment) -> PolicyResult:
    """Advisory: recommend a review date. Never blocks."""
    # Always 'passes' since advisory — just informational
    return PolicyResult(
        "recommends_review_date", True, Enforcement.ADVISORY,
        "Advisory: ensure a review date is set",
    )


POLICIES = [
    policy_pii_guardrail,
    policy_phi_baa,
    policy_elevated_signoff,
    policy_residency,
    policy_action_authority,
    policy_advisory_review_date,
]


def evaluate_deployment(d: Deployment) -> Verdict:
    verdict = Verdict(deployment=d.name, allowed=True, overridable=True)
    hard_fail = False
    soft_fail = False

    for policy in POLICIES:
        result = policy(d)
        verdict.results.append(result)
        verdict.evidence[result.policy_name] = {
            "passed": result.passed,
            "enforcement": result.enforcement.value,
            "message": result.message,
        }
        if not result.passed:
            if result.enforcement == Enforcement.HARD_MANDATORY:
                hard_fail = True
            elif result.enforcement == Enforcement.SOFT_MANDATORY:
                soft_fail = True
            # advisory failures don't affect allow/block

    if hard_fail:
        verdict.allowed = False
        verdict.overridable = False
    elif soft_fail:
        verdict.allowed = False
        verdict.overridable = True

    return verdict


def print_verdict(v: Verdict):
    print(f"\n{'='*64}")
    print(f"  Deployment: {v.deployment}")
    print(f"{'='*64}")
    for r in v.results:
        mark = "✓" if r.passed else "✗"
        level = f"[{r.enforcement.value}]"
        print(f"  {mark} {r.policy_name:26s} {level:10s} {r.message}")
    print("  " + "-" * 60)
    if v.allowed:
        print("  RESULT: ✓ DEPLOYMENT ALLOWED")
    elif v.overridable:
        print("  RESULT: ✗ BLOCKED (soft) — overridable by authorized approver with justification")
    else:
        print("  RESULT: ✗ BLOCKED (hard) — NOT overridable")


def main():
    print("Policy-as-Code — Deployment Gate Evaluation")
    print("Prose policy decomposed into decidable, enforced predicates.")

    deployments = [
        # Compliant Standard deployment
        Deployment(
            name="Internal RAG (compliant)",
            lane="Standard",
            handles_pii=True,
            data_classification="pii",
            guardrails=["pii_detection", "output_filtering", "injection_detection"],
            provider_baa_signed=True,
            has_signoff=True,
            provider_region="us-east-1",
            tenant_required_region="us-east-1",
            takes_actions=False,
            has_authority_policy=False,
        ),
        # PHI without BAA — hard block
        Deployment(
            name="Clinical assistant (no BAA)",
            lane="Elevated Risk",
            handles_pii=True,
            data_classification="phi",
            guardrails=["pii_detection", "output_filtering"],
            provider_baa_signed=False,          # HARD FAIL
            has_signoff=True,
            provider_region="us-east-1",
            tenant_required_region="us-east-1",
            takes_actions=False,
            has_authority_policy=False,
        ),
        # Elevated without sign-off — soft block (overridable)
        Deployment(
            name="Analytics model (no sign-off)",
            lane="Elevated Risk",
            handles_pii=False,
            data_classification="general",
            guardrails=["output_filtering"],
            provider_baa_signed=True,
            has_signoff=False,                  # SOFT FAIL
            provider_region="us-east-1",
            tenant_required_region="us-east-1",
            takes_actions=False,
            has_authority_policy=False,
        ),
        # Residency violation — hard block
        Deployment(
            name="EU tenant on US region",
            lane="Standard",
            handles_pii=True,
            data_classification="pii",
            guardrails=["pii_detection", "output_filtering"],
            provider_baa_signed=True,
            has_signoff=True,
            provider_region="us-east-1",        # HARD FAIL vs required
            tenant_required_region="eu-west-1",
            takes_actions=False,
            has_authority_policy=False,
        ),
        # Agent taking actions without authority policy — soft block
        Deployment(
            name="Support agent (no authority policy)",
            lane="Elevated Risk",
            handles_pii=True,
            data_classification="pii",
            guardrails=["pii_detection", "output_filtering", "injection_detection"],
            provider_baa_signed=True,
            has_signoff=True,
            provider_region="us-east-1",
            tenant_required_region="us-east-1",
            takes_actions=True,
            has_authority_policy=False,         # SOFT FAIL
        ),
    ]

    for d in deployments:
        print_verdict(evaluate_deployment(d))

    print(f"\n{'='*64}")
    print("  Reading the result")
    print(f"{'='*64}")
    print("  Hard-mandatory failures (no BAA for PHI, residency violation) block")
    print("  with NO override — these are non-negotiable.")
    print("  Soft-mandatory failures (missing sign-off, missing authority policy)")
    print("  block but an authorized approver can override with justification.")
    print("  Advisory checks inform but never block.")
    print("  Every evaluation emits evidence — the audit trail of enforcement.")


if __name__ == "__main__":
    main()
