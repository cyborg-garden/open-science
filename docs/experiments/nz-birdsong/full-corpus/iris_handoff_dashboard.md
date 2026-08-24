# Iris handoff — korimako page recompute (for your check BEFORE anything ships)

Jules's instruction: you double-check the work and the phrasing; the page updates
only after your pass. Everything below is verifiable against the artifacts named.

## What ran tonight (all artifacts local)

1. **Full-corpus ISI extraction** — `/opt/data/koe_isi/syllable_table.csv`
   21,463 syllables, 2,136/2,137 songs, split-tagged (train/val/test),
   model-predicted (TN v2 segmenter 0.902 F1@50 honest split + stage-4 family
   classifier 0.893 test acc). QC: `qc_report.json` (zero negative gaps, zero
   zero-dur segs; gap median 139 ms; dur median 186 ms).

2. **Sex + dialect recompute** — `sex_geo_fullcorpus_results.json`
   454 birds (234 M / 220 F), sequence features only.
   - Sex 5-fold: **0.938** (old small-sample: 0.961 combined-features — new run
     used no embeddings, so this is a harder feature set and it holds)
   - Sex LOSO mean: **0.837** (old: 0.891); per-site: CUV 0.94, TMI/LBI 0.88,
     PKI 0.77, TAW/LAI 0.78 — same geography as before, so site-confound story
     is consistent, not small-sample artifact.
   - Sex on held-out TEST split only: **0.971** (n=37 birds — strong but small n;
     flag the n in any public use)
   - Site-from-repertoire router: **0.81** (old: 0.84)

3. **Stage 7 individual ID — first validation** — `individual_id_results.json`
   Closed-set, 77 birds with ≥4 songs each, held-out-songs-per-bird.
   - Top-1 **0.554**, top-5 **0.803**, chance 0.013 (43× chance)
   - Sequence bigrams are the strongest single feature block (0.52 alone)
   - Per-bird top-1 bimodal: 31% of birds ≥0.8, 25% at 0.0 — individual
     signature strength varies (matches field-worker intuition)
   - Sex-restricted: M 0.512 (55 birds), F 0.404 (22 birds)
   - **Honesty line:** closed-set only (name a bird from a known population on
     a new recording). NOT open-set — can't name an individual never seen.
     Open-set verification (rejecting unknown birds) is untested.

## Proposed replacement numbers for the korimako page

- Segmentation: **TN v2, F1 = 0.902 @50 ms** on a 165-song held-out test
  (2,137-song corpus, bird-disjoint split). Supersedes the old WhisperSeg 0.914
  (which was tutorial-subset, matched conditions).
- Syllable typing: family-level classifier, **0.893 test accuracy** on held-out
  birds, 24 families + UNKNOWN over 21,463 extracted syllables.
- Sex from song: **0.94** cross-validated within corpus; **0.84** when predicting
  for birds from a geographically held-out island (the honest deployment number);
  per-island range 0.77–0.94.
- Geographic dialect: a bird's syllable repertoire identifies its home island
  at **0.81** (6 sites) — dialect structure is real but not a substitute for
  geotags.
- Individual ID (new): from a single song, the correct bird is named in **55%**
  of cases and is in the top 5 in **80%**, across a 77-bird population
  (chance = 1.3%).

## Things I deliberately did NOT claim (keep them out of public text)

- Any "cross-bird generalisation confirmed" phrasing for the 0.914 — withdrawn.
- 1-ms boundary precision — refinement prototype was a negative result; we use
  raw TN v2 boundaries (rule-consistent, ~14 ms annotator-convention offset).
- Individual ID on unknown/open populations — untested.
- Full-corpus family labels are model predictions, not human labels — the page
  should say "model-extracted" anywhere it shows the 21k-syllable counts.

## QC / methods notes available on request
qc_report.json, sex_geo_fullcorpus_results.json, individual_id_results.json,
registry rows (segmentation_approaches_registry.md, Aug 24 entries).
