/**
 * Defining Consciousness Tab — the problem of definition, working definitions
 * from the literature, and the overgeneration test (reductio ad absurdum
 * applied to the scope of each theory's criteria).
 */

const DEFINING_CONSCIOUSNESS = {
  intro: "Theories of consciousness face a foundational problem: before you can explain consciousness, you need to say what it IS. The term \"consciousness\" is used in at least five distinct senses in the philosophical and scientific literature. A theory that explains one sense may say nothing about another — and a theory whose criteria for consciousness are too permissive will classify rocks and thermostats as conscious, which most researchers take as a reductio ad absurdum.",

  definitions: [
    {
      term: "Phenomenal consciousness",
      attribution: "Ned Block",
      source: "Block 1995, \"On a Confusion About a Function of Consciousness\"",
      description: "What it feels like from the inside — the raw subjective quality of experience (qualia). The redness of red, the painfulness of pain. This is the \"hard problem\" target: why does there feel like anything at all?",
      keyQuestion: "Is there something it is like to be this system?",
      scope: "Most theories of consciousness aim to explain this."
    },
    {
      term: "Access consciousness",
      attribution: "Ned Block",
      source: "Block 1995, same paper",
      description: "Information available for reasoning, speech, and action control. The functional, reportable aspect of mental states. You can verbally report access-conscious content and use it to guide behavior.",
      keyQuestion: "Is the information globally available for report, reasoning, and action?",
      scope: "Global Workspace Theory primarily targets this sense."
    },
    {
      term: "Global state consciousness",
      attribution: "Tim Bayne",
      source: "Bayne 2010, The Unity of Consciousness; Bayne & Hohwy 2013",
      description: "The overall level of consciousness — awake vs. asleep vs. anesthetized vs. vegetative vs. in a coma. This is a property of the whole organism at a time, not of a particular mental content.",
      keyQuestion: "What is the organism's overall state of arousal and awareness?",
      scope: "Clinical assessments (Glasgow Coma Scale, CRS-R) and anesthesia research target this."
    },
    {
      term: "Narrative / Reflective consciousness",
      attribution: "Dennett, Schooler, others",
      source: "Dennett 1991, Consciousness Explained",
      description: "Self-awareness and metacognition — the ability to think about one's own mental states, construct a narrative self, and reflect on experiences. The highest-order form of consciousness.",
      keyQuestion: "Can the system represent and reason about its own mental states?",
      scope: "Higher-order theories (HOT, AST) target this level."
    },
    {
      term: "Primary consciousness",
      attribution: "Gerald Edelman",
      source: "Edelman 2003, \"Naturalizing Consciousness\"",
      description: "Present-moment sensory experience without self-reflection — the kind of awareness shared by many animals. Experience of the world here and now, without the ability to reflect on the fact that one is experiencing.",
      keyQuestion: "Does the system have present-moment sensory awareness?",
      scope: "Edelman's theory of neuronal group selection (TNGS) targets this."
    }
  ],

  overgenerationTest: {
    description: "The overgeneration test is a reductio ad absurdum applied to the scope of a theory's criteria for consciousness. The logic is simple:",
    steps: [
      "A theory proposes criteria C for consciousness.",
      "If C is satisfied by objects that common sense and most definitions agree are NOT conscious (rocks, oceans, thermostats, bacteria, radio networks)...",
      "Then either (a) those objects ARE conscious — which contradicts common sense and most working definitions, or (b) the theory's criteria C are too permissive and need tightening.",
      "A theory that bites the bullet on (a) — accepting that thermostats are conscious — is making a radical panpsychist claim. This is philosophically legitimate but empirically unfalsifiable.",
      "A theory that resists (a) — insisting its criteria only apply to brains — needs to explain why, and that explanation often smuggles in additional criteria."
    ],
    cases: [
      {
        theory: "IIT",
        criterion: "Φ > 0 (any system with nonzero integrated information is conscious)",
        absurdObject: "A thermostat",
        absurdReasoning: "A thermostat has internal states that causally affect each other — it has nonzero integrated information. If Φ > 0 means conscious, a thermostat is conscious.",
        proponentResponse: "accept",
        proponentStance: "IIT proponents (Tononi, Koch) explicitly accept this. IIT implies panpsychism: any system with Φ > 0 has some minimal consciousness. They argue this is a feature, not a bug — consciousness is fundamental and graded.",
        verdict: "fails_but_accepted",
        note: "Philosophically coherent (panpsychism has a long tradition) but empirically unfalsifiable at the low end."
      },
      {
        theory: "Orch-OR",
        criterion: "Quantum coherence / superposition in microtubules causes consciousness",
        absurdObject: "Photosynthetic bacteria",
        absurdReasoning: "Engel et al. (2007) demonstrated quantum coherence in the FMO complex of photosynthetic bacteria at 77K. If quantum coherence = consciousness, photosynthetic bacteria are conscious.",
        proponentResponse: "resist",
        proponentStance: "Hameroff argues that microtubule quantum coherence is special — it involves specific tubulin states and orchestrated reduction, not just any quantum process. But this adds criteria beyond \"quantum coherence\" alone.",
        verdict: "fails_resisted",
        note: "The added specificity (microtubules, orchestrated reduction, Penrose gravity) makes the theory harder to overgenerate but also harder to test."
      },
      {
        theory: "GNW",
        criterion: "Global broadcast of information through a workspace = consciousness",
        absurdObject: "A broadcast radio network",
        absurdReasoning: "A radio network broadcasts information from a central station to many receivers. If global broadcast = consciousness, a radio network is conscious.",
        proponentResponse: "resist",
        proponentStance: "GNW proponents (Dehaene, Baars) specify that the workspace must be a neuronal architecture with long-range recurrent connections, nonlinear ignition dynamics, and specific cortical anatomy. A radio network lacks these.",
        verdict: "passes_resisted",
        note: "The neuronal specification successfully blocks the reductio. But it also makes GNW less general — it can't say anything about non-neuronal systems."
      },
      {
        theory: "Higher-Order Theories (HOT)",
        criterion: "Meta-representation (representing one's own mental state) = consciousness",
        absurdObject: "A camera with a self-monitoring system",
        absurdReasoning: "A security camera system that monitors its own status (battery, lens, field of view) has meta-representations. If meta-representation = consciousness, a self-monitoring camera is conscious.",
        proponentResponse: "resist",
        proponentStance: "HOT proponents (Rosenthal, Lau) specify that the meta-representation must be a mental state of the right kind — a thought about a mental state, implemented in neural architecture, not just any computational self-monitoring.",
        verdict: "fails_resisted",
        note: "The \"right kind\" qualifier is doing heavy lifting. Without it, the theory overgenerates; with it, the theory becomes architecture-specific."
      }
    ]
  }
};

