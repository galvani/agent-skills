# teach-me-right

Language coaching for developers, built into the coding agent they already use. It stays quiet
unless it has something to teach. When a message of yours has a real mistake, a short block shows
what you wrote, the fix with the changed words in bold, and why; then the agent does what you
asked. Clean messages, short replies, terse chat style and obvious typos get nothing, and it goes
fully silent when you are stressed, debugging, or close to your usage limit. English by default;
any language you pick, with the explanations optionally in your native language.

```
> 🗨️ can you explain me why the build is failing since two hours
> ✏️ can you explain **to** me why the build **has been** failing **for** two hours
> - `explain me` → `explain to me`: "explain" needs "to" before the person
> - `is failing` → `has been failing`: it started in the past and still goes on
> - `since two hours` → `for two hours`: "for" + a length, "since" + a start time (since 9am)
