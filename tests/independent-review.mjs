#!/usr/bin/env node
/** Independent limits, physical balance, exact probability and provenance gates.
 * Run: node tests/independent-review.mjs
 * Uses analytic counterexamples and integer enumeration, not implementation snapshots.
 */
import assert from 'node:assert/strict';
import {readFileSync, existsSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {schumannIdeal, oscillator, spectralResolution, binomialUpperTail} from '../models.js';

const root = fileURLToPath(new URL('../', import.meta.url));
const data = JSON.parse(readFileSync(path.join(root, 'data/research.json'), 'utf8'));
const near = (actual, expected, relative = 1e-11, label = '') => assert.ok(Math.abs(actual - expected) <= relative * Math.max(Math.abs(expected), 1e-15), `${label}: ${actual} != ${expected}`);
let passed = 0;
const check = (name, fn) => {fn(); console.log(`PASS ${name}`); passed++;};

check('Thin-shell radius and angular-mode scaling; invalid/overflow bounds', () => {
  near(schumannIdeal(), 10.591, .0001, 'Earth ideal mode');
  near(schumannIdeal(12742), schumannIdeal()/2);
  near(schumannIdeal(6371, 2)/schumannIdeal(), Math.sqrt(3));
  for(const input of [0,-1,NaN,Infinity,Number.MIN_VALUE,Number.MAX_VALUE]) assert.throws(()=>schumannIdeal(input), RangeError);
  for(const mode of [0,1.5,9]) assert.throws(()=>schumannIdeal(6371,mode), RangeError);
});

check('Oscillator static limit stores full constant-displacement potential energy', () => {
  const r=oscillator({naturalHz:1/Math.PI,driveHz:0,quality:3,massKg:2,forceN:8});
  near(r.amplitudeM,1); near(r.stiffness,8); near(r.meanEnergyJ,4);
  assert.equal(r.averagePowerW,0); assert.equal(r.phaseRad,0);
});

check('Oscillator power and stored energy agree with independent cycle quadrature', () => {
  for(const driveHz of [.2,4,8,12,60]) {
    const spec={naturalHz:8,driveHz,quality:3.2,massKg:.7,forceN:.15};
    const r=oscillator(spec);let energy=0,input=0,loss=0;
    const n=8192,omega=2*Math.PI*driveHz;
    for(let i=0;i<n;i++) {
      const angle=2*Math.PI*(i+.5)/n;
      const x=r.amplitudeM*Math.cos(angle-r.phaseRad);
      const v=-r.amplitudeM*omega*Math.sin(angle-r.phaseRad);
      energy+=(spec.massKg*v*v/2+r.stiffness*x*x/2)/n;
      input+=spec.forceN*Math.cos(angle)*v/n;
      loss+=r.damping*v*v/n;
    }
    near(r.meanEnergyJ,energy);near(r.averagePowerW,input,1e-10);near(input,loss,1e-10);
  }
  const r=oscillator({forceN:0});assert.equal(r.amplitudeM,0);assert.equal(r.meanEnergyJ,0);assert.equal(r.averagePowerW,0);
  near(oscillator().gain,5);near(oscillator().phaseRad,Math.PI/2);
  assert.throws(()=>oscillator({naturalHz:Number.MAX_VALUE}),RangeError);
  assert.throws(()=>oscillator({quality:0}),RangeError);
});

check('DFT spacing agrees with the actual integer sample count', () => {
  const r=spectralResolution(256,1.003);
  assert.equal(r.samples,256);near(r.binSpacingHz,1);near(r.effectiveDurationS,1);
  near(r.binSpacingHz*r.samples,256);
  for(const pair of [[1,.01],[1000,.001],[0,1],[256,Infinity],[1e20,100]])assert.throws(()=>spectralResolution(...pair),RangeError);
});

check('Binomial tails match exact integer enumeration of all 4-category outcomes', () => {
  for(const n of [1,2,4,10,20,50]) {
    const denominator=4n**BigInt(n);
    let choose=1n;const terms=[];
    for(let k=0;k<=n;k++) {
      terms.push(choose*3n**BigInt(n-k));
      if(k<n)choose=choose*BigInt(n-k)/BigInt(k+1);
    }
    let tail=0n;
    for(let k=n;k>=0;k--) {tail+=terms[k];near(binomialUpperTail(n,k),Number(tail)/Number(denominator),2e-12,`n=${n},k=${k}`);}
  }
  near(binomialUpperTail(10000,5000,.5)+binomialUpperTail(10000,5001,.5),1,1e-9);
  assert.equal(binomialUpperTail(10000,0),1);
  // Zero is floating-point underflow for this case, never a mathematical impossibility.
  assert.equal(binomialUpperTail(10000,10000),0);
  for(const args of [[0,0],[10,11],[10,-1],[10,1.1],[10001,2],[10,2,1]])assert.throws(()=>binomialUpperTail(...args),RangeError);
});

check('Every source, graph endpoint, citation and roadmap dependency resolves', () => {
  for(const group of ['sources','experiments','history','rounds','roadmap']) {
    const ids=data[group].map(x=>x.id);assert.equal(new Set(ids).size,ids.length,`${group} duplicate IDs`);
  }
  const sources=new Set(data.sources.map(s=>s.id)),nodes=new Set(data.network.nodes.map(n=>n.id));
  assert.equal(nodes.size,data.network.nodes.length);
  for(const source of data.sources) {
    assert.match(source.url,/^https:\/\//,source.id);
    assert.ok(source.readingDepth && source.limitations,`${source.id} missing reading scope/limit`);
  }
  for(const group of [data.experiments,data.history,data.network.nodes,data.network.edges])for(const row of group)for(const id of row.sourceIds||[])assert.ok(sources.has(id),`Unknown citation ${id}`);
  for(const edge of data.network.edges) {
    assert.ok(nodes.has(edge.source)&&nodes.has(edge.target),'Unknown graph endpoint');
    assert.ok(edge.type && edge.label,'Unlabeled graph relationship');
  }
  const tasks=new Map(data.roadmap.map(r=>[r.id,r]));
  function visit(id,stack=new Set()) {assert.ok(tasks.has(id),`Unknown dependency ${id}`);assert.ok(!stack.has(id),'Roadmap dependency cycle');for(const dep of tasks.get(id).dependsOn||[])visit(dep,new Set([...stack,id]));}
  for(const id of tasks.keys())visit(id);
});

check('Executed/reviewed rounds have actual local outputs, with all six statuses visible', () => {
  assert.deepEqual(data.rounds.map(r=>r.id),['R1','R2','R3','R4','R5','R6']);
  for(const round of data.rounds) {
    assert.ok(round.status,`No status for ${round.id}`);
    const folder=path.join(root,'research',`round${round.id.slice(1)}`);
    if(/executed/i.test(round.status))for(const f of ['contract.md','results.json','interpretation.md'])assert.ok(existsSync(path.join(folder,f)),`${round.id}: missing ${f}`);
    if(/independent review recorded/i.test(round.status))assert.ok(existsSync(path.join(folder,'independent-review.json')),`${round.id}: review missing`);
  }
  for(const e of data.experiments)for(const a of e.artifacts||[]) {
    const url=a.url||a.path;if(url&&!/^(https?:|#|projects\/)/.test(url))assert.ok(existsSync(path.resolve(root,url)),`${e.id}: artifact missing ${url}`);
  }
});

console.log(`${passed} independent review gates passed. Source content truth and clinical efficacy are not inferred by these checks.`);
