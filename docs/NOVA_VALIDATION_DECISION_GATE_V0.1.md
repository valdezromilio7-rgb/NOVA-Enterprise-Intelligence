# NOVA Validation Decision Gate v0.1

The validation decision gate converts an evidence-backed experiment result into a traceable decision.

- **passed** -> proceed_to_build_review
- **failed** -> kill_or_reframe
- **inconclusive** -> hold_and_retest

The gate never directly authorizes spending, production, or scaling. A passed validation proceeds only to build review under NOVA governance. Every decision must reference the experiment's result evidence.
