#!/usr/bin/env node
/** Behavioral DOM review. Install happy-dom, or set HAPPY_DOM_MODULE to its
 * lib/index.js path. This checks DOM behavior, not visual browser rendering.
 */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath, pathToFileURL} from 'node:url';
import path from 'node:path';
import * as models from '../models.js';

const {Window}=await import(process.env.HAPPY_DOM_MODULE ? pathToFileURL(process.env.HAPPY_DOM_MODULE).href : 'happy-dom');
const root=fileURLToPath(new URL('../',import.meta.url));
const data=JSON.parse(readFileSync(path.join(root,'data/research.json'),'utf8'));
// A review-pending execution is neither an unstarted plan nor an accepted result.
data.roadmap.push({id:'G-REVIEW-FIXTURE',title:'Executed result awaiting review',status:'Executed; review pending',detail:'Synthetic status-classification fixture',dependsOn:[]});
const window=new Window({url:'https://example.test/brainwave_opensync/research/',settings:{disableJavaScriptFileLoading:true,disableCSSFileLoading:true}});
const requests=[],persisted=new Map(),blobs=[],downloads=[];
let failWrites=false,writeCount=0;
const storage={getItem:key=>persisted.get(key)??null,setItem:(key,value)=>{writeCount++;if(failWrites)throw new Error('Quota exceeded');persisted.set(key,String(value));},removeItem:key=>persisted.delete(key),clear:()=>persisted.clear()};
Object.defineProperty(window,'localStorage',{value:storage});
window.fetch=async url=>{requests.push(String(url));assert.equal(String(url),'./data/research.json','Unexpected network request');return new window.Response(JSON.stringify(data),{status:200,headers:{'Content-Type':'application/json'}});};
window.URL.createObjectURL=blob=>{blobs.push(blob);return `blob:review-${blobs.length}`;};
window.URL.revokeObjectURL=()=>{};
window.HTMLAnchorElement.prototype.click=function(){downloads.push(this.download);};
window.HTMLElement.prototype.scrollIntoView=()=>{};
window.confirm=()=>true;
Object.assign(window,models);
window.document.write(readFileSync(path.join(root,'index.html'),'utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,''));
const app=readFileSync(path.join(root,'app.js'),'utf8').replace(/^import[^\n]+\n/,'');
// Keep declarations module-local (notably history, which is also a Window API).
window.eval(`(() => {\n${app}\n})();`);
await new Promise(resolve=>setTimeout(resolve,20));
const $=selector=>window.document.querySelector(selector);
const go=hash=>{window.location.hash=hash;window.dispatchEvent(new window.HashChangeEvent('hashchange'));};
const input=(selector,value)=>{const node=$(selector);assert.ok(node,`Missing ${selector}`);node.value=value;node.dispatchEvent(new window.Event('input',{bubbles:true}));};
const click=selector=>{const node=$(selector);assert.ok(node,`Missing ${selector}`);node.dispatchEvent(new window.MouseEvent('click',{bubbles:true,cancelable:true}));};
let passed=0;
const check=async(name,fn)=>{await fn();console.log(`PASS ${name}`);passed++;};

try {
  await check('All authored route views render and preserve distinct source reading scope',()=>{
    for(const route of ['overview','experiments','sources','history','dreams','network','panel','projects']) {go(route);assert.ok($('#main h1'),`${route} heading missing`);assert.equal(window.document.querySelector('[aria-current="page"]')?.dataset.nav,route);}
    go('sources?source=H12');const item=$('#source-H12');assert.ok(item);assert.match(item.textContent,/not read|located/i);
    assert.ok(item.querySelector('details'),'Reading-depth distinction hidden from source view');
    input('#source-search','THIS-QUERY-SHOULD-MATCH-NOTHING');assert.match($('#source-results').textContent,/No sources match/);
  });

  await check('Model controls reject blank, out-of-range and undersampled input without stale results',()=>{
    go('experiments?model=schumann');assert.match($('#schumann-value').textContent,/10\.59/);
    input('#radius','');assert.ok($('#model-error').textContent);assert.equal($('#schumann-value').textContent,'—');
    input('#radius','1000001');assert.ok($('#model-error').textContent);
    click('[data-reset-model]');assert.match($('#schumann-value').textContent,/10\.59/);
    go('experiments?model=resonance');input('#drive','0');assert.equal($('#power-value').textContent,'0');
    go('experiments?model=spectra');input('#sample-rate','1');input('#duration','.01');assert.ok($('#model-error').textContent);assert.equal($('#samples-value').textContent,'—');
  });

  await check('Network overview contains connected experiments and complete accessible edge table',()=>{
    go('network');assert.ok(window.document.querySelectorAll('.network-line').length>0,'Visual graph has no edges');
    assert.ok(window.document.querySelector('[data-node="R1"]'),'Experiment missing from overview');
    assert.equal(window.document.querySelectorAll('.data-table tbody tr').length,data.network.edges.length);
    const node=$('[data-node="R1"]');node.dispatchEvent(new window.KeyboardEvent('keydown',{key:'Enter',bubbles:true}));
    assert.match($('#node-detail').textContent,/Incoming|Outgoing/);
    assert.equal(node.getAttribute('aria-pressed'),'true');
  });

  await check('Planned tasks and actual round states are not conflated',()=>{
    go('overview');assert.match($('#main').textContent,/PLANNED.*RECORDED|planned.*recorded/i);
    go('panel');assert.equal(window.document.querySelectorAll('.round-card').length,6);
    const columns=[...window.document.querySelectorAll('.roadmap-col')];
    const unstarted=columns.find(c=>c.textContent.includes('G10'));
    assert.match(unstarted.querySelector('h3').textContent,/Next|open/);
    const pendingReview=columns.find(c=>c.textContent.includes('G-REVIEW-FIXTURE'));
    assert.match(pendingReview.querySelector('h3').textContent,/progress|review/i);
    for(const r of data.rounds)assert.ok([...window.document.querySelectorAll('.round-card')].some(c=>c.textContent.includes(r.id)&&c.textContent.toLowerCase().includes(r.status.toLowerCase().replace(/[_-]/g,' '))),`Missing status ${r.id}`);
  });

  await check('Typing sensitive recall does not save or transmit it; explicit save is disclosed',()=>{
    go('dreams');assert.match($('#main').textContent,/unencrypted/i);assert.match($('#main').textContent,/stores and generates no targets/i);
    const before=writeCount;input('#dream-account','PRIVATE TEST RECALL');input('#dream-interpretation','LATER TEST INTERPRETATION');
    assert.equal(writeCount,before,'Unexpected autosave');assert.equal(persisted.size,0);
    $('#dream-journal-form').dispatchEvent(new window.Event('submit',{bubbles:true,cancelable:true}));
    assert.equal(persisted.size,1);assert.match($('#journal-entries').textContent,/PRIVATE TEST RECALL/);assert.match($('#journal-entries').textContent,/LATER TEST INTERPRETATION/);
    assert.deepEqual(requests,['./data/research.json'],'Journal caused a network request');
  });

  await check('Storage quota failure retains new recall for immediate export',async()=>{
    failWrites=true;input('#dream-account','SECOND PRIVATE RECALL');
    $('#dream-journal-form').dispatchEvent(new window.Event('submit',{bubbles:true,cancelable:true}));
    assert.match($('#journal-status').textContent,/memory|unavailable/i);
    assert.match($('#journal-entries').textContent,/SECOND PRIVATE RECALL/,'Failed persistent save disappeared from memory view');
    click('[data-export-journal]');assert.equal(downloads.at(-1),'dream-observations.json');
    const exported=JSON.parse(await blobs.at(-1).text());assert.equal(exported.entries.length,2);assert.equal(exported.entries[1].account,'SECOND PRIVATE RECALL');
    click('[data-clear-journal]');assert.equal(persisted.size,0);assert.match($('#journal-entries').textContent,/No observations saved/);
  });

  await check('Chance calculator distinguishes underflow, invalid hits and an unexecuted study template',async()=>{
    input('#dream-trials','10000');input('#dream-hits','10000');assert.match($('#binomial-value').textContent,/^</);
    input('#dream-trials','2');assert.ok($('#binomial-error').textContent);assert.equal($('#binomial-value').textContent,'—');
    click('[data-export-protocol]');const protocol=JSON.parse(await blobs.at(-1).text());assert.match(protocol.status,/no study executed/);assert.equal(protocol.targetNotOnParticipantDevice,true);assert.equal(protocol.fixedTrialCount,null);
  });
  console.log(`${passed} behavioral DOM gates passed. No visual layout, audible output or true participant blinding was tested.`);
} finally {await window.happyDOM.abort();}
