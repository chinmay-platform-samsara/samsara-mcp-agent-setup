#!/usr/bin/env python3
"""Render setup.md into index.html using template.html.

Run with: uv run --with markdown python build.py
"""

import pathlib
import re

import markdown

ROOT = pathlib.Path(__file__).parent
SETUP_URL = "https://chinmay-platform-samsara.github.io/samsara-mcp-agent-setup/setup.md"


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Split YAML-style front matter from the markdown body.

    Args:
        text: Full contents of setup.md.

    Returns:
        A (metadata, body) tuple. Metadata values are raw strings.

    Raises:
        ValueError: If the file has no front matter block.
    """
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        raise ValueError("setup.md is missing its front matter block")
    meta = {}
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def main() -> None:
    meta, body = _split_front_matter((ROOT / "setup.md").read_text())
    content = markdown.markdown(body, extensions=["tables", "fenced_code", "toc"])
    page = (
        (ROOT / "template.html").read_text()
        .replace("{{CONTENT}}", content)
        .replace("{{SETUP_URL}}", SETUP_URL)
        .replace("{{LAST_UPDATED}}", meta["last_updated"])
    )
    (ROOT / "index.html").write_text(page)


if __name__ == "__main__":
    main()
