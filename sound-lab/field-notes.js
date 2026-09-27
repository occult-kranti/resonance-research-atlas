/** Field notes: source-driven research record and conditional model calculator. */
const $ = selector => document.querySelector(selector);
const list = value => Array.isArray(value) ? value : [];
const text = value => value == null ? '' : typeof value === 'object' ? JSON.stringify(value) : String(value);
const escapeHTML = value => text(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const human = value => text(value).replaceAll('_',' ');
const state = {panel:null, sources:[], dictionary:null, catalog:null, experiment:'electric', selected:null, model:null, energy:null};
const presets = {shared:[4,0,2,2], differential:[4,0,2,1], unstable:[4,1,2,2]};
const fieldIds = ['target-alpha','reference-alpha','target-beta','reference-beta'];
const energyFieldIds=['inductance','capacitance','internal-r','load-r','voltage-peak','angular-frequency'];

function artifactURL(value) {
  const path=text(value).trim();
  if (/^https?:\/\//i.test(path)) return path;
  if (!path || path.startsWith('/') || path.includes('..') || /^[a-z][a-z\d+.-]*:/i.test(path) || /[\\\u0000-\u001f]/.test(path)) return null;
  return `../${path}`;
}
const link = (path,label,cls='') => artifactURL(path) ? `<a ${cls?`class="${escapeHTML(cls)}"`:''} href="${escapeHTML(artifactURL(path))}">${escapeHTML(label)}</a>` : '';
async function getJSON(path) { const response=await fetch(artifactURL(path)); if(!response.ok)throw new Error(`${path}: HTTP ${response.status}`);return response.json(); }
const statusName = status => ({accepted_narrow:'Accepted within model',accepted:'Reviewed',executed_pending_review:'Awaiting review',producer_completed:'Producer complete',completed_producer:'Producer complete',completed:'Recorded',rejected_or_repair:'Repair required',frozen:'Contract frozen',frozen_before_production:'Contract frozen'}[status]||human(status)||'Not yet recorded');
const accepted = record => ['accepted_narrow','accepted'].includes(record?.status);

const experiments = {
  electric: {
    title:'Account for the complete circuit',change:'One declared circuit condition',fixed:'Boundary & instrument settings',observe:'Voltage, current and time',unresolved:'Any new energy source',
    description:'Begin with the selected passive series RLC model. Compare energy delivered to a load with signed external input, internal dissipation and the change in stored energy.',
    steps:['State the system boundary and list the storage elements before interpreting a result.','Use the proposed low-energy apparatus plan and log initial conditions, load and instrument settings.','Keep signed voltage and current together over the same time interval; retain initial and final storage readings.'],
    controls:['Unpowered baseline and instrument offset','Stored energy at both interval endpoints','Meter loading, wire losses and timing mismatch'],
    limit:'An apparent surplus caused by omitted initial storage is an accounting error. A numerical energy balance is not a hardware result or a demonstration of a new energy source.'
  },
  magnetic: {
    title:'Trace the force through the supports',change:'Magnetic geometry / control',fixed:'Scale boundary & support geometry',observe:'Net load and ordinary-force controls',unresolved:'Any change in gravity',
    description:'A scale responds to forces transmitted through its support. Specify which magnets, cables and supports lie on the scale and which lie outside it.',
    steps:['Draw the complete weighing boundary and mark every external support, cable and nearby magnetic object.','Follow the selected low-force plan and record tare, orientation and ordinary magnetic controls.','Compare reversed and null configurations using the same reporting rule. Keep all trials and return-to-baseline readings.'],
    controls:['Magnetic attraction to objects outside the scale boundary','Vibration, air motion, support contact and drift','Reversal and background controls declared before measurement'],
    limit:'A changed scale reading alone cannot establish antigravity. Ordinary electromagnetic forces, support forces and instrument response must be distinguished within a declared model.'
  },
  reference: {
    title:'A reference beside the target', change:'Reference present / absent',
    description:'Test whether a reference can reveal a changing recording gain. A simultaneous reference adds information only when its own stability and the shared recording response are justified.',
    steps:['Fix the recorder, target and playback source at marked positions. Log the actual distances and gain settings.','Save source-off, reference-only, target-only and combined takes. Use a comfortable low playback level.','Compare the same fit window and retain every raw take. Check whether separating the reference changes the target estimate.'],
    controls:['Reference stability independent of the target','Target-only and reference-only cross-talk checks','Clipping, automatic gain, noise floor and fit-window sensitivity'],
    limit:'A known digital reference is not a known acoustic reference at the microphone. The first computational round starts with separated model channels; inspect later rounds for any tested mixture or admission extensions.'
  },
  tap: {
    title:'One bowl. Repeated gentle taps.', change:'One documented condition',
    description:'Use a small tap to ask how repeatable the recorded decay is. Keep support, microphone position, tap location and recording settings fixed before comparing a changed condition.',
    steps:['Place a household bowl securely on soft support. Mark one tap location and keep the phone stationary.','Record background, then make a gentle tap with a wooden spoon. Leave space for the tail to decay.','Repeat the declared order, save all takes and log rejected ones. Introduce only one documented condition change.'],
    controls:['Repeat baseline before and after the changed condition','Same impact-relative fit window and background check','Look for beating, multiple modes, gain drift and early/late window disagreement'],
    limit:'A single decay fit describes a recorded trace within its accepted window. It does not identify the bowl’s composition, intrinsic material damping, healing properties or a historical mechanism.'
  }
};
function renderExperiment() {
  const item=experiments[state.experiment];
  $('#experiment-detail').innerHTML=`<div class="experiment-head"><h3>${escapeHTML(item.title)}</h3><span class="tag pending">Proposed physical comparison</span></div><p class="experiment-lede">${escapeHTML(item.description)}</p><div class="protocol-columns"><div><h4>Set up & record</h4><ol>${item.steps.map(s=>`<li>${escapeHTML(s)}</li>`).join('')}</ol></div><div><h4>Keep these controls</h4><ul>${item.controls.map(s=>`<li>${escapeHTML(s)}</li>`).join('')}</ul></div></div><p class="experiment-limit"><strong>Claim boundary.</strong> ${escapeHTML(item.limit)}</p>`;
  $('#change-label').textContent=item.change;
  $('#fixed-label').textContent=item.fixed||'Geometry & recording settings';$('#observe-label').textContent=item.observe||'Digital traces and fit stability';$('#unresolved-label').textContent=item.unresolved||'Intrinsic material damping';
  document.querySelectorAll('[data-experiment]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.experiment===state.experiment)));
  renderSetups();
}
function renderSetups() {
  const all=list(state.catalog?.entries||state.catalog?.setups||state.catalog?.assets);
  const scientific=all.filter(entry=>/svg|png|jpe?g|webp$/i.test(entry.file||entry.path||'')&&!/concept/i.test(entry.kind||entry.id||''));
  let matches=scientific.filter(entry=>entry.experiment===state.experiment);
  if(!matches.length){const pattern={electric:'electric|capacitor|circuit|R3',magnetic:'magnet|force|pendulum|R4|R5',reference:'reference|pilot|R1|witness',tap:'tap|bowl|spoon|decay'}[state.experiment];matches=scientific.filter(entry=>new RegExp(pattern,'i').test([entry.id,entry.title].join(' ')));}
  if(!matches.length){$('#setup-plates').innerHTML='<p class="empty">Coordinate plans have not loaded. Use the written protocol and record your actual geometry.</p>';return;}
  const figure=entry=>`<figure class="setup-figure"><a href="${escapeHTML(artifactURL(entry.file||entry.path))}"><img src="${escapeHTML(artifactURL(entry.file||entry.path))}" alt="${escapeHTML(entry.alt||entry.title||'Proposed scientific setup; see caption for coordinates and limits')}" loading="lazy"></a><figcaption><strong>${escapeHTML(entry.title)}</strong> · ${escapeHTML(entry.caption||'Proposed setup, not an executed experiment.')}</figcaption></figure>`;
  const first=matches.find(entry=>/svg$/i.test(entry.file||entry.path))||matches[0];
  $('#setup-plates').innerHTML=figure(first)+`<div class="setup-links">${link(first.file||first.path,'Open scientific plan ↗')}${link('docs/panel-v4/setup-catalog.json','Setup provenance ↗')}</div>`+(matches.length>1?`<details class="setup-extra"><summary>Inspect coordinate 3D views & companion plates</summary>${matches.filter(entry=>entry!==first).map(figure).join('')}</details>`:'')+(['reference','tap'].includes(state.experiment)?'<details class="setup-extra"><summary>View the illustrative sound-study concept</summary><figure class="sound-concept"><img src="../assets/sound-lab-v4/tabletop-concept.png" alt="Generated concept of a proposed bowl and phone sound experiment" loading="lazy"><figcaption>Generated concept illustration; proposed arrangement, not to scale or an executed experiment. A playback phone’s own speaker can replace the separate speaker.</figcaption></figure></details>':'');
}

/** Rates are in s^-1; relative envelopes are stipulated, not inferred. */
export function referenceModel(alpha, referenceAlpha, targetBeta, referenceBeta) {
  const input=[alpha,referenceAlpha,targetBeta,referenceBeta];
  if(!input.every(Number.isFinite)||alpha<0||alpha>20||referenceAlpha<0||referenceAlpha>20||Math.abs(targetBeta)>10||Math.abs(referenceBeta)>10)throw new RangeError('Enter finite decays from 0 to 20 and gain drifts from −10 to 10 s⁻¹.');
  const targetSlope=targetBeta-alpha,referenceSlope=referenceBeta-referenceAlpha;
  const corrected=referenceSlope-targetSlope,bias=corrected-alpha;
  const rows=Array.from({length:101},(_,i)=>{const t=i/100;return {time_s:t,target_log_amplitude:targetSlope*t,reference_log_amplitude:referenceSlope*t,stipulated_target_log_amplitude:-alpha*t};});
  return {alpha,referenceAlpha,targetBeta,referenceBeta,targetSlope,referenceSlope,naive:-targetSlope,corrected,bias,rows};
}
function plotModel(model) {
  const width=Math.max(250,$('#model-plot').clientWidth||720),height=238,left=46,right=14,top=16,bottom=34;
  const values=model.rows.flatMap(row=>[row.target_log_amplitude,row.reference_log_amplitude,row.stipulated_target_log_amplitude]);
  let low=Math.min(0,...values),high=Math.max(0,...values);if(high-low<1){low-=.5;high+=.5;}
  const pad=(high-low)*.1;low-=pad;high+=pad;
  const X=t=>left+t*(width-left-right),Y=v=>top+(high-v)/(high-low)*(height-top-bottom);
  const path=key=>model.rows.map((row,i)=>`${i?'L':'M'}${X(row.time_s).toFixed(2)},${Y(row[key]).toFixed(2)}`).join(' ');
  const ticks=Array.from({length:5},(_,i)=>low+(high-low)*i/4);
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="reference-plot-title reference-plot-desc"><title id="reference-plot-title">Synthetic logarithmic amplitude over one second</title><desc id="reference-plot-desc">Target recorded slope ${model.targetSlope} per second; reference recorded slope ${model.referenceSlope} per second; stipulated target slope ${-model.alpha} per second. These are analytical model traces.</desc>${ticks.map(value=>`<line x1="${left}" x2="${width-right}" y1="${Y(value)}" y2="${Y(value)}" stroke="#e2e5db"/><text x="${left-8}" y="${Y(value)+3}" text-anchor="end" fill="#647267" font-size="9">${value.toFixed(1)}</text>`).join('')}${[0,.25,.5,.75,1].map(t=>`<text x="${X(t)}" y="${height-14}" text-anchor="middle" fill="#647267" font-size="9">${t.toFixed(2)}</text>`).join('')}<text x="${left}" y="10" fill="#647267" font-size="9">ln(A / A₀)</text><text x="${width-right}" y="${height-1}" text-anchor="end" fill="#647267" font-size="9">Time (s)</text><path d="${path('stipulated_target_log_amplitude')}" fill="none" stroke="#8a968a" stroke-width="2.5" stroke-dasharray="6 5"/><path d="${path('target_log_amplitude')}" fill="none" stroke="#315f48" stroke-width="2.3"/><path d="${path('reference_log_amplitude')}" fill="none" stroke="#a4613c" stroke-width="2.3"/></svg>`;
}
function calculate() {
  $('#export-status').textContent='';
  try {
    const values=fieldIds.map(id=>{const field=$(`#${id}`);if(field.value.trim()==='')throw new RangeError('Fill all four rates before calculating.');return Number(field.value);});
    const m=referenceModel(...values);state.model=m;
    $('#corrected-alpha').textContent=m.corrected.toFixed(2);$('#naive-alpha').textContent=`${m.naive.toFixed(2)} s⁻¹`;$('#true-alpha').textContent=`${m.alpha.toFixed(2)} s⁻¹`;$('#correction-bias').textContent=`${m.bias>0?'+':''}${m.bias.toFixed(2)} s⁻¹`;
    const biased=Math.abs(m.bias)>1e-10;const assumedStable=m.referenceAlpha===0&&m.targetBeta===m.referenceBeta;
    $('#bias-status').textContent=biased?'Correction retains a bias':'Zero bias under these premises';$('#bias-status').classList.toggle('biased',biased);
    $('#model-plot').innerHTML=plotModel(m);
    $('#model-explanation').textContent=assumedStable?'The stipulated stable reference removes the shared exponential gain. A real recording must independently justify both premises.':biased?'The apparent correction differs from the stipulated target. Reference decay or unequal gain can remain hidden inside the corrected slope.':'These chosen errors cancel algebraically. A zero net bias here does not establish a stable reference or a shared gain mechanism.';
    $('#export-model').disabled=false;
  }catch(error){state.model=null;['corrected-alpha','naive-alpha','true-alpha','correction-bias'].forEach(id=>$(`#${id}`).textContent='—');$('#model-plot').innerHTML=`<p class="empty error">${escapeHTML(error.message)}</p>`;$('#bias-status').textContent='Calculation withheld';$('#bias-status').classList.add('biased');$('#model-explanation').textContent='Correct the input values to restore the model. The prior output has been cleared.';$('#export-model').disabled=true;}
}
function downloadModel() {
  if(!state.model)return;const m=state.model;
  const rows=[['# synthetic_model','reference_correction_R1'],['# units','time_s; logarithmic relative amplitude'],['# premise','stipulated separated envelopes; no physical measurement'],['# alpha_per_s',m.alpha],['# reference_alpha_per_s',m.referenceAlpha],['# target_beta_per_s',m.targetBeta],['# reference_beta_per_s',m.referenceBeta],['# corrected_alpha_per_s',m.corrected],['# bias_per_s',m.bias],['time_s','target_log_amplitude','reference_log_amplitude','stipulated_target_log_amplitude'],...m.rows.map(row=>Object.values(row))];
  const blob=new Blob([rows.map(row=>row.join(',')).join('\n')+'\n'],{type:'text/csv;charset=utf-8'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='reference-model-synthetic.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('#export-status').textContent='Model CSV exported with parameters, units and synthetic label.';
}

/** Exact sinusoidal steady state of a passive series RLC; SI inside the model. */
export function rlcModel(inductance_mH,capacitance_uF,internalR,loadR,voltagePeak,omega) {
  const params=[inductance_mH,capacitance_uF,internalR,loadR,voltagePeak,omega];
  if(!params.every(Number.isFinite)||inductance_mH<.01||inductance_mH>1000||capacitance_uF<.01||capacitance_uF>10000||internalR<0||internalR>1000||loadR<.01||loadR>1000||voltagePeak<0||voltagePeak>5||omega<1||omega>100000)throw new RangeError('Use positive L, C, load and frequency within the shown limits; internal resistance and source voltage may be zero.');
  const L=inductance_mH/1000,C=capacitance_uF/1e6,R=internalR+loadR,X=omega*L-1/(omega*C),impedance=Math.hypot(R,X),phase=Math.atan2(X,R),currentPeak=voltagePeak/impedance,period=2*Math.PI/omega;
  const inputPower=.5*currentPeak**2*R,loadPower=.5*currentPeak**2*loadR,internalPower=.5*currentPeak**2*internalR;
  const capacitorPeak=currentPeak/(omega*C),voltageGain=1/(omega*C*impedance),resonanceOmega=1/Math.sqrt(L*C);
  const rows=Array.from({length:401},(_,i)=>{const angle=2*Math.PI*i/400,time_s=angle/omega,voltage=voltagePeak*Math.sin(angle),current=currentPeak*Math.sin(angle-phase),capacitorVoltage=-capacitorPeak*Math.cos(angle-phase),input=voltage*current,load=loadR*current**2,internal=internalR*current**2,stored=.5*L*current**2+.5*C*capacitorVoltage**2;return {time_s,phase_cycle:i/400,voltage_V:voltage,current_A:current,capacitor_voltage_V:capacitorVoltage,signed_input_W:input,load_W:load,internal_loss_W:internal,storage_rate_W:input-load-internal,stored_energy_J:stored};});
  return {L,C,internalR,loadR,voltagePeak,omega,X,impedance,phase,currentPeak,period,inputPower,loadPower,internalPower,capacitorPeak,voltageGain,resonanceOmega,rows};
}
function plotEnergy(model) {
  const width=Math.max(250,$('#energy-plot').clientWidth||720),height=238,left=49,right=14,top=16,bottom=34;
  const vals=model.rows.flatMap(row=>[row.signed_input_W,row.load_W+row.internal_loss_W,row.storage_rate_W]);let low=Math.min(0,...vals),high=Math.max(0,...vals);if(high-low<1e-8){low=-.1;high=.1;}const pad=(high-low)*.12;low-=pad;high+=pad;
  const X=t=>left+t*(width-left-right),Y=v=>top+(high-v)/(high-low)*(height-top-bottom);
  const path=fn=>model.rows.map((row,i)=>`${i?'L':'M'}${X(row.phase_cycle).toFixed(2)},${Y(fn(row)).toFixed(2)}`).join(' ');
  const ticks=Array.from({length:5},(_,i)=>low+(high-low)*i/4);
  const format=n=>Math.abs(high)<.01&&n!==0?n.toExponential(1):n.toFixed(3);
  return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-labelledby="energy-plot-title energy-plot-desc"><title id="energy-plot-title">Calculated instantaneous powers over one source cycle</title><desc id="energy-plot-desc">Mean signed input ${model.inputPower} W; load ${model.loadPower} W; internal loss ${model.internalPower} W. All curves are analytical, not measured.</desc>${ticks.map(value=>`<line x1="${left}" x2="${width-right}" y1="${Y(value)}" y2="${Y(value)}" stroke="#e2e5db"/><text x="${left-8}" y="${Y(value)+3}" text-anchor="end" fill="#647267" font-size="9">${format(value)}</text>`).join('')}<line x1="${left}" x2="${width-right}" y1="${Y(0)}" y2="${Y(0)}" stroke="#b7c4b3"/>${[0,.25,.5,.75,1].map(t=>`<text x="${X(t)}" y="${height-14}" text-anchor="middle" fill="#647267" font-size="9">${t.toFixed(2)}</text>`).join('')}<text x="${left}" y="10" fill="#647267" font-size="9">Power (W)</text><text x="${width-right}" y="${height-1}" text-anchor="end" fill="#647267" font-size="9">Source cycle</text><path d="${path(row=>row.storage_rate_W)}" fill="none" stroke="#8a968a" stroke-width="2" stroke-dasharray="6 5"/><path d="${path(row=>row.load_W+row.internal_loss_W)}" fill="none" stroke="#a4613c" stroke-width="3.8"/><path d="${path(row=>row.signed_input_W)}" fill="none" stroke="#315f48" stroke-width="2.2"/></svg>`;
}
function calculateEnergy() {
  $('#energy-export-status').textContent='';
  try{const values=energyFieldIds.map(id=>{const field=$(`#${id}`);if(field.value.trim()==='')throw new RangeError('Fill all six circuit parameters before calculating.');return Number(field.value);});const m=rlcModel(...values);state.energy=m;
    const watts=value=>value!==0&&value<.001?`${value.toExponential(2)} W`:`${value.toFixed(3)} W`;
    $('#input-power').textContent=m.inputPower!==0&&m.inputPower<.001?m.inputPower.toExponential(2):m.inputPower.toFixed(3);$('#load-power').textContent=watts(m.loadPower);$('#internal-power').textContent=watts(m.internalPower);$('#voltage-gain').textContent=`${m.voltageGain.toFixed(2)} ×`;
    $('#energy-status').textContent='Modeled input balances dissipation over a full cycle';$('#energy-status').classList.remove('biased');$('#energy-plot').innerHTML=plotEnergy(m);
    $('#energy-explanation').textContent=`The capacitor peak is ${m.capacitorPeak.toFixed(3)} V. Its voltage ratio follows the passive circuit impedance; average load power plus internal loss equals the signed input power.`;
    $('#energy-secondary').textContent=`Current peak: ${m.currentPeak.toPrecision(4)} A · Resonant angular frequency: ${m.resonanceOmega.toPrecision(5)} rad/s · Source cycle: ${(m.period*1000).toPrecision(4)} ms. The stored-energy trace and signed powers are included in the CSV.`;
    $('#export-energy').disabled=false;
  }catch(error){state.energy=null;['input-power','load-power','internal-power','voltage-gain'].forEach(id=>$(`#${id}`).textContent='—');$('#energy-status').textContent='Calculation withheld';$('#energy-status').classList.add('biased');$('#energy-plot').innerHTML=`<p class="empty error">${escapeHTML(error.message)}</p>`;$('#energy-explanation').textContent='Correct the inputs to restore the model. The prior output has been cleared.';$('#energy-secondary').textContent='';$('#export-energy').disabled=true;}
}
function downloadEnergy() {
  if(!state.energy)return;const m=state.energy;
  const rows=[['# model','analytical_passive_series_RLC_steady_state_not_measurement'],['# L_H',m.L],['# C_F',m.C],['# Rinternal_ohm',m.internalR],['# Rload_ohm',m.loadR],['# source_peak_V',m.voltagePeak],['# omega_rad_per_s',m.omega],['# initial_stored_energy_J',m.rows[0].stored_energy_J],Object.keys(m.rows[0]),...m.rows.map(row=>Object.values(row))];
  const blob=new Blob([rows.map(row=>row.join(',')).join('\n')+'\n'],{type:'text/csv;charset=utf-8'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='series-RLC-analytical-cycle.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);$('#energy-export-status').textContent='Calculated cycle exported with SI units, parameters and initial storage.';
}

function reviews() { return list(state.panel?.reviews||state.panel?.loops); }
function roundRecords(round) { return reviews().filter(item=>Number(item.round||text(item.id).match(/R(\d)/)?.[1])===round); }
function renderLedger() {
  const records=reviews();const completed=records.filter(accepted).length;
  $('#program-status').textContent=state.panel?`${records.length} loop records · ${completed} accepted reviews · physical experiments remain proposed`:'Research ledger unavailable. Open the source record to inspect status.';
  $('#round-index').innerHTML=Array.from({length:5},(_,i)=>{const n=i+1,entries=roundRecords(n);const title=entries[0]?.title||'Next question not selected';return `<div class="round-index-group"><div class="round-index-name"><span>0${n}</span><strong>${escapeHTML(title)}</strong></div><div class="loop-buttons">${['A','B'].map(letter=>{const r=entries.find(e=>e.id===`R${n}${letter}`||text(e.loop).toUpperCase()===letter);return `<button type="button" data-loop="R${n}${letter}" ${r?'':'disabled'} aria-current="${state.selected===r?.id}" aria-label="Round ${n}, loop ${letter}${r?'':', not recorded'}">${letter==='A'?'A · Produce':'B · Review'}</button>`;}).join('')}</div></div>`;}).join('');
  const r=records.find(item=>item.id===state.selected)||records[0];
  if(!r){$('#round-detail').innerHTML='<p class="empty">The current ledger has no recorded loop result. A planned round is not an executed computation.</p>';return;}
  state.selected=r.id;document.querySelectorAll('[data-loop]').forEach(b=>b.setAttribute('aria-current',String(b.dataset.loop===r.id)));
  const metrics=Object.entries(r.metrics||{});const figures=list(r.figurePaths||r.figures).map(f=>typeof f==='string'?f:f.path||f.file).filter(artifactURL);
  const scope=text(r.scope||r.claimCeiling||r.evidenceType||'See the frozen contract for the exact model.');
  const limits=list(r.withheld||r.limits||r.limitations);
  $('#round-detail').innerHTML=`<div class="round-meta"><span>${escapeHTML(r.id)} / ${/B$/.test(r.id)?'Skeptical review':'Evidence production'}</span><span class="tag ${accepted(r)?'':'pending'}">${escapeHTML(statusName(r.status))}</span></div><h3>${escapeHTML(r.title||r.question)}</h3><p class="round-question">${escapeHTML(r.question)}</p><div class="finding"><span>${accepted(r)?'Narrow finding':'Recorded finding · see review status'}</span><p>${escapeHTML(r.finding||r.result||'Finding not supplied.')}</p></div><div class="round-facts"><div><h4>What this supports</h4><p>${escapeHTML(scope)}</p></div><div><h4>What remains unestablished</h4>${limits.length?`<ul>${limits.map(value=>`<li>${escapeHTML(value)}</li>`).join('')}</ul>`:'<p>No wider physical claim is inferred. Inspect the contract and review.</p>'}</div></div>${metrics.length?`<details class="metrics-details"><summary>Inspect recorded model quantities (${metrics.length})</summary><div class="table-scroll"><table class="metrics-table"><tbody>${metrics.map(([key,value])=>`<tr><th scope="row">${escapeHTML(human(key))}</th><td>${escapeHTML(typeof value==='number'?Number(value.toPrecision(7)):text(value))}</td></tr>`).join('')}</tbody></table></div></details>`:''}${figures.slice(0,2).map(path=>`<figure class="research-figure"><a href="${escapeHTML(artifactURL(path))}"><img src="${escapeHTML(artifactURL(path))}" alt="${escapeHTML(r.id)} computational result figure; see linked result and raw data for values and model assumptions" loading="lazy"></a><figcaption>${escapeHTML(r.id)} · ${escapeHTML(human(r.evidenceType||'computational evidence'))}. ${link(path,'Open full-size figure ↗')}</figcaption></figure>`).join('')}<div class="artifact-links">${link(r.contractPath,'Frozen contract ↗')}${link(r.resultsPath||r.resultPath,'Numerical results ↗')}${link(r.reviewPath,'Independent review ↗')}${link(r.reportPath,'Research report ↗')}${list(r.rawPaths).map((path,i)=>link(path,`Raw data ${i+1} ↗`)).join('')}</div>${r.nextDecision?`<p class="round-next"><strong>Next decision.</strong> ${escapeHTML(r.nextDecision)}</p>`:''}`;
  const roadmap=state.panel?.nextDecision||state.panel?.stopDecision||state.panel?.nextAuthorized||state.panel?.roadmapSummary;
  $('#roadmap-record').innerHTML=`${roadmap?`<p><strong>Advisor direction.</strong> ${escapeHTML(roadmap)}</p>`:''}<p>${link(state.panel?.roadmapPath||'docs/panel-v4/roadmap-v4.md','Read the step-by-step roadmap ↗')} · ${link('docs/panel-v4/panel-log.md','Panel planning record ↗')} · ${link('research/panel-v4-decisions.json','Complete decision ledger ↗')}</p>`;
}

function sourceCategory(source) {
  const v=[source.category,source.claim_category,source.evidenceType,source.type,source.provenance,source.title].join(' ').toLowerCase();
  if(/patent|reddit|fringe|gateway|stargate|discourse|claim|rumou?r|bashar/.test(v))return 'claims';
  if(/history|historic|alchemy|newton|jung|manuscript|dictionary|nomenclature/.test(v))return 'historical';
  return 'scientific';
}
function renderSources() {
  const query=$('#source-search').value.trim().toLowerCase(),category=$('#source-filter').value;
  const matches=state.sources.filter(source=>(category==='all'||sourceCategory(source)===category)&&(!query||JSON.stringify(source).toLowerCase().includes(query)));
  $('#source-count').textContent=`${state.sources.length} source records`;
  $('#source-filter-status').textContent=`${matches.length} of ${state.sources.length} records shown. Reading depth is stated for each source.`;
  $('#source-records').innerHTML=matches.length?matches.map(source=>`<details class="source-entry"><summary><span class="source-id">${escapeHTML(source.id)}</span><span class="source-title">${escapeHTML(source.title)}<small>${escapeHTML(human(source.reading_status||source.readingStatus||source.status||'Reading depth in record'))} · ${escapeHTML(source.claim_category||source.category||human(sourceCategory(source)))}</small></span></summary><div class="source-detail"><p><strong>Read:</strong> ${escapeHTML(source.reading_depth||source.readingDepth||source.depth||'See the source ledger.')}</p>${source.sections_read?`<p><strong>Passages:</strong> ${escapeHTML(Array.isArray(source.sections_read)?source.sections_read.join('; '):source.sections_read)}</p>`:''}<p><strong>Supports:</strong> ${escapeHTML(source.supports||source.claimSupported||'See the source record.')}</p><p><strong>Does not establish:</strong> ${escapeHTML(source.does_not_support||source.does_not_establish||source.doesNotEstablish||source.limitations||'No conclusion beyond the documented reading scope.')}</p><p><strong>Provenance:</strong> ${escapeHTML(source.provenance||source.evidenceType||source.category||'See the source ledger.')}</p>${link(source.url,'Open original source ↗')}</div></details>`).join(''):'<p class="empty">No matching source records. Try a shorter term or choose all source types.</p>';
}
function renderDictionary() {
  const dictionary=state.dictionary,entries=list(dictionary?.entries||dictionary?.terms);
  if(!entries.length){$('#alchemy-record').innerHTML='<p class="empty">The current dictionary is unavailable. <a href="index.html#materials">Inspect the inherited material record ↗</a>.</p>';return;}
  $('#alchemy-record').innerHTML=`<p>${escapeHTML(dictionary.display_notice||dictionary.scope||'These are contextual candidate readings, not assays of historical materials.')}</p><div class="table-scroll"><table class="material-table"><thead><tr><th scope="col">Historical term</th><th scope="col">Modern reading</th><th scope="col">Why context matters</th><th scope="col">Evidence needed</th></tr></thead><tbody>${entries.map(entry=>`<tr><td><span class="material-symbol">${escapeHTML(list(entry.symbols).join(' '))}</span><strong>${escapeHTML(entry.term||entry.historicalTerm)}</strong><small>${escapeHTML(human(entry.mappingStatus||entry.status))}</small></td><td>${escapeHTML(entry.modernCandidate||entry.modernReading||'No justified unique assignment')}<small>${list(entry.elements).length?`Candidate elements: ${escapeHTML(entry.elements.join(', '))}`:''}</small></td><td>${escapeHTML(entry.contextLimit||entry.limit||entry.context)}<p>${escapeHTML(entry.primaryContext||entry.passage)}</p></td><td>${escapeHTML(entry.discriminatingAssay||entry.requiredEvidence||'A literal passage and independent sample measurement.')}<small>${entry.actualSampleAssayed?'See the specimen assay record':'No historical sample assayed'}</small><p>${escapeHTML(list(entry.sourceIds).join(', '))}</p></td></tr>`).join('')}</tbody></table></div><p class="small-note">A word-to-element mapping does not supply compound, phase, purity or sample identity. ${link('docs/panel-v4/alchemy-dictionary.json','Download dictionary ↗')}</p>`;
}

async function init() {
  renderExperiment();calculate();calculateEnergy();renderLedger();
  document.querySelectorAll('[data-experiment]').forEach(button=>button.addEventListener('click',()=>{state.experiment=button.dataset.experiment;renderExperiment();}));
  $('#reference-form').addEventListener('submit',event=>event.preventDefault());
  fieldIds.forEach(id=>$(`#${id}`).addEventListener('input',()=>{$('#model-preset').value='custom';calculate();}));
  $('#model-preset').addEventListener('change',()=>{const values=presets[$('#model-preset').value];if(values){fieldIds.forEach((id,i)=>$(`#${id}`).value=values[i]);calculate();}});
  $('#export-model').addEventListener('click',downloadModel);
  $('#energy-form').addEventListener('submit',event=>event.preventDefault());
  energyFieldIds.forEach(id=>$(`#${id}`).addEventListener('input',()=>{$('#energy-preset').value='custom';calculateEnergy();}));
  $('#energy-preset').addEventListener('change',()=>{const preset=$('#energy-preset').value;if(preset==='custom')return;const values=[10,100,1,4,1,{resonance:1000,below:500,above:2000}[preset]];energyFieldIds.forEach((id,i)=>$(`#${id}`).value=values[i]);calculateEnergy();});
  $('#export-energy').addEventListener('click',downloadEnergy);
  $('#round-index').addEventListener('click',event=>{const button=event.target.closest('[data-loop]');if(button&&!button.disabled){state.selected=button.dataset.loop;renderLedger();}});
  $('#source-search').addEventListener('input',renderSources);$('#source-filter').addEventListener('change',renderSources);
  if(typeof ResizeObserver!=='undefined'){
    const widths=new Map();const observer=new ResizeObserver(entries=>{for(const entry of entries){const width=entry.contentRect.width;if(Math.abs(width-(widths.get(entry.target.id)||0))<1)continue;widths.set(entry.target.id,width);if(entry.target.id==='model-plot'&&state.model)entry.target.innerHTML=plotModel(state.model);if(entry.target.id==='energy-plot'&&state.energy)entry.target.innerHTML=plotEnergy(state.energy);}});observer.observe($('#model-plot'));observer.observe($('#energy-plot'));
  }
  const results=await Promise.allSettled([getJSON('research/panel-v4-decisions.json'),getJSON('data/sources-v4.json'),getJSON('docs/panel-v4/alchemy-dictionary.json'),getJSON('docs/panel-v4/setup-catalog.json')]);
  if(results[0].status==='fulfilled'){state.panel=results[0].value;state.selected=reviews().filter(accepted).at(-1)?.id||reviews().at(-1)?.id;renderLedger();}else{$('#program-status').textContent='Research ledger unavailable. Use the linked source record.';$('#round-detail').innerHTML='<p class="empty error">The decision ledger could not be loaded. No completion status is inferred. <a href="../research/panel-v4-decisions.json">Open the ledger directly ↗</a>.</p>';}
  if(results[1].status==='fulfilled'){state.sources=list(results[1].value.sources||results[1].value.entries||results[1].value);renderSources();}else{$('#source-count').textContent='Ledger unavailable';$('#source-records').innerHTML='<p class="empty error">The source ledger could not be loaded. <a href="../data/sources-v4.json">Open the file directly ↗</a>.</p>';}
  if(results[2].status==='fulfilled')state.dictionary=results[2].value;renderDictionary();
  if(results[3].status==='fulfilled')state.catalog=results[3].value;renderSetups();
}
if(typeof document!=='undefined')init();
