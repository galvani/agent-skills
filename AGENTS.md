# Agent instructions

These instructions are for an agent working **in this repository** as a contributor. If you cloned
it only to install a skill for the user, they do not apply to you: copy `skills/<name>/`, delete
the clone, and stop reading here.

`CONTRIBUTING.md` is the one place the rules live: the layout, the `SKILL.md` conventions, the
checks and the pull request. Read it and follow it. This file adds only what is specific to you as
an agent.

## When the user asks you to install a skill from this repo

1. Ask which agent and which scope (all projects or one project) if it is not clear.
2. Clone the repo into a temporary folder and copy only `skills/<name>/` to the agent's skills
   folder: `~/.claude/skills/` for Claude Code (opencode reads it too), `<project>/.claude/skills/`
   for one project. On Windows use `$HOME\.claude\skills\`.
3. Never overwrite an existing skill folder without asking. Delete the temporary clone.
4. Tell the user to restart the agent, then name the skill's main command.

## When the user asks you to add or share a skill here

This applies only when the user is working in this repository and asked for the skill to go here.
A skill they wrote for their own use belongs in their own repo. Everything added here is public: it
is committed, installable, and listed in the marketplace. Do not add, move or publish a skill on
your own initiative.

Follow `CONTRIBUTING.md`. On top of it:

- Show the user the diff and the pull request text before you push or open it.
- Report what you ran and what you could not test. Never claim a test you did not run, and never
  describe a feature the skill does not have.
- When something might be personal data (a name, a hostname, an employer, a path), ask the user
  instead of guessing.
