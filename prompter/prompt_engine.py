from dataclasses import dataclass
from enum import Enum


class TargetPreset(str, Enum):
    CODEX = "Codex"
    OLLAMA = "Ollama"
    VSCODE_CLAUDE = "VS Code / Claude"


DEFAULT_CODEX_CONSTRAINTS = "\n".join(
    [
        "- Keep the change minimal.",
        "- Do not reformat unrelated code.",
        "- Do not refactor outside the requested scope.",
        "- Prefer editing existing files over creating new files unless needed.",
        "- Preserve existing style.",
    ]
)


@dataclass(frozen=True)
class PromptRequest:
    goal: str
    context: str
    constraints: str
    success: str
    target: TargetPreset
    run_tests: bool


def build_prompt(request: PromptRequest) -> str:
    goal = request.goal.strip()
    context = request.context.strip()
    constraints = request.constraints.strip()
    success = request.success.strip()

    if request.target == TargetPreset.CODEX:
        return _codex_prompt(goal, context, constraints, success, request.run_tests)
    if request.target == TargetPreset.OLLAMA:
        return _ollama_prompt(goal, context, constraints, success, request.run_tests)
    if request.target == TargetPreset.VSCODE_CLAUDE:
        return _vscode_claude_prompt(goal, context, constraints, success, request.run_tests)
    raise ValueError(f"Unsupported target preset: {request.target}")


def _contract(goal: str, context: str, constraints: str, success: str) -> str:
    return (
        f"Goal:\n{goal}\n\n"
        f"Context:\n{context}\n\n"
        f"Constraints:\n{constraints}\n\n"
        f"Success:\n{success}"
    )


def _codex_prompt(goal: str, context: str, constraints: str, success: str, run_tests: bool) -> str:
    testing = (
        "Run the smallest relevant test set needed to verify the change. Do not run the full suite unless the change requires it."
        if run_tests
        else "Do not run tests unless they are necessary to inspect or validate the requested change. If tests are skipped, state that they were skipped."
    )
    return f"{_contract(goal, context, constraints, success)}\n\nRun Tests:\n{testing}"


def _ollama_prompt(goal: str, context: str, constraints: str, success: str, run_tests: bool) -> str:
    testing = (
        "Run or recommend the smallest relevant test set needed to verify the change. Do not run the full suite unless the change requires it."
        if run_tests
        else "Do not run or recommend tests unless they are necessary to inspect or validate the requested change. If tests are skipped, state that they were skipped."
    )
    return (
        "Use the following contract. Return only the requested result. Do not restate the prompt.\n\n"
        f"{_contract(goal, context, constraints, success)}\n\n"
        "Output Rules:\n"
        "- Be concise.\n"
        "- Do not include conversational filler.\n"
        "- Do not invent missing APIs, files, or facts.\n\n"
        f"Run Tests:\n{testing}"
    )


def _vscode_claude_prompt(goal: str, context: str, constraints: str, success: str, run_tests: bool) -> str:
    testing = (
        "Run or recommend the smallest relevant test set. Avoid unnecessary full-suite runs."
        if run_tests
        else "Do not run or recommend broad test runs unless clearly necessary. If tests are skipped, say so briefly."
    )
    return (
        "Please work from this contract and keep the response implementation-focused.\n\n"
        f"{_contract(goal, context, constraints, success)}\n\n"
        "Working Style:\n"
        "- Identify any blocking ambiguity before editing.\n"
        "- Keep changes scoped.\n"
        "- Prefer a concise patch plan before code changes.\n\n"
        f"Testing:\n{testing}"
    )
