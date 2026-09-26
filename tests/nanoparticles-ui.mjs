#!/usr/bin/env node
/** Nanoparticle model and behavior checks. Uses independent numerical ODE
 * integrations and synthetic DOM fixtures; no physical experiment is claimed.
 * HAPPY_DOM_MODULE can identify an existing happy-dom/lib/index.js installation.
 */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
import * as models from '../models.js';
const root=fileURLToPath(new URL('../',import.meta.url));
let passed=0;
const check=async(name,fn)=>{await fn();console.log(`PASS ${name}`);passed++;};
const near=(actual,expected,relative=1e-7,absolute=1e-12)=>assert.ok(Math.abs(actual-expected)<=absolute+relative*Math.abs(expected),`Expected ${actual} ≈ ${expected}`);

await check('N1 loop work matches independent time-domain Debye integration',()=>{
  for(const x of [.1,1,10]) {
    // Dimensionless time s=t/tau, normalized m=M/(chi0 Hpeak).
    // Integrate dm/ds=cos(x s)-m; calculate integral H dm over the final cycle.
    const period=2*Math.PI/x,cycles=Math.ceil(40/period)+1,stepsPerCycle=4096,dt=period/stepsPerCycle;
    let m=0,t=0,area=0;
    for(let i=0;i<cycles*stepsPerCycle;i++) {
      const old=m,oldH=Math.cos(x*t);
      const f=(time,value)=>Math.cos(x*time)-value;
      const k1=f(t,m),k2=f(t+dt/2,m+dt*k1/2),k3=f(t+dt/2,m+dt*k2/2),k4=f(t+dt,m+dt*k3);
      m+=dt*(k1+2*k2+2*k3+k4)/6;t+=dt;
      if(i>=(cycles-1)*stepsPerCycle)area+=(oldH+Math.cos(x*t))*(m-old)/2;
    }
    const model=models.magneticDebye({chi0:.02,tauS:1e-6,fieldPeakApm:1,frequencyHz:x/(2*Math.PI*1e-6)});
    near(model.cycleEnergyJpm3,area*models.VACUUM_PERMEABILITY_REFERENCE*.02,1e-6,1e-16);
    near(model.powerWpm3,model.cycleEnergyJpm3*x/(2*Math.PI*1e-6),1e-12);
  }
});
await check('N1 distinguishes the cycle-energy peak from increasing fixed-field power',()=>{
  const point=x=>models.magneticDebye({frequencyHz:x/(2*Math.PI*1e-6)});
  const low=point(.1),peak=point(1),high=point(10);
  near(low.cycleEnergyJpm3,high.cycleEnergyJpm3);
  assert.ok(peak.cycleEnergyJpm3>high.cycleEnergyJpm3);
  assert.ok(low.powerWpm3<peak.powerWpm3&&peak.powerWpm3<high.powerWpm3);
  near(models.magneticDebye({fieldPeakApm:0}).powerWpm3,0);
  assert.throws(()=>models.magneticDebye({tauS:0}),RangeError);
  assert.throws(()=>models.magneticDebye({fieldPeakApm:Infinity}),RangeError);
});
await check('N2 closed form agrees with independent coupled thermal ODE integration',()=>{
  for(const sensorTauS of [10,200,400]) {
    const p={heatCapacityJpK:4,powerW:.2,conductanceWpK:.02,sensorTauS,timeS:60};
    let theta=0,y=0;const dt=p.timeS/30000;
    const f=(a,b)=>[(p.powerW-p.conductanceWpK*a)/p.heatCapacityJpK,(a-b)/p.sensorTauS];
    for(let i=0;i<30000;i++) {
      const k1=f(theta,y),k2=f(theta+dt*k1[0]/2,y+dt*k1[1]/2),k3=f(theta+dt*k2[0]/2,y+dt*k2[1]/2),k4=f(theta+dt*k3[0],y+dt*k3[1]);
      theta+=dt*(k1[0]+2*k2[0]+2*k3[0]+k4[0])/6;y+=dt*(k1[1]+2*k2[1]+2*k3[1]+k4[1])/6;
    }
    const actual=models.thermalReadout(p);near(actual.temperatureRiseK,theta);near(actual.sensorRiseK,y);
    assert.ok(actual.apparentPowerW<p.powerW);
  }
});
await check('N2 scaling ambiguity and limiting cases remain explicit',()=>{
  const baseline=models.thermalReadout(),scaled=models.thermalReadout({heatCapacityJpK:8,powerW:.4,conductanceWpK:.04});
  near(scaled.sensorRiseK,baseline.sensorRiseK);near(scaled.temperatureRiseK,baseline.temperatureRiseK);near(scaled.apparentPowerW,2*baseline.apparentPowerW);
  const noLoss=models.thermalReadout({conductanceWpK:0,sensorTauS:0});near(noLoss.temperatureRiseK,3);near(noLoss.sensorRiseK,3);near(noLoss.apparentPowerW,.2);
  const initial=models.thermalReadout({timeS:0});assert.equal(initial.sensorRiseK,0);assert.equal(initial.apparentPowerW,null);
  near(models.thermalReadout({sensorTauS:200.000001}).sensorRiseK,models.thermalReadout({sensorTauS:200}).sensorRiseK,1e-7);
});
await check('Channel conversion compares units without equating mechanisms',()=>{
  const c=models.frequencyChannels();near(c.audioPeriodS,1/220);near(c.magneticPeriodS,1e-5);near(c.opticalHz,599584916000000);near(c.opticalPeriodS*c.opticalHz,1);
  assert.throws(()=>models.frequencyChannels({opticalNm:0}),RangeError);
});

