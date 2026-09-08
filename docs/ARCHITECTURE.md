# Universal Dragon Core Architecture

## Design Principle

Universal Dragon separates reasoning from authority.

```text
AI / reasoning proposes
        |
        v
policy evaluates
        |
        v
approval authorizes when required
        |
        v
bounded tool adapter executes
        |
        v
verification proves the result
        |
        v
audit receipt records the outcome
```

The current foundation implements the routing, policy, approval decision, and receipt-planning boundary. It intentionally does not implement unrestricted tool execution.

## Current Request Flow

```text
POST /api/chat
    |
    +--> validate mode + message size
    |
    +--> route to NOVA / EVE / DRAGON core mode
    |
    +--> return core-only response

POST /api/actions/plan
    |
    +--> validate action proposal
    |
    +--> classify supplied risk
    |
    +--> apply external-effect rule
    |
    +--> return policy decision + receipt
    |
    +--> never execute the action
```

## Policy States

| Risk / effect | Decision | State |
| --- | --- | --- |
| Low, no external effect | allow | ready |
| Medium, no external effect | review | waiting_policy |
| High | require_approval | waiting_approval |
| Any external effect | require_approval | waiting_approval |

An external effect means the action can change something outside the core process, for example sending a message, making a call, changing a remote account, controlling hardware, purchasing, deleting, or modifying external state.

## Intended Full State Machine

Later execution layers should use explicit durable states rather than guessing whether an operation happened:

```text
RECEIVED
  -> VALIDATED
  -> PLANNED
  -> WAITING_POLICY
  -> WAITING_APPROVAL
  -> APPROVED
  -> EXECUTING
  -> VERIFYING
  -> COMPLETED

Any state may transition to FAILED with an error receipt.
```

Retries of externally-visible operations must use idempotency keys so reconnects do not accidentally repeat a sensitive action.

## Model Provider Boundary

A model provider is deliberately not hard-coded into the core. A future provider adapter should:

1. receive a validated conversation request;
2. return structured reasoning or a proposed tool plan;
3. have no direct authority to execute tools;
4. have explicit timeouts and bounded retries;
5. avoid returning raw provider exceptions to clients;
6. keep provider keys in deployment secrets, never in Git.

## Tool Adapter Boundary

Future tool adapters should be capability-specific, such as:

- `read_system_health`
- `open_approved_app`
- `query_public_information`
- `control_approved_device`
- `draft_message`

Avoid an unrestricted generic shell capability for model-generated commands.

## Approval Boundary

Approval must be bound to the exact action being approved. An approval record should contain at least:

- action ID
- action type
- normalized parameters or parameter hash
- requesting identity/session
- risk level
- approval timestamp
- expiration

Changing sensitive parameters after approval must invalidate the approval.

## Verification Boundary

A successful command or API response is not enough to mark an action complete. The system should verify post-conditions where possible.

Example:

```text
restart service
  -> command accepted
  -> query service state
  -> health check passes
  -> mark COMPLETED
```

## Audit Boundary

Receipts must never contain secrets. Store only the metadata needed to explain what was requested, how policy decided, what was approved, what executed, and how the result was verified.

## Deployment Boundary

Public deployments must not expose:

- API keys or tokens
- private IP addresses
- internal device identifiers unless required and access-controlled
- raw provider errors
- unrestricted administrative endpoints

CORS should use an explicit allow-list configured by environment.

## Next Safe Implementation Stages

1. persistent audit/receipt storage;
2. authenticated approval endpoint with expiry;
3. pluggable NOVA/EVE model-provider adapter;
4. one low-risk read-only tool adapter;
5. verification and idempotency support;
6. backup and rollback modules for controlled repository/deployment changes.

Each stage should arrive with tests before expanding capability.
