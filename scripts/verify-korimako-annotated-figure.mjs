#!/usr/bin/env node
/**
 * Provenance gate for the public Koe/Dryad annotated-song figure.
 *
 * This guards the published artifact, not the truth of every annotation in the
 * corpus. It deliberately has no network dependency: the validated PNG and its
 * source-label evidence are committed with the figure.
 */
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';

const root = new URL('../', import.meta.url).pathname;
const pagePath = join(root, 'docs/experiments/nz-birdsong/index.html');
const dir = join(root, 'docs/experiments/nz-birdsong/figures');
const pngPath = join(dir, 'korimako_hand_annotated_song.png');
const webpPath = join(dir, 'korimako_hand_annotated_song.webp');
const evidencePath = join(dir, 'korimako_hand_annotated_song.provenance.json');
const errors = [];
const require = (condition, message) => { if (!condition) errors.push(message); };
const read = (path) => readFileSync(path);
const hash = (path) => createHash('sha256').update(read(path)).digest('hex');

const evidence = JSON.parse(read(evidencePath, 'utf8'));
const page = readFileSync(pagePath, 'utf8');
require(evidence.schema === 'korimako-annotated-song-provenance-v1', 'Unknown provenance schema');
require(evidence.approval?.approver === 'Jules', 'Jules approval not recorded');
require(evidence.approval?.approved === true, 'Figure is not marked approved');
require(evidence.audio?.source === 'Dryad tutorial subset', 'Audio source is not the matched Dryad tutorial subset');
require(evidence.audio?.song_id === 'WHW021_08', 'Unexpected song identity');
require(evidence.audio?.legacy_koe_wavs_directory_used === false, 'Legacy Koe wavs/ directory must not be used');
require(evidence.annotation?.timing_adjustment_ms === 0, 'Annotation timing adjustment is forbidden');
require(evidence.annotation?.family_remapping_used === false, 'Family remapping is forbidden');
require(evidence.annotation?.count === 20, 'Expected 20 hand-labelled syllables');
require(evidence.annotation?.dryad_intervals_equal_supplementary === true, 'Dryad/Supplementary interval equality not established');
require(evidence.annotation?.source_doi === '10.3389/fevo.2021.755633', 'Unexpected annotation DOI');
require(evidence.annotation?.label_families?.length === 7, 'Expected seven original family labels');
require(evidence.artifact?.png_sha256 === hash(pngPath), 'Approved PNG hash mismatch');
require(evidence.artifact?.webp_sha256 === hash(webpPath), 'Inline WebP hash mismatch');
require(evidence.artifact?.lossless_webp_verified === true, 'Lossless WebP pixel verification not recorded');

const figure = page.match(/<figure class="annotated-song" id="korimako-hand-annotation-example">([\s\S]*?)<\/figure>/);
require(figure, 'Korimako hand-annotation figure missing from page');
if (figure) {
  require(figure[1].includes('src="figures/korimako_hand_annotated_song.webp"'), 'Inline image is not the approved WebP');
  require(figure[1].includes('href="figures/korimako_hand_annotated_song.png"'), 'Full-resolution approved PNG is not linked');
  require(figure[1].includes('Twenty hand-labelled syllables'), 'Hand-labelled count missing');
  require(figure[1].includes('original family labels'), 'Original family-label provenance missing');
  require(figure[1].includes('not an automatic segmentation'), 'Caption must distinguish hand annotation from model output');
  require(figure[1].includes('10.5061/dryad.h44j0zpfg'), 'Dryad DOI missing');
  require(figure[1].includes('10.3389/fevo.2021.755633'), 'Webb et al. DOI missing');
  require(!figure[1].includes('208262'), 'Withdrawn first candidate must not be referenced');
}
require(!page.includes('korimako_koe_annotated_song_preview'), 'Withdrawn first preview is referenced by the page');

if (errors.length) {
  console.error('Korimako annotated-figure provenance gate FAILED:');
  for (const error of errors) console.error(`  - ${error}`);
  process.exit(1);
}
console.log('Korimako annotated-figure provenance gate PASS');
console.log(`  approved PNG: ${hash(pngPath)}`);
console.log('  source: Dryad tutorial audio + exact Supplementary Data 3 intervals');
console.log('  20 hand-labelled syllables; 7 original families; no timing adjustment/remapping');
