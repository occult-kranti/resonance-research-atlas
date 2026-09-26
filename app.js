import {schumannIdeal, oscillator, spectralResolution, binomialUpperTail} from './models.js';

const $ = (selector, parent = document) => parent.querySelector(selector);
const main = $('#main');
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const list = value => Array.isArray(value) ? value : value == null ? [] : [value];
const readable = value => typeof value === 'string' ? value : typeof value === 'object' && value ? value.text || value.summary || value.title || JSON.stringify(value) : String(value ?? '');
const slug = value => String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '-');
const safeUrl = value => {
  const url = String(value || '').trim();
  if (/^(https?:\/\/|\.?\.?\/|#)/i.test(url) || (!/[:\\]/.test(url) && !url.startsWith('//'))) return escape(url);
  return '#';
};
const pill = (value = 'hypothesis') => `<span class="pill ${slug(value)}">${escape(String(value).replace(/[_-]/g, ' '))}</span>`;
const prose = value => list(value).map(v => escape(readable(v))).join('<br>');
const bullets = value => `<ul class="inline-list">${list(value).map(v => `<li>${escape(readable(v))}</li>`).join('')}</ul>`;
const linkAttrs = url => /^https?:\/\//.test(url || '') ? ' target="_blank" rel="noopener noreferrer"' : '';
let data = {meta:{},experiments:[],sources:[],history:[],rounds:[],roadmap:[],network:{nodes:[],edges:[]},projects:[]};
let dataIssue = '';
let activeModel = 'schumann';
let activeProcess = 'separation';
let sourceState = {query:'',evidence:'all',type:'all'};
let selectedNode = null;
const pageLabels = {overview:'Overview',experiments:'Experiments & models',sources:'Source library',history:'History & alchemy',dreams:'Dreams & perception',network:'Evidence network',panel:'Panel & roadmap',projects:'Connected projects'};

const earthSVG = (hero = false) => `<svg class="${hero ? 'hero-art' : 'mini-earth'}" viewBox="0 0 560 410" role="img" aria-label="Conceptual Earth cavity: an idealized spherical field, not a scale drawing"><defs><radialGradient id="earth-${hero}"><stop stop-color="${hero ? '#41685a' : '#e0e9d4'}"/><stop offset="1" stop-color="${hero ? '#204c41' : '#edf2e2'}"/></radialGradient><clipPath id="sphere-${hero}"><circle cx="305" cy="197" r="116"/></clipPath></defs><g fill="none" stroke="${hero ? '#648875' : '#b6c7a4'}" stroke-width=".8"><ellipse cx="305" cy="197" rx="207" ry="89" transform="rotate(-29 305 197)"/><ellipse cx="305" cy="197" rx="183" ry="156" transform="rotate(22 305 197)" stroke-dasharray="2 7"/><circle cx="305" cy="197" r="145"/><circle cx="305" cy="197" r="165" opacity=".4"/><path d="M71 197h463M305 25v344" stroke-dasharray="2 7" opacity=".5"/></g><circle cx="305" cy="197" r="116" fill="url(#earth-${hero})" stroke="${hero ? '#8eac91' : '#91ab7c'}" stroke-width="1.1"/><g fill="none" stroke="${hero ? '#77977e' : '#a5bc8e'}" stroke-width=".8" clip-path="url(#sphere-${hero})"><ellipse cx="305" cy="197" rx="36" ry="116"/><ellipse cx="305" cy="197" rx="77" ry="116"/><ellipse cx="305" cy="197" rx="104" ry="116"/><path d="M189 197h232M194 158q111-45 222 0M212 123q93-31 186 0M194 236q111 45 222 0M212 271q93 31 186 0"/><path d="M196 189c15-4 20-27 37-15s18 24 35 17 21-20 40-16 14 19 34 25 34-3 49 6 18 18 30 10" stroke="${hero ? '#d0b38a' : '#a47850'}" stroke-width="2"/></g><g fill="${hero ? '#c4cfb8' : '#7c946a'}" font-family="ui-sans-serif, sans-serif" font-size="8" letter-spacing="1.3"><text x="407" y="64">IDEAL SPHERICAL CAVITY</text><text x="80" y="332">l = 1</text><text x="418" y="345">R</text></g><g stroke="${hero ? '#a2b79a' : '#829d6e'}" stroke-width=".7" fill="none"><path d="M403 69l-26 34M112 326l36-38M305 197l91 119"/></g><circle cx="159" cy="245" r="4" fill="${hero ? '#c49a70' : '#a7774e'}"/><circle cx="407" cy="134" r="3" fill="${hero ? '#b7c9a4' : '#799564'}"/></svg>`;

const icon = kind => `<svg viewBox="0 0 44 44" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">${kind === 'history' ? '<path d="M16 7h12M18 7v13L9 34q-2 4 3 4h20q5 0 3-4l-9-14V7M14 28h16"/><circle cx="19" cy="32" r="1"/><circle cx="25" cy="29" r="1"/>' : kind === 'network' ? '<path d="M11 12l21 8M11 12l10 23M32 20L21 35"/><circle cx="11" cy="12" r="5"/><circle cx="32" cy="20" r="5"/><circle cx="21" cy="35" r="4"/>' : '<rect x="9" y="8" width="26" height="30" rx="2"/><path d="M15 15h14M15 22h14M15 29h9M16 5v6M28 5v6"/>'}</svg>`;

function intro(eyebrow, title, description, extra = '') {
  return `<div class="page-intro"><div><div class="eyebrow">${eyebrow}</div><h1>${title}</h1><p>${description}</p></div>${extra}</div>`;
}

function sourceChips(ids) {
  return `<div class="source-chips">${list(ids).map(id => {
    const source = data.sources.find(s => s.id === id);
    return `<a class="source-chip" href="#sources?source=${encodeURIComponent(id)}" title="${escape(source?.title || id)}">${escape(id)} ↗</a>`;
  }).join('')}</div>`;
}

function artifactLinks(artifacts) {
  return list(artifacts).length ? `<div class="artifacts">${list(artifacts).map(a => `<a href="${safeUrl(a.url || a.path)}"${linkAttrs(a.url)}> ${escape(a.label || a.title || 'View artifact')} ↗</a>`).join('')}</div>` : '';
}

function overview() {
  return `${intro('AN OPEN RESEARCH OBSERVATORY', 'A field guide to the unknown.', 'Historical ideas, modern measurements, and experiments you can inspect.', `<div class="date-tag">${escape(data.meta.updated || '')}</div>`)}
  ${dataIssue ? `<div class="status-notice">${escape(dataIssue)}</div>` : ''}
  <section class="hero"><div class="hero-copy"><div class="eyebrow">CURIOSITY, WITH A METHOD</div><h1>Questions worth<br><em>measuring.</em></h1><p>Explore resonance, matter, and the ideas that connect them. Move from an intriguing claim to a source, a model, and a test.</p><div class="hero-actions"><a class="button light" href="#experiments">Explore experiments <span aria-hidden="true">↗</span></a><a class="text-link" href="#sources">Open source library →</a></div></div>${earthSVG(true)}<div class="hero-foot">SPHERICAL CAVITY / CONCEPTUAL FIELD STUDY</div></section>
  <div class="stats" aria-label="Research collection counts"><div class="stat"><div class="value">${String(data.experiments.length).padStart(2,'0')}</div><div class="label">EXPERIMENTS & HYPOTHESES</div></div><div class="stat"><div class="value">${String(data.sources.length).padStart(2,'0')}</div><div class="label">REFERENCED SOURCES</div></div><div class="stat"><div class="value">03<span class="suffix">interactive</span></div><div class="label">TRANSPARENT MODELS</div></div><div class="stat"><div class="value">${String(data.rounds.length).padStart(2,'0')}</div><div class="label">PLANNED & RECORDED ROUNDS</div></div></div>
  <div class="correction-strip"><span class="pill documented">CORRECTION NOTE</span><span>The first Resonant Vessels interpretation has been revised against its sources.</span><a href="projects/resonant-vessels/research-corrections.html">Read what changed ↗</a></div>
  <div class="section-heading"><div><h2>Start with a measurable question</h2><p>Adjust a model. Read its assumptions. Follow the evidence.</p></div><a class="text-link" href="#experiments">All experiments ↗</a></div>
  <div class="grid-two"><article class="card"><div class="card-top"><span class="small-label">MODEL 01 / EARTH–IONOSPHERE</span>${pill('idealized model')}</div><div class="focus-model"><div><h3 class="serif">What does a planet<br>sound like in a model?</h3><p>Explore the ideal spherical cavity frequencies and why real Schumann resonances differ.</p><a href="#experiments?model=schumann" class="text-link" style="display:inline-block;margin-top:14px">Open the model <span aria-hidden="true">↗</span></a></div>${earthSVG()}</div><div class="model-inline-result"><span class="big-number">${schumannIdeal().toFixed(2)}</span><span class="unit">Hz</span><span class="model-caveat">Ideal first mode · R = 6,371 km</span></div></article>
  <article class="card"><div class="small-label">HOW THIS ATLAS WORKS</div><h3 class="serif" style="font-size:25px">Keep the evidence in view.</h3><p>A historical account and a replicated result answer different questions. Each has a place here.</p><ol class="evidence-steps"><li><span class="evidence-step-dot">1</span> Find the original source <small>PROVENANCE</small></li><li><span class="evidence-step-dot">2</span> State a testable claim <small>HYPOTHESIS</small></li><li><span class="evidence-step-dot">3</span> Define a measurement <small>EXPERIMENT</small></li><li><span class="evidence-step-dot">4</span> Report what survives <small>REVIEW</small></li></ol></article></div>
  <div class="section-heading"><div><h2>Follow a thread</h2><p>Different ways into the same research workspace.</p></div></div>
  <div class="grid-three"><article class="card feature-card">${icon('history')}<h3>From manuscript to material</h3><p>Read historical claims alongside conceptual diagrams of phase transfer, separation, material state, and branching.</p><a class="text-link" href="#history">History & alchemy ↗</a></article><article class="card feature-card">${icon('network')}<h3>See the connections</h3><p>Inspect how sources, claims, models, and experiments connect. Every edge has a stated relationship.</p><a class="text-link" href="#network">Evidence network ↗</a></article><article class="card feature-card">${icon('panel')}<h3>Research, under review</h3><p>Read panel decisions, unresolved questions, and the next experiments in the shared roadmap.</p><a class="text-link" href="#panel">Panel & roadmap ↗</a></article></div>
  <div class="bottom-banner"><div><h3>A human has many measurable signals.</h3><p>Electrical activity, movement, sound, and radiation require different instruments and units.</p></div><a class="button outline" href="#experiments?model=spectra">Explore measurement channels <span aria-hidden="true">↗</span></a></div>`;
}

function experimentCard(e, index) {
  const detailPairs = [['Question', e.question], ['Method', e.method], ['Predicted observation', e.prediction], ['Limitations', e.limitations], ['Scope & safety', e.safety]];
  return `<article class="card research-card" id="experiment-${escape(e.id)}"><div class="card-top"><span class="card-index">${String(index+1).padStart(2,'0')}</span><span class="meta">${escape(e.domain || 'Research question')}</span></div><h3>${escape(e.title)}</h3><div class="tags">${pill(e.evidence || 'hypothesis')}${e.status ? pill(e.status) : ''}</div><p>${prose(e.summary)}</p><details class="research-details"><summary>Question, method & limits</summary><dl>${detailPairs.filter(p=>p[1]).map(([label,value])=>`<dt>${label}</dt><dd>${prose(value)}</dd>`).join('')}</dl>${sourceChips(e.sourceIds)}${artifactLinks(e.artifacts)}</details></article>`;
}

const modelLabels = {schumann:'Schumann cavity',resonance:'Driven resonance',spectra:'Measurement channels'};
function experiments() {
  return `${intro('MEASURE / MODEL / CHALLENGE', 'Experiments & models.', 'Explore explicit equations, change the inputs, and inspect the limits. Models here do not establish biological effects or clinical efficacy.')}
  <div class="correction-strip"><span class="pill documented">SOURCE AUDIT</span><span>Read the corrections to the inherited Resonant Vessels interpretation.</span><a href="projects/resonant-vessels/research-corrections.html">View corrections ↗</a></div>
  <div class="tabs" role="tablist" aria-label="Interactive model"><button class="tab" role="tab" id="tab-schumann" aria-controls="model-panel" data-model="schumann" aria-selected="${activeModel==='schumann'}">01 &nbsp; Schumann cavity</button><button class="tab" role="tab" id="tab-resonance" aria-controls="model-panel" data-model="resonance" aria-selected="${activeModel==='resonance'}">02 &nbsp; Driven resonance</button><button class="tab" role="tab" id="tab-spectra" aria-controls="model-panel" data-model="spectra" aria-selected="${activeModel==='spectra'}">03 &nbsp; Measurement channels</button></div>
  <div id="model-panel" role="tabpanel" aria-labelledby="tab-${activeModel}">${modelTemplate(activeModel)}</div>
  <div class="section-heading"><div><h2>Research register</h2><p>Proposed experiments, recorded simulations, and the limits attached to each.</p></div><span class="small-label">${data.experiments.length} ENTRIES</span></div>
  <div class="grid-equal">${data.experiments.length ? data.experiments.map(experimentCard).join('') : '<div class="empty">The research register will appear when its source data is available.</div>'}</div>`;
}

function numberInput(id, label, value, unit, min, max, step = 'any') {
  return `<div class="field"><label for="${id}">${label}</label><div class="input-unit"><input id="${id}" type="number" min="${min}" max="${max}" step="${step}" value="${value}" inputmode="decimal"><span>${unit}</span></div></div>`;
}

function modelTemplate(model) {
  if(model==='schumann') return `<section class="model-panel"><div class="model-head"><div><div class="eyebrow">AN IDEAL GEOMETRIC LIMIT</div><h2>The thin spherical shell model</h2><p>An ideal, perfectly conducting, nondispersive thin spherical shell cavity gives a useful reference. The real Earth–ionosphere system is lossy, variable, and dispersive.</p></div>${pill('idealized model')}</div><div class="model-body"><div class="controls">${numberInput('radius','Planet radius',6371,'km',1,1000000)}<div class="field"><label for="mode">Angular mode index</label><select id="mode">${Array.from({length:8},(_,i)=>`<option value="${i+1}">l = ${i+1}${i===0?' · first mode':''}</option>`).join('')}</select><p class="field-note">Mode indices 1–8; the zero mode is excluded.</p></div><div class="field"><span class="small-label">FIXED CONSTANT</span><p class="field-note">c = 299,792,458 m s⁻¹<br>Vacuum speed of light</p></div><button class="toggle-button" data-reset-model="schumann">Reset to Earth reference</button></div><div class="model-output"><div class="small-label">PREDICTED IDEAL FREQUENCY</div><div style="margin-top:12px"><span class="big-number" id="schumann-value">—</span> <span class="unit">Hz</span></div><div class="formula">f<sub>l</sub> = c / (2πR) · √[l(l + 1)]</div><div id="schumann-chart"></div><div class="callout white"><strong>This output is not an observed Schumann peak.</strong> For Earth the ideal first mode is about 10.59 Hz; the observed first resonance is commonly near 7.8 Hz. Conductivity, propagation, cavity height, and time variation matter.</div><p class="model-error" id="model-error" role="status"></p></div></div></section>`;
  if(model==='resonance') return `<section class="model-panel"><div class="model-head"><div><div class="eyebrow">LINEAR FORCED OSCILLATOR</div><h2>Resonance moves energy.</h2><p>Inspect steady periodic motion under a sinusoidal force. Gain describes a response amplitude; the damping consumes power supplied by the drive.</p></div>${pill('classical model')}</div><div class="model-body"><div class="controls">${numberInput('natural','Natural frequency',10,'Hz',.01,100000)}${numberInput('drive','Drive frequency',10,'Hz',0,100000)}${numberInput('quality','Quality factor Q',5,'dimensionless',.05,10000)}${numberInput('mass','Mass',1,'kg',.000001,100000)}${numberInput('force','Force amplitude',1,'N',0,100000)}<button class="toggle-button" data-reset-model="resonance">Reset model</button></div><div class="model-output"><div class="small-label">STEADY-STATE RESPONSE</div><div class="result-grid"><div class="result-cell"><div class="small-label">Displacement</div><span class="big-number" id="amplitude-value">—</span> <span class="unit">mm · amplitude</span></div><div class="result-cell"><div class="small-label">Drive power</div><span class="big-number" id="power-value">—</span> <span class="unit">mW · mean</span></div><div class="result-cell"><div class="small-label">Stored energy</div><span class="big-number" id="energy-value">—</span> <span class="unit">mJ · mean</span></div></div><div id="resonance-chart"></div><div class="formula">mẍ + bẋ + kx = F₀ cos(ωt)</div><p class="model-note">k = mω₀²; b = mω₀/Q; ω = 2πf. The chart shows normalized transfer gain, k / √[(k − mω²)² + (bω)²], independent of the force amplitude. At zero drive frequency the model uses static potential energy; at positive frequency it uses cycle means. Assumes a linear, time-invariant oscillator.</p><div class="callout white"><strong>Energy balance:</strong> mean drive power equals mean dissipated power, ½bω²A². Increasing Q increases resonance amplitude; it does not create energy.</div><p class="model-error" id="model-error" role="status"></p></div></div></section>`;
  return `<section class="model-panel"><div class="model-head"><div><div class="eyebrow">DEFINE THE SIGNAL BEFORE THE FREQUENCY</div><h2>One object. Many spectra.</h2><p>A spectrum describes a particular measured quantity over time. A person or object has no single universal frequency that combines all physical channels.</p></div>${pill('measurement design')}</div><div class="model-body"><div class="controls"><div class="field"><label for="channel">Measurement channel</label><select id="channel"><option value="electrical">Electrical potential</option><option value="mechanical">Mechanical displacement</option><option value="acoustic">Acoustic pressure</option><option value="optical">Optical / infrared radiation</option></select></div>${numberInput('sample-rate','Sample rate',256,'samples / s',1,1000000)}${numberInput('duration','Recording duration',30,'s',.01,86400)}<div class="field"><p class="field-note">Ideal sampling reference only. Instrument bandwidth, calibration, noise, aliasing, and windowing also govern useful measurements.</p></div><button class="toggle-button" data-reset-model="spectra">Reset model</button></div><div class="model-output"><div id="channel-description" class="callout" style="margin-top:0"></div><div class="result-grid"><div class="result-cell"><div class="small-label">Nyquist limit</div><span class="big-number" id="nyquist-value">—</span> <span class="unit">Hz</span></div><div class="result-cell"><div class="small-label">DFT bin spacing</div><span class="big-number" id="resolution-value">—</span> <span class="unit">Hz</span></div><div class="result-cell"><div class="small-label">Nominal samples</div><span class="big-number" id="samples-value">—</span> <span class="unit">samples</span></div></div><div class="formula">f<sub>N</sub> = f<sub>s</sub> / 2 &nbsp; · &nbsp; Δf = f<sub>s</sub> / N</div><p class="model-note" id="duration-note"></p><div class="table-wrap"><table class="data-table"><thead><tr><th>Channel</th><th>Observable</th><th>Example instrument</th></tr></thead><tbody><tr><td>Electrical</td><td>Potential difference · V</td><td>Calibrated electrodes & amplifier</td></tr><tr><td>Mechanical</td><td>Displacement · m</td><td>Laser vibrometer</td></tr><tr><td>Acoustic</td><td>Pressure · Pa</td><td>Calibrated microphone</td></tr><tr><td>Optical</td><td>Spectral radiance</td><td>Spectrometer or radiometer</td></tr></tbody></table></div><div class="callout white"><strong>A frequency match alone is not a mechanism.</strong> To test coupling, specify the source, field strength, exposure, transfer path, response quantity, and controls.</div><p class="model-error" id="model-error" role="status"></p></div></div></section>`;
}

const pretty = value => !Number.isFinite(value) ? '—' : value === 0 ? '0' : Math.abs(value)>=10000 || Math.abs(value)<.001 ? value.toExponential(2) : Number(value.toPrecision(4)).toLocaleString('en-US',{maximumFractionDigits:4});

function updateModel() {
  const error = $('#model-error');
  if(!error) return;
  try {
    for(const input of document.querySelectorAll('#model-panel input[type=number]')) {
      if(input.value.trim()==='' || !input.checkValidity()) throw new RangeError(`${document.querySelector(`label[for="${input.id}"]`)?.textContent || 'Input'} must be between ${input.min} and ${input.max}.`);
    }
    if(activeModel==='schumann') {
      const radius = Number($('#radius').value), mode = Number($('#mode').value);
      const result = schumannIdeal(radius,mode);
      $('#schumann-value').textContent = pretty(result);
      const values = Array.from({length:8},(_,i)=>schumannIdeal(radius,i+1));
      const max = Math.max(...values)*1.15;
      $('#schumann-chart').innerHTML = `<svg class="chart" viewBox="0 0 580 225" role="img" aria-label="Ideal cavity frequencies for modes one through eight. Selected mode ${mode}: ${result.toFixed(2)} hertz."><line class="grid" x1="42" y1="183" x2="557" y2="183"/>${[0,.5,1].map(p=>`<line class="grid" x1="42" y1="${183-p*145}" x2="557" y2="${183-p*145}"/><text x="32" y="${187-p*145}" text-anchor="end">${pretty(max*p)}</text>`).join('')}${values.map((v,i)=>`<rect x="${62+i*63}" y="${183-v/max*145}" width="23" height="${v/max*145}" rx="2" fill="${i+1===mode?'#a66e47':'#8ea67c'}"/><text x="${73+i*63}" y="204" text-anchor="middle">${i+1}</text>`).join('')}<text x="47" y="16">Hz · ideal frequency</text><text x="555" y="222" text-anchor="end">Angular mode l</text></svg>`;
    } else if(activeModel==='resonance') {
      const values={naturalHz:Number($('#natural').value),driveHz:Number($('#drive').value),quality:Number($('#quality').value),massKg:Number($('#mass').value),forceN:Number($('#force').value)};
      const result = oscillator(values);
      $('#amplitude-value').textContent=pretty(result.amplitudeM*1000);
      $('#power-value').textContent=pretty(result.averagePowerW*1000);
      $('#energy-value').textContent=pretty(result.meanEnergyJ*1000);
      const maxHz=Math.max(values.naturalHz*2,values.driveHz*1.15,1);
      const positions=Array.from({length:241},(_,i)=>maxHz*i/240);
      positions.push(values.naturalHz,values.driveHz);
      positions.sort((a,b)=>a-b);
      const points=positions.map(f=>({f,g:oscillator({...values,driveHz:f}).gain}));
      const maxGain=Math.max(...points.map(p=>p.g),1)*1.15;
      const x=f=>44+f/maxHz*510,y=g=>182-g/maxGain*145;
      $('#resonance-chart').innerHTML=`<svg class="chart" viewBox="0 0 580 225" role="img" aria-label="Response amplitude gain by drive frequency. Selected gain ${result.gain.toFixed(3)} at ${values.driveHz} hertz.">${[0,.5,1].map(p=>`<line class="grid" x1="44" y1="${y(maxGain*p)}" x2="554" y2="${y(maxGain*p)}"/><text x="34" y="${y(maxGain*p)+4}" text-anchor="end">${pretty(maxGain*p)}</text>`).join('')}<path class="curve" d="${points.map((p,i)=>`${i?'L':'M'}${x(p.f).toFixed(2)},${y(p.g).toFixed(2)}`).join(' ')}"/><line class="guide" x1="${x(values.driveHz)}" x2="${x(values.driveHz)}" y1="${y(result.gain)}" y2="182"/><circle class="marker" cx="${x(values.driveHz)}" cy="${y(result.gain)}" r="5"/>${[0,.25,.5,.75,1].map(p=>`<text x="${x(maxHz*p)}" y="202" text-anchor="middle">${pretty(maxHz*p)}</text>`).join('')}<text x="45" y="16">Normalized transfer gain</text><text x="555" y="221" text-anchor="end">Drive frequency · Hz</text></svg>`;
    } else {
      const result=spectralResolution(Number($('#sample-rate').value),Number($('#duration').value));
      $('#nyquist-value').textContent=pretty(result.nyquistHz);
      $('#resolution-value').textContent=pretty(result.binSpacingHz);
      $('#samples-value').textContent=pretty(result.samples);
      $('#duration-note').textContent=`N = floor(sample rate × requested duration). Effective record duration: ${pretty(result.effectiveDurationS)} s. DFT bin spacing uses this integer sample count.`;
      const descriptions={electrical:'<strong>Electrical potential:</strong> electrodes measure voltage differences at defined locations. The recording depends on placement, reference, instrument bandwidth, and artifacts.',mechanical:'<strong>Mechanical displacement:</strong> a vibration spectrum describes motion along a specified axis and at a specified point. Geometry and boundary conditions change the modes.',acoustic:'<strong>Acoustic pressure:</strong> a microphone measures pressure fluctuations at its location. The room, distance, noise floor, and microphone response affect the spectrum.',optical:'<strong>Optical / infrared radiation:</strong> a spectrometer measures radiation versus wavelength or optical frequency. The sampling controls here describe a recorded time series, not the optical carrier frequency.'};
      $('#channel-description').innerHTML=descriptions[$('#channel').value];
    }
    error.textContent='';
  } catch(e) { error.textContent=e.message; document.querySelectorAll('#model-panel .big-number').forEach(el=>el.textContent='—'); for(const id of ['schumann-chart','resonance-chart','duration-note']) { const chart=document.getElementById(id); if(chart)chart.innerHTML=''; } }
}

function sources() {
  const types=[...new Set(data.sources.map(s=>s.type).filter(Boolean))].sort();
  const evidence=[...new Set(data.sources.map(s=>s.evidence).filter(Boolean))].sort();
  return `${intro('PROVENANCE BEFORE INTERPRETATION', 'The source library.', 'Original documents, scientific papers, and historical claims. Evidence labels describe how a source is used here; a patent or government archive is not proof that a claim works.')}
  <div class="filters"><label class="sr-only" for="source-search">Search sources</label><input class="search-box" type="search" id="source-search" placeholder="Search titles, authors, claims, or source IDs…" value="${escape(sourceState.query)}"><label class="sr-only" for="evidence-filter">Filter by evidence</label><select id="evidence-filter"><option value="all">All evidence levels</option>${evidence.map(e=>`<option value="${escape(e)}" ${sourceState.evidence===e?'selected':''}>${escape(e)}</option>`).join('')}</select><label class="sr-only" for="type-filter">Filter by source type</label><select id="type-filter"><option value="all">All source types</option>${types.map(t=>`<option value="${escape(t)}" ${sourceState.type===t?'selected':''}>${escape(t)}</option>`).join('')}</select></div>
  <div id="source-results" aria-live="polite">${sourceResults()}</div>`;
}

function sourceResults() {
  const query=sourceState.query.toLowerCase().trim();
  const results=data.sources.filter(s=>(sourceState.evidence==='all'||s.evidence===sourceState.evidence)&&(sourceState.type==='all'||s.type===sourceState.type)&&[s.id,s.title,s.author,s.summary,s.claim,s.section].join(' ').toLowerCase().includes(query));
  return `<div class="result-count">${results.length} of ${data.sources.length} sources${query?' matching your search':''}</div><div class="source-list">${results.length ? results.map(s=>`<article class="source-item" id="source-${escape(s.id)}"><div class="card-top"><span class="source-identifier">${escape(s.id)} · ${escape(s.type || 'source')}</span>${pill(s.evidence || 'documented')}</div><h3><a href="${safeUrl(s.url)}"${linkAttrs(s.url)}>${escape(s.title)}<span class="source-link-icon" aria-hidden="true">↗</span></a></h3><div class="source-meta">${[s.author,s.year,s.section].filter(Boolean).map(escape).join(' · ')}</div><p>${prose(s.summary || s.claim)}</p>${s.claim&&s.summary?`<p style="margin-top:8px"><strong>Claim in scope:</strong> ${prose(s.claim)}</p>`:''}${s.limitations||s.readingDepth||s.verifiedAt?`<details><summary>Reading scope & limitations</summary>${s.readingDepth?`<p style="margin-top:10px">Reading scope: ${prose(s.readingDepth)}</p>`:''}${s.limitations?`<p>${prose(s.limitations)}</p>`:''}${s.verifiedAt?`<p>Source checked: ${escape(s.verifiedAt)}</p>`:''}</details>`:''}</article>`).join('') : '<div class="empty">No sources match these filters. Try a broader search or select all evidence levels.</div>'}</div>`;
}

const processes={
  separation:{name:'Phase transfer',label:'A1 / SUBLIMATION & INVENTORY',sourceIds:['H01'],description:'Newton’s December 1678 notes record sublimation and residues. This modern inventory diagram separates source, condensate, residue, and escaped material without identifying a historical reagent.',measure:'For every conserved component, compare initial inventory with every final reservoir. The normalized closure residual is (input − recovered) / input. An omitted escape channel creates an accounting gap.',limit:'Conceptual mass accounting, not a recreation. A missing reservoir is not evidence of matter creation. No temperatures, reagent identities, or construction instructions are supplied.'},
  dissolution:{name:'Ambiguous identity',label:'A2 / EXTRACTION & SEPARATION',sourceIds:['H01'],description:'Newton’s measured extracts and residues motivate an inverse question: can different compositions generate the same observations? The two synthetic mixtures shown have identical two-channel outputs.',measure:'Use y = Ac with A = [[1,0,1],[0,1,1]]. The added independent row [1,1,0] produces outputs 0 and 2. A duplicate row cannot resolve the ambiguity.',limit:'Components and channels are dimensionless relative amounts, not fractions constrained to sum to one. They are not identified with Newton’s chemicals or any calibrated optical spectrum.'},
  crystallization:{name:'Material state',label:'A3 / FUSION & STRUCTURE',sourceIds:['H01'],description:'The notes discuss fusibility and mixtures that did not combine. This modern illustration keeps composition fixed while changing material state, distinguishing structure from constituent identity.',measure:'Track a state response against a normalized control variable. Compare heating and cooling records before fitting a transition midpoint or claiming an equilibrium model.',limit:'The sigmoid is an illustrative function, p = 1/[1 + exp(−12(θ − ½))], not measured Newton data. It does not identify a historical substance or a physical transition temperature.'},
  calcination:{name:'Branching patterns',label:'A4 / VEGETATION & MORPHOLOGY',sourceIds:['H02'],description:'Newton’s mineral-and-living-growth analogy motivates competing generative explanations. Different mechanisms may produce similar final morphology; resemblance alone cannot identify the cause.',measure:'Compare branch count, occupied area, and scale-dependent box counts; then inspect held-out time-resolved growth. Matching one summary statistic is not a complete mechanism test.',limit:'The two branching sketches and trajectories are conceptual illustrations, not executed diffusion-limited aggregation simulations or evidence of “metal life.” The historical growth principle remains an attributed idea.'}
};

function processDiagram(key) {
  const defs='<defs><marker id="process-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10" fill="#91a77b"/></marker></defs><style>.v{fill:none;stroke:#7b9464;stroke-width:1.6}.p{fill:#8eab75}.q{fill:#b99762}.a{fill:none;stroke:#91a77b;stroke-width:1.4;marker-end:url(#process-arrow)}.t{font:12px ui-sans-serif,system-ui;fill:#526b3e}.s{font:10px ui-sans-serif,system-ui;fill:#90a17a}.b{fill:#eff3e5;stroke:#cbd7b9;stroke-width:1}</style>';
  const dots=(points,c='p')=>points.map(([x,y])=>`<circle class="${c}" cx="${x}" cy="${y}" r="4"/>`).join('');
  let body='';
  if(key==='separation')body=`<rect x="28" y="40" width="554" height="176" rx="10" fill="none" stroke="#a5b991" stroke-dasharray="5 4"/><text class="s" x="47" y="61">DECLARED ACCOUNTING BOUNDARY</text><g><path class="v" d="M65 95v69q0 12 12 12h46q12 0 12-12V95"/><path class="v" d="M277 95v69q0 12 12 12h46q12 0 12-12V95"/><path class="v" d="M456 95v69q0 12 12 12h46q12 0 12-12V95"/></g>${dots([[88,154],[105,164],[119,151]])}${dots([[293,157],[313,164]])}${dots([[478,166],[502,164]],'q')}<path class="a" d="M150 131h109M361 131h78M315 93q92-85 315 0"/><rect class="b" x="628" y="89" width="105" height="74" rx="7"/><text class="t" x="680" y="120" text-anchor="middle">Escaped</text><text class="t" x="680" y="138" text-anchor="middle">reservoir</text><text class="t" x="100" y="199" text-anchor="middle">Source</text><text class="t" x="312" y="199" text-anchor="middle">Condensate</text><text class="t" x="492" y="199" text-anchor="middle">Residue</text><text class="s" x="40" y="248">Partial inventory</text><rect x="149" y="239" width="110" height="10" rx="2" fill="#bac7a8"/><rect x="259" y="239" width="30" height="10" rx="2" fill="none" stroke="#b99762" stroke-dasharray="3 2"/><text class="s" x="355" y="248">Complete inventory</text><rect x="477" y="239" width="140" height="10" rx="2" fill="#819f6b"/><text class="s" x="40" y="269">Illustrative accounting; bar lengths are schematic, not measured masses.</text>`;
  if(key==='dissolution')body=`<rect class="b" x="28" y="55" width="175" height="68" rx="5"/><rect class="b" x="28" y="162" width="175" height="68" rx="5"/><text class="t" x="116" y="82" text-anchor="middle">Candidate A</text><text class="t" x="116" y="103" text-anchor="middle">c = (0, 0, 1)</text><text class="t" x="116" y="189" text-anchor="middle">Candidate B</text><text class="t" x="116" y="211" text-anchor="middle">c = (1, 1, 0)</text><path class="a" d="M211 88h88M211 196h88"/><rect class="b" x="310" y="55" width="160" height="68" rx="5"/><rect class="b" x="310" y="162" width="160" height="68" rx="5"/><text class="s" x="390" y="81" text-anchor="middle">TWO CHANNELS</text><text class="t" x="390" y="106" text-anchor="middle">y = (1, 1)</text><text class="s" x="390" y="188" text-anchor="middle">TWO CHANNELS</text><text class="t" x="390" y="211" text-anchor="middle">y = (1, 1)</text><path class="a" d="M482 88h76M482 196h76"/><rect class="b" x="570" y="55" width="162" height="68" rx="5"/><rect class="b" x="570" y="162" width="162" height="68" rx="5"/><text class="s" x="651" y="81" text-anchor="middle">INDEPENDENT ASSAY</text><text class="t" x="651" y="106" text-anchor="middle">[1, 1, 0] · c = 0</text><text class="s" x="651" y="188" text-anchor="middle">INDEPENDENT ASSAY</text><text class="t" x="651" y="211" text-anchor="middle">[1, 1, 0] · c = 2</text><text class="s" x="29" y="264">Synthetic relative amounts · all channels dimensionless · no hidden sum-to-one condition</text>`;
  if(key==='crystallization'){
    const points=Array.from({length:81},(_,i)=>{const t=i/80;return `${i?'L':'M'}${(425+t*268).toFixed(2)},${(204-141/(1+Math.exp(-12*(t-.5)))).toFixed(2)}`;}).join(' ');
    body=`<rect class="b" x="35" y="79" width="125" height="118" rx="6"/><rect class="b" x="220" y="79" width="125" height="118" rx="6"/>${dots([[61,107],[92,107],[123,107],[61,137],[92,137],[123,137],[61,167],[92,167],[123,167]])}${dots([[244,103],[300,98],[281,121],[318,148],[240,152],[279,177],[318,176],[303,134],[255,182]])}<path class="a" d="M171 137h36"/><text class="t" x="97" y="225" text-anchor="middle">Ordered state</text><text class="t" x="282" y="225" text-anchor="middle">Different structure</text><text class="s" x="187" y="252" text-anchor="middle">Same abstract component inventory</text><path class="v" d="M424 49v156h281"/><path d="${points}" fill="none" stroke="#9c7e4f" stroke-width="2.3"/><text class="s" x="414" y="65" text-anchor="end">1</text><text class="s" x="414" y="207" text-anchor="end">0</text><text class="s" x="418" y="36">Liquid fraction p</text><text class="s" x="559" y="226" text-anchor="middle">Normalized control variable θ</text><text class="s" x="559" y="252" text-anchor="middle">Illustrative model; not measured Newton data</text>`;
  }
  if(key==='calcination')body=`<g class="v"><path d="M114 193v-42l-36-36-16-30M78 115l-35-8M114 151l35-31 26-10M149 120l6-42M114 170l-42-20M114 142l-6-46"/><path d="M331 193l-6-35-25-32-8-46M300 126l-37-4M325 158l36-28 24 7M361 130l-5-48M331 171l-37-4M322 154l18-48"/></g><text class="t" x="111" y="223" text-anchor="middle">Pattern A</text><text class="t" x="326" y="223" text-anchor="middle">Pattern B</text><text class="s" x="214" y="253" text-anchor="middle">Synthetic branching sketches, not executed growth models</text><rect class="b" x="440" y="49" width="281" height="47" rx="5"/><text class="t" x="580" y="77" text-anchor="middle">Similar shape ≠ unique mechanism</text><path class="v" d="M465 122v92h232"/><path d="M466 208Q530 205 559 171T684 133" fill="none" stroke="#89a56f" stroke-width="2"/><path d="M466 208Q520 148 573 142T684 133" fill="none" stroke="#b99762" stroke-width="2" stroke-dasharray="5 3"/><text class="s" x="581" y="237" text-anchor="middle">Compare trajectories, not only endpoints</text><text class="s" x="690" y="258" text-anchor="end">Illustrative growth histories → time</text>`;
  return `<svg class="process-diagram" viewBox="0 0 760 280" role="img" aria-label="${escape(processes[key].name)} conceptual process: ${escape(processes[key].description)}">${defs}${body}</svg>`;
}

function processContent() {
  const p=processes[activeProcess];
  return `${processDiagram(activeProcess)}${sourceChips(p.sourceIds)}<div class="process-copy"><div><h3>Historical anchor & modern interpretation</h3><p>${p.description}</p><h3 style="margin-top:18px">What to measure</h3><p>${p.measure}</p></div><div><h3>Interpretive boundary</h3><p>${p.limit}</p><div class="callout white">A source-bound modern interpretation. No historical chemical identification or completed physical replication is claimed.</div></div></div>`;
}

function history() {
  return `${intro('HISTORY IS A SOURCE, NOT A VERDICT', 'Manuscripts to measurements.', 'Read historical ideas in their own context, then translate selected claims into observables. Conceptual diagrams separate familiar material processes from extraordinary interpretations.')}
  <div class="card history-note"><div class="card-top"><span class="small-label">FOUR SOURCE-BOUND MODERN INTERPRETATIONS</span>${pill('schematic / not a recipe')}</div><div class="process-tabs" role="tablist" aria-label="Material transformation process">${Object.entries(processes).map(([id,p])=>`<button class="process-choice" role="tab" id="process-${id}" aria-controls="process-content" data-process="${id}" aria-selected="${activeProcess===id}"><span>${p.label}</span>${p.name}</button>`).join('')}</div><div id="process-content" role="tabpanel" aria-labelledby="process-${activeProcess}">${processContent()}</div></div>
  <div class="section-heading"><div><h2>Historical threads</h2><p>Attributed ideas, documented context, and the evidence attached to them.</p></div></div><div class="timeline">${data.history.length?data.history.map(h=>`<article class="timeline-item"><div class="eyebrow">${escape(h.person || 'Historical research')}${h.year?` · ${escape(h.year)}`:''}</div><h3>${escape(h.title)}</h3><div style="margin-bottom:11px">${pill(h.evidence || 'documented')}</div><p>${prose(h.summary)}</p>${sourceChips(h.sourceIds)}${artifactLinks(h.artifacts)}</article>`).join(''):'<div class="empty">Historical source annotations are being prepared.</div>'}</div><div class="callout"><strong>Interpretation rule:</strong> a reconstructed diagram is an explanatory aid. It is not evidence that the historical author built that apparatus or that an attributed effect was demonstrated.</div>`;
}

function edgeEnds(edge) { return [typeof edge.source==='object'?edge.source.id:edge.source,typeof edge.target==='object'?edge.target.id:edge.target]; }
function graphSVG() {
  const allNodes=data.network.nodes;
  const degree = id => data.network.edges.filter(e => edgeEnds(e).includes(id)).length;
  const groups=[['source'],['person','history','claim','interpretation','historical assertion'],['model','concept'],['experiment','hypothesis','project']];
  const positions=new Map();
  const buckets=[[],[],[],[]];
  allNodes.forEach(n=>{let gi=groups.findIndex(g=>g.includes(String(n.type).toLowerCase()));buckets[gi<0?2:gi].push(n);});
  buckets.forEach((bucket,gi)=>{buckets[gi]=bucket.sort((a,b)=>degree(b.id)-degree(a.id)).slice(0,10);});
  const visible=buckets.flat();
  buckets.forEach((bucket,gi)=>bucket.forEach((node,ni)=>positions.set(node.id,{x:95+gi*190,y:74+(ni+.5)*430/Math.max(1,bucket.length)})));
  const edges=data.network.edges.filter(e=>edgeEnds(e).every(id=>positions.has(id)));
  const labels=['SOURCES','CLAIMS / HISTORY','MODELS / CONCEPTS','EXPERIMENTS'];
  return `<svg viewBox="0 0 760 550" role="group" aria-label="Evidence graph. Select a node to inspect relationships. All edges are also available in the accessible table below."><defs><pattern id="graph-dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".7" fill="#e6ebdc"/></pattern><marker id="graph-arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10" fill="#97ad81"/></marker></defs><rect width="760" height="550" fill="url(#graph-dots)"/>${labels.map((l,i)=>`<text x="${95+i*190}" y="40" text-anchor="middle" font-size="9" letter-spacing="1" fill="#a0ad8d">${l}</text>`).join('')}${edges.map(e=>{const [a,b]=edgeEnds(e).map(id=>positions.get(id));return `<path class="network-line" data-kind="${slug(e.type)}" marker-end="url(#graph-arrow)" d="M${a.x} ${a.y}C${(a.x+b.x)/2} ${a.y},${(a.x+b.x)/2} ${b.y},${b.x} ${b.y}"><title>${escape(e.label||e.type||'related to')}</title></path>`;}).join('')}${visible.map(n=>{const p=positions.get(n.id);const label=String(n.label||n.title||n.id);const words=label.length>27?`${label.slice(0,25)}…`:label;return `<g class="network-node" data-node="${escape(n.id)}" data-kind="${slug(n.type)}" tabindex="0" role="button" aria-label="Inspect ${escape(label)}" aria-pressed="${selectedNode===n.id}"><circle cx="${p.x}" cy="${p.y}" r="${String(n.type).toLowerCase()==='experiment'?11:8}"/><text x="${p.x}" y="${p.y+25}" text-anchor="middle">${escape(words)}</text><title>${escape(label)}</title></g>`;}).join('')}</svg>`;
}

function nodeDetail() {
  const n=data.network.nodes.find(n=>n.id===selectedNode);
  if(!n) return `<span class="small-label">INSPECT A CONNECTION</span><h3>Every edge has a meaning.</h3><p>Select a node in the graph to see its source references and incoming and outgoing relationships.</p><div class="callout white">A connection records a relationship. It does not establish causality, equivalence, or efficacy.</div>`;
  const edges=data.network.edges.filter(e=>edgeEnds(e).includes(n.id));
  return `<span class="small-label">${escape(n.type||'research node')}</span><h3>${escape(n.label||n.title||n.id)}</h3><p>${prose(n.summary)}</p>${sourceChips(n.sourceIds)}<ul class="edge-list">${edges.map(e=>{const ids=edgeEnds(e);const otherId=ids[0]===n.id?ids[1]:ids[0];const other=data.network.nodes.find(x=>x.id===otherId);return `<li><strong>${ids[0]===n.id?'Outgoing':'Incoming'} · ${escape(e.type||'related')}</strong>${escape(other?.label||other?.title||otherId)}${e.label?`<p class="micro-note">${escape(e.label)}</p>`:''}${sourceChips(e.sourceIds)}</li>`;}).join('')}</ul>`;
}

function graphTable() {
  const label=id=>{const n=data.network.nodes.find(n=>n.id===id);return escape(n?.label||n?.title||id);};
  return `<div class="table-wrap"><table class="data-table"><caption class="sr-only">All directed relationships in the evidence network</caption><thead><tr><th>From</th><th>Relationship</th><th>To</th><th>Sources</th></tr></thead><tbody>${data.network.edges.map(e=>{const [a,b]=edgeEnds(e);return `<tr><td>${label(a)}</td><td>${escape(e.type||'related')}${e.label?`<br><span class="micro-note">${escape(e.label)}</span>`:''}</td><td>${label(b)}</td><td>${sourceChips(e.sourceIds)}</td></tr>`;}).join('')}</tbody></table></div>`;
}

function network() {
  return `${intro('CONNECTIONS YOU CAN INSPECT', 'The evidence network.', 'Trace sources into claims, claims into models, and models into experiments. Arrows are directed; their labels describe the relationship, not the strength of a causal effect.')}
  ${data.network.nodes.length?`<div class="network-layout"><div class="network-stage"><div id="graph-svg">${graphSVG()}</div><div class="network-legend"><span><i class="legend-dot" style="background:#a6b695"></i>Source</span><span><i class="legend-dot" style="background:#b28c5d"></i>Claim / history</span><span><i class="legend-dot" style="background:#81988f"></i>Model / concept</span><span><i class="legend-dot" style="background:#427457"></i>Experiment</span></div></div><aside class="network-detail" id="node-detail" aria-live="polite">${nodeDetail()}</aside></div><p class="graph-caption">${data.network.nodes.length} nodes · ${data.network.edges.length} directed relationships · The visual overview shows up to 10 connected nodes in each category; the table below contains every relationship.. Solid green: supports. Dashed copper: tests or derived from. Dotted copper: contradicts. Other relationships are labeled in the table.</p><div class="section-heading"><div><h2>All relationships</h2><p>An accessible, complete view of the graph and its provenance.</p></div></div><div class="card" style="padding:0">${graphTable()}</div>`:'<div class="empty">The graph will appear when source-linked research relationships are available.</div>'}`;
}

function roundCard(r,index) {
  return `<article class="round-card"><div class="card-top"><span class="eyebrow">${escape(r.id || `ROUND ${index+1}`)}</span>${pill(r.status || 'recorded')}</div><h3>${escape(r.title)}</h3><p>${prose(r.question || r.summary)}</p>${r.participants?`<p class="micro-note" style="margin-top:12px">Panel: ${list(r.participants).map(readable).map(escape).join(' · ')}</p>`:''}<div class="round-cols"><div><h4>Findings & challenges</h4>${bullets(r.findings)}</div><div><h4>Decisions</h4>${bullets(r.decisions)}${list(r.next).length?`<h4 style="margin-top:17px">Next actions</h4>${bullets(r.next)}`:''}</div></div>${artifactLinks(r.artifacts)}</article>`;
}

function roadmap() {
  const buckets={completed:[],active:[],planned:[]};
  data.roadmap.forEach(r=>{const s=String(r.status||'planned').toLowerCase();const stage=/not.started|planned|unexecuted|proposed|blocked|deferred/.test(s)?'planned':/review.pending|pending.review|under.review|awaiting.review/.test(s)?'active':/complete|done|verified|shipped|executed/.test(s)?'completed':/active|in.progress|review|started/.test(s)?'active':'planned';buckets[stage].push(r);});
  return `<div class="roadmap">${[['completed','Recorded / complete'],['active','In progress / review'],['planned','Next / open']].map(([key,title])=>`<div class="roadmap-col"><h3>${title} · ${buckets[key].length}</h3>${buckets[key].length?buckets[key].map(r=>`<article class="roadmap-item"><span class="small-label">${escape(r.id||'research task')}</span><h4>${escape(r.title)}</h4><p>${prose(r.detail || r.summary)}</p>${r.owner?`<small>Owner: ${escape(r.owner)}</small>`:''}${list(r.dependsOn).length?`<small>Depends on: ${list(r.dependsOn).map(escape).join(', ')}</small>`:''}${r.status?`<div style="margin-top:12px">${pill(r.status)}</div>`:''}</article>`).join(''):'<p class="micro-note">No tasks in this stage.</p>'}</div>`).join('')}</div>`;
}

function panel() {
  return `${intro('RESEARCH THAT CHANGES ITS MIND', 'The panel & the next test.', 'Review the recorded exchange between historical interpretation, physical modeling, implementation, and skeptical assessment. A panel decision is a research decision, not scientific validation.')}
  <div class="callout"><strong>Review standard:</strong> name the claim, inspect provenance, specify an observable, expose model assumptions, and report unresolved objections.</div><div class="section-heading"><div><h2>Recorded panel rounds</h2><p>What was considered, what changed, and what remains open.</p></div></div>${data.rounds.length?data.rounds.map(roundCard).join(''):'<div class="empty">No completed panel rounds have been loaded.</div>'}<div class="section-heading"><div><h2>Shared research roadmap</h2><p>Dependencies and ownership keep parallel work connected.</p></div></div>${roadmap()}`;
}

function projects() {
  return `${intro('A CONNECTED RESEARCH WORKSPACE', 'Different instruments.<br>One research map.', 'Open the audio tools, historical archives, geometry studies, and hypothesis notebooks connected through this atlas.')}
  <div class="grid-equal">${data.projects.length?data.projects.map((p,i)=>`<article class="card project-card"><div class="card-top"><span class="card-index">${String(i+1).padStart(2,'0')}</span>${pill(p.status||'connected project')}</div><h3>${escape(p.name)}</h3><p>${prose(p.role || p.description)}</p><a class="button outline" href="${safeUrl(p.url)}"${linkAttrs(p.url)}>Open project <span aria-hidden="true">↗</span></a>${p.repository?`<a href="${safeUrl(p.repository)}" class="text-link" style="margin-top:12px"${linkAttrs(p.repository)}>Source repository ↗</a>`:''}</article>`).join(''):'<div class="empty">Connected project links will appear here when available.</div>'}</div>
  <div class="section-heading"><div><h2>Design an experiment before building it</h2><p>A visual concept helps discuss layout; a schematic and measurement plan establish the test.</p></div></div><div id="concept-slot" hidden><img class="concept-image" src="assets/lab-concept.png" alt="Concept illustration of a research bench for discussing resonance experiments"><p class="image-caption">Concept illustration only. Apparatus details are not an engineering schematic or an instruction for construction.</p></div><div class="callout"><strong>Shared boundary:</strong> audio tools synthesize signals; simulations compute consequences of assumptions; historical archives document ideas. Biological, anti-gravity, or energy-generation claims require independent measurements beyond those capabilities.</div>`;
}

const journalKey='resonance-atlas-dream-journal-v1';
let journalMemory=[];
let journalMemoryAuthoritative=false;
function readJournal() { if(journalMemoryAuthoritative)return journalMemory;try {const saved=JSON.parse(localStorage.getItem(journalKey)||'[]');return Array.isArray(saved)?saved:[];}catch{return journalMemory;} }
function journalEntries() {
  const entries=readJournal();
  return `<p class="result-count">${entries.length} saved ${entries.length===1?'entry':'entries'} in this browser</p>${entries.length?entries.slice().reverse().map(e=>`<details class="source-item" style="margin-bottom:10px"><summary>${escape(e.date)} · ${escape(e.recall==='none'?'No dream recalled':e.awareness==='yes'?'Awareness reported':'Dream recalled')}</summary><div class="source-meta">Recorded ${escape(e.recordedAt)} · sleep stage unknown</div><p><strong>Immediate recall:</strong> ${escape(e.account||'No dream recalled.')}</p><p><strong>Awareness during the dream:</strong> ${escape(e.awareness)}</p><p><strong>Perceived control:</strong> ${escape(e.control)}</p><p><strong>Self-location experience:</strong> ${escape(e.location||'Not recorded')}</p><p><strong>Emotion:</strong> ${escape(e.emotion||'Not recorded')}</p><p><strong>Order-of-events confidence:</strong> ${escape(e.certainty)}</p>${e.interpretation?`<p><strong>Later interpretation (separate):</strong> ${escape(e.interpretation)}</p>`:''}</details>`).join(''):'<div class="empty">No observations saved. “No dream recalled” is a valid entry.</div>'}`;
}
function dreams() {
  const sourceIds=list(data.dreams?.sourceIds).length?data.dreams.sourceIds:data.sources.filter(s=>/dream|lucid|astral|out.of.body|sleep/i.test(`${s.title} ${s.summary}`)).map(s=>s.id);
  return `${intro('ROUND 06 / EXPERIENCE & EXTERNAL INFORMATION', 'Dreams, with a clear record.', 'Dream awareness, a change in felt self-location, and acquiring concealed information are three different claims. Record the experience; test an external claim with an independent protocol.')}
  <div class="grid-three"><article class="card"><div class="small-label">SUBJECTIVE EXPERIENCE</div><h3 class="serif">“I knew I was dreaming.”</h3><p>A report of awareness during a dream. Laboratory studies can add independently scored sleep and a prearranged signal; this journal cannot verify sleep stage.</p></article><article class="card"><div class="small-label">SELF-LOCATION</div><h3 class="serif">“I felt outside my body.”</h3><p>A meaningful first-person account. The felt location of awareness does not by itself establish that a physical entity left the body.</p></article><article class="card"><div class="small-label">EXTERNAL INFORMATION</div><h3 class="serif">“I knew the hidden target.”</h3><p>A separate, testable accuracy claim. It needs locked responses, concealed randomized targets, complete logging, and independent leakage checks.</p></article></div>
  <div class="callout"><strong>Evidence in scope:</strong> lucid-dream research and body-ownership experiments do not establish astral travel or remote access to concealed information. This atlas does not treat a vivid or confident report as external verification.${sourceChips(sourceIds)}</div>
  <div class="section-heading"><div><h2>A sleep-friendly observation session</h2><p>Optional recall practice, with ordinary uninterrupted sleep.</p></div>${pill('observation / no efficacy claim')}</div>
  <div class="card"><ol class="session-steps"><li><span>Before your usual bedtime</span><p>Write a neutral intention: “If I remember a dream, I will record what I experienced.”</p></li><li><span>Keep your normal routine</span><p>Let sleep remain uninterrupted. This session uses no alarms, scheduled awakenings, stimulation, substances, or sleep restriction.</p></li><li><span>After naturally waking</span><p>Write the recall before interpreting it. “No dream recalled” is useful information too.</p></li><li><span>Keep observation and interpretation separate</span><p>Record awareness, perceived control, self-location, emotion, and uncertainty independently. Skip the exercise if it disrupts sleep or feels distressing.</p></li></ol></div>
  <div class="section-heading"><div><h2>Your observation journal</h2><p>Entries stay in this browser, unencrypted. This page does not send journal entries to a server.</p></div></div>
  <form id="dream-journal-form" class="card journal-form"><div class="grid-equal"><div class="field"><label for="dream-date">Approximate recall time</label><input id="dream-date" name="date" type="datetime-local" required></div><div class="field"><label for="dream-recall">Recall</label><select id="dream-recall" name="recall"><option value="recalled">Dream recalled</option><option value="none">No dream recalled</option></select></div><div class="field"><label for="dream-awareness">Aware you were dreaming during the dream?</label><select id="dream-awareness" name="awareness"><option value="uncertain">Uncertain</option><option value="yes">Yes, as remembered</option><option value="no">No</option><option value="not applicable">Not applicable</option></select></div><div class="field"><label for="dream-control">Perceived control during the dream</label><select id="dream-control" name="control"><option value="uncertain">Uncertain</option><option value="none">None</option><option value="some">Some</option><option value="substantial">Substantial</option><option value="not applicable">Not applicable</option></select></div></div><div class="field"><label for="dream-account">Immediate recall — what you experienced</label><textarea id="dream-account" name="account" rows="4" maxlength="12000" placeholder="Describe what you remember, without needing to explain it."></textarea></div><div class="grid-equal"><div class="field"><label for="dream-location">Perceived self-location / bodily experience</label><input id="dream-location" name="location" maxlength="500" placeholder="Ordinary, floating, shifted, uncertain…"></div><div class="field"><label for="dream-emotion">Emotional tone</label><input id="dream-emotion" name="emotion" maxlength="500" placeholder="In your own words"></div></div><div class="field"><label for="dream-certainty">How certain are you about the order of events?</label><select id="dream-certainty" name="certainty"><option value="uncertain">Uncertain</option><option value="low">Low confidence</option><option value="moderate">Moderate confidence</option><option value="high">High confidence</option></select></div><div class="field"><label for="dream-interpretation">Later interpretation — clearly separate from recall</label><textarea id="dream-interpretation" name="interpretation" rows="2" maxlength="6000" placeholder="Optional. Do not overwrite your immediate account with an explanation."></textarea></div><div class="journal-actions"><button class="button" type="submit">Save in this browser <span aria-hidden="true">↗</span></button><button class="button outline" type="button" data-export-journal>Export entries</button><button class="text-button" type="button" data-clear-journal>Clear saved entries</button></div><p id="journal-status" class="model-error" role="status"></p></form><div id="journal-entries" style="margin-top:18px">${journalEntries()}</div>
  <div class="section-heading"><div><h2>Four-choice chance calculator</h2><p>A statistical reference for a fixed-count, independent, prespecified design. No target test is conducted here.</p></div></div><section class="model-panel"><div class="model-head"><div><div class="eyebrow">EXACT BINOMIAL UPPER TAIL</div><h2>How surprising is a hit count?</h2><p>Under a uniform four-choice null, each independent trial has chance probability ¼. Enter the full frozen trial count and total hits.</p></div>${pill('methodology calculator')}</div><div class="model-body"><div class="controls">${numberInput('dream-trials','Prespecified trials',40,'trials',1,10000,1)}${numberInput('dream-hits','Observed hits',10,'hits',0,10000,1)}<div class="field"><span class="small-label">NULL PROBABILITY</span><p class="field-note">p₀ = 0.25 · fixed<br>Uniform independent targets</p></div></div><div class="model-output"><div class="small-label">P(X ≥ HITS | N, P₀ = 0.25)</div><div style="margin-top:12px"><span class="big-number" id="binomial-value">—</span></div><div class="formula">P(X ≥ k) = ∑<sub>j=k…N</sub> C(N,j) p₀ʲ (1−p₀)<sup>N−j</sup></div><p id="binomial-description" class="model-note"></p><div class="callout white"><strong>This number does not verify a study or a mechanism.</strong> The calculation assumes independent trials, the full prespecified sample, exact scoring, and no selective reporting or optional stopping. It is not the probability that a paranormal explanation is true.</div><p id="binomial-error" class="model-error" role="status"></p></div></div></section>
  <div class="section-heading"><div><h2>Before an external-information study</h2><p>A proposed research design, separate from the journal and calculator.</p></div></div><div class="grid-equal"><div class="card"><h3>Freeze the rules</h3><p>Specify four targets, exact-label scoring, sample size, exclusions, stopping rule, and primary endpoint before any response. Keep every eligible trial and report all misses.</p><h3>Keep the target elsewhere</h3><p>An independent custodian randomizes targets. Targets and decryption material must not reach the participant’s device before a response is locked. This site stores and generates no targets.</p></div><div class="card"><h3>Audit the information path</h3><p>Check people, devices, notifications, screens, files, caches, and reveal timing. Independent timestamps and logs must establish response-before-reveal order.</p><h3>Interpret the outcome narrowly</h3><p>An above-chance result still needs leakage and error checks, then independent replication. A null result limits the specific tested effect at the study’s precision.</p><button class="button outline" type="button" data-export-protocol style="margin-top:20px">Export blank study template ↗</button></div></div>`;
}
function updateBinomial() {
  if(!$('#dream-trials'))return;
  try {
    for(const id of ['dream-trials','dream-hits']) {const input=document.getElementById(id);if(input.value.trim()===''||!input.checkValidity())throw new RangeError('Enter whole-number counts within the displayed limits.');}
    const trials=Number($('#dream-trials').value),hits=Number($('#dream-hits').value),value=binomialUpperTail(trials,hits);
    $('#binomial-value').textContent=value===0?'< 5 × 10⁻³²⁴':value<.001?value.toExponential(4):value.toFixed(5);
    $('#binomial-description').textContent=`${hits} hits in ${trials} trials; ${(hits/trials*100).toFixed(1)}% hit rate. Expected hits under the null: ${pretty(trials/4)}. One-sided upper tail, without multiplicity correction.${value===0?' The positive mathematical tail is below floating-point range; the display reports numerical underflow, not an exact zero.':''}`;
    $('#binomial-error').textContent='';
  }catch(error){$('#binomial-value').textContent='—';$('#binomial-description').textContent='';$('#binomial-error').textContent=error.message;}
}
function exportJSON(value, filename) {
  const blob=new Blob([JSON.stringify(value,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob);
  const anchor=document.createElement('a');anchor.href=url;anchor.download=filename;document.body.append(anchor);anchor.click();anchor.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}

const renderers={overview,experiments,sources,history,dreams,network,panel,projects};
function route() {
  const raw=(location.hash.slice(1)||'overview').split('?');
  const page=Object.hasOwn(renderers,raw[0])?raw[0]:'overview';
  const params=new URLSearchParams(raw[1]||'');
  if(page==='experiments'&&Object.hasOwn(modelLabels,params.get('model')))activeModel=params.get('model');
  if(page==='sources'&&params.has('source'))sourceState={query:'',evidence:'all',type:'all'};
  main.innerHTML=renderers[page]();
  document.title=`${pageLabels[page]} — Resonance Research Atlas`;
  $('#page-label').textContent=pageLabels[page];
  document.querySelectorAll('[data-nav]').forEach(a=>{if(a.dataset.nav===page)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  if(page==='experiments')updateModel();
  if(page==='dreams') {
    updateBinomial();
    const now=new Date();now.setMinutes(now.getMinutes()-now.getTimezoneOffset());$('#dream-date').value=now.toISOString().slice(0,16);
  }
  if(page==='sources'&&params.has('source')) {
    const target=document.getElementById(`source-${params.get('source')}`);
    if(target){target.style.borderColor='#618260';requestAnimationFrame(()=>target.scrollIntoView({block:'center'}));}
  } else window.scrollTo(0,0);
  if(page==='projects') {
    const img=$('#concept-slot img');
    if(img){img.onload=()=>$('#concept-slot')?.removeAttribute('hidden');if(img.complete&&img.naturalWidth)$('#concept-slot').hidden=false;}
  }
}

main.addEventListener('click',event=>{
  if(event.target.closest('[data-export-journal]'))exportJSON({schema:'resonance-dream-journal-v1',exportedAt:new Date().toISOString(),scope:'Personal recall only. Sleep stage and external information acquisition are not verified.',entries:readJournal()},'dream-observations.json');
  if(event.target.closest('[data-clear-journal]')&&window.confirm('Delete every saved journal entry from this browser? Export first if you want a copy.')){try{localStorage.removeItem(journalKey);journalMemory=[];journalMemoryAuthoritative=false;$('#journal-entries').innerHTML=journalEntries();$('#journal-status').textContent='Saved entries cleared from this browser.';}catch{$('#journal-status').textContent='The browser prevented deletion. Saved entries could not be cleared.';}}
  if(event.target.closest('[data-export-protocol]'))exportJSON({schema:'external-information-study-plan-v1',status:'blank design template; no study executed',question:'',preregistrationDate:'',primaryEndpoint:'Exact four-choice target agreement',fixedTrialCount:null,nullProbability:.25,decisionThreshold:null,independentCustodian:'',targetRandomizationProcedure:'',responseLockProcedure:'',revealProcedure:'',targetNotOnParticipantDevice:true,leakageAudit:'',exclusionsDeclaredBeforeData:'',allInitiatedEligibleTrialsLogged:true,independentReplicationPlan:'',limitations:''},'external-information-study-template.json');
  const model=event.target.closest('[data-model]');
  if(model){activeModel=model.dataset.model;location.hash=`experiments?model=${activeModel}`;}
  const reset=event.target.closest('[data-reset-model]');
  if(reset){$('#model-panel').innerHTML=modelTemplate(activeModel);updateModel();}
  const process=event.target.closest('[data-process]');
  if(process){activeProcess=process.dataset.process;document.querySelectorAll('[data-process]').forEach(b=>b.setAttribute('aria-selected',b.dataset.process===activeProcess));$('#process-content').innerHTML=processContent();$('#process-content').setAttribute('aria-labelledby',`process-${activeProcess}`);}
  const node=event.target.closest('[data-node]');
  if(node){selectedNode=node.dataset.node;document.querySelectorAll('[data-node]').forEach(n=>n.setAttribute('aria-pressed',n.dataset.node===selectedNode));$('#node-detail').innerHTML=nodeDetail();}
});

main.addEventListener('keydown',event=>{
  const node=event.target.closest('[data-node]');
  if(node&&(event.key==='Enter'||event.key===' ')){event.preventDefault();node.dispatchEvent(new MouseEvent('click',{bubbles:true}));}
  const tab=event.target.closest('[role=tab]');
  if(tab&&['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) {
    const tabs=[...tab.parentElement.querySelectorAll('[role=tab]')];const i=tabs.indexOf(tab);
    const next=event.key==='Home'?tabs[0]:event.key==='End'?tabs[tabs.length-1]:tabs[(i+(event.key==='ArrowRight'?1:-1)+tabs.length)%tabs.length];
    event.preventDefault();next.focus();next.click();
  }
});

main.addEventListener('input',event=>{
  if(event.target.id==='source-search'){sourceState.query=event.target.value;$('#source-results').innerHTML=sourceResults();}
  else if(event.target.closest('#model-panel'))updateModel();
  else if(['dream-trials','dream-hits'].includes(event.target.id))updateBinomial();
});
main.addEventListener('submit',event=>{
  if(event.target.id!=='dream-journal-form')return;
  event.preventDefault();
  const form=new FormData(event.target),entry=Object.fromEntries(form.entries());entry.recordedAt=new Date().toISOString();entry.recordingTimeZone=Intl.DateTimeFormat().resolvedOptions().timeZone;entry.sleepStage='unknown';
  if(entry.recall==='recalled'&&!entry.account.trim()){$('#journal-status').textContent='Add an immediate recall account, or choose “No dream recalled.”';return;}
  if(entry.recall==='none'){entry.awareness='not applicable';entry.control='not applicable';}
  const entries=[...readJournal(),entry];journalMemory=entries;
  try{localStorage.setItem(journalKey,JSON.stringify(entries));journalMemoryAuthoritative=false;$('#journal-status').textContent='Entry saved in this browser. No journal data was sent.';}catch{journalMemoryAuthoritative=true;$('#journal-status').textContent='Browser storage is unavailable. Entry is in this page’s memory only; export now to retain it.';}
  $('#journal-entries').innerHTML=journalEntries();
  for(const id of ['dream-account','dream-location','dream-emotion','dream-interpretation'])document.getElementById(id).value='';
});
main.addEventListener('change',event=>{
  if(event.target.id==='evidence-filter'){sourceState.evidence=event.target.value;$('#source-results').innerHTML=sourceResults();}
  else if(event.target.id==='type-filter'){sourceState.type=event.target.value;$('#source-results').innerHTML=sourceResults();}
  else if(event.target.closest('#model-panel'))updateModel();
});
window.addEventListener('hashchange',route);
$('.skip-link').addEventListener('click',event=>{event.preventDefault();main.focus();main.scrollIntoView({block:'start'});});

async function init() {
  try {
    const response=await fetch('./data/research.json');
    if(!response.ok)throw new Error(`Research data unavailable (${response.status})`);
    const incoming=await response.json();
    data={...data,...incoming};
    for(const key of ['experiments','sources','history','rounds','roadmap','projects'])data[key]=list(data[key]);
    data.meta=data.meta||{};
    data.network={nodes:list(data.network?.nodes),edges:list(data.network?.edges)};
  }catch(error){dataIssue='The source register could not be loaded. The three educational models remain available; research counts below reflect only loaded records.';console.error(error);}
  route();
}
init();
