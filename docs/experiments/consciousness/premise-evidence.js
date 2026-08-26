/**
 * Premise Evidence Tab — per-premise evidence breakdown for testable theories.
 * Each theory is organized by premise, and each premise has evidence entries
 * with direction indicators (supporting/refuting/mixed/etc.) and independence flags.
 *
 * All citations verified by the project maintainer through Crossref/OpenAlex/DataCite.
 */

const PREMISE_EVIDENCE = [
  {
    theory: "Integrated Information Theory (IIT)",
    proponent: "Giulio Tononi",
    testabilityRank: 1, // most testable
    summary: "IIT generates the most empirically testable predictions of any consciousness theory. Its premises map onto measurable neural quantities, and several have been directly tested — with mixed but informative results.",
    premises: [
      {
        text: "Φ (integrated information) measures consciousness and drops when consciousness is lost",
        evidence: [
          {
            citation: "Casali et al. 2013, Science Translational Medicine",
            doi: "10.1126/scitranslmed.3006294",
            finding: "PCI (Perturbational Complexity Index) discriminates waking/sleep/anesthesia/brain-damaged states. TMS-EEG measure derived from IIT principles.",
            direction: "supporting_with_caveats",
            independent: true,
            note: "Φ approximation alone insufficient; needs connectivity measures too."
          },
          {
            citation: "Kim et al. 2018, Frontiers in Human Neuroscience",
            doi: null,
            finding: "EEG-based Φ alone \"insufficient to discriminate certain states of anesthesia\" — needed multi-dimensional parameter space.",
            direction: "refuting_with_caveats",
            independent: true,
            note: "Partially refutes the strong claim that Φ alone tracks consciousness."
          },
          {
            citation: "2025, Neuroscience of Consciousness",
            doi: null,
            finding: "Φ decreases during anesthesia on fMRI at global and local levels, but authors note \"empirical data supporting this claim remain limited\".",
            direction: "supporting_with_caveats",
            independent: true,
            note: "Direction confirmed but empirical base acknowledged as thin."
          }
        ]
      },
      {
        text: "Cerebellum doesn't contribute to consciousness despite ~80B neurons (feedforward = low Φ)",
        evidence: [
          {
            citation: "Well-established clinical neurology",
            doi: null,
            finding: "Large cerebellar lesions don't abolish consciousness. Patients with cerebellar agenesis or massive resections retain full awareness.",
            direction: "supporting",
            independent: true,
            note: "One of the strongest empirical anchors for IIT's architectural claim."
          },
          {
            citation: "Tononi 2004, BMC Neuroscience",
            doi: "10.1186/1471-2202-5-42",
            finding: "Original IIT paper — computed cerebellar architecture yields low Φ due to feedforward connectivity.",
            direction: "supporting",
            independent: false,
            note: "From the theory's proponents; computes the prediction from the theory itself."
          }
        ]
      },
      {
        text: "Split-brain → split consciousness (Φ maximized within each hemisphere)",
        evidence: [
          {
            citation: "Tononi 2004, BMC Neuroscience",
            doi: "10.1186/1471-2202-5-42",
            finding: "Computed Φ=72 unified vs Φ=61 each hemisphere — the theory predicts split consciousness after callosotomy.",
            direction: "theoretical_prediction",
            independent: false,
            note: "Quantitative prediction from the theory, not yet directly tested via Φ measurement."
          },
          {
            citation: "Volz & Gazzaniga 2017; Pinto et al. 2017; Neuropsychologia 2021",
            doi: null,
            finding: "Some preserved cognitive unity after callosotomy. 2021 paper argues \"independent and unified consciousness co-exist\" in split-brain patients.",
            direction: "refuting",
            independent: true,
            note: "Challenges the strong split-consciousness prediction; the reality may be more nuanced."
          }
        ]
      },
      {
        text: "Posterior cortex is the 'hot zone' of consciousness (not prefrontal)",
        evidence: [
          {
            citation: "COGITATE Consortium 2025, Nature",
            doi: "10.1038/s41586-025-08888-1",
            finding: "256 participants, fMRI+MEG+iEEG. Found conscious content in visual/ventrotemporal cortex (partially supports IIT location claim) BUT lack of sustained synchronization within posterior cortex contradicts IIT's connectivity claim.",
            direction: "mixed",
            independent: true,
            note: "Adversarial collaboration — predictions agreed ex-ante by both IIT and GNW proponents."
          }
        ]
      },
      {
        text: "Feedforward AI not conscious regardless of size (unique IIT prediction)",
        evidence: [
          {
            citation: "Not yet empirically testable",
            doi: null,
            finding: "No current method can measure Φ in large-scale artificial systems or verify absence of consciousness.",
            direction: "untestable_currently",
            independent: true,
            note: "This is the key theory-discriminating prediction vs GNW — GNW allows that sufficiently large feedforward systems could be conscious; IIT denies this."
          }
        ]
      },
      {
        text: "Covert consciousness in vegetative state patients (Φ without behavioral output)",
        evidence: [
          {
            citation: "Owen et al. 2006, Science",
            doi: "10.1126/science.1130197",
            finding: "Vegetative patient followed commands via fMRI mental imagery (tennis imagery vs spatial navigation).",
            direction: "supporting",
            independent: true,
            note: "Also supports GNW (intact workspace, disconnected output). Theory-discriminating only if Φ can be measured."
          },
          {
            citation: "Cruse et al. 2011, Lancet",
            doi: null,
            finding: "~17% of vegetative patients show covert command-following with EEG-based methods.",
            direction: "supporting",
            independent: true,
            note: "Replicates the covert-consciousness finding with a more scalable method."
          }
        ]
      }
    ],
    discriminatingTests: [
      { name: "Wada test", description: "One hemisphere anesthetized, other conscious — supports IIT's prediction of local consciousness per hemisphere.", direction: "supporting" },
      { name: "Hemispherectomy", description: "One hemisphere removed, patient conscious — supports IIT (remaining hemisphere has high Φ).", direction: "supporting" },
      { name: "Locked-in syndrome", description: "Conscious with intact thalamocortical integration despite no motor output — supports IIT (Φ intact, output disconnected).", direction: "supporting" }
    ]
  },

  {
    theory: "Orch-OR (Penrose-Hameroff)",
    proponent: "Stuart Hameroff & Roger Penrose",
    testabilityRank: 2,
    summary: "Orch-OR makes physical predictions that are testable in principle — quantum coherence in microtubules, anesthetic action on tubulin — and a few have been tested. The results are contested, with independent physics analyses challenging the core mechanism.",
    premises: [
      {
        text: "Quantum coherence in microtubules at brain temperature (37°C) lasts long enough for neurophysiological relevance",
        evidence: [
          {
            citation: "Tegmark 2000, Physical Review E",
            doi: "10.1103/PhysRevE.61.4194",
            finding: "Calculated decoherence times ~10⁻¹³ to 10⁻²⁰ s, far too short for neural processes (~ms). Independent physics paper, not about consciousness.",
            direction: "strongly_refuting",
            independent: true,
            note: "The most cited critique. Not from consciousness researchers — pure physics calculation."
          },
          {
            citation: "Hagan, Hameroff & Tuszynski 2002, Physical Review E",
            doi: "10.1103/PhysRevE.65.061901",
            finding: "Recalculate decoherence, extend to 10⁻⁵ to 10⁻¹ s under alternative assumptions.",
            direction: "rebuttal",
            independent: false,
            note: "From Orch-OR proponents themselves — not an independent confirmation."
          },
          {
            citation: "McKemmish et al. 2009, Physical Review E",
            doi: "10.1103/PhysRevE.80.021912",
            finding: "Orch-OR requires biologically implausible energy gaps for tubulin states. Quantum computation framework doesn't map onto known microtubule physics.",
            direction: "refuting",
            independent: true,
            note: "Independent quantum physics analysis — challenges the physical plausibility of the mechanism."
          },
          {
            citation: "Engel et al. 2007, Nature",
            doi: "10.1038/nature05678",
            finding: "Quantum coherence in photosynthetic FMO complex (but at 77K, different system). Proves warm biology CAN sustain coherence — but for ~300fs, not the ms Orch-OR needs.",
            direction: "supporting_in_principle",
            independent: true,
            note: "Proof of principle for warm quantum biology, but the timescale gap is 6+ orders of magnitude."
          },
          {
            citation: "Babcock et al. 2024, J Phys Chem B",
            doi: null,
            finding: "UV superradiance in tryptophan networks in microtubules at 37°C. Closest evidence to date — but excitonic energy transfer ≠ quantum superposition Orch-OR requires.",
            direction: "suggestive_but_inconclusive",
            independent: true,
            note: "Genuine quantum effect in microtubules at body temperature. Suggestive but not the type of coherence Orch-OR needs."
          }
        ]
      },
      {
        text: "Anesthetics act through microtubules (disrupting quantum channels)",
        evidence: [
          {
            citation: "Craddock et al. 2012, PLoS ONE",
            doi: "10.1371/journal.pone.0037251",
            finding: "Computational predictions that anesthetics bind tubulin at quantum-relevant sites. Hameroff is co-author.",
            direction: "computational_only",
            independent: false,
            note: "In silico modeling only — not experimental validation."
          },
          {
            citation: "Kalra et al. 2023, ACS Central Science",
            doi: null,
            finding: "Experimental: anesthetics dampen quantum optical effects in microtubules. Genuine discriminating test (anesthetics vs non-anesthetic controls).",
            direction: "supporting",
            independent: true,
            note: "First experimental evidence that anesthetics interact with microtubule quantum properties. Not yet replicated."
          },
          {
            citation: "Khan, Wiest et al. 2024, eNeuro",
            doi: "10.1523/ENEURO.0291-24.2024",
            finding: "Epothilone B (microtubule stabilizer) delays anesthetic onset in rats by 69s (Cohen's d=1.9). Direct test of Orch-OR prediction.",
            direction: "supporting",
            independent: true,
            note: "Strong effect size. If microtubules are involved in anesthesia, stabilizing them should delay onset — and it does."
          },
          {
            citation: "Mashour 2024, Neuron",
            doi: "10.1016/j.neuron.2024.03.002",
            finding: "Mainstream anesthesia framework: GABA, NMDA, two-pore K channels, thalamocortical network disconnection. Microtubules mentioned but not primary. 190 references.",
            direction: "confounding",
            independent: true,
            note: "Anesthetics are promiscuous — they bind multiple targets. The microtubule effect may be real but not the primary mechanism."
          }
        ]
      },
      {
        text: "Penrose's gravity-driven objective reduction causes wavefunction collapse",
        evidence: [
          {
            citation: "No independent experimental tests exist",
            doi: null,
            finding: "Proposed experiments (FELIX satellite, Marshall optomechanical, matter-wave interferometry) not yet conducted. The core physical mechanism remains untested.",
            direction: "untestable_currently",
            independent: true,
            note: "This is the most speculative component of Orch-OR — Penrose's own physics beyond standard quantum mechanics."
          }
        ]
      }
    ],
    discriminatingTests: []
  }
];

