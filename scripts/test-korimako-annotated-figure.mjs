#!/usr/bin/env node
/** Adversarial self-tests for the approved-figure gate (no fixture files added). */
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, copyFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname } from 'node:path';
import { execFileSync } from 'node:child_process';

const repo = new URL('../', import.meta.url).pathname;
const relPage = 'docs/experiments/nz-birdsong/index.html';
const relScript = 'scripts/verify-korimako-annotated-figure.mjs';
const cases = [
  ['approved artifact passes', () => {}, true],
  ['unapproved figure fails', (root) => {
    const p = join(root, 'docs/experiments/nz-birdsong/figures/korimako_hand_annotated_song.provenance.json');
    const d = JSON.parse(readFileSync(p)); d.approval.approved = false; writeFileSync(p, JSON.stringify(d));
  }, false],
  ['altered image fails', (root) => {
    const p = join(root, 'docs/experiments/nz-birdsong/figures/korimako_hand_annotated_song.png');
    writeFileSync(p, Buffer.concat([readFileSync(p), Buffer.from('tampered')]));
  }, false],
  ['legacy audio selection fails', (root) => {
    const p = join(root, 'docs/experiments/nz-birdsong/figures/korimako_hand_annotated_song.provenance.json');
    const d = JSON.parse(readFileSync(p)); d.audio.legacy_koe_wavs_directory_used = true; writeFileSync(p, JSON.stringify(d));
  }, false],
  ['timestamp adjustment fails', (root) => {
    const p = join(root, 'docs/experiments/nz-birdsong/figures/korimako_hand_annotated_song.provenance.json');
    const d = JSON.parse(readFileSync(p)); d.annotation.timing_adjustment_ms = 120; writeFileSync(p, JSON.stringify(d));
  }, false],
  ['model-output ambiguity fails', (root) => {
    const p = join(root, relPage); const s = readFileSync(p, 'utf8');
    writeFileSync(p, s.replace('not an automatic segmentation', 'an automatic segmentation'));
  }, false],
];
for (const [name, mutate, shouldPass] of cases) {
  const root = mkdtempSync(join(tmpdir(), 'korimako-gate-'));
  try {
    for (const rel of [relPage, relScript]) {
      const dest = join(root, rel); mkdirSync(dirname(dest), { recursive: true }); copyFileSync(join(repo, rel), dest);
    }
    const figDir = join(root, 'docs/experiments/nz-birdsong/figures');
    mkdirSync(figDir, { recursive: true });
    for (const suffix of ['png', 'webp', 'provenance.json']) {
      copyFileSync(join(repo, `docs/experiments/nz-birdsong/figures/korimako_hand_annotated_song.${suffix}`), join(figDir, `korimako_hand_annotated_song.${suffix}`));
    }
    mutate(root);
    let passed = true;
    try { execFileSync(process.execPath, [join(root, relScript)], { stdio: 'pipe' }); }
    catch { passed = false; }
    if (passed !== shouldPass) throw new Error(`${name}: expected pass=${shouldPass}, got ${passed}`);
    console.log(`PASS: ${name}`);
  } finally { rmSync(root, { recursive: true, force: true }); }
}
console.log('All provenance-gate adversarial tests passed.');
