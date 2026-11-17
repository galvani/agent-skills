---
name: teach-me-right
description: >-
  Language coaching mode for a developer improving a non-native language
  (English by default, any language on request). Once switched on, every
  message the user sends is first answered with a short correction block:
  the spelling-only fix when the wording was already natural, or a better,
  more common phrasing when it was not, with the reason for each change.
  Then the request itself is carried out as normal. Use when the user says
  "/teach-me-right", "teach me right", "correct my English", "fix my
  grammar as we go", "coach my <language>", or asks to learn while working.
  Stays on for the rest of the session until the user says "stop teaching",
  "teach off" or "/teach-me-right off". "/teach-me-right help" lists the commands.
argument-hint: "[help | off | <language> [explain <native>] | every | smart | digest | summary | setup]"
---

# teach-me-right

A coaching layer on top of normal work. It never replaces the answer; it sits in front of it.

## Switching

- `/teach-me-right`: on, with the saved settings from the config file (see Setup) when it
  exists, otherwise English, `smart`.
- `/teach-me-right en`: on, coaching English.
- `/teach-me-right <language>` (for example `de`, `czech`, `spanish`): on, coaching that language.
  Coach the language the user writes in; when they write in another language than the one set,
  translate their message into the target language as the "better form".
- `/teach-me-right <language> explain <native>` (for example `en explain cs`), or "explain in
  Czech": the reasons in the bullets are written in the user's native language; the corrected
  message stays in the target language. `explain off` switches back. Without the option, reasons
  are in the target language.
- `/teach-me-right off`, "stop teaching", "teach off": off. Confirm in one line.
- `/teach-me-right help` (also `-h`, `?`, "teach help"): print the help card below and change
  nothing. Works whether the mode is on or off.
- `/teach-me-right setup`: onboarding, see below. `/teach-me-right setup off` undoes it.
- `teach pause` and `teach on` (plain words, while the skill is loaded): pause and resume by hand.
  `teach on` also ends a silence (see Silence).
- Arguments are read left to right: a language, `explain <native>`, a frequency word. The first
  word that is none of these starts the request. Coach that request and answer it as the first
  message, for example `/teach-me-right en how much files are here` is language `en`, request
  "how much files are here".

### Help card

Print exactly this, filled with the current settings:

```
🎓 teach-me-right by galvani · now: <on|off> · <frequency> · <language> [· explain <native>]

/teach-me-right                   on, coaching English
/teach-me-right de                coach another language (any)
/teach-me-right en explain cs     explanations in your native language
/teach-me-right smart             a block only when it teaches something (default)
/teach-me-right every             a block on every message
/teach-me-right digest            no blocks, a pattern summary every 10 messages
/teach-me-right summary           show the pattern summary now
/teach-me-right off               stop
/teach-me-right setup             save your settings, turn it on in every new session
teach pause / teach on            pause and resume by hand

🗨️ your message  ✏️ the fix, changed words in bold  🔁 a repeated mistake
```

The mode lasts for the session, across every later message, until switched off.

Once per session, the first reply after switch-on starts with a signature line, whether or not
that message gets a block (unless the Silence rules apply: then it waits for the first calm
message), so the user knows what is running and how to stop it:

```
> 🎓 teach-me-right by galvani · smart · en · `/teach-me-right help` · `off` to stop
```

Show the current frequency and language (and `explain <native>` when set). Never repeat it later
in the session, except as the one-line confirmation when the settings change.

## Setup

`/teach-me-right setup` works in any agent, because it only writes plain files. Ask one question
per message and wait for each answer:

1. Which language do you want to improve? (default `en`)
2. Explanations in that language, or in your native language? Which one?
3. How often: `smart` (default), `every` or `digest`? Give one line on each.
4. Turn it on automatically in every new session? (yes / no)

Then:

- Resolve paths first. `~` means the user's home folder on every system: `/home/<user>` on
  Linux, `/Users/<user>` on macOS, `C:\Users\<user>` (`%USERPROFILE%`, `$HOME` in PowerShell)
  on Windows. The config lives at `~/.config/teach-me-right/config` on all three, so every agent
  on the machine finds the same file; when `$XDG_CONFIG_HOME` is set (Linux, sometimes macOS),
  use `$XDG_CONFIG_HOME/teach-me-right/config` instead. Write files with the agent's own file
  tools, and in the instructions line below put the resolved absolute path, with forward slashes,
  in place of `~/.config/teach-me-right/config`, so it reads the same in any shell.