// Direction → emoji + label mapping
const DIRECTION_MAP = {
  supporting:                 { icon: "🟢", label: "Supports",           color: "var(--green)" },
  supporting_with_caveats:    { icon: "🟡", label: "Supports (caveated)", color: "var(--gold)" },
  supporting_in_principle:    { icon: "🟡", label: "Supports in principle", color: "var(--gold)" },
  suggestive_but_inconclusive:{ icon: "🟡", label: "Suggestive",         color: "var(--gold)" },
  refuting:                   { icon: "🔴", label: "Refutes",            color: "var(--accent)" },
  refuting_with_caveats:      { icon: "🟠", label: "Refutes (caveated)", color: "var(--accent)" },
  strongly_refuting:          { icon: "🔴", label: "Strongly refutes",   color: "var(--accent)" },
  mixed:                      { icon: "🟠", label: "Mixed",              color: "var(--gold)" },
  theoretical_prediction:     { icon: "🔵", label: "Theoretical prediction", color: "var(--blue)" },
  untestable_currently:       { icon: "⚪", label: "Untestable (current)", color: "var(--ink-faint)" },
  rebuttal:                   { icon: "🔵", label: "Proponent rebuttal", color: "var(--blue)" },
  computational_only:         { icon: "🟠", label: "Computational only", color: "var(--gold)" },
  confounding:                { icon: "🟠", label: "Confounding",        color: "var(--gold)" }
};

