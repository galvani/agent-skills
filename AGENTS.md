# Agent instructions

This repo is a collection of skills for AI coding agents. Each skill is a self-contained folder
under `skills/<name>/` with a `SKILL.md`. Humans read `README.md` and `CONTRIBUTING.md`; this file
is for you, the agent.

## When the user asks you to install a skill from this repo

1. Ask which agent and which scope (all projects or one project) if it is not clear.
2. Clone the repo into a temporary folder and copy only `skills/<name>/` to the agent's skills
   folder: `~/.claude/skills/` for Claude Code (opencode reads it too), `<project>/.claude/skills/`
   for one project. On Windows use `$HOME\.claude\skills\`.
3. Never overwrite an existing skill folder without asking. Delete the temporary clone.
4. Tell the user to restart the agent, then name the skill's main command.

## When the user asks you to add or share a skill

1. Create `skills/<name>/SKILL.md` following `CONTRIBUTING.md`. Copy the structure of an existing
   skill rather than inventing one.
2. Remove personal data before anything is committed: names, emails, hostnames, employers,
   customers, tokens, absolute paths from the user's machine. Replace them with `~` and
   placeholders. If something is ambiguous, ask the user instead of guessing.
3. Run `python3 scripts/check_skills.py` and, in Claude Code, `claude plugin validate .`. Fix
   every finding.
4. Load the skill in a fresh session and run its main command. Report what you ran and what you
   could not test.
5. Work on a branch in the user's fork, one skill per branch, and open a pull request with `gh`.
   Show the user the diff and the pull request text before you push or open it.

## Rules for every change

- Edit only the skill you were asked to touch.
- A new skill is also added as one row in the table in `README.md`.
- Keep `SKILL.md` short and write it in the present tense, as rules. No history, no ticket keys,
  no TODOs, no open questions.
- Never invent a feature the skill does not have, and never claim a test you did not run.
