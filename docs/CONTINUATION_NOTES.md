# Continuation Notes

This branch continues the Universal Dragon Core work after the earlier Claude coding-agent task failed during model initialization and produced no file changes.

## What this continuation changes

- replaces the misleading mock `DRAGON: Executing` response with truthful routing that performs no external action;
- adds a small policy engine for low, medium, and high risk action proposals;
- forces externally-visible effects into an approval-required state;
- emits action-planning receipts without executing tools;
- validates chat and action-plan inputs;
- adds safe generic server error handling;
- restricts CORS to an environment-configured allow-list;
- adds health and capability endpoints;
- adds automated tests and GitHub Actions CI;
- documents the architecture and next safe implementation stages.

## Deliberate non-goals

This branch does not claim to provide:

- a configured LLM/model provider;
- unrestricted shell access;
- device-control execution;
- authenticated approvals;
- persistent audit storage;
- completed backup/rollback tooling.

Those are separate stages and should only be added with tests and explicit security boundaries.
