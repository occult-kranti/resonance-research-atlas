#!/usr/bin/env node
/** Sound-lab DOM and numeric behavior. No physical sound data is inferred. */
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {Window} from 'happy-dom';

const root=fileURLToPath(new URL('../',import.meta.url));
const ledger=JSON.parse(readFileSync(path.join(root,'research/panel-v3-decisions.json')));
const win=new Window({url:'https://example.test/resonance-research-atlas/sound-lab/',settings:{disableJavaScriptFileLoading:true,disableCSSFileLoading:true}});
const downloaded=[];let requests=[];
win.document.write(readFileSync(path.join(root,'sound-lab/index.html'),'utf8'));
// Module imports use file URLs in Node; resolve against this module's root, independent of checkout directory.
win.fetch=async url=>{const parsed=new URL(String(url)),mount=new URL('../',win.location.href).pathname;const relative=parsed.protocol==='file:'?path.relative(root,fileURLToPath(parsed.href)):parsed.pathname.slice(mount.length);assert.ok(!path.isAbsolute(relative)&&!relative.startsWith('..'),'Unexpected fixture path');requests.push(relative);const full=path.join(root,relative);return existsSync(full)?new win.Response(readFileSync(full,'utf8'),{status:200}):new win.Response('missing',{status:404})};
win.URL.createObjectURL=blob=>{downloaded.push(blob);return `blob:lab-${downloaded.length}`};win.URL.revokeObjectURL=()=>{};
win.HTMLAnchorElement.prototype.click=function(){downloaded.push(this.download)};
win.HTMLElement.prototype.scrollIntoView=()=>{};
const restore={document:globalThis.document,fetch:globalThis.fetch,URL:globalThis.URL,Blob:globalThis.Blob,matchMedia:globalThis.matchMedia};
Object.assign(globalThis,{document:win.document,fetch:win.fetch,URL:win.URL,Blob:win.Blob,matchMedia:()=>({matches:false})});
const $=selector=>win.document.querySelector(selector);
const click=selector=>{const node=$(selector);assert.ok(node,`Missing ${selector}`);node.dispatchEvent(new win.MouseEvent('click',{bubbles:true,cancelable:true}))};
let passed=0;async function check(name,fn){await fn();console.log(`PASS ${name}`);passed++}
try{
 await import(pathToFileURL(path.join(root,'sound-lab/app.js')).href);
 await new Promise(resolve=>setTimeout(resolve,30));
 await check('Data adapter preserves source status, exact review and ten-loop navigation',()=>{
  assert.equal($('#loop-index').querySelectorAll('button').length,10);
  assert.equal($('#planning-panels').querySelectorAll('.panel-card').length,3);
  const first=ledger.reviews.find(r=>r.id==='S1A');assert.ok(first);
  assert.match($('#loop-detail').textContent,new RegExp(first.finding.slice(0,24)));
  assert.match($('#loop-detail').textContent,/accepted within model/i);
  assert.ok($('#loop-detail a[href$="S1A-review.json"]'));
  click('[data-loop="S5B"]');const last=ledger.reviews.find(r=>r.id==='S5B');
  if(last)assert.match($('#loop-detail').textContent,new RegExp(last.finding.slice(0,20)));
  else{assert.match($('#loop-detail').textContent,/not been recorded|awaiting selection/i);assert.equal($('#loop-detail').querySelectorAll('.research-figure').length,0)}
  assert.ok($('#loop-index button[aria-current="true"][data-loop="S5B"]'));
 });
 await check('Artifacts, dictionary and conditional tier retain explicit provenance',()=>{
  click('[data-loop="S1A"]');assert.ok($('#apparatus-diagram img[alt]'));assert.ok($('#loop-detail .inference img[alt]'));
  assert.equal($('#alchemy-record table tbody').querySelectorAll('tr').length,7);
  assert.equal($('#alchemy-record').querySelectorAll('tr').length,16);
  assert.match($('#alchemy-record').textContent,/No historical sample assayed/);
  assert.equal($('#b-rounds').querySelectorAll('.b-card').length,3);
  assert.match($('#interpretation').textContent,/does not decide whether AI has subjective experience/i);
  const bSummary=JSON.parse(readFileSync(path.join(root,'research/consciousness-v3/summary.json')));
  if(bSummary.rounds.length){const b1=$('#b-rounds .b-card');assert.match(b1.textContent,/Agreement is not additional information|conditional protocol audit/i);assert.ok(b1.querySelector('details'));assert.ok(b1.querySelector('.b-metric-wrap'));assert.ok(b1.querySelector('.b-figure'));if(!ledger.reviews.some(r=>r.id==='B1'))assert.equal(b1.querySelector('a[href$="B1-review.json"]'),null)}
  assert.ok($('#loop-detail .source-depth a[href^="https://"]'));
  assert.ok($('#cli-guide').textContent.includes('intake_v2.py'));
  if(ledger.reviews.some(r=>r.id==='S5B'&&r.status==='accepted_narrow')){
   assert.ok($('#batch-guide').textContent.includes('batch_intake.py'));
   assert.match($('#batch-guide').textContent,/primary contrast is withheld/i);
  }
  assert.equal($('#source-index').querySelectorAll('.source-entry').length,32);
  assert.match($('#source-index').textContent,/Distinct source records: 32/);
  const catalog=JSON.parse(readFileSync(path.join(root,'docs/panel-v3/setup-catalog.json')));
  assert.equal($('#setup-gallery-items').querySelectorAll('figure').length,catalog.entries.length);
  assert.ok($('#setup-gallery-items img[src$="s1-bench-3d.png"]'));
  assert.ok($('#setup-gallery-items img[src$="s2-spoon-3d.png"]'));
  for(const e of catalog.entries)assert.ok($('#setup-gallery-items').querySelector(`a[href="../${e.file}"]`),`Missing gallery plate ${e.id}`);
 });
 await check('Model bench exports synthetic axes and clears stale output after invalid input',async()=>{
  assert.match($('#model-result-title').textContent,/Calculated/);
  assert.match($('#result-line').textContent,/Q = 6/);
  click('#tab-echo');assert.match($('#result-line').textContent,/200 Hz/);
  $('#model-reflection').value='0';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));assert.match($('#result-line').textContent,/no delayed path/i);
  $('#model-reflection').value='.6';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));
  $('#model-delay').value='0';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));
  assert.equal($('#plot-wrap').children.length,0);assert.equal($('#result-line').textContent,'');assert.match($('#model-error').textContent,/between/);
  $('#model-delay').value='NaN';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));assert.equal($('#plot-wrap').children.length,0);
  $('#model-delay').value='5';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));
  click('#download-csv');assert.equal(downloaded.at(-1),'sound-echo-synthetic.csv');
  const csv=await downloaded.at(-2).text();assert.match(csv,/# synthetic model output; no physical measurement/);assert.match(csv,/x=Frequency \/ Hz/);
  click('#tab-damping');assert.match($('#result-line').textContent,/e-fold/);
  assert.match($('#model-form').textContent,/Undamped natural frequency/);
  $('#model-q').value='';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));assert.equal($('#plot-wrap').children.length,0);
  click('#tab-reference');assert.match($('#result-line').textContent,/requires η < \|H₀\|/);
  $('#model-noise').value='.2';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));
  assert.match($('#model-error').textContent,/denominator has no positive lower bound/);assert.equal($('#plot-wrap').children.length,0);assert.equal($('#result-line').textContent,'');
  $('#model-noise').value='.01';$('#model-form').dispatchEvent(new win.Event('submit',{bubbles:true,cancelable:true}));assert.match($('#result-line').textContent,/worst-case ratio-error/);
 });
 await check('Local CSV screen reports digital quantities without network transmission',async()=>{
  const before=requests.length,input=$('#recording-file');
  const file=new win.File(['time_s,amplitude_FS\n0,0\n0.001,0.5\n0.002,-1\n'],'tap.csv',{type:'text/csv'});
  Object.defineProperty(input,'files',{configurable:true,value:[file]});input.dispatchEvent(new win.Event('change'));await new Promise(resolve=>setTimeout(resolve,20));
  assert.match($('#intake-result').textContent,/3/);assert.match($('#intake-result').textContent,/clipped/i);
  assert.match($('#intake-status').textContent,/No file was uploaded/);assert.equal(requests.length,before);
  click('#download-intake');assert.equal(downloaded.at(-1),'sound-recording-screen.json');
 });
 await check('Truncated WAV and overlapping file reads cannot leave false current metadata',async()=>{
  const input=$('#recording-file'),bytes=new Uint8Array(48),dv=new DataView(bytes.buffer),four=(offset,s)=>{for(let i=0;i<4;i++)bytes[offset+i]=s.charCodeAt(i)};
  four(0,'RIFF');four(8,'WAVE');four(12,'fmt ');dv.setUint32(16,16,true);dv.setUint16(20,1,true);dv.setUint16(22,1,true);dv.setUint32(24,8000,true);dv.setUint32(28,16000,true);dv.setUint16(32,2,true);dv.setUint16(34,16,true);four(36,'data');dv.setUint32(40,3,true);
  Object.defineProperty(input,'files',{configurable:true,value:[new win.File([bytes],'partial.wav')]});input.dispatchEvent(new win.Event('change'));await new Promise(resolve=>setTimeout(resolve,20));assert.match($('#intake-status').textContent,/partial sample frame/i);assert.equal($('#download-intake'),null);
  let release;const slow={name:'old.csv',size:20,text:()=>new Promise(resolve=>{release=resolve})},fast={name:'new.csv',size:34,text:async()=>`time_s,amplitude_FS\n0,0\n.001,.2\n.002,.4`};
  Object.defineProperty(input,'files',{configurable:true,value:[slow]});input.dispatchEvent(new win.Event('change'));
  Object.defineProperty(input,'files',{configurable:true,value:[fast]});input.dispatchEvent(new win.Event('change'));await new Promise(resolve=>setTimeout(resolve,20));assert.match($('#intake-result').textContent,/new.csv/);
  release(`time_s,amplitude_FS\n0,0\n.001,1`);await new Promise(resolve=>setTimeout(resolve,20));assert.match($('#intake-result').textContent,/new.csv/);assert.doesNotMatch($('#intake-result').textContent,/old.csv/);
 });
 console.log(`${passed} sound-lab behavior gates passed.`);
}finally{Object.assign(globalThis,restore);await win.happyDOM.close()}
