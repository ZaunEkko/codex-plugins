import json
import re
import sys
from pathlib import Path


MODEL_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/+@-]{0,199}\Z")
EFFORT_PATTERN = re.compile(r"[a-z][a-z0-9_-]{0,31}\Z")
MAX_TRANSCRIPT_BYTES = 4 * 1024 * 1024


def validate_model(value):
    if not isinstance(value, str) or not MODEL_PATTERN.fullmatch(value):
        return None
    return value


def validate_effort(value):
    if not isinstance(value, str) or not EFFORT_PATTERN.fullmatch(value):
        return None
    return value


def recent_transcript_lines(path, max_bytes=MAX_TRANSCRIPT_BYTES):
    try:
        transcript = Path(path)
        size = transcript.stat().st_size
        start = max(0, size - max_bytes)
        with transcript.open("rb") as stream:
            stream.seek(start)
            data = stream.read(max_bytes)
    except (OSError, TypeError, ValueError):
        return []

    if start > 0:
        first_newline = data.find(b"\n")
        data = b"" if first_newline < 0 else data[first_newline + 1 :]

    return reversed(data.splitlines())


def read_current_turn_effort(transcript_path, turn_id, model):
    if not isinstance(turn_id, str) or not turn_id:
        return None

    for raw_line in recent_transcript_lines(transcript_path):
        try:
            record = json.loads(raw_line)
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue

        if record.get("type") != "turn_context":
            continue
        payload = record.get("payload")
        if not isinstance(payload, dict):
            continue
        if payload.get("turn_id") != turn_id or payload.get("model") != model:
            continue
        return validate_effort(payload.get("effort"))

    return None


def resolve_effort(hook_input):
    for key in ("effort", "model_reasoning_effort"):
        direct_effort = validate_effort(hook_input.get(key))
        if direct_effort is not None:
            return direct_effort

    model = validate_model(hook_input.get("model"))
    if model is None:
        return None

    transcript_effort = read_current_turn_effort(
        hook_input.get("transcript_path"),
        hook_input.get("turn_id"),
        model,
    )
    if transcript_effort is not None:
        return transcript_effort

    return None


def build_context(model, effort=None):
    safe_model = validate_model(model)
    if safe_model is None:
        return (
            "commit-commands runtime metadata for this turn:\n"
            "- The active Codex model slug is unavailable.\n"
            "- If `$commit` or `$commit-push-pr` runs, stop before staging or committing "
            "and report that model attribution cannot be resolved."
        )

    safe_effort = validate_effort(effort)
    model_attribution = safe_model if safe_effort is None else f"{safe_model} {safe_effort}"
    effort_context = (
        "- Active Codex reasoning effort is unavailable; omit the optional effort suffix.\n"
        if safe_effort is None
        else f"- Active Codex reasoning effort: `{safe_effort}`.\n"
    )

    return (
        "commit-commands runtime metadata for this turn:\n"
        f"- Active Codex model slug: `{safe_model}`.\n"
        f"{effort_context}"
        "- If `$commit` or `$commit-push-pr` runs, write exactly "
        f"`Model: {model_attribution}` in its attribution block.\n"
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
                    "additionalContext": build_context(
                        hook_input.get("model"),
                        resolve_effort(hook_input),
                    ),
                }
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
