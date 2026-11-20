# FDE Proof — Conversation Traces (public, scrubbed)

**Status: public.** The redaction pass (`scrub.py`, below) has been run and the output
verified clean. This archive shipped alongside the experiment as the durable record behind
the claim "the process is rerunnable."

These are the session transcripts for the FDE formalization work the open-science experiment
page references. They preserve the texture of the work — tool calls, builds, the failures and
recoveries — with operational detail (infra paths, IDs, tokens, hostnames) deterministically
scrubbed.

## What's here

- `fde-lean-proof-thread.SCRUBBED.md` — the complete "FDE LEAN Proof" record
  (Cyborg.Garden #open-science), covering the completeness assembly, corollaries, both
  external-review cycles, and the repo/publication work. This is the public, scrubbed file
  (the `.SCRUBBED` suffix marks it as the redacted version — the only one shipped).
- `ARCHIVE_MANIFEST.md` — what was captured, from where, when, and the redaction standard.
- `scrub.py` — the deterministic redaction script, so the scrub is auditable and re-runnable.

## Re-running the scrub

`scrub.py` holds only the generic rules (paths, snowflakes, links, token mechanics, ports).
The names specific to one deployment — machine hostnames and the git bot's app name — are read
at run time, so the script never names what it removes:

```bash
SCRUB_HOSTS="example-host,example-host.local" SCRUB_GIT_BOTS="example-git-app" \
  python3 scrub.py raw-thread.md fde-lean-proof-thread.SCRUBBED.md
```

Or copy `scrub.local.example.txt` to `scrub.local.txt` (git-ignored) and list them there, one
per line. A hostname also covers a trailing `:port`. The script stops if no hostname is
configured; `SCRUB_NO_LOCAL=1` runs the generic rules alone. Operators: keep your real list in
`scrub.local.txt` or your shell environment, never in a tracked file.

## Provenance

Captured 2026-08-11 by the Matilde agent from the Discord channel history.
The proving work was done entirely in these Discord threads between Juni Bevensee and the
Matilde agent, running on **Kimi K3** (open-weight, Moonshot AI) via OpenRouter. Iris appears
as a supporting agent (comms/encouragement), not as a prover. Claude's only role in the
project is an independent audit, relayed near the end.

**Coverage:** the complete derivation arc — origin/niche search (Aug 7), soundness,
completeness (design, the `refutes` regression, the honest-W walkback, the repair), the
degraded-channel outage, corollaries (Aug 9–10), publication, and both external-review
cycles (Aug 10–11). Sourced from the two Lean threads (the corrupted/v1 thread and the main
FDE thread).

## Redaction standard (per Juni, 2026-08-11) — applied

The scrub has been run and verified. The standard it applied:

KEEP — these are part of the honest record:
- Names: Juni and Matilde are fine to appear.
- Human steering and our interactions, including the encouraging/funny moments.
- The tool-calling problems that happened mid-proof — that's useful, realistic context.

STRIPPED before publication — anything vulnerable or personal:
- Port numbers, device names, internal links / hostnames.
- Private repo references that aren't meant to be public.
- The Discord thread / channel IDs and the Discord link itself.
- Any keys, tokens, or credential mechanics.
- User IDs / snowflakes.
- Internal filesystem paths (→ `<repo>` etc.) — genericized.
