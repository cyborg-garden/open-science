#!/usr/bin/env node
/** Offline integrity gate for the non-destructive guided review packet. */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const root=new URL('../docs/experiments/nz-birdsong/',import.meta.url).pathname;
const manifest=JSON.parse(readFileSync(join(root,'review_assets/manifest.json'),'utf8'));
const errors=[];const require=(x,m)=>{if(!x)errors.push(m)};
require(manifest.schema==='korimako-guided-review-v1','wrong schema');
require(manifest.n_cases===48,'pilot must contain 48 cases');
require(new Set(manifest.cases.map(c=>c.id)).size===48,'duplicate case IDs');
for(const kind of ['family_disagreement','fine_disagreement','unmatched_prediction'])require(manifest.cases.filter(c=>c.kind===kind).length===16,`wrong ${kind} count`);
require(manifest.reference_provenance.includes('not independently expert-vetted'),'reference vetting limitation missing');
require(manifest.case_provenance.includes('reviewing changes no source annotation'),'non-destructive scope missing');
for(const c of manifest.cases){
  require(c.song_id&&c.individual,`missing identity ${c.id}`);
  require(c.pred_offset_ms>c.pred_onset_ms,`invalid model interval ${c.id}`);
  require(c.p_family>=0&&c.p_family<=1,`invalid confidence ${c.id}`);
  if(c.kind==='unmatched_prediction')require(!c.has_human_match&&!c.ref_segment_id,`fabricated human match ${c.id}`);
  else require(c.has_human_match&&c.ref_segment_id&&c.ref_end_ms>c.ref_start_ms,`missing real reference ${c.id}`);
  for(const key of ['crop_image','context_image','crop_audio','whole_audio'])require(existsSync(join(root,c[key])),`missing ${c[key]}`);
  for(const fam of c.alternative_families)require((manifest.references['family::'+fam]||[]).length>0,`empty family gallery ${fam}`);
}
let refs=0;
for(const [key,entries] of Object.entries(manifest.references)){
  if(!entries.length)require(key.startsWith('fine::'),`unexpected empty reference group ${key}`);
  for(const r of entries){
    refs++;
    require(r.split==='train',`non-training reference ${r.id}`);
    require(key===`family::${r.family}`||key===`fine::${r.family}|||${r.fine}`,`reference substituted under wrong label ${key} / ${r.id}`);
    for(const k of ['image','audio'])require(existsSync(join(root,r[k])),`missing ${r[k]}`);
  }
}
require(refs===112,'reference count changed unexpectedly');
require(manifest.browser_audio_encoding?.includes('original PCM source WAVs unchanged'),'browser/source audio distinction missing');
if(errors.length){console.error('Guided-review packet gate FAILED');for(const e of errors)console.error('  - '+e);process.exit(1)}
console.log(`Guided-review packet PASS: ${manifest.n_cases} cases; ${refs} training-only reference units; all assets present; no label substitution`);
