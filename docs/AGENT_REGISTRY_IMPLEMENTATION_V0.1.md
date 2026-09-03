# NOVA Agent Registry — Implementation v0.1

**Status:** Implemented / Foundational
**Authority:** NOVA CORP

## 1. Scope

v0.1 implements a deterministic, in-memory registry for bounded Product Factory agents.
It establishes capability declarations and a least-privilege authorization check without
introducing an external orchestration platform or provider-specific dependency.

## 2. Canonical implementation

`factory/agents/registry.py` provides:

- `AgentStatus` lifecycle: `DRAFT -> EVALUATING -> APPROVED -> ACTIVE -> RESTRICTED -> RETIRED`;
- immutable `AgentDefinition` records;
- explicit task requirements through `TaskAuthorization`;
- `AgentRegistry` registration, lookup, listing, and authorization;
- machine-readable `AuthorizationResult` reasons.

## 3. Authorization rules

An agent is authorized only when all configured checks pass:

1. agent status is `ACTIVE`;
2. task is not forbidden;
3. task is within the allowed task set when one is declared;
4. required tools are granted;
5. required data access is granted;
6. required write access is granted;
7. budget exposure does not exceed the agent financial limit.

The registry authorizes capability. It does not execute work, grant production credentials,
or override governance gates.

## 4. Evaluation rule

Agents in `APPROVED` or `ACTIVE` status must declare an evaluation suite. This prevents
permission expansion from being represented only by configuration or prompts.

## 5. Deliberate v0.1 boundaries

Not yet implemented:

- persistent registry storage;
- cryptographic identity/credential issuance;
- provider/model routing;
- execution event persistence;
- concurrency quotas;
- runtime secret management;
- automatic lifecycle promotion;
- production environment authorization.

These belong to subsequent execution/orchestration layers and must preserve this registry
as the capability control point.

## 6. Test contract

`tests/factory/test_agent_registry.py` verifies registration, duplicate prevention, bounded
authorization, forbidden tasks, tool/write restrictions, financial limits, inactive-agent
denial, and evaluation requirements.
