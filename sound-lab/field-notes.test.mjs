#!/usr/bin/env node
/** Independent numerical identities and user-visible data/interaction checks. */
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
import {Window} from 'happy-dom';

const root=fileURLToPath(new URL('../',import.meta.url));
const win=new Window({url:'https://example.test/resonance-research-atlas/sound-lab/field-notes.html',settings:{disableJavaScriptFileLoading:true,disableCSSFileLoading:true}});
win.document.write(readFileSync(path.join(root,'sound-lab/field-notes.html'),'utf8'));
const blobs=[],downloads=[];
win.fetch=async url=>{const parsed=new URL(String(url),win.document.baseURI),mount='/resonance-research-atlas/',relative=parsed.pathname.slice(mount.length);assert.ok(parsed.pathname.startsWith(mount)&&!relative.startsWith('..'));const full=path.join(root,relative);return existsSync(full)?new win.Response(readFileSync(full,'utf8'),{status:200}):new win.Response('missing',{status:404});};
win.URL.createObjectURL=blob=>{blobs.push(blob);return `blob:field-notes-${blobs.length}`;};win.URL.revokeObjectURL=()=>{};win.HTMLAnchorElement.prototype.click=function(){downloads.push(this.download);};
const restore={document:globalThis.document,fetch:globalThis.fetch,URL:globalThis.URL,Blob:globalThis.Blob};
Object.assign(globalThis,{document:win.document,fetch:win.fetch,URL:win.URL,Blob:win.Blob});
const $=selector=>win.document.querySelector(selector);
const event=(selector,type)=>$(selector).dispatchEvent(new win.Event(type,{bubbles:true}));
const click=selector=>$(selector).dispatchEvent(new win.MouseEvent('click',{bubbles:true,cancelable:true}));
const approx=(actual,expected,tolerance=1e-12)=>assert.ok(Math.abs(actual-expected)<=tolerance,`${actual} differs from ${expected}`);
let count=0;async function check(name,fn){await fn();count++;console.log(`PASS ${name}`);}
try{
 const {referenceModel,rlcModel}=await import(pathToFileURL(path.join(root,'sound-lab/field-notes.js')).href);
 await new Promise(resolve=>setTimeout(resolve,40));
 await check('RLC resonance power and passive voltage magnification agree with independent values',()=>{
   const m=rlcModel(10,100,1,4,1,1000);approx(m.currentPeak,.2);approx(m.inputPower,.1);approx(m.loadPower,.08);approx(m.internalPower,.02);approx(m.capacitorPeak,2);approx(m.voltageGain,2);
   approx(m.resonanceOmega,1000);assert.ok(m.rows[0].stored_energy_J>0,'Steady-state initial storage must not be silently zero');
   approx(m.rows[0].stored_energy_J,.0002);
 });
 await check('Off-resonance cycle integration conserves signed work and separates reactive storage',()=>{
   for(const omega of [500,2000]){
    const m=rlcModel(10,100,1,4,1,omega),dt=m.period/400;let input=0,heat=0,storage=0;
    for(let i=1;i<m.rows.length;i++){const a=m.rows[i-1],b=m.rows[i];input+=(a.signed_input_W+b.signed_input_W)*dt/2;heat+=(a.load_W+a.internal_loss_W+b.load_W+b.internal_loss_W)*dt/2;storage+=(a.storage_rate_W+b.storage_rate_W)*dt/2;}
    approx(input,m.inputPower*m.period);approx(input,heat);approx(storage,0);approx(m.rows[0].stored_energy_J,m.rows.at(-1).stored_energy_J);assert.ok(m.rows.some(row=>row.signed_input_W<0),'Reactive circuit returns power during part of its cycle');
   }
 });
 await check('Reference correction retains differential and unstable-reference errors',()=>{
   approx(referenceModel(4,0,2,2).corrected,4);approx(referenceModel(4,0,2,1).corrected,3);approx(referenceModel(4,1,2,2).corrected,3);approx(referenceModel(4,1,1,2).bias,0);
   assert.throws(()=>referenceModel(NaN,0,0,0),RangeError);assert.throws(()=>rlcModel(0,100,1,4,1,1000),RangeError);assert.throws(()=>rlcModel(10,100,-1,4,1,1000),RangeError);
 });
 await check('Ledger shows exact recorded loops and latest reviewed finding, never a guessed future title',()=>{
   const panel=JSON.parse(readFileSync(path.join(root,'research/panel-v4-decisions.json'))),records=panel.reviews;
   assert.equal($('#round-index').querySelectorAll('.round-index-group').length,5);assert.equal($('#round-index').querySelectorAll('button:not([disabled])').length,records.length);
   const selected=records.filter(r=>['accepted_narrow','accepted'].includes(r.status)).at(-1)||records.at(-1);
   assert.ok($('#round-detail').textContent.includes(selected.finding));
   click('[data-loop="R1A"]');assert.ok($('#round-detail').textContent.includes(records.find(r=>r.id==='R1A').finding));
   assert.ok($('#round-detail a[href$="R1.json"]'));assert.ok($('#round-detail').textContent.includes('What remains unestablished'));
 });
 await check('Electrical and magnetic setups are separate from retained sound controls',()=>{
   assert.match($('#page-title').textContent,/Energy/);click('[data-experiment="magnetic"]');assert.match($('#experiment-detail').textContent,/antigravity/);assert.match($('#unresolved-label').textContent,/gravity/);
   click('[data-experiment="reference"]');assert.match($('#experiment-detail').textContent,/recording gain/);assert.match($('#unresolved-label').textContent,/material damping/);assert.equal($('[data-experiment="reference"]').getAttribute('aria-pressed'),'true');
   click('[data-experiment="electric"]');assert.match($('#experiment-detail').textContent,/signed external input/);
 });
 await check('Both calculators clear stale outputs on invalid input and restore from real presets',()=>{
   $('#model-preset').value='differential';event('#model-preset','change');assert.equal($('#corrected-alpha').textContent,'3.00');
   $('#target-alpha').value='';event('#target-alpha','input');assert.equal($('#corrected-alpha').textContent,'—');assert.equal($('#export-model').disabled,true);assert.equal($('#model-plot svg'),null);
   $('#model-preset').value='shared';event('#model-preset','change');assert.equal($('#corrected-alpha').textContent,'4.00');
   $('#capacitance').value='0';event('#capacitance','input');assert.equal($('#input-power').textContent,'—');assert.equal($('#export-energy').disabled,true);assert.equal($('#energy-plot svg'),null);
   $('#energy-preset').value='below';event('#energy-preset','change');assert.ok($('#energy-plot svg'));assert.equal($('#export-energy').disabled,false);
   $('#energy-preset').value='resonance';event('#energy-preset','change');assert.equal($('#input-power').textContent,'0.100');assert.equal($('#voltage-gain').textContent,'2.00 ×');
 });
 await check('CSV exports include model identity, inputs, units and signed power with initial energy',async()=>{
   click('#export-model');click('#export-energy');assert.deepEqual(downloads,['reference-model-synthetic.csv','series-RLC-analytical-cycle.csv']);
   const first=await blobs[0].text(),second=await blobs[1].text();assert.match(first,/synthetic_model/);assert.match(first,/target_log_amplitude/);assert.match(second,/not_measurement/);assert.match(second,/initial_stored_energy_J/);assert.match(second,/signed_input_W/);assert.match(second,/stored_energy_J/);
 });
 await check('Source search and material dictionary preserve reading-depth distinctions',()=>{
   const sources=JSON.parse(readFileSync(path.join(root,'data/sources-v4.json'))).sources,entries=JSON.parse(readFileSync(path.join(root,'docs/panel-v4/alchemy-dictionary.json'))).entries;
   assert.equal($('#source-records').querySelectorAll('.source-entry').length,sources.length);assert.equal($('#alchemy-record tbody').querySelectorAll('tr').length,entries.length);assert.match($('#alchemy-record').textContent,/No historical sample assayed/);assert.match($('#source-records').textContent,/metadata only/);
   $('#source-search').value='not-a-real-source-94';event('#source-search','input');assert.equal($('#source-records').querySelectorAll('.source-entry').length,0);assert.match($('#source-records').textContent,/No matching/);
   $('#source-search').value='';event('#source-search','input');assert.equal($('#source-records').querySelectorAll('.source-entry').length,sources.length);
 });
 await check('Every rendered figure and concrete artifact link exists locally',()=>{
   const missing=[];
   for(const node of win.document.querySelectorAll('a[href],img[src]')){const raw=node.getAttribute('href')||node.getAttribute('src');if(!raw||/^(https?:|#|blob:)/.test(raw))continue;const clean=raw.split('#')[0].split('?')[0],full=path.resolve(root,'sound-lab',clean);if(!existsSync(full))missing.push(clean);}
   assert.deepEqual([...new Set(missing)],[]);
   assert.equal(win.document.querySelectorAll('audio,video[autoplay]').length,0);
 });
 console.log(`Field notes: ${count} checks passed. Rendered desktop/mobile inspection is a separate release check.`);
}finally{Object.assign(globalThis,restore);win.happyDOM.abort();}
