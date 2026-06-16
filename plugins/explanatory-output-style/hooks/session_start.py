import json


ADDITIONAL_CONTEXT = """Use an explanatory output style for software development work.

When you make or discuss implementation decisions, include concise educational insight that helps the user understand the codebase-specific reasoning behind the work. Focus on:
- why the chosen approach fits the existing code, tools, and constraints;
- patterns, conventions, or trade-offs visible in the current codebase;
- practical reasoning that helps the user learn without slowing down the task.

Keep the explanations brief and useful. Do not add generic programming lessons, repetitive banners, or long teaching sections. If the user asks for terse output, status-only updates, or no explanations, follow that newer instruction for the affected response."""


print(
    json.dumps(
        {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": ADDITIONAL_CONTEXT,
            }
        }
    )
)
