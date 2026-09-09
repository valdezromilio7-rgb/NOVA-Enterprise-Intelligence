# NOVA Account Intelligence — Business Problem Bridge v0.1

## Purpose

Convert an evidence-backed Account Intelligence context into an explicit business problem and then reuse the canonical NOVA `Opportunity` contract.

## Flow

`ACCOUNT → SIGNAL → CONTEXT → WHY NOW → BUSINESS PROBLEM → OPPORTUNITY`

The bridge is deterministic and provider-agnostic. It does not authorize execution, assign commercial scores, or invent evidence.

## Business Problem contract

Each problem preserves:

- account and signal identity;
- context and Why Now versions;
- problem statement;
- current solution/workaround;
- identified gap;
- desired outcome;
- evidence references;
- confidence and provenance;
- deterministic identifier and contract version.

## Evidence boundary

Observation references are not automatically canonical Evidence IDs. Until the Evidence Engine exists, they remain explicit references in the business problem and opportunity metadata. `Opportunity.evidence_ids` stays empty rather than relabeling observations as evidence.

## Governance

1. Context must contain explicit facts.
2. Why Now is an assessment, not a fact.
3. A business problem requires evidence references.
4. Context and Why Now must belong to the same account and signal.
5. The bridge does not bypass the Opportunity Engine, Agent Registry, Execution Contract, Orchestrator, Workflow State, or Audit Trail.
6. No external connector, CRM write, outbound action, autonomous spend, or production side effect is introduced by this layer.

## Next layer

The next P0 integration is an end-to-end deterministic evaluation from raw observations through signals, scoring, context, Why Now, business problem, and opportunity, followed by evidence-backed verification metrics.
