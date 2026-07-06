# PromptHelper Implementation Plan

## Goal
Create a standalone desktop app for quickly generating structured LLM prompts using the four-part contract:

```text
Goal:
Context:
Constraints:
Success:
```

Primary target: Windows 11 standalone `.exe`.
Secondary target: macOS standalone `.app`, built on macOS from the same Python source.

Primary workflow focus: Codex prompts that align with AGENTS.md.
Secondary presets: Ollama and VS Code / Claude.

## Technology

Use Python 3 + PySide6.

Reasons:

- Cross-platform GUI code for Windows and macOS.
- Can package as a click-to-run Windows executable.
- Can package as a click-to-run macOS app bundle.
- Easy to keep prompt-generation logic separate from UI.
- Easy to add templates/snippets as JSON files later.

Do not use web frameworks, Electron, or local servers for this version.

## Core UX Principle

The main window must be fast to use.

The first screen should contain everything needed for the normal workflow:

- Goal multiline input
- Context multiline input
- Constraints multiline input
- Success multiline input
- Target preset dropdown
- Run Tests checkbox
- Generated prompt preview
- Copy Prompt button
- Clear button

Avoid tab-heavy or wizard-style UI for the first version.

## Main Window Layout

Recommended layout:

```text
PromptHelper

Target: [ Codex ▼ ]       [x] Run Tests       [ Copy Prompt ]

Goal:
[ multiline input ]

Context:
[ multiline input ]

Constraints:
[ multiline input ]

Success:
[ multiline input ]

Generated Prompt:
[ readonly multiline preview ]

[ Clear ] [ Save Template ] [ Load Template ]
```

The `Copy Prompt` button should be the primary action.

## Target Presets

Implement three target presets:

1. Codex
2. Ollama
3. VS Code / Claude

The preset affects only the generated prompt wrapper and default constraints. It should not change the user's raw field text.

### Codex Preset

Codex is the primary target.

Generated prompt should be terse and map directly to AGENTS.md:

```text
Goal:
{goal}

Context:
{context}

Constraints:
{constraints}

Success:
{success}
```

Append test instruction based on Run Tests checkbox.

If Run Tests is checked:

```text
Run Tests:
Run the smallest relevant test set needed to verify the change. Do not run the full suite unless the change requires it.
```

If Run Tests is unchecked:

```text
Run Tests:
Do not run tests unless they are necessary to inspect or validate the requested change. If tests are skipped, state that they were skipped.
```

Default Codex constraint snippets:

```text
- Keep the change minimal.
- Do not reformat unrelated code.
- Do not refactor outside the requested scope.
- Prefer editing existing files over creating new files unless needed.
- Preserve existing style.
```

These defaults should be optional and removable in settings later, but hardcoded is acceptable for version 1.

### Ollama Preset

Ollama output should be more explicit because smaller/local models may need stricter output boundaries:

```text
Use the following contract. Return only the requested result. Do not restate the prompt.

Goal:
{goal}

Context:
{context}

Constraints:
{constraints}

Success:
{success}

Output Rules:
- Be concise.
- Do not include conversational filler.
- Do not invent missing APIs, files, or facts.
```

Run Tests wording can still be included when coding-related, but should be treated as normal prompt text.

### VS Code / Claude Preset

This should work well when pasted into a VS Code chat panel using Claude or another coding assistant:

```text
Please work from this contract and keep the response implementation-focused.

Goal:
{goal}

Context:
{context}

Constraints:
{constraints}

Success:
{success}

Working Style:
- Identify any blocking ambiguity before editing.
- Keep changes scoped.
- Prefer a concise patch plan before code changes.
```

Run Tests checkbox wording:

Checked:

```text
Testing:
Run or recommend the smallest relevant test set. Avoid unnecessary full-suite runs.
```

Unchecked:

```text
Testing:
Do not run or recommend broad test runs unless clearly necessary. If tests are skipped, say so briefly.
```

## Run Tests Checkbox Behavior

The checkbox should be visible on the main form.

Label:

```text
Run Tests
```

Default:

```text
Checked
```

Tooltip:

```text
When checked, the generated prompt asks the assistant to run the smallest relevant test set. When unchecked, it asks the assistant not to run tests unless necessary.
```

The checkbox must not say “Run all tests.”

The generated prompt should discourage full-suite runs by default.

## Prompt Generation Rules

Implement prompt generation in a non-UI module:

```text
prompthelper/prompt_engine.py
```

Suggested API:

```python
from dataclasses import dataclass
from enum import Enum

class TargetPreset(str, Enum):
    CODEX = "Codex"
    OLLAMA = "Ollama"
    VSCODE_CLAUDE = "VS Code / Claude"

@dataclass(frozen=True)
class PromptRequest:
    goal: str
    context: str
    constraints: str
    success: str
    target: TargetPreset
    run_tests: bool


def build_prompt(request: PromptRequest) -> str:
    ...
```

Rules:

- Trim leading/trailing whitespace from each input field.
- Preserve internal line breaks.
- Do not silently remove user text.
- Do not add empty placeholder text to the generated prompt.
- If a field is blank, leave the heading with a blank body.
- Generated prompt preview updates as the user types.
- Copy button copies exactly the preview text.

## File Layout

Recommended project layout:

```text
PromptHelper/
    pyproject.toml
    README.md
    AGENTS.md
    prompthelper/
        __init__.py
        app.py
        main_window.py
        prompt_engine.py
        settings.py
    tests/
        test_prompt_engine.py
    packaging/
        pyinstaller_windows.spec
        pyinstaller_macos.spec
        build_windows.ps1
        build_macos.sh
```

## Dependencies

Use only the minimum dependencies for version 1:

```text
PySide6
pyinstaller
pytest
```

## Implementation Steps for Codex

### Step 1: Create project skeleton

Create the package layout, pyproject.toml, README.md, and empty tests.

Success:

- `python3 -m pytest` runs.
- App package imports without error.

### Step 2: Implement prompt engine

Implement `PromptRequest`, `TargetPreset`, and `build_prompt`.

Add tests covering:

- Codex preset with Run Tests checked.
- Codex preset with Run Tests unchecked.
- Ollama preset.
- VS Code / Claude preset.
- Whitespace trimming.
- Internal newline preservation.

Success:

- Prompt engine tests pass.

### Step 3: Implement PySide6 main window

Create a single-window app with:

- Four labeled multiline inputs.
- Preset dropdown.
- Run Tests checkbox.
- Readonly generated prompt preview.
- Copy Prompt button.
- Clear button.

Success:

- App launches.
- Typing updates preview live.
- Copy button copies preview to clipboard.
- Clear button clears all four user inputs.

### Step 4: Add keyboard shortcuts

Add:

- Ctrl+Enter: copy generated prompt.
- Ctrl+L: clear fields after confirmation.
- Ctrl+1: Codex preset.
- Ctrl+2: Ollama preset.
- Ctrl+3: VS Code / Claude preset.

On macOS, Qt should map Ctrl-equivalent shortcuts appropriately where possible. Do not add OS-specific shortcut code unless necessary.

Success:

- Shortcuts work on Windows.
- No platform-specific code is required for normal use.

### Step 5: Add lightweight persistence

Use Qt settings or a small JSON file under the user config directory.

Persist:

- Last selected preset.
- Run Tests checkbox state.
- Window size.

Do not persist prompt text in version 1 unless explicitly added later.

Success:

- Reopening app restores preset, checkbox, and window size.

### Step 6: Add packaging scripts

Windows build script:

```powershell
python -m pip install -U pip
python -m pip install -e .
python -m pip install pyinstaller
pyinstaller packaging/pyinstaller_windows.spec --clean --noconfirm
```

macOS build script:

```bash
python3 -m pip install -U pip
python3 -m pip install -e .
python3 -m pip install pyinstaller
pyinstaller packaging/pyinstaller_macos.spec --clean --noconfirm
```

Success:

- Windows build produces a double-clickable app under `dist/`.
- macOS build produces a `.app` bundle under `dist/`.

## PyInstaller Notes

### Windows

Use `--windowed` so no console opens.

Recommended first version:

- Folder build, not one-file build.
- Faster startup.
- Fewer Qt packaging surprises.

Optional later:

- One-file `.exe` if startup time and antivirus false positives are acceptable.

### macOS

Build on macOS.

The app should produce a `.app` bundle.

Unsigned apps may trigger Gatekeeper warnings on other Macs. For personal use on your own Mac, this is usually manageable. For distribution to other users, plan for signing and notarization later.

## Version 1 Non-Goals

Do not implement these in version 1:

- Direct Codex API integration.
- Direct Ollama API integration.
- Direct VS Code integration.
- Prompt history database.
- Template marketplace.
- Rich Markdown editor.
- Token counting.
- Cloud sync.

These are useful later, but the first version should optimize for speed.

## CODEX Kickoff Prompt

Use this prompt to start implementation:

```text
Goal:
Create a new Python 3 + PySide6 desktop app named PromptHelper. It should generate structured LLM prompts using four multiline fields: Goal, Context, Constraints, and Success. Primary target is Windows 11, but source code must remain portable to macOS.

Context:
This is a new standalone project, not part of Zet. Follow the local AGENTS.md. The main workflow is pasting prompts into Codex. The app should also support Ollama and VS Code / Claude presets. The app should package with PyInstaller on Windows and macOS, built separately on each OS.

Constraints:
- Keep version 1 minimal and fast to use.
- Use Python 3 and PySide6.
- Keep prompt-generation logic separate from UI code.
- Main window must include four multiline inputs: Goal, Context, Constraints, Success.
- Main window must include a Target preset dropdown with Codex, Ollama, and VS Code / Claude.
- Main window must include a visible Run Tests checkbox.
- Run Tests checked means: ask for the smallest relevant test set, not the full suite by default.
- Run Tests unchecked means: ask not to run tests unless necessary; if skipped, state that tests were skipped.
- Include Copy Prompt and Clear buttons.
- Generated prompt preview must update live.
- Do not add direct AI integrations in version 1.
- Do not add prompt history or token counting in version 1.

Success:
- App launches locally.
- Copy Prompt copies the generated prompt exactly.
- Prompt engine has unit tests for all presets and both Run Tests states.
- Windows PyInstaller spec/build script exists.
- macOS PyInstaller spec/build script exists.
- README explains how to run and build on Windows and macOS.
```
