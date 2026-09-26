/** Bounded audio analogues for the nanoparticle measurement research branch.
 * Existing deterministic engine functions are composed, never modified.
 * The output is a digital audio waveform; no acoustic or magnetic calibration.
 */
import { dbToLin, renderBinaural, renderMonaural } from '@/engine/synth';
import { encodeWav } from '@/engine/wav';
import { hannWindow, magnitudeSpectrum } from '@/dsp/fft';

export type NanoSignalKind = 'two-tone' | 'am' | 'baseband' | 'carrier';
export interface NanoRecipe { kind: NanoSignalKind; carrierHz: number; rateHz: number; durationSec: number; gainDb: number }
export interface SpectralLine { hz: number; amplitude: number; label: string }
export interface NanoSpectrum { fftSize: number; binHz: number; observationSec: number; points: { hz: number; dbFs: number }[]; strongestBins: { hz: number; dbFs: number }[] }
export interface NanoRender { recipe: NanoRecipe; left: Float32Array; right: Float32Array; sampleRate: number; samplePeak: number; peakDbFs: number; rmsDbFs: number; spectrum: NanoSpectrum; predictedLines: SpectralLine[] }

export const NANO_SAMPLE_RATE = 48000;
export const NANO_FADE_SEC = .05;
export const NANO_KINDS: readonly NanoSignalKind[] = ['two-tone', 'am', 'baseband', 'carrier'];
export const DEFAULT_NANO_RECIPE: NanoRecipe = { kind: 'two-tone', carrierHz: 400, rateHz: 16, durationSec: 10, gainDb: -24 };
export const NANO_LABELS: Record<NanoSignalKind, string> = { 'two-tone': 'Two-tone sum', am: 'Amplitude modulation', baseband: 'Actual baseband tone', carrier: 'Carrier-only control' };

function range(value: unknown, name: string, min: number, max: number): number {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < min || value > max) throw new RangeError(`${name} must be between ${min} and ${max}.`);
  return value;
}
export function validateNanoRecipe(input: unknown): NanoRecipe {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw new TypeError('A signal recipe must be an object.');
  const x = input as Record<string, unknown>;
  if (!NANO_KINDS.includes(x.kind as NanoSignalKind)) throw new RangeError('Choose a supported signal kind.');
  const recipe: NanoRecipe = { kind: x.kind as NanoSignalKind, carrierHz: range(x.carrierHz, 'Carrier Hz', 80, 1000), rateHz: range(x.rateHz, 'Rate Hz', 1, 80), durationSec: range(x.durationSec, 'Duration seconds', 2, 30), gainDb: range(x.gainDb, 'Master gain dBFS', -60, -18) };
  const { kind, carrierHz: fc, rateHz: rate } = recipe;
  const low = kind === 'am' ? fc - rate : kind === 'two-tone' ? fc - rate / 2 : kind === 'baseband' ? rate : fc;
  const high = kind === 'am' ? fc + rate : kind === 'two-tone' ? fc + rate / 2 : low;
  if (low <= 0 || high >= NANO_SAMPLE_RATE / 2) throw new RangeError('Active tones and sidebands must be positive and below Nyquist.');
  return recipe;
}

export function predictedNanoLines(input: NanoRecipe): SpectralLine[] {
  const r = validateNanoRecipe(input), g = dbToLin(r.gainDb);
  if (r.kind === 'two-tone') return [{ hz: r.carrierHz - r.rateHz / 2, amplitude: g / 2, label: 'Lower tone' }, { hz: r.carrierHz + r.rateHz / 2, amplitude: g / 2, label: 'Upper tone' }];
  if (r.kind === 'am') return [{ hz: r.carrierHz - r.rateHz, amplitude: g / 4, label: 'Lower sideband' }, { hz: r.carrierHz, amplitude: g / 2, label: 'Carrier' }, { hz: r.carrierHz + r.rateHz, amplitude: g / 4, label: 'Upper sideband' }];
  return [{ hz: r.kind === 'baseband' ? r.rateHz : r.carrierHz, amplitude: g, label: r.kind === 'baseband' ? 'Baseband' : 'Carrier' }];
}

/** Hann spectrum of a centered, unfaded segment. Bin amplitudes include
 * coherent-gain correction; off-bin leakage still spreads a sinusoidal line.
 */
