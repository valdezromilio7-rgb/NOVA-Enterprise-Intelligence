# NOVA Product Factory — Decision Gates v0.1

**Status:** Proposed / Governance
**Authority:** NOVA CORP

## 1. Principle

The factory may automate execution, but authority is explicit. A workflow cannot infer permission from a successful previous task.

## 2. Gate 0 — Discovery

**Default:** autonomous.

Input: signals.
Output: ranked opportunities and evidence ledgers.

May execute automatically when no material external side effect occurs.

## 3. Gate 1 — Validation Authorization

**Default:** recommendation + approval when required.

Human approval is required for:

- material spend;
- external contractual commitments;
- sensitive/personal data processing;
- elevated legal/security/reputational risk;
- actions outside a pre-approved validation budget.

Output: authorized validation plan.

## 4. Gate 2 — Build Authorization

**Default:** human approval.

Required before:

- material engineering expenditure;
- creation of a production-bound product;
- new recurring infrastructure commitments;
- material third-party contracts;
- handling of sensitive or regulated data.

The approval must reference the opportunity and product specification version being authorized.

## 5. Gate 3 — Production Release

A release candidate must pass automated readiness checks covering:

- tests;
- security;
- dependency health;
- configuration;
- secrets handling;
- observability;
- rollback capability;
- acceptance criteria;
- known-risk review.

Human approval is mandatory for high-risk, regulated, security-sensitive, or materially financial systems unless NOVA CORP has explicitly delegated release authority under a documented policy.

## 6. Gate 4 — Scale / Hold / Kill / Pivot

Inputs:

- customer evidence;
- revenue and unit economics where applicable;
- retention/usage;
- operational reliability;
- acquisition economics;
- strategic fit;
- risk profile.

The factory generates the recommendation. NOVA CORP retains strategic authority unless a documented delegation applies.

## 7. Emergency controls

Any authorized operator or security mechanism may suspend an agent, workflow, deployment, or product when predefined safety thresholds are breached.

Emergency suspension must create an audit event and require explicit reactivation.

## 8. Approval record

Every human approval must capture:

- approver identity;
- timestamp;
- decision;
- object/version approved;
- scope;
- constraints;
- expiration where applicable;
- rationale when material.

## 9. No implicit escalation

If required approval is missing, the workflow stops or moves to `WAITING_FOR_APPROVAL`.

Agents must never interpret silence as approval.

## 10. Delegation policy

NOVA CORP may delegate authority by policy, but every delegation must define:

- scope;
- maximum financial exposure;
- allowed product/domain classes;
- environment;
- duration;
- revocation condition;
- responsible owner.

Delegation is versioned and auditable.
