/**
 * Pure, unit-explicit educational models. No biological efficacy is inferred.
 * UI data contract for ./data/research.json (every collection is optional):
 * meta: {title, subtitle, updated, status}
 * experiments: [{id,title,domain,status,evidence,summary,question,method,
 *   prediction,limitations,safety,sourceIds:[],modelId}]
 * sources: [{id,title,author,year,url,type,evidence,summary,claim}]
 * history: [{id,title,person,summary,evidence,sourceIds:[]}]
 * rounds: [{id,title,status,participants:[],question,findings:[],decisions:[],next:[]}]
 * roadmap: [{id,title,status,owner,dependsOn:[],detail}]
 * network: {nodes:[{id,label,type,summary,sourceIds:[]}],
 *   edges:[{source,target,type,label,sourceIds:[]}]}
 * projects: [{name,url,role,status}]
 * evidence: established | documented | preliminary | hypothesis | unsupported
 */
export const LIGHT_SPEED = 299792458;

function positive(value, name) {
  if (!Number.isFinite(value) || value <= 0) throw new RangeError(`${name} must be greater than zero.`);
  return value;
}

export function schumannIdeal(radiusKm = 6371, mode = 1) {
  positive(radiusKm, 'Radius');
  if (!Number.isInteger(mode) || mode < 1 || mode > 8) throw new RangeError('Mode must be an integer from 1 to 8.');
  const frequency = LIGHT_SPEED / (2 * Math.PI * radiusKm * 1000) * Math.sqrt(mode * (mode + 1));
  if (!Number.isFinite(frequency) || frequency <= 0) throw new RangeError('Radius is outside the supported numerical range.');
  return frequency;
}

export function oscillator({naturalHz = 10, driveHz = 10, quality = 5, massKg = 1, forceN = 1} = {}) {
  positive(naturalHz, 'Natural frequency'); positive(quality, 'Quality factor'); positive(massKg, 'Mass');
  if (!Number.isFinite(driveHz) || driveHz < 0 || !Number.isFinite(forceN) || forceN < 0) throw new RangeError('Drive frequency and force must be nonnegative.');
  const omega0 = 2 * Math.PI * naturalHz;
  const omega = 2 * Math.PI * driveHz;
  const stiffness = massKg * omega0 ** 2;
  const damping = massKg * omega0 / quality;
  const denominator = Math.hypot(stiffness - massKg * omega ** 2, damping * omega);
  const amplitudeM = forceN / denominator;
  const averagePowerW = damping * omega ** 2 * amplitudeM ** 2 / 2;
  const meanEnergyJ = driveHz === 0 ? stiffness * amplitudeM ** 2 / 2 : (massKg * omega ** 2 + stiffness) * amplitudeM ** 2 / 4;
  const result = {amplitudeM, averagePowerW, meanEnergyJ, stiffness, damping,
    gain: stiffness / denominator, phaseRad: Math.atan2(damping * omega, stiffness - massKg * omega ** 2)};
  if (Object.values(result).some(value => !Number.isFinite(value)) || stiffness <= 0 || damping <= 0) throw new RangeError('Parameters are outside the supported numerical range.');
  return result;
}

export function spectralResolution(sampleRateHz, durationS) {
  positive(sampleRateHz, 'Sample rate'); positive(durationS, 'Duration');
  const samples = Math.floor(sampleRateHz * durationS);
  if (!Number.isSafeInteger(samples) || samples < 2) throw new RangeError('The recording must contain at least two samples and a safe integer sample count.');
  const effectiveDurationS = samples / sampleRateHz;
  return {nyquistHz: sampleRateHz / 2, binSpacingHz: sampleRateHz / samples,
    samples, effectiveDurationS};
}

/** Exact finite-binomial upper tail, evaluated with stable log probabilities.
 * It assumes independent fixed-count trials with a prespecified chance rate.
 * A probability from user-entered counts does not authenticate the study.
 */
export function binomialUpperTail(trials, hits, chance = .25) {
  if (!Number.isInteger(trials) || trials < 1 || trials > 10000) throw new RangeError('Trials must be an integer from 1 to 10,000.');
  if (!Number.isInteger(hits) || hits < 0 || hits > trials) throw new RangeError('Hits must be an integer between zero and the trial count.');
  if (!Number.isFinite(chance) || chance <= 0 || chance >= 1) throw new RangeError('Chance must be strictly between zero and one.');
  if(hits === 0) return 1;
  let logChoose = 0;
  for(let i = 1; i <= hits; i++) logChoose += Math.log(trials - i + 1) - Math.log(i);
  let logTerm = logChoose + hits * Math.log(chance) + (trials - hits) * Math.log1p(-chance);
  const logs = [logTerm];
  for(let k = hits; k < trials; k++) {
    logTerm += Math.log(trials - k) - Math.log(k + 1) + Math.log(chance) - Math.log1p(-chance);
    logs.push(logTerm);
  }
  const maxLog = Math.max(...logs);
  return Math.min(1, Math.exp(maxLog + Math.log(logs.reduce((sum,l) => sum + Math.exp(l-maxLog), 0))));
}
