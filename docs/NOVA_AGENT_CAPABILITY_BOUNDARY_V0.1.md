# NOVA Agent Capability Boundary v0.1

Agents receive explicit capabilities rather than implicit authority. Capabilities include repository read/write, tests, PR creation, deployment, spending, and secret access.

Sensitive capabilities can be marked approval-required. Denied capabilities raise a permission error. This contract establishes least privilege before connecting real execution tools.
