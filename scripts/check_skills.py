#!/usr/bin/env python3
"""Check this repo: skill frontmatter, folder layout, links, personal data, indexes.

The Agent Skills specification itself is checked by `skill-validator` (see CONTRIBUTING.md).
This script covers the rules of this repository: the folder layout, every skill being listed in
README.md and .claude-plugin/plugin.json, local links resolving, and no personal data.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HOME_PATH = re.compile(r"(/home/|/Users/|C:\\Users\\|C:/Users/)(?!<)[A-Za-z0-9._-]+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```", re.MULTILINE)
TEXT = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".ps1"}
SKIP_DIRS = {".git", ".ruff_cache", "__pycache__", "node_modules"}
ALLOWED_IN_SKILL = {"SKILL.md", "references", "scripts", "assets"}
MAX_DESCRIPTION = 1024
MAX_NAME = 64
MAX_SKILL_LINES = 500

errors = []
warnings = []


def error(message):
    errors.append(message)


def warn(message):
    warnings.append(message)


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    return text[4:end] if end != -1 else None


def field(fm, key):
    """Read a top-level frontmatter value, joining YAML block scalars."""
    lines = fm.splitlines()
    for number, line in enumerate(lines):
        match = re.match(rf"^{re.escape(key)}:\s*(.*)$", line)
        if not match:
            continue
        value = match.group(1).strip()
        if value[:1] in {">", "|", ">-", "|-", ">+", "|+"}:
            block = []
            for following in lines[number + 1 :]:
                if following.strip() and not following.startswith((" ", "\t")):
                    break
                block.append(following.strip())
            return " ".join(part for part in block if part)
        return value
    return None


def markdown_body(text):
    """Text with fenced code blocks removed, so examples are not read as links."""
    out, in_fence = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def slug(heading):
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def anchors(path):
    text = markdown_body(path.read_text(encoding="utf-8", errors="ignore"))
    return {slug(line.lstrip("#")) for line in text.splitlines() if line.startswith("#")}


def check_links(path):
    """Every relative link resolves to a file, and to a heading that exists."""
    for target in LINK.findall(markdown_body(path.read_text(encoding="utf-8"))):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("//"):
            continue
        where = path.relative_to(ROOT)
        file_part, _, fragment = target.partition("#")
        destination = path if not file_part else (path.parent / file_part).resolve()
        if not destination.exists():
            error(f"{where}: link '{target}' points at a path that does not exist")
            continue
        if fragment and destination.is_file() and destination.suffix == ".md":
            if slug(fragment) not in anchors(destination):
                error(f"{where}: link '{target}' points at a heading that does not exist")


def check_skill(folder):
    name = folder.name
    skill = folder / "SKILL.md"
    if not skill.is_file():
        return error(f"{name}: SKILL.md is missing")

    text = skill.read_text(encoding="utf-8")
    fm = frontmatter(text)
    if fm is None:
        return error(f"{name}: SKILL.md has no frontmatter between --- lines")

    declared = field(fm, "name")
    if not declared:
        error(f"{name}: frontmatter has no name")
    else:
        if declared != name:
            error(f"{name}: name is '{declared}', must equal the folder name")
        if not NAME.match(declared):
            error(f"{name}: name must be lowercase words joined by hyphens")
        if len(declared) > MAX_NAME:
            error(f"{name}: name is {len(declared)} characters, the maximum is {MAX_NAME}")

    description = field(fm, "description")
    if not description:
        error(f"{name}: frontmatter has no description")
    elif len(description) > MAX_DESCRIPTION:
        error(
            f"{name}: description is {len(description)} characters, "
            f"the maximum is {MAX_DESCRIPTION}"
        )

    tools = field(fm, "allowed-tools")
    if tools is not None and not tools:
        error(f"{name}: allowed-tools is empty, remove the field or list tools")

    for entry in sorted(folder.iterdir()):
        if entry.name not in ALLOWED_IN_SKILL:
            warn(
                f"{name}: '{entry.name}' is not part of the layout; skills hold only "
                "SKILL.md, references/, scripts/ and assets/. Human docs go to docs/<name>.md"
            )

    lines = len(text.splitlines())
    if lines > MAX_SKILL_LINES:
        warn(f"{name}: SKILL.md is {lines} lines, keep it under {MAX_SKILL_LINES}")
    if len(FENCE.findall(text)) % 2:
        error(f"{name}: SKILL.md has an unclosed code fence")


def check_personal_data():
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT:
            continue
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pattern, what in ((HOME_PATH, "personal path"), (EMAIL, "email address")):
                match = pattern.search(line)
                if match:
                    error(
                        f"{path.relative_to(ROOT)}:{number}: {what} '{match.group(0)}'"
                    )


def check_plugin(folders):
    """marketplace.json lists every skill, and every listed path is a real skill folder."""
    manifest = ROOT / ".claude-plugin" / "marketplace.json"
    if not manifest.is_file():
        return error(".claude-plugin/marketplace.json is missing")
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as problem:
        return error(f".claude-plugin/marketplace.json: invalid JSON ({problem})")

    if not data.get("name"):
        error(".claude-plugin/marketplace.json: no name")
    if not data.get("owner", {}).get("name"):
        error(".claude-plugin/marketplace.json: no owner.name")
    listed = {}
    for plugin in data.get("plugins", []):
        for relative in plugin.get("skills", []):
            path = (ROOT / relative).resolve()
            if not path.is_dir():
                error(
                    f".claude-plugin/marketplace.json: skills path '{relative}' "
                    "does not exist"
                )
            elif not (path / "SKILL.md").is_file():
                error(f".claude-plugin/marketplace.json: '{relative}' has no SKILL.md")
            else:
                listed[path.name] = plugin.get("version")
        if not plugin.get("version"):
            warn(
                f".claude-plugin/marketplace.json: plugin "
                f"'{plugin.get('name')}' has no version"
            )
    for folder in folders:
        if folder.name not in listed:
            error(
                f"{folder.name}: not listed in .claude-plugin/marketplace.json, "
                "so /plugin install cannot reach it"
            )


def check_readme(folders):
    readme = ROOT / "README.md"
    if not readme.is_file():
        return error("README.md is missing")
    text = markdown_body(readme.read_text(encoding="utf-8"))
    for folder in folders:
        if f"skills/{folder.name}" not in text:
            error(f"{folder.name}: not added to the skills table in README.md")


def main():
    skill_root = ROOT / "skills"
    folders = sorted(p for p in skill_root.iterdir() if p.is_dir()) if skill_root.is_dir() else []
    if not folders:
        print("no skills found under skills/")
        return 1

    for folder in folders:
        check_skill(folder)
    check_plugin(folders)
    check_readme(folders)
    check_personal_data()
    for path in sorted(ROOT.rglob("*.md")):
        if SKIP_DIRS & set(path.relative_to(ROOT).parts):
            continue
        check_links(path)

    for message in errors:
        print(f"error: {message}")
    for message in warnings:
        print(f"warning: {message}")
    print(
        f"{len(folders)} skill(s) checked, "
        f"{len(errors)} error(s), {len(warnings)} warning(s)"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
