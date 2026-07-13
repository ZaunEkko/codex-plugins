import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


FOOTER = "Generated with [Codex](https://chatgpt.com/codex)"
LEGACY_FOOTERS = {
    "Generated with Codex assistance.",
    "Generated with Codex",
}
PR_URL_PATTERN = re.compile(r"https?://[^/\s]+/[^/\s]+/[^/\s]+/pull/\d+")


def final_nonempty_line(body):
    for line in reversed(body.splitlines()):
        if line.strip():
            return line.strip()
    return None


def render_body(body):
    lines = body.rstrip().splitlines()
    if lines and lines[-1].strip() in LEGACY_FOOTERS | {FOOTER}:
        lines.pop()

    content = "\n".join(lines).rstrip()
    return f"{content}\n\n{FOOTER}\n" if content else f"{FOOTER}\n"


def normalized_body(body):
    return "\n".join(body.splitlines()).rstrip()


def body_matches(actual, expected):
    return normalized_body(actual) == normalized_body(expected)


def read_body(body_file):
    try:
        return body_file.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as error:
        raise SystemExit("commit-commands: PR body file must be UTF-8") from error
    except OSError as error:
        raise SystemExit(f"commit-commands: cannot read PR body file: {error}") from error


def run_gh(arguments):
    try:
        return subprocess.run(
            ["gh", *arguments],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError as error:
        raise SystemExit("commit-commands: GitHub CLI `gh` is unavailable") from error
    except subprocess.CalledProcessError as error:
        detail = (error.stderr or error.stdout or str(error)).strip()
        raise SystemExit(f"commit-commands: gh command failed: {detail}") from error


def pull_request_url(output):
    matches = PR_URL_PATTERN.findall(output)
    if not matches:
        raise SystemExit("commit-commands: `gh pr create` did not return a pull request URL")
    return matches[-1]


def read_pull_request(url):
    result = run_gh(["pr", "view", url, "--json", "body,url"])
    try:
        pull_request = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise SystemExit("commit-commands: `gh pr view` returned invalid JSON") from error

    if not isinstance(pull_request, dict):
        raise SystemExit("commit-commands: `gh pr view` returned an invalid pull request")
    return pull_request


def create_pull_request(body, gh_arguments):
    rendered_body = render_body(body)
    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            suffix=".md",
            delete=False,
        ) as stream:
            stream.write(rendered_body)
            temporary_path = Path(stream.name)

        result = run_gh(
            ["pr", "create", *gh_arguments, "--body-file", str(temporary_path)]
        )
        url = pull_request_url(result.stdout)
        pull_request = read_pull_request(url)

        if not body_matches(pull_request.get("body") or "", rendered_body):
            run_gh(["pr", "edit", url, "--body-file", str(temporary_path)])
            pull_request = read_pull_request(url)

        if not body_matches(pull_request.get("body") or "", rendered_body):
            raise SystemExit(
                "commit-commands: pull request body does not match the expected UTF-8 content"
            )

        return pull_request.get("url") or url
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def parse_arguments(argv=None):
    parser = argparse.ArgumentParser(
        description="Create a pull request whose body ends with Codex attribution."
    )
    parser.add_argument(
        "--body-file",
        type=Path,
        required=True,
        help="read the pull request body from a UTF-8 Markdown file",
    )
    parser.add_argument("gh_arguments", nargs=argparse.REMAINDER)
    arguments = parser.parse_args(argv)
    gh_arguments = list(arguments.gh_arguments)
    if gh_arguments and gh_arguments[0] == "--":
        gh_arguments.pop(0)

    forbidden = {"--body", "-b", "--body-file", "-F"}
    for argument in gh_arguments:
        if (
            argument in forbidden
            or argument.startswith("--body=")
            or argument.startswith("--body-file=")
        ):
            parser.error(
                "use the wrapper's --body-file option; do not pass body options to gh"
            )
    return arguments.body_file, gh_arguments


def main():
    body_file, gh_arguments = parse_arguments()
    print(create_pull_request(read_body(body_file), gh_arguments))


if __name__ == "__main__":
    main()
