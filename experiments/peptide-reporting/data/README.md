# Peptide community-pharmacovigilance dataset

Full data artifacts behind the [peptide-reporting dashboard](../). Released so the
analysis can be verified, re-run with different models or taxonomies, or extended
to other peptides.

## Files

| File | Records | What it is |
|------|---------|------------|
| `peptide_data_raw.json` | 2,981 | Raw posts scraped from r/Peptides, r/Nootropics, r/bpc_157 via the Arctic Shift archive. |
| `peptide_llm_encoded.jsonl` | 2,979 | Pass 1 — each post encoded by `qwen3.5:9b` (local Ollama): self-report flag, peptides, extracted effects with valence/confidence/category. |
| `peptide_llm_filtered.jsonl` | 620 | Pass 2 — verified self-reports only (pre-use questions and advice-seeking removed). |
| `peptide_effects.json` | — | Normalized aggregation: 3,657 raw effect mentions collapsed into 17 canonical groups, valence preserved. |

## Provenance

- **Source:** Arctic Shift Reddit archive (the same source used by Sehgal et al., 2026).
- **Encoding:** `qwen3.5:9b` on local Ollama, thinking mode disabled. ~6 hours total compute on a single consumer GPU. Zero API cost.
- **Method:** see the dashboard's *Method* tab.

## Privacy

- The `author` field in `peptide_data_raw.json` has been **nulled** for every record — Reddit usernames are not published.
- The derived files (`*_encoded`, `*_filtered`, `effects`) never contained author identifiers.
- Post **bodies and titles are public Reddit content**, verbatim apart from contact details and user mentions: email addresses, phone numbers, messaging or social handles, Reddit usernames and `u/` mentions, and personal website links in the post text are replaced with placeholders (`[email removed]`, `[phone removed]`, `[handle removed]`, `[link removed]`). Posts may occasionally contain other self-disclosed details; these were not machine-rewritten. Open an issue if you find something that should be redacted.

## Reuse

Public, for research and replication. Not medical advice; self-reports cannot establish causation, prevalence, or safety. See the dashboard disclaimer.
