# NOVA Public Context + Why Now v0.1

NOVA now has canonical, account-optional Context and Why Now contracts. They extend the real public-data path without introducing fake accounts.

Flow:

PROVIDER → NORMALIZED OBSERVATION → SIGNAL → EVIDENCE → CONTEXT → WHY NOW

Account Intelligence remains compatible through its existing account-scoped constructors, while new generic consumers use the canonical contracts.

Rules:
- account_id may be None for public/global intelligence;
- evidence references remain explicit;
- Why Now does not infer urgency silently;
- deterministic IDs preserve lineage;
- no provider-specific types enter canonical contracts;
- no Opportunity is created at this stage.
