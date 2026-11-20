# Reasoning trace

The working session behind the [peptide-reporting study](../) — published as part of the experiment. Closed labs withhold reasoning traces (citing distillation); this one is open. You get the result *and* the path to it.

## Files

| File | What it is |
|------|------------|
| `peptide-reasoning-trace.md` | Human-readable transcript — prompts, Matilde's replies, every tool call, tool results, and reasoning where the model exposed it. |
| `peptide-reasoning-trace.sanitized.jsonl` | The same record, one message per line, for machine use. Fields: `session`, `role`, `content`, `tool_name`, `tool_calls`, `reasoning`, `timestamp`. |

## Sanitization

- **Redacted:** names (→ *Researcher* / *Collaborator*), phone numbers, UUIDs, Signal group IDs, emails, and `@handles`. Server IP addresses in tool output are replaced with `[ip removed]`. The agent's own name (Matilde) is kept.
- **Excluded entirely:** four unrelated sessions (a separate paper-validation request) that have nothing to do with the peptide work.
- **Left as-is:** Reddit `u/` references that appear inside tool output — public source data, consistent with the published dataset.
- Generated programmatically from the agent's message store (`state.db`); the residual-PII scan over both outputs returns zero for every pattern above.

11 sessions · 644 messages · 233 tool-call turns.
