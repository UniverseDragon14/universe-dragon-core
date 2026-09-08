# Next Safe Development Slice

After this foundation is merged, the next implementation should be **one authenticated, read-only capability** rather than broad device control.

Recommended order:

1. add persistent action/audit storage;
2. add authenticated sessions and approval records;
3. add a pluggable NOVA/EVE model adapter with timeouts;
4. add one read-only health tool;
5. verify the tool result before reporting completion;
6. add idempotency before any externally-visible write action.

Do not add unrestricted shell execution as a shortcut.
