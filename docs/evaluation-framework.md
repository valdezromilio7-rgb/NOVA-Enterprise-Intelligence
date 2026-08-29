# Evaluation Framework — V0.1

NOVA is evaluated against a hidden ground-truth layer after each experiment.

## Primary metrics

### Detection Recall

`true events detected / total true events`

### False Discovery Rate

`false discoveries / total discoveries`

### Root Cause Accuracy

Whether the discovery identifies the underlying driver rather than only the symptom.

### Economic Accuracy

How close NOVA's estimated economic impact is to the measured impact.

### Time to Discovery

`discovery date − event start date`

### Economic Discovery Coverage

`economic value correctly identified / total economic value represented by evaluable events`

## Discovery quality

A discovery should contain:

- title;
- description;
- affected entities;
- evidence;
- probable cause;
- estimated economic impact;
- confidence.

## Evaluation principle

The evaluation system must not reward NOVA for guessing event names. It should reward evidence-backed identification of economically meaningful patterns and causes.

## Counterfactual evaluation

Future versions will compare the simulated outcome without intervention against an outcome after a validated NOVA recommendation. This will allow measurement of economic value attributable to intervention.
