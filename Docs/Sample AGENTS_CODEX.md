### Environment Fallback
- Always prioritize Python 3 over Python 2.
- Use `python3` explicitly for executing any python scripts on Unix-like systems.
- On Windows, use `python` only when the active environment is already known to be Python 3.
- Do not assume system `python` points to a modern release.

### Project Scope
- This repository contains Prompter, a standalone desktop prompt-building app.
- Primary target is Windows 11.
- Secondary target is macOS from the same source code.
- Keep the app local-first and clipboard-focused.
- Do not add direct Codex, Ollama, Claude, VS Code, or network integrations unless explicitly requested.

### Architecture Boundary
- Keep prompt assembly logic in backend/application code, not inside UI event handlers.
- Keep GUI code focused on layout, user interaction, state updates, and calling prompt-generation functions.
- Keep packaging scripts under `packaging/`.
- Keep tests under `tests/`.
- If a package is not available, do not design a work-around. Stop and ask that the desired package be installed.

### Terse Responses
Cut out all conversational filler, preambles, and polite explanations. Return only the requested code block, minimal bullet points, or the direct structural diff.

### Token Economy

Minimize token usage.

- Read only the files required for the current task.
- Never summarize unrelated code.
- Avoid opening large files unless the task explicitly requires them.
- Prefer searching for symbols over reading entire files.
- Stop reading once sufficient context has been gathered.

### Minimal Changes

When modifying code:

- Produce the smallest correct change.
- Prefer editing existing functions over rewriting them.
- Do not reformat unrelated code.
- Preserve existing style.
- Do not rename variables, functions, or files unless required.

### Diff Preference

Unless explicitly requested otherwise:

- Apply minimal edits.
- Do not regenerate an entire file for localized changes.
- Do not duplicate unchanged code.

### Scope Discipline

Stay inside the requested scope.

Do not:

- perform opportunistic refactoring
- modernize unrelated code
- improve comments outside the requested area
- fix unrelated warnings
- reorganize project structure
- add integrations, persistence, templates, or history beyond the requested version

unless explicitly instructed.

### Stop Conditions

When blocked:

- Ask one concise question.
- Do not speculate.
- Do not invent missing APIs.
- Do not implement placeholders without permission.

### Prompt Contract Template

Every task should be interpreted using this contract.

Goal:
<what should be true>

Context:
<only relevant files or functionality>

Constraints:
<what must not change>

Success:
<how success is verified>

Anything outside this contract is out of scope.

### Prompter Defaults

When implementing Prompter features:

- Optimize for fast manual prompt creation.
- Keep the main window usable without opening secondary dialogs.
- The primary output is text copied to the clipboard.
- Preserve the four prompt sections exactly: Goal, Context, Constraints, Success.
- Keep Codex as the primary preset.
- Include Ollama and VS Code / Claude as secondary presets.
- Keep Run Tests as a first-class visible checkbox on the main form.

### Run Tests Semantics

When `Run Tests` is enabled:

- Ask for the smallest relevant test set needed to verify the change.
- Do not ask for the full suite unless the change requires it.

When `Run Tests` is disabled:

- Ask not to run tests unless necessary to inspect or validate the requested change.
- If tests are skipped, state that they were skipped.

### Reasoning Budget

Choose the simplest solution that satisfies the request.

Do not compare multiple architectures unless asked.

Do not explore alternatives unless requested.

Avoid speculative analysis.
