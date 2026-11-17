# agent-skills

Skills for AI coding agents, by [galvani](https://github.com/galvani). A skill is a folder with a
`SKILL.md` that the agent loads when it is relevant. Claude Code and opencode read this format;
each skill here is self-contained, so you can take one without the rest.

## Skills

| Skill | What it does |
| --- | --- |
| [teach-me-right](skills/teach-me-right/) | Language coaching while you work. Quiet by default: it speaks up only when a message of yours has a real mistake worth learning from, shows the fix and the reason, and the agent carries on. Silent when you are stressed or near your usage limit. |

Running costs are small: about 190 tokens per session for the skill list entry, ~3.4k when it
loads, ~150 per correction. The full table is in the
[teach-me-right README](skills/teach-me-right/README.md#cost).

## Install a skill

Tell your agent:

> Install the skill `teach-me-right` from https://github.com/galvani/agent-skills. Clone the repo
> into a temporary folder, copy `skills/teach-me-right/` into my agent's skills folder (ask me
> which one if unsure, and never overwrite an existing folder without asking), delete the clone,
> and tell me to restart the agent. Then I will run `/teach-me-right setup`.

Or do it by hand.

Linux and macOS:

```sh
git clone https://github.com/galvani/agent-skills
mkdir -p ~/.claude/skills
cp -r agent-skills/skills/teach-me-right ~/.claude/skills/
```

Windows (PowerShell):

```powershell
git clone https://github.com/galvani/agent-skills
New-Item -ItemType Directory -Force $HOME\.claude\skills | Out-Null
Copy-Item -Recurse agent-skills\skills\teach-me-right $HOME\.claude\skills\
```

Restart the agent afterwards.

- **Claude Code** reads `~/.claude/skills/` (all projects) and `<project>/.claude/skills/` (one
  project).
- **opencode** also reads `~/.claude/skills/`, so one copy serves both. If yours does not pick it
  up, add the folder to `skills.paths` in its config.
- **Other agents** that read `SKILL.md` folders: copy the folder where the agent looks for skills.
  Agents without skills support can still use the body of `SKILL.md` as instructions.

### Claude Code plugin

```
/plugin marketplace add galvani/agent-skills
/plugin install teach-me-right@galvani-skills
```

A plugin namespaces its commands: use `/teach-me-right:teach-me-right`. A plain copy gives you
`/teach-me-right`.

## Contribute

Share your own skill or improve one: see [CONTRIBUTING.md](CONTRIBUTING.md). If you use an AI
agent, point it at [AGENTS.md](AGENTS.md).

## Licence

[MIT](LICENSE)
