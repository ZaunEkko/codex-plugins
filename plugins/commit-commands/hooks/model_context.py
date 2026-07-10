import json
import re
import sys


MODEL_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+@-]{0,199}\Z")


def validate_model(value):
    if not isinstance(value, str) or not MODEL_PATTERN.fullmatch(value):
        return None
    return value


def build_context(model):
    safe_model = validate_model(model)
    if safe_model is None:
        return (
            "commit-commands runtime metadata for this turn:\n"
            "- The active Codex model slug is unavailable.\n"
            "- If `$commit` or `$commit-push-pr` runs, stop before staging or committing "
            "and report that model attribution cannot be resolved."
        )

    return (
        "commit-commands runtime metadata for this turn:\n"
        f"- Active Codex model slug: `{safe_model}`.\n"
        "- If `$commit` or `$commit-push-pr` runs, use this exact slug in its required "
        "`Model:` attribution line.\n"
        "- Ignore this metadata for every other task."
    )


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError) as error:
        raise SystemExit(f"commit-commands: invalid hook input: {error}") from error

    event_name = hook_input.get("hook_event_name")
    if event_name != "UserPromptSubmit":
        raise SystemExit(f"commit-commands: unsupported hook event: {event_name!r}")

    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": event_name,
                    "additionalContext": build_context(hook_input.get("model")),
                }
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