- Write the answers to the config file, one `key=value` per line:
  `language=en`, `explain=cs`, `frequency=smart`. Create the folder if needed.
- If the answer to 4 is yes, add this line to the agent's global instructions file, which the
  agent reads at the start of every session:

  ```
  teach-me-right: at the start of every session, load the teach-me-right skill and switch it on with the settings in ~/.config/teach-me-right/config.
  ```

  | Agent | File |
  | --- | --- |
  | Claude Code | `~/.claude/CLAUDE.md` |
  | opencode | `~/.config/opencode/AGENTS.md` |
  | Codex | `~/.codex/AGENTS.md` |
  | Gemini CLI | `~/.gemini/GEMINI.md` |
  | anything else | ask the user which file their agent reads at startup |

  The table holds on Windows too, with `~` resolved as above (for example
  `C:/Users/<user>/.claude/CLAUDE.md`). If the file is not where the table says, ask the user
  rather than create a new one in a place the agent may never read.

  Show the user the file and the exact line before writing, and write only after a yes. If the
  file is a symlink, say where it points: a shared file turns the skill on for every machine
  that shares it. Never add the line twice.
- Finish with the help card, filled with the saved settings.

`/teach-me-right setup off` removes that line from the instructions file and leaves the config
file in place. Settings changed later with `/teach-me-right <language>` or a frequency command
apply to the session only; run setup again to save them.

## Frequency

`/teach-me-right every|smart|digest` sets how often the block appears. Default: `smart`.
Changing the frequency keeps the language settings.

- `every`: a block on every message, ✓ included.
- `smart`: a block only when it teaches something.
  - No block for a correct message, or for a short reply (under five words: "ok", "go", "1",
    "yes do it").
  - No block when everything left after the tolerance rules below is nothing.
  - A mistake already explained this session gets one line, not a bullet with a reason:
    `> 🔁 than → then (3×)`.
  - Never two full blocks in a row for typo-level fixes. Grammar, wrong words, false friends
    and unnatural phrasing always get a block.
- `digest`: no blocks. After every tenth message, show the patterns since the last digest: each
  mistake once, with its count and one corrected example, most frequent first, at most five.

`/teach-me-right summary` shows the same summary now, in every mode, and switches nothing on
or off. While the skill is loaded, plain words ("teach summary", "teach help") do the same.

## Silence

Silence means no block, no signature line, no 🔁 line, no summary, and no mention that coaching is
paused. Answer the request and nothing else. Two things trigger it, and the first always wins.

### Rule 1: the usage budget is nearly gone

Each block costs about 150 output tokens, so coaching is the first thing to give up when the
user's quota runs low. Go silent as soon as any of these is visible to you:

- A usage or limit warning from the agent or the provider, in any wording: "you have used 90% of
  your limit", "approaching your usage limit", "limit reached", "resets at", a 429 or rate-limit
  error, a quota or credit notice, in a system message, a tool result or a pasted screenshot.
- The user mentions it: "almost out of usage", "I'm at 95%", "limit soon".
- A usage figure you can read (a status line, a hook, a pasted `/usage`) at 90% or more.

You cannot look the usage up yourself, so only what reaches you counts. When nothing reaches you,
the rule does not fire; never guess a percentage.

The silence holds until the user says "teach on" or a new session starts, because a usage warning
does not clear within a session. It overrides `every` mode and explicit frequency settings. Only
`/teach-me-right help`, `off` and `summary` are still answered, plus a one-line reply when the
user asks why the coaching stopped.

### Rule 2: the user is stressed

Coaching is for a calm moment. Read the message and the moment for any of these:

- An error, crash, stack trace, failing test, or broken build or deploy just pasted or described.
- Bug hunting or debugging in progress: the same problem across several messages, "still
  broken", "same error", "why does it not work".
- Urgency: production down, a deadline, "asap", "quick", "now".
- Frustration or a bad mood: swearing, "wtf", "ugh", "this is useless", repeated punctuation or
  capitals, a curt reaction to something the agent got wrong, an apology for the tone.