export function inspectNanoSpectrum(samples: Float32Array): NanoSpectrum {
  const available = samples.length - Math.ceil(2 * NANO_FADE_SEC * NANO_SAMPLE_RATE);
  if (available < 1024 || samples.length > 30 * NANO_SAMPLE_RATE) throw new RangeError('Unsupported analysis length.');
  let fftSize = 1024;
  while (fftSize * 2 <= Math.min(available, 131072)) fftSize *= 2;
  const offset = Math.floor((samples.length - fftSize) / 2);
  const window = hannWindow(fftSize, true), input = new Float32Array(fftSize);
  let windowSum = 0;
  for (let i = 0; i < fftSize; i++) { input[i] = samples[offset + i] * window[i]; windowSum += window[i]; }
  const magnitudes = magnitudeSpectrum(input), correction = fftSize / windowSum, binHz = NANO_SAMPLE_RATE / fftSize;
  const point = (k: number) => ({ hz: k * binHz, dbFs: 20 * Math.log10(Math.max(1e-8, magnitudes[k] * correction)) });
  const last = Math.min(magnitudes.length - 1, Math.ceil(1200 / binHz));
  const points = Array.from({ length: last + 1 }, (_, k) => point(k));
  const peaks = points.filter((p, i) => i > 0 && i < points.length - 1 && p.dbFs > points[i - 1].dbFs && p.dbFs >= points[i + 1].dbFs);
  const strongestBins = peaks.sort((a, b) => b.dbFs - a.dbFs).slice(0, 5);
  return { fftSize, binHz, observationSec: fftSize / NANO_SAMPLE_RATE, points, strongestBins };
}

export function renderNanoSignal(input: NanoRecipe): NanoRender {
  const recipe = validateNanoRecipe(input);
  const { kind, carrierHz, rateHz, durationSec, gainDb } = recipe;
  const phase = { durationSec, carrierHz: kind === 'baseband' ? rateHz : kind === 'two-tone' ? carrierHz - rateHz / 2 : carrierHz, beatHz: kind === 'two-tone' || kind === 'am' ? rateHz : 0, mode: 'monaural' as const, gainDb: 0 };
  // renderBinaural is a two-sinusoid helper here; summing to identical L/R
  // produces physical superposition, not a dichotic binaural presentation.
  const raw = kind === 'am' ? renderMonaural(phase, NANO_SAMPLE_RATE) : renderBinaural(phase, NANO_SAMPLE_RATE);
  const gain = dbToLin(gainDb), fade = Math.round(NANO_FADE_SEC * NANO_SAMPLE_RATE);
  let samplePeak = 0, squareSum = 0;
  for (let i = 0; i < raw.left.length; i++) {
    const edge = Math.min(1, i / fade, (raw.left.length - 1 - i) / fade);
    const envelope = .5 - .5 * Math.cos(Math.PI * edge);
    const x = (kind === 'two-tone' ? (raw.left[i] + raw.right[i]) / 2 : raw.left[i]) * gain * envelope;
    raw.left[i] = x; raw.right[i] = x;
    samplePeak = Math.max(samplePeak, Math.abs(raw.left[i])); squareSum += raw.left[i] ** 2;
  }
  return { recipe, left: raw.left, right: raw.right, sampleRate: NANO_SAMPLE_RATE, samplePeak, peakDbFs: 20 * Math.log10(Math.max(samplePeak, 1e-15)), rmsDbFs: 10 * Math.log10(Math.max(squareSum / raw.left.length, 1e-30)), spectrum: inspectNanoSpectrum(raw.left), predictedLines: predictedNanoLines(recipe) };
}

export function nanoManifest(rendered: NanoRender) {
  return { format: 'opensync-nano-audio', version: 1, renderer: 'nanolab-v1', recipe: rendered.recipe, units: { samples: 'dimensionless digital full-scale amplitude', frequency: 'Hz', gain: 'dBFS sample-amplitude ceiling' }, sampleRateHz: rendered.sampleRate, nyquistHz: rendered.sampleRate / 2, framesPerChannel: rendered.left.length, actualDurationSec: rendered.left.length / rendered.sampleRate, channels: 'identical L/R (diotic)', masterGainDb: rendered.recipe.gainDb, samplePeakDbFs: rendered.peakDbFs, rmsDbFs: rendered.rmsDbFs, edgeFadeSec: NANO_FADE_SEC, wavEncoding: 'PCM16 stereo', predictedLinesBeforeEdgeFades: rendered.predictedLines, analysis: { window: 'periodic Hann, centered segment, coherent-gain corrected', fftSize: rendered.spectrum.fftSize, binSpacingHz: rendered.spectrum.binHz, observationSec: rendered.spectrum.observationSec, strongestBins: rendered.spectrum.strongestBins, warning: 'Window leakage broadens lines. FFT bins are not exact component frequencies or reconstructed true peaks.' }, physicalCalibration: null, scope: 'Digital audio/acoustic analogy only. No magnetic field, optical exposure, nanoparticle response, dose or treatment is specified.', source: { synthesis: 'src/engine/synth.ts', adapter: 'src/nanolab/model.ts', encoder: 'src/engine/wav.ts' } };
}

export async function exportNanoSignal(rendered: NanoRender): Promise<{ wav: Uint8Array; manifest: Uint8Array }> {
  const wav = encodeWav(rendered.left, rendered.right, rendered.sampleRate, 'pcm16');
  const digest = await crypto.subtle.digest('SHA-256', wav.buffer.slice(wav.byteOffset, wav.byteOffset + wav.byteLength) as ArrayBuffer);
  const sha256 = Array.from(new Uint8Array(digest), byte => byte.toString(16).padStart(2, '0')).join('');
  return { wav, manifest: new TextEncoder().encode(JSON.stringify({ ...nanoManifest(rendered), wavBytes: wav.length, wavSha256: sha256 }, null, 2) + '\n') };
}
