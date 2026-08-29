# ANTIGRAVITY ACTION LOGGING & OPERATING RULE (MASTER STANDARD)

## Obsidian Vault Target
- **Vault Name**: `AntiGravity Logs`
- **Vault Root Path**: `C:\Users\bradl\Documents\Antigravity Logs\AntiGravity Logs`
- **Obsidian Executable**: `C:\Program Files\Obsidian\Obsidian.exe`

---

## 1. PURPOSE
This rule is the shared memory system for every Antigravity instance across all machines, IDEs, and devices (Laptop, Desktop, Phone, etc.).
- Preserves project history across sessions.
- Prevents repeated explanations.
- Tracks meaningful actions immediately.
- Provides future sessions with accurate context.

---

## 2. SCOPE OF LOGGING
**DO NOT log**:
- Normal conversational back-and-forth
- User chat messages word-for-word
- Internal agent thinking/reasoning
- Trivial read-only exploratory actions that do not alter the project state

**DO log**:
- File modifications and code edits
- Created/deleted files
- Commands executed (builds, installs, git, migrations, tests)
- Deployments & hosting updates
- Configuration changes
- Debugging attempts & error resolutions
- Architecture & technical decisions
- Verification results

---

## 3. TIMING & PROTOCOL

### Before Making Changes (Session Start / Task Start)
1. Read the latest relevant log files inside `C:\Users\bradl\Documents\Antigravity Logs\AntiGravity Logs`.
2. Determine the current project state, previous changes, outstanding tasks, and known issues before proceeding.

### During Work (Immediate Action Logging)
- As soon as a meaningful action or change is completed, append an **Action Log Entry** using the exact template format below to the active project session log file in the Obsidian vault.
- Never wait until the end of the session to log actions.

### Closing Session Log (Only on Explicit Command)
- Triggered **ONLY** when the user says: `"Done"`, `"Finished"`, `"End session"`, or `"Stop editing"`.
- Appends the standard **Closing Session Log** summarizing overall work, state, remaining tasks, and handoff notes for the next Antigravity session.

---

## 4. MASTER LOG FORMAT TEMPLATES

### A. Action Log Entry Template
```markdown
## ACTION-[NUMBER]

Date: YYYY-MM-DD
Time: HH:MM (Timezone)
Antigravity Device: [Device / OS]
Antigravity Version/Model: [Model Name]
Project: [Project Name]
Working Location: [Workspace Root Path]

Requested By:
(User / Antigravity recommendation / Required fix)

Action:
[Brief descriptive title of the action]

Target:
Files: [Paths to modified/created/deleted files]
Components: [Relevant components]
Application: [Application Name]
Website: [Website / URL if applicable]
Platform: [Node / Vite / OS / etc.]
Environment: [Development / Staging / Production]

Reason:
[Why this change was made]

Change Details:
Before:
[Summary or snippet of previous state]
After:
[Summary or snippet of updated state]

Tools / Commands Used:
[Tools or terminal commands executed]

Result:
SUCCESS / PARTIAL / FAILED / REVERTED

Verification:
[How the change was tested and verified]

Notes For Future Antigravity Sessions:
[Key points for the next Antigravity instance]
```

### B. Closing Session Log Template
```markdown
# CLOSING SESSION LOG

Session ID: [Session-YYYYMMDD-HHMM]
Date: YYYY-MM-DD
Device: [Device Name / OS]
Project: [Project Name]

## What Was Completed

## All Changes Made

Files changed:
Features added:
Bugs fixed:
Deployments completed:
Configurations changed:

## Current Project State

Completed:
In Progress:
Broken:
Needs Attention:

## Outstanding Tasks

1.
2.
3.

## Important Information For Next Antigravity

## Final Verification

[ ] Changes saved
[ ] Application/site tested
[ ] Deployment verified
[ ] No known errors remaining
[ ] Logs updated

Session Status:
COMPLETE / PARTIAL / BLOCKED / FAILED
```

---

## 5. GLOBAL ANTIGRAVITY INSTRUCTIONS
1. `AntiGravity Logs` is the source of project history.
2. Always read relevant previous logs before starting.
3. Never silently modify project files.
4. Never claim completion without verification.
5. Record failures and failed attempts.
6. Record important decisions.
7. Keep logs detailed but efficient.
8. Current project files override old logs.
9. Resolve conflicts by verifying current reality and updating logs.
10. The purpose is seamless handoff between Antigravity sessions across all devices.
