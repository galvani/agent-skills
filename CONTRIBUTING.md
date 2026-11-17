# Contributing

Thanks for sharing a skill or improving one. Small, focused changes are the easiest to merge.

## What belongs here

A skill that is useful to any developer with an AI coding agent, not tied to one machine, employer
or private service. If it only works with your own tools, keep it in your own repo.

## Layout

```
skills/<name>/
  SKILL.md        required
  README.md       optional, for humans: what it does, install, examples
  docs/           optional, design notes
  scripts/        optional, helpers the skill calls
```

- The folder name is lowercase words joined by hyphens and equals `name:` in the frontmatter.
- Everything a skill needs is inside its folder. Skills never import from each other.

## SKILL.md

- Frontmatter has `name` and `description`. The description says what the skill does and when to
  use it, in the words a user would type: it decides when the agent loads the skill.
- Instructions are written for the agent, in plain imperative sentences, with an example where the
  output format matters.
- No personal data: no real names, emails, hostnames, employers, customers, tokens or absolute
  paths from your machine. Use `~` and placeholders such as `<user>`.
- Say which systems it works on. If you only tested Linux, say so.
- Keep it short. Every line costs tokens in every session that loads the skill.

## Before you open a pull request

1. Run `python3 scripts/check_skills.py`. It checks the frontmatter and looks for personal paths
   and emails.
2. If you use Claude Code, run `claude plugin validate .`.
3. Load the skill in a fresh session of at least one agent and run its main command. A skill that
   was only read, never run, is not tested.
4. Open one pull request per skill. Say what it does, which agent and version you tested with,
   and what you did not test.

## Changing an existing skill

Describe the problem you saw (what you typed, what the agent did, what you expected) before the
fix. Keep unrelated edits out of the same pull request.

## Reporting a problem

Open an issue with the agent and its version, the exact message you sent, and what happened.

## Licence

By contributing you agree that your contribution is released under the [MIT licence](LICENSE).