/**
 * Renders the Premise Evidence tab into the target container.
 * Call: renderPremiseEvidence(document.getElementById('premise-evidence-list'))
 */
function renderPremiseEvidence(container) {
  if (!container) container = document.getElementById('premise-evidence-list');
  if (!container) return;
  container.innerHTML = '';

  PREMISE_EVIDENCE.forEach(theory => {
    // Theory-level card
    const card = document.createElement('div');
    card.className = 'card';
    let html = '';

    // Theory header
    html += `<div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">`;
    html += `<span style="font-family:var(--mono);font-size:0.7rem;color:var(--ink-faint);background:var(--bg-warm);padding:3px 10px;border-radius:12px;border:1px solid var(--border-soft);">RANK ${theory.testabilityRank}</span>`;
    html += `</div>`;
    html += `<h3>${theory.theory}</h3>`;
    html += `<p style="color:var(--ink-soft);font-style:italic;margin-bottom:12px;">${theory.proponent}</p>`;
    html += `<p style="font-size:0.92rem;color:var(--ink-soft);margin-bottom:20px;">${theory.summary}</p>`;

    // Premises
    theory.premises.forEach((premise, pIdx) => {
      const dirColors = premise.evidence.map(e => DIRECTION_MAP[e.direction]?.color || 'var(--border)');
      // Determine overall premise status from evidence directions
      const directions = premise.evidence.map(e => e.direction);
      let premiseStatus = 'contested';
      if (directions.every(d => d === 'supporting' || d === 'supporting_with_caveats' || d === 'supporting_in_principle')) {
        premiseStatus = directions.every(d => d === 'supporting') ? 'supported' : 'supported_caveated';
      } else if (directions.every(d => d === 'refuting' || d === 'strongly_refuting')) {
        premiseStatus = 'refuted';
      } else if (directions.some(d => d === 'untestable_currently') && directions.length === 1) {
        premiseStatus = 'untestable';
      }

      const statusConfig = {
        supported:          { label: "Supported", color: "var(--green)", bg: "var(--green-bg)" },
        supported_caveated: { label: "Supported (with caveats)", color: "var(--gold)", bg: "var(--gold-bg)" },
        contested:          { label: "Contested", color: "var(--accent)", bg: "var(--accent-bg)" },
        refuted:            { label: "Refuted", color: "var(--accent)", bg: "var(--accent-bg)" },
        untestable:         { label: "Untestable", color: "var(--ink-faint)", bg: "var(--bg-warm)" }
      };
      const sc = statusConfig[premiseStatus] || statusConfig.contested;

      // Premise block
      html += `<div style="margin-bottom:24px;border:1px solid var(--border-soft);border-radius:8px;overflow:hidden;">`;

      // Premise header
      html += `<div style="background:${sc.bg};padding:14px 18px;border-bottom:1px solid var(--border-soft);">`;
      html += `<div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap;">`;
      html += `<div style="flex:1;min-width:200px;">`;
      html += `<span style="font-family:var(--mono);font-size:0.68rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.08em;">Premise ${pIdx + 1}</span>`;
      html += `<div style="font-family:var(--serif);font-weight:500;font-size:1.05rem;color:var(--ink);margin-top:4px;line-height:1.4;">${premise.text}</div>`;
      html += `</div>`;
      html += `<span style="font-family:var(--mono);font-size:0.68rem;color:${sc.color};background:${sc.bg};border:1px solid ${sc.color}33;padding:4px 12px;border-radius:12px;white-space:nowrap;flex-shrink:0;">${sc.label}</span>`;
      html += `</div>`;
      html += `</div>`;

      // Evidence entries
      html += `<div style="padding:16px 18px;background:var(--bg-card);">`;
      premise.evidence.forEach((ev, eIdx) => {
        const dir = DIRECTION_MAP[ev.direction] || { icon: "⚪", label: ev.direction, color: "var(--ink-faint)" };

        html += `<div style="${eIdx > 0 ? 'border-top:1px solid var(--border-soft);margin-top:14px;padding-top:14px;' : ''}">`;
        html += `<div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:8px;">`;
        html += `<span style="font-size:1.1rem;flex-shrink:0;line-height:1.6;">${dir.icon}</span>`;
        html += `<div style="flex:1;">`;
        // Citation line
        html += `<div style="font-weight:600;font-size:0.92rem;color:var(--ink);">`;
        if (ev.doi) {
          html += `<a href="https://doi.org/${ev.doi}" target="_blank" style="color:var(--blue);text-decoration:none;">${ev.citation}</a>`;
        } else {
          html += ev.citation;
        }
        html += `</div>`;
        // Direction badge + independence flag
        html += `<div style="display:flex;gap:8px;flex-wrap:wrap;margin:6px 0 8px;">`;
        html += `<span style="font-family:var(--mono);font-size:0.62rem;text-transform:uppercase;letter-spacing:0.05em;padding:2px 8px;border-radius:10px;background:${dir.color}1a;color:${dir.color};">${dir.label}</span>`;
        if (ev.independent) {
          html += `<span style="font-family:var(--mono);font-size:0.62rem;text-transform:uppercase;letter-spacing:0.05em;padding:2px 8px;border-radius:10px;background:var(--green-bg);color:var(--green);">Independent source</span>`;
        } else {
          html += `<span style="font-family:var(--mono);font-size:0.62rem;text-transform:uppercase;letter-spacing:0.05em;padding:2px 8px;border-radius:10px;background:var(--accent-bg);color:var(--accent);">Theory proponents</span>`;
        }
        html += `</div>`;
        // Finding text
        html += `<div style="font-size:0.88rem;color:var(--ink-soft);line-height:1.6;">${ev.finding}</div>`;
        // Note
        if (ev.note) {
          html += `<div style="font-size:0.82rem;color:var(--ink-faint);font-style:italic;margin-top:6px;padding-left:12px;border-left:2px solid var(--border-soft);">${ev.note}</div>`;
        }
        html += `</div>`;
        html += `</div>`;
      });
      html += `</div>`; // close evidence entries div
      html += `</div>`; // close premise block
    });

    // Discriminating tests
    if (theory.discriminatingTests && theory.discriminatingTests.length > 0) {
      html += `<div class="cogitate-box" style="margin-top:20px;">`;
      html += `<h3>🧪 Discriminating Test Cases</h3>`;
      html += `<p style="font-size:0.88rem;color:var(--ink-soft);margin-bottom:14px;">Clinical phenomena that distinguish this theory's predictions from rivals:</p>`;
      theory.discriminatingTests.forEach(tc => {
        const dir = DIRECTION_MAP[tc.direction] || { icon: "🟢", label: "", color: "var(--green)" };
        html += `<div class="finding">`;
        html += `<span class="finding-icon">${dir.icon}</span>`;
        html += `<span class="finding-text"><strong>${tc.name}</strong> — ${tc.description}</span>`;
        html += `</div>`;
      });
      html += `</div>`;
    }

    card.innerHTML = html;
    container.appendChild(card);
  });

  // Legend at the bottom
  const legend = document.createElement('div');
  legend.className = 'card';
  let legendHtml = '<h3>Direction Indicators</h3>';
  legendHtml += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-top:8px;">';
  const seen = new Set();
  Object.values(DIRECTION_MAP).forEach(d => {
    if (seen.has(d.icon)) return;
    seen.add(d.icon);
    legendHtml += `<div style="display:flex;align-items:center;gap:8px;font-size:0.85rem;"><span style="font-size:1.1rem;">${d.icon}</span><span style="color:var(--ink-soft);">${d.label}</span></div>`;
  });
  legendHtml += '</div>';
  legendHtml += '<div style="margin-top:16px;padding-top:16px;border-top:1px solid var(--border-soft);font-size:0.82rem;color:var(--ink-faint);">';
  legendHtml += '<strong style="color:var(--green);">Independent source</strong> = from researchers outside the theory\'s proponents &nbsp;·&nbsp; ';
  legendHtml += '<strong style="color:var(--accent);">Theory proponents</strong> = from the theory\'s own advocates';
  legendHtml += '</div>';
  legend.innerHTML = legendHtml;
  container.appendChild(legend);
}
