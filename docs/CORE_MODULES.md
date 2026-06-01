# Core Modules

Universe Dragon Core is organized around small safe modules.

## Modules

1. Doctor Check
   - reads system state
   - reports problems
   - does not auto-fix without approval

2. Backup Engine
   - creates a safe copy before changes
   - saves file list and timestamp

3. Patch Engine
   - prepares small controlled changes
   - runs only after approval

4. Error Handler
   - records failures
   - explains what happened
   - suggests safe recovery

5. Rollback Flow
   - restores last known working state
   - used when patch or deploy fails

6. Approval Gate
   - asks Aslam before risky actions
   - blocks silent destructive commands

## Rule

Start small. Keep it safe. Expand only after testing.