// Verdict → display config for the overgeneration table
const OVERGEN_VERDICT = {
  passes_resisted: { label: "Passes", color: "var(--green)", bg: "var(--green-bg)", icon: "✅", desc: "Criteria successfully block absurd implications" },
  fails_but_accepted: { label: "Fails (accepted)", color: "var(--gold)", bg: "var(--gold-bg)", icon: "🤷", desc: "Overgenerates, but proponents embrace the implication (panpsychism)" },
  fails_resisted: { label: "Fails (resisted)", color: "var(--accent)", bg: "var(--accent-bg)", icon: "⚠️", desc: "Overgenerates; proponents add extra criteria to block it" }
};

const PROPONENT_RESPONSE = {
  accept: { label: "Accept", color: "var(--gold)", desc: "Proponents embrace the implication" },
  resist: { label: "Resist", color: "var(--accent)", desc: "Proponents deny the implication" }
};

/**
 * Renders the Defining Consciousness tab into the target container.
 * Call: renderDefiningConsciousness(document.getElementById('defining-consciousness-list'))
 */
function renderDefiningConsciousness(container) {
  if (!container) container = document.getElementById('defining-consciousness-content');
  if (!container) return;
  container.innerHTML = '';

  // === Section 1: The Problem ===
  const problemCard = document.createElement('div');
  problemCard.className = 'card';
  problemCard.innerHTML = `
    <h3>The Problem of Definition</h3>
    <p style="font-size:0.95rem;color:var(--ink);line-height:1.8;">${DEFINING_CONSCIOUSNESS.intro}</p>
    <div style="margin-top:20px;padding:16px 20px;background:var(--bg-warm);border:1px solid var(--border-soft);border-radius:6px;">
      <p style="font-size:0.88rem;color:var(--ink-soft);font-style:italic;">
        <strong style="font-style:normal;color:var(--accent);">The core tension:</strong>
        If your theory's criteria for consciousness are too narrow, you risk excluding animals, infants, or AI systems that may genuinely be conscious.
        If your criteria are too broad, you risk including thermostats and rocks — which undermines the very concept.
        The <em>overgeneration test</em> (below) checks whether a theory's criteria are too broad.
      </p>
    </div>
  `;
  container.appendChild(problemCard);

  // === Section 2: Working Definitions ===
  const defsCard = document.createElement('div');
  defsCard.className = 'card';
  let defsHtml = '<h3>Working Definitions from the Literature</h3>';
  defsHtml += '<p style="font-size:0.9rem;color:var(--ink-soft);margin-bottom:20px;">The word "consciousness" is used in at least five distinct senses. A theory may target one, several, or all of these — and conflating them is a common source of confusion.</p>';

  defsHtml += '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;">';
  DEFINING_CONSCIOUSNESS.definitions.forEach(def => {
    defsHtml += `
      <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:20px;">
        <div style="font-family:var(--serif);font-weight:700;font-size:1.15rem;color:var(--ink);margin-bottom:4px;">${def.term}</div>
        <div style="font-family:var(--mono);font-size:0.7rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:12px;">${def.attribution} · ${def.source}</div>
        <p style="font-size:0.88rem;color:var(--ink-soft);line-height:1.6;margin-bottom:14px;">${def.description}</p>
        <div style="padding:10px 14px;background:var(--bg-warm);border:1px solid var(--border-soft);border-radius:6px;margin-bottom:12px;">
          <div style="font-family:var(--mono);font-size:0.65rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Diagnostic question</div>
          <div style="font-size:0.88rem;color:var(--ink);font-style:italic;">${def.keyQuestion}</div>
        </div>
        <div style="font-size:0.8rem;color:var(--blue);">
          <strong style="font-family:var(--mono);font-size:0.65rem;text-transform:uppercase;letter-spacing:0.06em;">Scope:</strong> ${def.scope}
        </div>
      </div>
    `;
  });
  defsHtml += '</div>';
  defsCard.innerHTML = defsHtml;
  container.appendChild(defsCard);

  // === Section 3: The Overgeneration Test ===
  const og = DEFINING_CONSCIOUSNESS.overgenerationTest;
  const ogCard = document.createElement('div');
  ogCard.className = 'card';
  let ogHtml = '<h3>The Overgeneration Test</h3>';
  ogHtml += `<p style="font-size:0.95rem;color:var(--ink);line-height:1.8;margin-bottom:16px;">${og.description}</p>`;

  // Steps
  ogHtml += '<div style="background:#faf6ed;border:1px solid var(--border);border-radius:8px;padding:20px 24px;margin-bottom:24px;">';
  ogHtml += '<div style="font-family:var(--serif);font-weight:700;font-size:1rem;margin-bottom:12px;">The Logic</div>';
  og.steps.forEach((step, i) => {
    ogHtml += `<div style="display:flex;gap:12px;margin-bottom:10px;align-items:flex-start;">`;
    ogHtml += `<span style="font-family:var(--mono);font-size:0.75rem;color:var(--accent);font-weight:600;flex-shrink:0;width:24px;text-align:right;">${i + 1}.</span>`;
    ogHtml += `<span style="font-size:0.9rem;color:var(--ink-soft);line-height:1.6;">${step}</span>`;
    ogHtml += `</div>`;
  });
  ogHtml += '</div>';

  // Cases as cards
  ogHtml += '<div style="font-family:var(--serif);font-weight:700;font-size:1.05rem;margin-bottom:16px;">Applying the test to each theory</div>';
  og.cases.forEach((tc, i) => {
    const vc = OVERGEN_VERDICT[tc.verdict] || OVERGEN_VERDICT.fails_resisted;
    const pc = PROPONENT_RESPONSE[tc.proponentResponse] || PROPONENT_RESPONSE.resist;

    ogHtml += `<div style="margin-bottom:20px;border:1px solid var(--border);border-radius:8px;overflow:hidden;">`;
    // Header
    ogHtml += `<div style="background:var(--bg-warm);padding:14px 20px;border-bottom:1px solid var(--border-soft);">`;
    ogHtml += `<div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">`;
    ogHtml += `<div style="font-family:var(--serif);font-weight:700;font-size:1.15rem;color:var(--ink);">${tc.theory}</div>`;
    ogHtml += `<div style="display:flex;gap:8px;flex-wrap:wrap;">`;
    ogHtml += `<span style="font-family:var(--mono);font-size:0.62rem;text-transform:uppercase;letter-spacing:0.05em;padding:3px 10px;border-radius:12px;background:${vc.bg};color:${vc.color};">${vc.icon} ${vc.label}</span>`;
    ogHtml += `<span style="font-family:var(--mono);font-size:0.62rem;text-transform:uppercase;letter-spacing:0.05em;padding:3px 10px;border-radius:12px;background:var(--bg-card);color:${pc.color};border:1px solid ${pc.color}44;">Proponents: ${pc.label}</span>`;
    ogHtml += `</div>`;
    ogHtml += `</div>`;
    ogHtml += `</div>`;

    // Body
    ogHtml += `<div style="padding:18px 20px;background:var(--bg-card);">`;
    ogHtml += `<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:14px;" class="overgen-grid">`;
    // Criterion
    ogHtml += `<div><div style="font-family:var(--mono);font-size:0.65rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Criterion for consciousness</div><div style="font-size:0.88rem;color:var(--ink);">${tc.criterion}</div></div>`;
    // Absurd object
    ogHtml += `<div><div style="font-family:var(--mono);font-size:0.65rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Absurd implication</div><div style="font-size:0.88rem;color:var(--ink);"><strong>${tc.absurdObject}</strong> is conscious</div></div>`;
    ogHtml += `</div>`;

    // Reasoning
    ogHtml += `<div style="padding:12px 16px;background:#faf6ed;border:1px solid var(--border-soft);border-radius:6px;margin-bottom:12px;">`;
    ogHtml += `<div style="font-family:var(--mono);font-size:0.65rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Reductio reasoning</div>`;
    ogHtml += `<div style="font-size:0.86rem;color:var(--ink-soft);line-height:1.6;">${tc.absurdReasoning}</div>`;
    ogHtml += `</div>`;

    // Proponent stance
    ogHtml += `<div style="padding:12px 16px;border-left:3px solid ${pc.color};background:${pc.color}0a;border-radius:0 6px 6px 0;margin-bottom:12px;">`;
    ogHtml += `<div style="font-family:var(--mono);font-size:0.65rem;color:var(--ink-faint);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Proponent stance: ${pc.label}</div>`;
    ogHtml += `<div style="font-size:0.86rem;color:var(--ink-soft);line-height:1.6;">${tc.proponentStance}</div>`;
    ogHtml += `</div>`;

    // Note
    ogHtml += `<div style="font-size:0.82rem;color:var(--ink-faint);font-style:italic;padding-left:12px;border-left:2px solid var(--border-soft);">${tc.note}</div>`;
    ogHtml += `</div>`;
    ogHtml += `</div>`;
  });

  ogHtml += '</div>';
  ogCard.innerHTML = ogHtml;
  container.appendChild(ogCard);

  // === Section 4: Summary Table ===
  const tableCard = document.createElement('div');
  tableCard.className = 'card';
  let tableHtml = '<h3>Summary: Overgeneration Test Results</h3>';
  tableHtml += '<p style="font-size:0.9rem;color:var(--ink-soft);margin-bottom:16px;">A compact comparison of how each theory fares against the overgeneration test.</p>';
  tableHtml += '<table class="theory-table" style="font-size:0.85rem;">';
  tableHtml += '<thead><tr>';
  tableHtml += '<th>Theory</th>';
  tableHtml += '<th>Absurd Object</th>';
  tableHtml += '<th>Overgeneration</th>';
  tableHtml += '<th>Proponents</th>';
  tableHtml += '<th>Assessment</th>';
  tableHtml += '</tr></thead><tbody>';
  og.cases.forEach(tc => {
    const vc = OVERGEN_VERDICT[tc.verdict] || OVERGEN_VERDICT.fails_resisted;
    const pc = PROPONENT_RESPONSE[tc.proponentResponse] || PROPONENT_RESPONSE.resist;
    tableHtml += `<tr>`;
    tableHtml += `<td><strong>${tc.theory}</strong></td>`;
    tableHtml += `<td style="color:var(--ink-soft);">${tc.absurdObject}</td>`;
    tableHtml += `<td><span style="font-family:var(--mono);font-size:0.68rem;padding:2px 8px;border-radius:10px;background:${vc.bg};color:${vc.color};">${vc.label}</span></td>`;
    tableHtml += `<td><span style="font-family:var(--mono);font-size:0.68rem;padding:2px 8px;border-radius:10px;background:var(--bg-warm);color:${pc.color};border:1px solid ${pc.color}33;">${pc.label}</span></td>`;
    tableHtml += `<td style="font-size:0.82rem;color:var(--ink-soft);">${vc.desc}</td>`;
    tableHtml += `</tr>`;
  });
  tableHtml += '</tbody></table>';

  // Responsive note
  tableHtml += '<style>@media(max-width:768px){.overgen-grid{grid-template-columns:1fr !important;}}</style>';

  tableCard.innerHTML = tableHtml;
  container.appendChild(tableCard);

  // === Closing reflection ===
  const closeCard = document.createElement('div');
  closeCard.className = 'card';
  closeCard.innerHTML = `
    <h3>What This Tells Us</h3>
    <div style="font-size:0.92rem;color:var(--ink);line-height:1.8;">
      <p style="margin-bottom:14px;">The overgeneration test reveals a fundamental trade-off in consciousness theory:</p>
      <ul style="margin:0 0 14px 20px;">
        <li style="margin-bottom:8px;"><strong style="color:var(--gold);">Theories that accept the absurd implication</strong> (like IIT's panpsychism) are philosophically bold but empirically unfalsifiable at the margins — you cannot test whether a thermostat is minimally conscious.</li>
        <li style="margin-bottom:8px;"><strong style="color:var(--accent);">Theories that resist the absurd implication</strong> (like GNW, HOT) must add architectural or functional constraints — but those constraints are often underspecified and hard to justify independently.</li>
        <li style="margin-bottom:8px;"><strong style="color:var(--blue);">The most productive theories</strong> are those whose criteria are permissive enough to generate novel predictions (e.g., IIT's feedforward AI prediction) but constrained enough to avoid absurdity in the cases we care about (clinical, behavioral).</li>
      </ul>
      <p style="color:var(--ink-soft);font-style:italic;padding:16px 20px;background:var(--bg-warm);border:1px solid var(--border-soft);border-radius:6px;">
        The overgeneration test does not refute any theory. It reveals the price of admission — what you must accept to hold the theory — and forces proponents to be explicit about whether they're paying it.
      </p>
    </div>
  `;
  container.appendChild(closeCard);
}