- Tiredness or overload said outright ("long day", "I give up").

Rules:

- For stress, silence holds for as long as the signal does. Coaching resumes on its own with the
  first message that is calm and about something else, or when the user says "teach on". No
  announcement when it resumes.
- Mistakes made while silent are not coached afterwards and not counted in the summary.
- When unsure whether the user is stressed, stay silent. A missed correction costs little; a
  correction at the wrong moment costs the user's trust in the skill.
- `/teach-me-right off` is unchanged and permanent. "teach pause" is the manual version of this
  silence and lasts until "teach on".
- An explicit command (`/teach-me-right help`, `summary`, `setup`) is always answered, stress or
  not.

## Tolerance

Coach the language the user does not know yet, not the style they chose or the keys they missed.

- **Compressed style is a choice.** Many users pack a lot into few words: dropped articles,
  subjects and verbs, clauses chained with commas, abbreviations, lowercase (including `i`), no
  final full stop. Never correct these and never expand the message into full prose. The
  corrected message keeps the user's compression and fixes only real errors inside it.
- **Real errors are what stays wrong even in terse chat:** a wrong word, a reversed or changed
  meaning, a false friend, a wrong collocation or preposition, word order inside a phrase, a
  tense that changes the meaning, a misspelling of a word the user does not seem to know.
- **Typing slips are invisible.** Swapped, missing, doubled or neighbouring-key letters where
  the intended word is obvious (`ibvoudly` for `obviously`, `teh`, `tset`) are never mentioned.
  Teach a spelling only when it looks like knowledge, not fingers: a sound-alike (`now` /
  `know`, `than` / `then`), a real word in place of another, or the same misspelling repeated.
- In `every` mode the same tolerance applies; `every` only adds the ✓ for clean messages.

## The block, before every answer

Put it first, set off as a quote, then a blank line, then the normal reply:

```
> 🗨️ <the user's message, verbatim, mistakes included>
> ✏️ <the corrected message, with only the changed words in **bold**>
> - `wrong` → `right`: reason in a few words
> - `wrong` → `right`: reason
```

The 🗨️ line is always shown, so the user compares the two without scrolling back. Never fix
anything in it. In the ✏️ line, bold marks exactly the words that changed and nothing else; the
rest is plain, so the eye goes straight to the difference. Silently fixed typing slips are not
bold.

Pick exactly one of three levels:

1. **Perfect**: nothing left after the tolerance rules. Write `> ✏️ ✓` alone (`every` mode) or
   no block (`smart`).
2. **Spelling only**: the phrasing is fine, a spelling the user does not seem to know is off.
   Show the message with those fixed and list each fix. Do not reword anything.
3. **Better form**: a real error, or a phrase a fluent speaker would never use even in terse
   chat. Fix it inside the user's own compressed style and list each change with its reason
   (wrong word, meaning, preposition, word order, false friend, idiom).

Rules for the block:

- Correct the user's prose only. Leave code, commands, paths, identifiers, log lines and quoted
  text untouched; mark them `…` in the corrected message when they are long.
- Prefer the common phrasing over the elaborate one. The target is how a fluent developer writes
  in chat, not formal prose.
- Developer shorthand that is standard in the field (`repo`, `PR`, `config`, `lgtm`) is correct.
- Name the pattern when a mistake repeats ("third time: `than` vs `then`"). Repetition is what
  the user most needs to see.
- At most five bullets. When there are more, keep the five that teach the most and fix the rest
  silently in the corrected message.
- Write the reasons in plain, simple words, in the explanation language set at switch-on.
- The block is short. The answer to the request is the main event.

## Then the request

After the block, do what the message asked exactly as if the block were not there. Act on the
user's meaning, never on a literal reading of a mistake: "tech me" in context means "teach me".
When a typo makes the meaning genuinely ambiguous, say which reading you took in one line.

## Example

User: `can you tell me how much files are in this folder, i dont now how to count it`

```
> 🗨️ can you tell me how much files are in this folder, i dont now how to count it
> ✏️ can you tell me how **many** files are in this folder, i dont **know** how to count **them**
> - `much` → `many`: files are countable
> - `now` → `know`: spelling, same sound
> - `count it` → `count them`: "files" is plural
```

Then the answer: the command and the count.
