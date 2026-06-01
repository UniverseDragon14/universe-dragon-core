# Universe Dragon Core

Universe Dragon Core is a small foundation repository for the Universal Dragon system architecture.

This repo is for the clean core idea, not for private keys, backend secrets, or unstable experiments.

## Purpose

The core tracks the basic architecture shared across Universal Dragon projects:

- project identity
- safe automation rules
- assistant-first workflow
- backup and rollback discipline
- module planning
- future NOVA / EVE integration

## Core Workflow

```text
doctor -> backup -> patch -> test -> approval -> deploy -> rollback ready
```

## Small Capacity Scope

This repository starts as documentation and lightweight architecture only.

No risky automation is enabled here.

## Standard Modules

- doctor check
- error handler
- backup engine
- patch engine
- rollback flow
- approval gate
- deployment notes

## Safety

- no private API keys
- no tokens
- no private IP addresses
- no silent destructive commands
- approval required before risky actions

## Status

Small foundation completed.
