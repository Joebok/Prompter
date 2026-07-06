from prompter.prompt_engine import PromptRequest, TargetPreset, build_prompt


def request(target=TargetPreset.CODEX, run_tests=True, **fields):
    values = {
        "goal": "Do thing",
        "context": "File A",
        "constraints": "Keep it small",
        "success": "It works",
    }
    values.update(fields)
    return PromptRequest(target=target, run_tests=run_tests, **values)


def test_codex_checked():
    prompt = build_prompt(request())

    assert prompt == (
        "Goal:\nDo thing\n\n"
        "Context:\nFile A\n\n"
        "Constraints:\nKeep it small\n\n"
        "Success:\nIt works\n\n"
        "Run Tests:\n"
        "Run the smallest relevant test set needed to verify the change. Do not run the full suite unless the change requires it."
    )


def test_codex_unchecked():
    prompt = build_prompt(request(run_tests=False))

    assert "Do not run tests unless they are necessary" in prompt
    assert "If tests are skipped, state that they were skipped." in prompt


def test_ollama_preset():
    prompt = build_prompt(request(target=TargetPreset.OLLAMA))

    assert prompt.startswith("Use the following contract.")
    assert "Output Rules:" in prompt
    assert "- Do not invent missing APIs, files, or facts." in prompt


def test_vscode_claude_preset():
    prompt = build_prompt(request(target=TargetPreset.VSCODE_CLAUDE, run_tests=False))

    assert prompt.startswith("Please work from this contract")
    assert "Working Style:" in prompt
    assert "Testing:\nDo not run or recommend broad test runs" in prompt


def test_trims_outer_whitespace():
    prompt = build_prompt(request(goal="  Goal text\n", context="\nContext text  "))

    assert "Goal:\nGoal text\n\n" in prompt
    assert "Context:\nContext text\n\n" in prompt


def test_preserves_internal_newlines():
    prompt = build_prompt(request(constraints="First\nSecond"))

    assert "Constraints:\nFirst\nSecond\n\n" in prompt
