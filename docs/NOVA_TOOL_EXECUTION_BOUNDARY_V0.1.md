# NOVA Tool Execution Boundary v0.1

## Purpose

Provide the first governed boundary between an agent capability policy and a concrete tool invocation.

## Contract

A tool execution requires:

1. an explicit agent policy;
2. a capability allowed by that policy;
3. an approval record when the capability is marked approval-required;
4. optional task binding for sensitive execution;
5. a non-empty output reference.

The executor returns a typed result containing the tool name, capability, agent identity, status, timestamp, and output reference.

## Governance

The executor does not create permissions, credentials, budgets, or approvals. It only consumes existing authorization artifacts and invokes the supplied callable.

This is intentionally provider-agnostic: real integrations can be added behind adapters without changing the governance contract.
