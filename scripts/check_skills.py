#!/usr/bin/env python3
"""Check every skill folder: frontmatter, folder name, and personal data."""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HOME_PATH = re.compile(r"(/home/|/Users/|C:\\Users\\|C:/Users/)(?!<)[A-Za-z0-9._-]+")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
TEXT = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".sh", ".ps1"}


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    return text[4:end] if end != -1 else None


def check_skill(folder):
    problems = []
    skill = folder / "SKILL.md"
    if not skill.is_file():
        return [f"{folder.name}: SKILL.md is missing"]
    fm = frontmatter(skill.read_text(encoding="utf-8"))
    if fm is None:
        return [f"{folder.name}: SKILL.md has no frontmatter between --- lines"]
    name = re.search(r"^name:\s*(\S+)\s*$", fm, re.MULTILINE)
    if not name:
        problems.append(f"{folder.name}: frontmatter has no name")
    else:
        if name.group(1) != folder.name:
            problems.append(
                f"{folder.name}: name is '{name.group(1)}', must equal the folder name"
            )
        if not NAME.match(name.group(1)):
            problems.append(
                f"{folder.name}: name must be lowercase words joined by hyphens"
            )
    if not re.search(r"^description:\s*\S", fm, re.MULTILINE):
        problems.append(f"{folder.name}: frontmatter has no description")
    for path in sorted(folder.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for pattern, what in (
                (HOME_PATH, "personal path"),
                (EMAIL, "email address"),
            ):
                match = pattern.search(line)
                if match:
                    problems.append(
                        f"{path.relative_to(ROOT)}:{number}: {what} '{match.group(0)}'"
                    )
    return problems


def main():
    folders = sorted(p for p in (ROOT / "skills").iterdir() if p.is_dir())
    if not folders:
        print("no skills found under skills/")
        return 1
    problems = [p for folder in folders for p in check_skill(folder)]
    for problem in problems:
        print(problem)
    print(f"{len(folders)} skill(s) checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
