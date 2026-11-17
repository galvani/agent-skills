# Contributing

Thanks for sharing a skill or improving one. Small, focused changes are the easiest to merge.

## What belongs here

A skill that is useful to any developer with an AI coding agent, not tied to one machine, employer
or private service. If it only works with your own tools, keep it in your own repo. Everything
merged here is public under the MIT licence and installable by anyone, so send a skill here only
when you mean to publish it.

## Layout

```
skills/<name>/
  SKILL.md          required
  references/       optional, extra detail the agent reads on demand
  scripts/          optional, helpers the skill calls
  assets/           optional, templates and other resources
docs/<name>.md      optional, for humans: what it does, install, examples
```

- The folder name is lowercase words joined by hyphens and equals `name:` in the frontmatter.
- Everything a skill needs is inside its folder. Skills never import from each other.
- Keep the folder lean: anything only a human reads (install steps, cost, examples) belongs in
  `docs/<name>.md`, because every file in the skill folder ships to the user and may be loaded
  into the agent's context.

## Adding a skill

1. Copy the layout of an existing skill rather than inventing one.
2. Add a row for it to the skills table in `README.md`, and a plugin entry with its `skills` path
   to `.claude-plugin/marketplace.json`. `scripts/check_skills.py` fails until both exist, because
   a skill listed in neither cannot be installed.
3. Run the checks below, then open the pull request.

## SKILL.md

- Frontmatter has `name` and `description`. The description says what the skill does and when to
  use it, in the words a user would type: it decides when the agent loads the skill.
- Instructions are written for the agent, in plain imperative sentences, with an example where the
  output format matters.
- Write in the present tense, as rules: no history, no ticket keys, no TODOs, no open questions.
- No personal data: no real names, emails, hostnames, employers, customers, tokens or absolute
  paths from your machine. Use `~` and placeholders such as `<user>`.
- Say which systems it works on. If you only tested Linux, say so.
- Keep it short. Every line costs tokens in every session that loads the skill.

## Before you open a pull request

CI runs all of this on every push to `main` and on every pull request
(`.github/workflows/validate.yml`). Running it locally first is faster:

1. `python3 scripts/check_skills.py`: frontmatter, folder layout, local links, personal paths and
   emails, and that the skill is listed in `README.md` and `.claude-plugin/marketplace.json`.
2. `skill-validator check --strict --allow-extra-frontmatter skills/`: the Agent Skills
   specification, internal links, code fences and token budget. `pre-commit` (step 3) builds it for
   you; to run it directly, install it with `brew install agent-ecosystem/tap/skill-validator` or
   take a release binary from its GitHub releases.
3. `pre-commit install` once per clone, and the two checks above plus a secret scan run on commit.
4. If you use Claude Code, run `claude plugin validate .`.
5. Load the skill in a fresh session of at least one agent and run its main command. A skill that
   was only read, never run, is not tested.
6. Open one pull request per skill. Say what it does, which agent and version you tested with,
   and what you did not test.

## Run CI locally

The workflow in `.github/workflows/validate.yml` also runs on your machine through
[act](https://github.com/nektos/act), so a red pipeline is not the first thing you learn about.
`act` needs Docker, and nothing else:

```sh
# once: act is a single binary, no daemon of its own
curl -fsSL -o /tmp/act.tgz \
  https://github.com/nektos/act/releases/download/v0.2.98/act_Linux_x86_64.tar.gz
mkdir -p ~/.local/bin && tar xzf /tmp/act.tgz -C ~/.local/bin act

# the `spec` job: specification, links, code fences, token budget
act push -j spec -P ubuntu-latest=catthehacker/ubuntu:act-latest

# the `repo` job: layout, links, marketplace, personal data
act push -j repo -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

- `-P` chooses the runner image. The default image in `act` has no `curl` and no `python3`, so the
  jobs fail for a reason that has nothing to do with your skill.
- The first run pulls the image (about 1.3 GB) and caches it; later runs take seconds.
- One job per invocation: with two `-j` flags `act` runs only the last one.
- Under rootless Docker, `docker` works but `act` asks for `/var/run/docker.sock` and is refused.
  Point it at the rootless socket first:
  `export DOCKER_HOST=unix:///run/user/$(id -u)/docker.sock`
- The `secrets` job is the one `act` cannot run honestly: it does not fill the push payload, so
  gitleaks reports "No commits to scan" and passes without scanning anything. Scan by hand:
  `docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest git /repo --redact`

`pre-commit install` covers the same checks on every commit without Docker, so you rarely need the
two `act` runs.

## Changing an existing skill

Describe the problem you saw (what you typed, what the agent did, what you expected) before the
fix. Keep unrelated edits out of the same pull request.

## Reporting a problem

Open an issue with the agent and its version, the exact message you sent, and what happened.

## Licence

By contributing you agree that your contribution is released under the [MIT licence](LICENSE).
