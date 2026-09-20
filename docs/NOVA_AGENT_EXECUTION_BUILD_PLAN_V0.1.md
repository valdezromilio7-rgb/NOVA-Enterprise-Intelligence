# NOVA Agent Execution / Build Plan v0.1

Build plans translate a ProductSpecification into bounded agent tasks. Every task references the specification, declares a role, objective, deliverable, dependencies, and risk level.

`approval_required` remains true by default. Creating a build plan does not authorize execution, spending, deployment, or production access.
