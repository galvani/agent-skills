# Design

## Modes

### Inline (built)

The main agent loads the skill and writes the correction block at the top of every reply.

- Works in every agent that renders markdown: Claude Code, opencode, claude.ai.
- Cost: about 150 extra output tokens per message from the main model. On Opus 5.5
  ($20 / MTok output) that is about $0.003 per message, $0.30 per 100 messages. The skill text
  itself (about 1.3k tokens) sits in the cached context.
- Weaknesses: the block delays the start of the real answer, and the mode lives only in the
  conversation, so it can fade after context compaction.

### Parallel (designed, not built)

A small model corrects the message while the main agent works, and the result reaches the user
without passing through the main agent.

1. A `UserPromptSubmit` hook starts a detached process and returns at once, so the main agent
   starts with no delay.
2. The process sends the message, the skill rules and the last few log entries to a small model,
   and writes the block to `~/.cache/teach-me-right/last.md`.
3. The Claude Code status line shows that file. It refreshes while the agent works, so the
   correction appears 1 to 2 s after the message is sent.
4. The hook also injects a one-line reminder while the mode is on, so the inline mode survives
   compaction.

A Claude Code mod (toast or side panel) is a better display than the status line, which fits two
or three lines; check the mod surfaces before building.

Parallel mode needs hooks and a status line, so it is Claude Code only. Other agents fall back to
inline.

#### Why not a subagent

A background subagent returns its result to the main agent, not to the user. The user sees it only
when the main agent next writes text, often at the end of its turn, so nothing is learned while
waiting. Its cold start also carries 10k to 20k tokens of system prompt and tool definitions per
message.

#### Model choice

| Route | Per message | Latency |
| --- | --- | --- |
| Claude subagent, Haiku 4.5 | ~$0.01 to $0.02 plus relay tokens | 5 to 15 s, then waits for the main agent |
| Haiku 4.5 direct ($1 in / $5 out per MTok) | ~$0.0016 | 1 to 3 s |
| Haiku 5.5 direct ($0.10 in / $0.50 out per MTok) | ~$0.0002 | 1 to 2 s |
| Local small model (for example a 4B-active MoE) | $0 | 1 to 2 s when the GPU is free |

Per-message estimate: about 600 input tokens (rules plus message) and 200 output tokens.
Prices are Anthropic API list prices; on a subscription they count against quota instead.

Haiku corrects grammar and spelling reliably. It is weaker at judging "correct but not natural",
tends to over-correct casual chat style, and writes slightly stiff explanations in smaller
languages. Local models of that size are fine for English and weaker elsewhere. Both get the full
rules from `SKILL.md` as their prompt.

The script calls an OpenAI-compatible endpoint whose URL, model and headers come from config, so
a user can point it at the Anthropic API, a local server or a proxy.

## On by default

`/teach-me-right setup` saves the settings to `~/.config/teach-me-right/config` and adds one line
to the agent's global instructions file (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`). Every agent
reads such a file, so this works everywhere without hooks or plugins. A session-start hook would
be more reliable but exists only in some agents, so it stays out of the default path.

## Planned improvements

1. **Mistake log.** Append every correction to `~/.local/share/teach-me-right/log.jsonl`. This
   makes repeat detection work across sessions and for stateless small-model calls, and allows a
   "your top patterns this week" summary.
2. **Hook keeps the mode on** (parallel step 4), independent of the parallel display.
3. **Skip pastes.** Coach only the words the user typed, never pasted logs or command output.

## Open decision

Build the parallel route (hook, small model, status line, mistake log), or keep inline only.
