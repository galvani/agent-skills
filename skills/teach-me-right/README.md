# teach-me-right

Language coaching for developers, built into the coding agent they already use. Every message you
send gets a short correction block first: spelling fixes only when the wording was already natural,
or a better and more common phrasing with a reason for each change. Then the agent does what you
asked. English by default; any language on request, with the explanations optionally in your
native language.

```
> 🗨️ can you tell me how much files are in this folder, i dont now how to count it
> ✏️ can you tell me how **many** files are in this folder, i dont **know** how to count **them**
> - `much` → `many`: files are countable
> - `now` → `know`: spelling, same sound
> - `count it` → `count them`: "files" is plural
```

## Use

| Command | Effect |
| --- | --- |
| `/teach-me-right` | on, coaching English |
| `/teach-me-right de` | on, coaching German (any language works) |
| `/teach-me-right en explain cs` | coach English, explain the corrections in Czech |
| `explain off` | explanations back in the target language |
| `/teach-me-right smart` | a block only when it teaches something (default) |
| `/teach-me-right every` | a block on every message |
| `/teach-me-right digest` | no blocks; a summary of your patterns every ten messages |
| `/teach-me-right summary` | show the pattern summary now |
| `teach pause` / `teach on` | pause and resume by hand (plain words, while the skill is loaded) |
| `/teach-me-right off` | off |
| `/teach-me-right help` | list the commands and the current settings |
| `/teach-me-right setup` | save your settings and turn it on in every new session |
| `/teach-me-right setup off` | stop turning it on in new sessions |

## When it stays quiet

It says nothing when your Claude usage is nearly used up (any limit warning it can see, or you
saying so), because each correction costs tokens. It cannot read your usage by itself; it only
reacts to a warning that reaches it. It also says nothing when you look stressed: an error or failing test just pasted, a bug hunt that
has gone on for a while, urgency, swearing or frustration. It resumes on its own at the next
calm message. When unsure, it stays quiet.

## Cost

Measured with `claude plugin details` (token counts) and Anthropic's list prices. The skill is
`inline`: the agent itself writes the correction, so you pay in tokens of the model you already use.

| What | Tokens | When |
| --- | --- | --- |
| Skill description in the skill list | ~190 | every session, always |
| Skill text (`SKILL.md`) | ~3.3k | once per session, when it loads (cached afterwards) |
| One correction block | ~150 output | per message that gets a block (`smart` mode skips clean ones) |

| Model | One block | 100 blocks | Loading the skill once |
| --- | --- | --- | --- |
| Opus 5.5 ($4 in / $20 out per MTok) | $0.003 | $0.30 | $0.013 |
| Sonnet 5.5 ($2 in / $10 out per MTok) | $0.0015 | $0.15 | $0.007 |
| Haiku 5.5 ($0.10 in / $0.50 out per MTok) | $0.00008 | $0.008 | $0.0003 |

On a subscription these tokens count against your usage limit instead of costing money. The skill
stops coaching by itself when it sees that the limit is nearly reached. A block estimate is 150
tokens; longer messages with several fixes cost more, and `digest` mode costs a summary every ten
messages instead.

## Install

The skill is this folder, `teach-me-right/`, and works in any agent that reads
`SKILL.md` skills.

- **Claude Code, one user:** copy or symlink this folder into `~/.claude/skills/`.
- **Claude Code, one project:** copy it into `<project>/.claude/skills/`.
- **Other agents (opencode, Codex, and similar):** copy the folder into the agent's skills
  directory, or paste the body of `SKILL.md` into its instructions.

Then run `/teach-me-right setup` once. It asks for your languages and how often to correct you,
saves them to `~/.config/teach-me-right/config`, and, if you want, adds one line to your agent's
global instructions file so the skill switches on in every new session.

## Status

The inline mode works: the main agent writes the correction block itself. The parallel mode (a
small model corrects your message while the main agent works, shown in the status line) is
designed but not built; see [docs/DESIGN.md](docs/DESIGN.md).
