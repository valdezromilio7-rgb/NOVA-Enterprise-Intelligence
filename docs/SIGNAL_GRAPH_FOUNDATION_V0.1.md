# NOVA Signal Graph Foundation v0.1

## Purpose

The Signal Graph is the provider-agnostic relationship layer for NOVA Account Intelligence and future Product Factory capabilities.

It preserves the chain of custody from raw observation to commercial opportunity without collapsing distinct domain concepts.

## Canonical path

`ACCOUNT ↔ SOURCE ↔ OBSERVATION ↔ EVIDENCE ↔ SIGNAL ↔ CONTEXT ↔ WHY_NOW ↔ BUSINESS_PROBLEM ↔ OPPORTUNITY`

The graph is directed internally even when the domain relationship is described as bidirectional. Every edge has an explicit source, target, relation, provenance, and stable identity.

## Governance invariants

1. **Observation is raw source material.**
2. **Evidence is a representation of a claim supported by observations.**
3. **Signal is an interpretation of observations/evidence.**
4. **Context and Why Now are bounded analytical artifacts.**
5. **Business Problem is a structured problem abstraction.**
6. **Opportunity is a business abstraction.**
7. Evaluation ground truth never enters factory graph construction.
8. No provider-specific schema is introduced into the canonical graph contract.
9. Every traceable relationship carries provenance.
10. Graph serialization is deterministic for reproducibility and audit.

## Allowed relationship families

- Account → Source
- Source → Observation
- Account → Observation
- Observation → Evidence
- Observation → Signal
- Evidence → Signal
- Signal → Context
- Context → Why Now
- Why Now → Business Problem
- Business Problem → Opportunity
- Evidence → Context / Why Now / Business Problem / Opportunity

Invalid directions are rejected rather than silently normalized.

## Identity

Graph edge IDs are SHA-256-derived from the ordered relationship identity, including source/target types and IDs, relation, observed time, and provenance. Node identity remains owned by the canonical domain object.

## Serialization

`SignalGraph.serialize()` emits canonical JSON with sorted nodes, edges, metadata keys, and stable edge IDs. The same logical graph therefore produces identical serialization regardless of input ordering.

## Scope

v0.1 is intentionally infrastructure-light. It does not introduce a graph database, external provider, browser runtime, CRM, outbound action, or autonomous production behavior.

The graph is a reusable in-process contract first. Persistence and infrastructure choices remain future implementation decisions governed by NOVA architecture.

## Next layer

After this foundation is green, implement the Provider-Agnostic Data Abstraction Layer. Providers will feed normalized observations into this graph through adapters; they will not become dependencies of the canonical domain model.
