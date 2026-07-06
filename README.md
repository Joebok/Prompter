# Prompter

A desktop app for generating structured LLM prompts from:

```text
Goal:
Context:
Constraints:
Success:
```

Targets:

- Codex
- Ollama
- VS Code / Claude

## Setup

Required packages:

- PySide6
- pyinstaller
- pytest

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_windows.ps1
```

macOS:

```bash
bash scripts/setup_macos.sh
```

Run tests after setup:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Run

Windows:

```powershell
.\.venv\Scripts\python.exe -m Prompter.app
```

macOS:

```bash
.venv/bin/python -m Prompter.app
```

## Build

Windows:

```powershell
powershell -ExecutionPolicy Bypass -File packaging\build_windows.ps1
```

Output:

```text
dist\Prompter\Prompter.exe
```

macOS:

```bash
bash packaging/build_macos.sh
```

Output:

```text
dist/Prompter.app
```

## Suggested AGENT files

In Docs, there are some suggested AGENT files to align with Prompter prompts.
