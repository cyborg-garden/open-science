# fmri-pooling — decisions & future directions

Running log. Newest first. Attributed to whoever proposed the item.

## Decisions (current)

- **2026-08-12 — Adults only for the proof-of-concept pool.** Jules: keep the pooled
  cohort to adult datasets; drop the Pixar developmental dataset (ds000228, 3–12 yr
  children + adults) to avoid an age confound in validation. Revisit later with age
  as a covariate.
- **2026-08-12 — Alignment method: connectivity-based hyperalignment (CHA).** Jules:
  stimulus-agnostic pooling is the requirement; CHA is the branch of functional
  alignment that needs no shared stimulus. SRM/FastSRM stays available for
  same-stimulus subsets. Anatomical warp is the disclosed baseline everywhere.

## Future directions

### 1 · Stimulus-content annotation → encoding-based PROOF OF CONCEPT (Jules, 2026-08-12; refined 2026-08-12b)

Once the pooled datasets are aligned, annotate the *stimuli themselves* — the movies
and audio narratives are available — with feature timecourses far richer than what
the original papers used. Face frames, scene cuts, speech, motion, emotion, semantic
content. Convolve each feature timecourse with the HRF and use it as a regressor /
encoding model against the aligned brain data.

**Scope correction (Jules, 2026-08-12b): this is a PROOF OF CONCEPT, not the
validation.** It only works on stimuli that contain the annotated content (faces in
movies), and when the dataset doesn't ship feature regressors it requires real
computer-vision work on the movie frames — a cool direction, pursued in parallel,
but not the thing the pipeline's correctness rests on. The VALIDATION must be
stimulus-agnostic: grounded in anatomy or in whatever the literature's standard
benchmarks are (ISC of connectivity profiles, between-subject transfer,
fingerprinting preservation, cross-dataset transfer), so it applies to every
dataset we might ever pool, including ones with no face content at all.

**Why the proof of concept still matters:**
- Face-frame regressor should recover the fusiform face area; scene regressor the
  parahippocampal place area. A concrete, figure-able demonstration on the datasets
  that do have face content (Grand Budapest, StudyForrest, AOMIC) — persuasive
  even though it isn't the general validation.
- Strongest version: train the encoding model on one dataset, test on a held-out
  dataset (annotate Grand Budapest, predict FFA responses in StudyForrest).
- Lineage: Jules did exactly this kind of annotation work at the NIH in David A.
  Leopold's group (naturalistic stimuli, face-frame coding). The Grand Budapest
  dataset in our pool (ds003017) comes from the Gobbini group, whose program is
  face-selective topography from naturalistic movies — direct precedent.
- Head start: StudyForrest already ships partial stimulus annotations (cuts,
  depicted locations, speech) — verify coverage before annotating anew. Face/scene/
  semantic features can now be automated with off-the-shelf detectors, so "better
  than what they did in the paper" is cheap.
- Sits squarely in the naturalistic-stimulation genre (Hasson 2004 intersubject
  synchronization as the founding reference; Huth 2012/2016 semantic-space encoding
  models as the annotation-driven template).

### 2 · Method-selection policy for this project (Jules, 2026-08-12b)

For every methodological choice (parcellation, alignment variant, validation
metric, ...): do NOT guess which option is better. Rely on review / comparison
papers that benchmark the options **on the same dataset** and show which is better
for what. Weight by (a) recency and (b) rigor. If a recent, rigorous, same-data
comparison exists, it outranks intuition, convention, and developer defaults.
Applies to all future cases, not just the parcellation choice.