const {Window}=await import(process.env.HAPPY_DOM_MODULE?pathToFileURL(process.env.HAPPY_DOM_MODULE).href:'happy-dom');
const liveData=JSON.parse(readFileSync(path.join(root,'data/research.json'),'utf8'));
const fixture=structuredClone(liveData);
await check('Live dataset exposes all five nanoparticle rounds, artifacts and scoped graph',async()=>{
  assert.equal(liveData.rounds.length,6,'Original six rounds changed');
  assert.equal(liveData.nanoparticles.rounds.length,5,'Five additional rounds required');
  const live=new Window({url:'https://example.test/resonance-research-atlas/',settings:{disableJavaScriptFileLoading:true,disableCSSFileLoading:true}});
  live.fetch=async()=>new live.Response(JSON.stringify(liveData),{status:200});live.HTMLElement.prototype.scrollIntoView=()=>{};Object.assign(live,models);
  live.document.write(readFileSync(path.join(root,'index.html'),'utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,''));
  live.eval(`(() => {\n${readFileSync(path.join(root,'app.js'),'utf8').replace(/^import[^\n]+\n/,'')}\n})();`);
  await new Promise(resolve=>setTimeout(resolve,20));
  const route=hash=>{live.location.hash=hash;live.dispatchEvent(new live.HashChangeEvent('hashchange'));};
  try {
    assert.match(live.document.querySelector('.nano-overview-card').textContent,/05/);
    route('nanoparticles');assert.equal(live.document.querySelectorAll('[data-nano-round]').length,5);
    const plateCount=liveData.nanoparticles.labCards.flatMap(c=>c.artifacts||[]).filter(a=>/\.(svg|png|webp|jpg)(\?|$)/i.test(a.url||'')).length;
    assert.equal(live.document.querySelectorAll('.nano-single-plate').length,plateCount,'Plate gallery does not match source artifacts');
    assert.equal(plateCount,6,'Six historical measurement plates required');
    for(const round of liveData.nanoparticles.rounds) {
      const tab=live.document.querySelector(`[data-nano-round="${round.id}"]`);tab.dispatchEvent(new live.MouseEvent('click',{bubbles:true}));
      const detail=live.document.querySelector('#nano-round-content');assert.ok(detail.textContent.includes(round.status));
      for(const artifact of round.artifacts||[])assert.ok([...detail.querySelectorAll('a')].some(a=>a.getAttribute('href')===artifact.url),`Missing ${round.id} artifact ${artifact.label}`);
    }
    route('network?scope=nanoparticles');for(const id of ['N1','N2','N3','N4','N5'])assert.ok(live.document.querySelector(`[data-node="${id}"]`),`Scoped graph omitted ${id}`);
    assert.ok(live.document.querySelectorAll('.data-table tbody tr').length>5);
  } finally {await live.happyDOM.close();}
});
const originalRoundIds=fixture.rounds.map(r=>r.id);
fixture.nanoparticles={summary:'Synthetic UI fixture',rounds:Array.from({length:5},(_,i)=>({id:`N${i+1}`,title:`Nanoparticle fixture ${i+1}`,status:i===0?'Executed; independent review recorded':'Planned',question:'Which observation separates the mechanisms?',hypothesis:'A testable fixture claim',rivals:['A calibrated rival'],falsifiers:['A held-out mismatch'],method:'Synthetic fixture only',limitations:['No material data'],findings:i===0?['A model-specific fixture result']:[],sourceIds:[],artifacts:[{label:'Frozen contract',url:`research/nanoparticles/N${i+1}/contract.md`}]})),roadmap:[],models:[],labCards:[{id:'bench',title:'Proposed inert bench',kind:'hardware-proposal',status:'Proposed',summary:'No apparatus was built.'}]};
const window=new Window({url:'https://example.test/resonance-research-atlas/',settings:{disableJavaScriptFileLoading:true,disableCSSFileLoading:true}});
const requests=[],downloads=[],blobs=[];
window.fetch=async url=>{requests.push(String(url));return new window.Response(JSON.stringify(fixture),{status:200});};
window.URL.createObjectURL=blob=>{blobs.push(blob);return `blob:nano-test-${blobs.length}`;};window.URL.revokeObjectURL=()=>{};
window.HTMLAnchorElement.prototype.click=function(){downloads.push(this.download);};window.HTMLElement.prototype.scrollIntoView=()=>{};
Object.assign(window,models);
window.document.write(readFileSync(path.join(root,'index.html'),'utf8').replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,''));
const script=readFileSync(path.join(root,'app.js'),'utf8').replace(/^import[^\n]+\n/,'');
window.eval(`(() => {\n${script}\n})();`);await new Promise(resolve=>setTimeout(resolve,20));
const $=q=>window.document.querySelector(q),go=hash=>{window.location.hash=hash;window.dispatchEvent(new window.HashChangeEvent('hashchange'));};
const click=q=>{const el=$(q);assert.ok(el,`Missing ${q}`);el.dispatchEvent(new window.MouseEvent('click',{bubbles:true,cancelable:true}));};
const input=(q,value)=>{const el=$(q);assert.ok(el,`Missing ${q}`);el.value=value;el.dispatchEvent(new window.Event('input',{bubbles:true}));};
try {
  await check('Dedicated view preserves original rounds and separates fixture execution from plans',()=>{
    go('nanoparticles');assert.ok($('#nano-model'));assert.equal(window.document.querySelectorAll('[data-nano-round]').length,5);
    assert.match($('#nano-round-content').textContent,/Executed/);click('[data-nano-round="N5"]');assert.match($('#nano-round-content').textContent,/Planned/);assert.match($('#nano-round-content').textContent,/What would falsify/);
    assert.ok($('#nano-round-content a[href="research/nanoparticles/N5/contract.md"]'));
    assert.match($('#main').textContent,/PROPOSED HARDWARE STUDY/);
    go('panel');assert.equal(window.document.querySelectorAll('.round-card').length,originalRoundIds.length);go('dreams');assert.ok($('#dream-journal-form'));go('nanoparticles');
  });
  await check('N1 rejects invalid controls and exports an auditable SI-unit snapshot',async()=>{
    assert.match($('#nano-cycle-value').textContent,/39\.48/);assert.match($('#nano-power-value').textContent,/6\.283/);
    input('#nano-field','');assert.equal($('#nano-power-value').textContent,'—');assert.ok($('[data-export-nano]').disabled);assert.equal($('#nano-chart').textContent,'');
    click('[data-reset-nano]');input('#nano-field','0');assert.equal($('#nano-power-value').textContent,'0');click('[data-reset-nano]');click('[data-export-nano]');
    assert.equal(downloads.at(-1),'nanoparticle-debye-model.json');const snapshot=JSON.parse(await blobs.at(-1).text());assert.equal(snapshot.parameters.fieldPeakApm,1);assert.match(snapshot.units.fieldPeakApm,/peak A\/m/);assert.match(snapshot.scope,/not fitted/);
  });
  await check('N2 scale control leaves the trace fixed and changes the inferred power scale',()=>{
    click('[data-nano-model="thermal"]');const before=$('#nano-sensor-value').textContent;const estimate=Number($('#nano-apparent-value').textContent);
    click('[data-scale-nano-thermal]');assert.equal($('#nano-sensor-value').textContent,before);near(Number($('#nano-apparent-value').textContent),2*estimate,.001);
    input('#nano-read-time','0');assert.equal($('#nano-apparent-value').textContent,'—');assert.ok($('#nano-thermal-error').textContent);click('[data-reset-nano-thermal]');assert.notEqual($('#nano-apparent-value').textContent,'—');
  });
  await check('Audio link and channel table retain modality boundaries without new requests',()=>{
    assert.ok($(`a[href="https://occult-kranti.github.io/brainwave_opensync/nano-lab/"]`));assert.match($('#nano-channels').textContent,/No absorption/);
    input('#channel-optical','0');assert.equal($('#channel-optical-frequency').textContent,'—');assert.ok($('#nano-channel-error').textContent);
    assert.deepEqual(requests,['./data/research.json']);
  });
}finally{await window.happyDOM.close();}
console.log(`${passed} nanoparticle model/UI gates passed. Numerical models and DOM fixtures do not validate hardware, material properties, clinical effects or visual browser layout.`);
