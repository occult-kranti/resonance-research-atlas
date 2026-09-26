// src/engine/bowls.ts
var legacyAmps = (count) => Array.from({ length: count }, (_, i) => 1 / (1 + 1.2 * i));
var BOWL_MATERIALS = [
  {
    id: "tibetan-bronze",
    label: "Tibetan bronze",
    ratios: [1, 2.76, 5.4],
    amps: legacyAmps(3),
    decaySec: 6,
    fmDepth: 2e-3,
    fmHz: 1.1,
    doublet: 0,
    blurb: "The original Open Sync bowl: three inharmonic partials, medium ring-down."
  },
  {
    id: "himalayan-antique",
    label: "Himalayan antique",
    ratios: [1, 2.63, 4.91, 7.86],
    amps: [1, 0.55, 0.22, 0.09],
    decaySec: 9,
    fmDepth: 35e-4,
    fmHz: 0.65,
    doublet: 4e-3,
    blurb: "Thick hand-hammered alloy model: slow beating between split modes, long warm ring."
  },
  {
    id: "bell-bronze",
    label: "Bell bronze",
    ratios: [1, 2.71, 5.15, 8.42, 12.1],
    amps: [1, 0.62, 0.38, 0.2, 0.1],
    decaySec: 7.5,
    fmDepth: 25e-4,
    fmHz: 1.4,
    doublet: 15e-4,
    blurb: "Machine-cast B20 bronze model: bright, five clear partials, bell-like attack."
  },
  {
    id: "brass",
    label: "Brass",
    ratios: [1, 2.94, 5.72, 9.12],
    amps: [1, 0.7, 0.4, 0.18],
    decaySec: 3.5,
    fmDepth: 3e-3,
    fmHz: 1.7,
    doublet: 2e-3,
    blurb: "Thin brass model: louder upper partials and a shorter, more percussive decay."
  },
  {
    id: "crystal-quartz",
    label: "Crystal quartz",
    ratios: [1, 2.42, 4.17],
    amps: [1, 0.22, 0.06],
    decaySec: 14,
    fmDepth: 6e-4,
    fmHz: 0.35,
    doublet: 8e-4,
    blurb: "Frosted quartz model: near-pure fundamental, very long sustain, little shimmer."
  }
];
var BOWL_STRIKES = [
  { id: "mallet", label: "Mallet", weights: [1], attackSec: 0, sustained: false, blurb: "Plain strike: every partial speaks at once." },
  {
    id: "soft",
    label: "Soft mallet",
    weights: [1, 0.42, 0.22, 0.13, 0.08],
    attackSec: 0.012,
    sustained: false,
    blurb: "Padded mallet: fewer highs and a 12 ms bloom instead of a click."
  },
  {
    id: "rim",
    label: "Rim (singing)",
    weights: [1, 0.3, 0.12, 0.05, 0.03],
    attackSec: 0,
    sustained: true,
    blurb: "Rubbed rim: the bowl sings continuously, swelling in and releasing before each new pass."
  }
];
var BOWL_MATERIAL_IDS = BOWL_MATERIALS.map((m) => m.id);
var BOWL_STRIKE_IDS = BOWL_STRIKES.map((s) => s.id);
var NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
function noteToHz(midi) {
  return 440 * Math.pow(2, (midi - 69) / 12);
}
function noteMidi(name, octave) {
  return (octave + 1) * 12 + NOTE_NAMES.indexOf(name);
}
var BOWL_NOTE_CHOICES = (() => {
  const out = [];
  for (let midi = noteMidi("C", 2); midi <= noteMidi("B", 5); midi++) {
    const hz2 = noteToHz(midi);
    out.push({ label: `${NOTE_NAMES[midi % 12]}${Math.floor(midi / 12) - 1}`, hz: Math.round(hz2 * 100) / 100 });
  }
  return out;
})();
var hz = (name, octave) => Math.round(noteToHz(noteMidi(name, octave)) * 100) / 100;
var BOWL_SETS = [
  {
    id: "himalayan-trio",
    name: "Himalayan trio",
    blurb: "Three antique-style bowls a fifth and an octave apart, struck on staggered intervals.",
    bowls: [
      { material: "himalayan-antique", strike: "mallet", baseHz: 136.1, db: -24, pan: -0.45, restrikeSec: 12 },
      { material: "himalayan-antique", strike: "soft", baseHz: 204.15, db: -28, pan: 0.45, restrikeSec: 16 },
      { material: "tibetan-bronze", strike: "soft", baseHz: 272.2, db: -32, pan: 0, restrikeSec: 8 }
    ]
  },
  {
    id: "crystal-pair",
    name: "Crystal pair",
    blurb: "Two quartz bowls sung on the rim, C4 and G4, drifting slowly across the stereo field.",
    bowls: [
      { material: "crystal-quartz", strike: "rim", baseHz: hz("C", 4), db: -26, pan: -0.35, restrikeSec: 16 },
      { material: "crystal-quartz", strike: "rim", baseHz: hz("G", 4), db: -30, pan: 0.35, restrikeSec: 12 }
    ]
  },
  {
    id: "seven-note-set",
    name: "Seven-note set",
    blurb: 'A C-major seven-bowl set (C3 to B3), the layout sold as a "chakra set". The note-to-body mapping is folklore; the scale is real.',
    bowls: [
      { material: "himalayan-antique", strike: "mallet", baseHz: hz("C", 3), db: -26, pan: -0.6, restrikeSec: 16 },
      { material: "tibetan-bronze", strike: "mallet", baseHz: hz("D", 3), db: -28, pan: -0.4, restrikeSec: 12 },
      { material: "bell-bronze", strike: "soft", baseHz: hz("E", 3), db: -30, pan: -0.2, restrikeSec: 8 },
      { material: "himalayan-antique", strike: "soft", baseHz: hz("F", 3), db: -30, pan: 0, restrikeSec: 16 },
      { material: "tibetan-bronze", strike: "mallet", baseHz: hz("G", 3), db: -28, pan: 0.2, restrikeSec: 12 },
      { material: "bell-bronze", strike: "soft", baseHz: hz("A", 3), db: -30, pan: 0.4, restrikeSec: 8 },
      { material: "crystal-quartz", strike: "mallet", baseHz: hz("B", 3), db: -32, pan: 0.6, restrikeSec: 16 }
    ]
  },
  {
    id: "deep-drone",
    name: "Deep drone",
    blurb: "Two large bowls an octave apart, rim-sung, plus a brass accent every 12 s.",
    bowls: [
      { material: "himalayan-antique", strike: "rim", baseHz: hz("A", 2), db: -24, pan: -0.25, restrikeSec: 16 },
      { material: "crystal-quartz", strike: "rim", baseHz: hz("A", 3), db: -30, pan: 0.25, restrikeSec: 12 },
      { material: "brass", strike: "mallet", baseHz: hz("E", 4), db: -34, pan: 0.5, restrikeSec: 12 }
    ]
  },
  {
    id: "bright-bells",
    name: "Bright bells",
    blurb: "Bell bronze and brass at higher pitches for a glittering, faster-decaying texture.",
    bowls: [
      { material: "bell-bronze", strike: "mallet", baseHz: hz("E", 4), db: -28, pan: -0.5, restrikeSec: 8 },
      { material: "brass", strike: "mallet", baseHz: hz("B", 4), db: -32, pan: 0.5, restrikeSec: 12 },
      { material: "bell-bronze", strike: "soft", baseHz: hz("G#", 4), db: -30, pan: 0, restrikeSec: 16 }
    ]
  },
  {
    id: "golden-ratio-chord",
    name: "Golden-ratio chord",
    blurb: "Five bowls spaced by the golden ratio, 833 cents apart.",
    bowls: Array.from({ length: 5 }, (_, n) => ({
      material: "crystal-quartz",
      strike: "soft",
      baseHz: 110 * ((1 + Math.sqrt(5)) / 2) ** n,
      db: -26,
      pan: -0.6 + n * 0.3,
      restrikeSec: 12
    }))
  }
];

// src/engine/synth.ts
var TWO_PI = Math.PI * 2;
function dbToLin(db) {
  return Math.pow(10, db / 20);
}
function isFiniteNumber(x) {
  return typeof x === "number" && Number.isFinite(x);
}
function checkPhaseGuardrails(phase, sampleRate) {
  const warnings = [];
  const { carrierHz, beatHz, mode, durationSec, gainDb } = phase;
  if (!isFiniteNumber(durationSec) || durationSec < 0) {
    warnings.push(`phase durationSec=${String(durationSec)} is invalid; rendered as silence`);
  }
  if (!isFiniteNumber(carrierHz) || !isFiniteNumber(beatHz) || !isFiniteNumber(gainDb)) {
    warnings.push("phase contains NaN/Infinity parameter; rendered as silence");
    return warnings;
  }
  if (carrierHz < 0 || beatHz < 0) {
    warnings.push(`negative frequency (carrier=${carrierHz}, beat=${beatHz}); rendered as silence`);
    return warnings;
  }
  if (mode === "binaural") {
    if (carrierHz > 1e3) {
      warnings.push(
        `binaural carrier ${carrierHz} Hz > 1000 Hz: beat perception is weak above ~1 kHz`
      );
    }
    if (beatHz > 30) {
      warnings.push(
        `binaural beat ${beatHz} Hz > 30 Hz: not psychoacoustically perceivable as a beat`
      );
    }
  }
  const highest = mode === "binaural" ? carrierHz + beatHz : carrierHz;
  if (highest > sampleRate / 2) {
    warnings.push(`frequency ${highest} Hz exceeds Nyquist (${sampleRate / 2} Hz)`);
  }
  return warnings;
}
function phaseIsRenderable(phase) {
  return isFiniteNumber(phase.durationSec) && phase.durationSec >= 0 && isFiniteNumber(phase.carrierHz) && phase.carrierHz >= 0 && isFiniteNumber(phase.beatHz) && phase.beatHz >= 0 && isFiniteNumber(phase.gainDb);
}
function sampleCount(durationSec, sampleRate) {
  if (!isFiniteNumber(durationSec) || durationSec <= 0) return 0;
  return Math.round(durationSec * sampleRate);
}
function emptyResult(warnings) {
  return { left: new Float32Array(0), right: new Float32Array(0), warnings };
}
function silenceResult(n, warnings) {
  return { left: new Float32Array(n), right: new Float32Array(n), warnings };
}
function wrapPhase(p) {
  if (p >= TWO_PI || p < 0) return p % TWO_PI + (p < 0 ? TWO_PI : 0);
  return p;
}
function renderBinaural(phase, sampleRate, offsets = { left: 0, right: 0, beat: 0 }) {
  const warnings = checkPhaseGuardrails(phase, sampleRate);
  const n = sampleCount(phase.durationSec, sampleRate);
  if (n === 0) return { ...emptyResult(warnings), offsets };
  if (!phaseIsRenderable(phase)) return { ...silenceResult(n, warnings), offsets };
  const left = new Float32Array(n);
  const right = new Float32Array(n);
  const incL = TWO_PI * phase.carrierHz / sampleRate;
  const incR = TWO_PI * (phase.carrierHz + phase.beatHz) / sampleRate;
  let phL = offsets.left;
  let phR = offsets.right;
  for (let i = 0; i < n; i++) {
    left[i] = Math.sin(phL);
    right[i] = Math.sin(phR);
    phL = wrapPhase(phL + incL);
    phR = wrapPhase(phR + incR);
  }
  return { left, right, warnings, offsets: { left: phL, right: phR, beat: offsets.beat } };
}
function renderMonaural(phase, sampleRate, offsets = { left: 0, right: 0, beat: 0 }) {
  const warnings = checkPhaseGuardrails(phase, sampleRate);
  const n = sampleCount(phase.durationSec, sampleRate);
  if (n === 0) return { ...emptyResult(warnings), offsets };
  if (!phaseIsRenderable(phase)) return { ...silenceResult(n, warnings), offsets };
  const left = new Float32Array(n);
  const right = new Float32Array(n);
  const incC = TWO_PI * phase.carrierHz / sampleRate;
  const incB = TWO_PI * phase.beatHz / sampleRate;
  let phC = offsets.left;
  let phB = offsets.beat;
  for (let i = 0; i < n; i++) {
    const env = 0.5 + 0.5 * Math.sin(phB);
    const s = Math.sin(phC) * env;
    left[i] = s;
    right[i] = s;
    phC = wrapPhase(phC + incC);
    phB = wrapPhase(phB + incB);
  }
  return { left, right, warnings, offsets: { left: phC, right: phC, beat: phB } };
}

// src/engine/wav.ts
var RIFF_HEADER_BYTES = 44;
var MAX_RIFF_BYTES = 4294967295;
function wavFormatInfo(format) {
  switch (format) {
    case "pcm16":
      return { audioFormatTag: 1, bytesPerSample: 2, bitsPerSample: 16 };
    case "pcm24":
      return { audioFormatTag: 1, bytesPerSample: 3, bitsPerSample: 24 };
    case "float32":
      return { audioFormatTag: 3, bytesPerSample: 4, bitsPerSample: 32 };
  }
}
function wavDataBytes(frames, format) {
  return frames * 2 * wavFormatInfo(format).bytesPerSample;
}
function assertWavSizeWithinRiff(frames, format) {
  const total = RIFF_HEADER_BYTES + wavDataBytes(frames, format);
  if (total > MAX_RIFF_BYTES) {
    throw new RangeError(
      `WAV would be ${total} bytes (> 4 GiB RIFF limit) for ${frames} frames as ${format}; split the session or use a lower bit depth`
    );
  }
}
function clampSample(x) {
  if (Number.isNaN(x)) return 0;
  return x < -1 ? -1 : x > 1 ? 1 : x;
}
function encodeWav(left, right, sampleRate, format = "pcm16") {
  const frames = Math.min(left.length, right.length);
  assertWavSizeWithinRiff(frames, format);
  const info = wavFormatInfo(format);
  const dataBytes = wavDataBytes(frames, format);
  const out = new Uint8Array(RIFF_HEADER_BYTES + dataBytes);
  const view = new DataView(out.buffer);
  view.setUint8(0, 82);
  view.setUint8(1, 73);
  view.setUint8(2, 70);
  view.setUint8(3, 70);
  view.setUint32(4, 36 + dataBytes, true);
  view.setUint8(8, 87);
  view.setUint8(9, 65);
  view.setUint8(10, 86);
  view.setUint8(11, 69);
  view.setUint8(12, 102);
  view.setUint8(13, 109);
  view.setUint8(14, 116);
  view.setUint8(15, 32);
  view.setUint32(16, 16, true);
  view.setUint16(20, info.audioFormatTag, true);
  view.setUint16(22, 2, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * 2 * info.bytesPerSample, true);
  view.setUint16(32, 2 * info.bytesPerSample, true);
  view.setUint16(34, info.bitsPerSample, true);
  view.setUint8(36, 100);
  view.setUint8(37, 97);
  view.setUint8(38, 116);
  view.setUint8(39, 97);
  view.setUint32(40, dataBytes, true);
  let o = RIFF_HEADER_BYTES;
  for (let i = 0; i < frames; i++) {
    for (const x of [clampSample(left[i]), clampSample(right[i])]) {
      if (format === "pcm16") {
        const s = Math.round(x < 0 ? x * 32768 : x * 32767);
        view.setInt16(o, s, true);
        o += 2;
      } else if (format === "pcm24") {
        const s = Math.round(x < 0 ? x * 8388608 : x * 8388607);
        out[o] = s & 255;
        out[o + 1] = s >> 8 & 255;
        out[o + 2] = s >> 16 & 255;
        o += 3;
      } else {
        view.setFloat32(o, x, true);
        o += 4;
      }
    }
  }
  return out;
}

// src/dsp/fft.ts
function isPow2(n) {
  return Number.isInteger(n) && n > 0 && (n & n - 1) === 0;
}
function assertPow2(n, what) {
  if (!isPow2(n)) throw new Error(`${what}: length must be a power of two, got ${n}`);
}
function fftInPlace(re, im, inverse = false) {
  const n = re.length;
  if (im.length !== n) throw new Error("fftInPlace: re/im length mismatch");
  assertPow2(n, "fftInPlace");
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      const tr = re[i];
      re[i] = re[j];
      re[j] = tr;
      const ti = im[i];
      im[i] = im[j];
      im[j] = ti;
    }
  }
  const sign = inverse ? 1 : -1;
  for (let len = 2; len <= n; len <<= 1) {
    const half = len >> 1;
    const ang = sign * 2 * Math.PI / len;
    const wr = Math.cos(ang);
    const wi = Math.sin(ang);
    for (let i = 0; i < n; i += len) {
      let cwr = 1;
      let cwi = 0;
      for (let k = 0; k < half; k++) {
        const ur = re[i + k];
        const ui = im[i + k];
        const vr = re[i + k + half] * cwr - im[i + k + half] * cwi;
        const vi = re[i + k + half] * cwi + im[i + k + half] * cwr;
        re[i + k] = ur + vr;
        im[i + k] = ui + vi;
        re[i + k + half] = ur - vr;
        im[i + k + half] = ui - vi;
        const nwr = cwr * wr - cwi * wi;
        cwi = cwr * wi + cwi * wr;
        cwr = nwr;
      }
    }
  }
  if (inverse) {
    for (let i = 0; i < n; i++) {
      re[i] /= n;
      im[i] /= n;
    }
  }
}
function fftReal(input) {
  assertPow2(input.length, "fftReal");
  const re = new Float32Array(input);
  const im = new Float32Array(input.length);
  fftInPlace(re, im, false);
  return { re, im };
}
function hannWindow(n, periodic = false) {
  if (n < 1) throw new Error("hannWindow: length must be >= 1");
  const w = new Float32Array(n);
  if (n === 1 && !periodic) {
    w[0] = 1;
    return w;
  }
  const denom = periodic ? n : n - 1;
  for (let i = 0; i < n; i++) {
    w[i] = 0.5 - 0.5 * Math.cos(2 * Math.PI * i / denom);
  }
  return w;
}
function magnitudeSpectrum(input) {
  const { re, im } = fftReal(input);
  const n = re.length;
  const out = new Float32Array(n / 2 + 1);
  for (let k = 0; k <= n / 2; k++) {
    const mag = Math.hypot(re[k], im[k]);
    out[k] = k === 0 || k === n / 2 ? mag / n : 2 * mag / n;
  }
  return out;
}

// src/nanolab/model.ts
var NANO_SAMPLE_RATE = 48e3;
var NANO_FADE_SEC = 0.05;
var NANO_KINDS = ["two-tone", "am", "baseband", "carrier"];
var DEFAULT_NANO_RECIPE = { kind: "two-tone", carrierHz: 400, rateHz: 16, durationSec: 10, gainDb: -24 };
var NANO_LABELS = { "two-tone": "Two-tone sum", am: "Amplitude modulation", baseband: "Actual baseband tone", carrier: "Carrier-only control" };
function range(value, name, min, max) {
  if (typeof value !== "number" || !Number.isFinite(value) || value < min || value > max) throw new RangeError(`${name} must be between ${min} and ${max}.`);
  return value;
}
function validateNanoRecipe(input) {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new TypeError("A signal recipe must be an object.");
  const x = input;
  if (!NANO_KINDS.includes(x.kind)) throw new RangeError("Choose a supported signal kind.");
  const recipe = { kind: x.kind, carrierHz: range(x.carrierHz, "Carrier Hz", 80, 1e3), rateHz: range(x.rateHz, "Rate Hz", 1, 80), durationSec: range(x.durationSec, "Duration seconds", 2, 30), gainDb: range(x.gainDb, "Master gain dBFS", -60, -18) };
  if (recipe.carrierHz - recipe.rateHz <= 0 || recipe.carrierHz + recipe.rateHz >= NANO_SAMPLE_RATE / 2) throw new RangeError("Sidebands must be positive and below Nyquist.");
  return recipe;
}
function predictedNanoLines(input) {
  const r = validateNanoRecipe(input), g = dbToLin(r.gainDb);
  if (r.kind === "two-tone") return [{ hz: r.carrierHz - r.rateHz / 2, amplitude: g / 2, label: "Lower tone" }, { hz: r.carrierHz + r.rateHz / 2, amplitude: g / 2, label: "Upper tone" }];
  if (r.kind === "am") return [{ hz: r.carrierHz - r.rateHz, amplitude: g / 4, label: "Lower sideband" }, { hz: r.carrierHz, amplitude: g / 2, label: "Carrier" }, { hz: r.carrierHz + r.rateHz, amplitude: g / 4, label: "Upper sideband" }];
  return [{ hz: r.kind === "baseband" ? r.rateHz : r.carrierHz, amplitude: g, label: r.kind === "baseband" ? "Baseband" : "Carrier" }];
}
function inspectNanoSpectrum(samples) {
  const available = samples.length - Math.ceil(2 * NANO_FADE_SEC * NANO_SAMPLE_RATE);
  if (available < 1024 || samples.length > 30 * NANO_SAMPLE_RATE) throw new RangeError("Unsupported analysis length.");
  let fftSize = 1024;
  while (fftSize * 2 <= Math.min(available, 131072)) fftSize *= 2;
  const offset = Math.floor((samples.length - fftSize) / 2);
  const window = hannWindow(fftSize, true), input = new Float32Array(fftSize);
  let windowSum = 0;
  for (let i = 0; i < fftSize; i++) {
    input[i] = samples[offset + i] * window[i];
    windowSum += window[i];
  }
  const magnitudes = magnitudeSpectrum(input), correction = fftSize / windowSum, binHz = NANO_SAMPLE_RATE / fftSize;
  const point = (k) => ({ hz: k * binHz, dbFs: 20 * Math.log10(Math.max(1e-8, magnitudes[k] * correction)) });
  const last = Math.min(magnitudes.length - 1, Math.ceil(1200 / binHz));
  const points = Array.from({ length: last + 1 }, (_, k) => point(k));
  const peaks = points.filter((p, i) => i > 0 && i < points.length - 1 && p.dbFs > points[i - 1].dbFs && p.dbFs >= points[i + 1].dbFs);
  const strongestBins = peaks.sort((a, b) => b.dbFs - a.dbFs).slice(0, 5);
  return { fftSize, binHz, observationSec: fftSize / NANO_SAMPLE_RATE, points, strongestBins };
}
function renderNanoSignal(input) {
  const recipe = validateNanoRecipe(input);
  const { kind, carrierHz, rateHz, durationSec, gainDb } = recipe;
  const phase = { durationSec, carrierHz: kind === "baseband" ? rateHz : kind === "two-tone" ? carrierHz - rateHz / 2 : carrierHz, beatHz: kind === "two-tone" || kind === "am" ? rateHz : 0, mode: "monaural", gainDb: 0 };
  const raw = kind === "am" ? renderMonaural(phase, NANO_SAMPLE_RATE) : renderBinaural(phase, NANO_SAMPLE_RATE);
  const gain = dbToLin(gainDb), fade = Math.round(NANO_FADE_SEC * NANO_SAMPLE_RATE);
  let samplePeak = 0, squareSum = 0;
  for (let i = 0; i < raw.left.length; i++) {
    const edge = Math.min(1, i / fade, (raw.left.length - 1 - i) / fade);
    const envelope = 0.5 - 0.5 * Math.cos(Math.PI * edge);
    const x = (kind === "two-tone" ? (raw.left[i] + raw.right[i]) / 2 : raw.left[i]) * gain * envelope;
    raw.left[i] = x;
    raw.right[i] = x;
    samplePeak = Math.max(samplePeak, Math.abs(raw.left[i]));
    squareSum += raw.left[i] ** 2;
  }
  return { recipe, left: raw.left, right: raw.right, sampleRate: NANO_SAMPLE_RATE, samplePeak, peakDbFs: 20 * Math.log10(Math.max(samplePeak, 1e-15)), rmsDbFs: 10 * Math.log10(Math.max(squareSum / raw.left.length, 1e-30)), spectrum: inspectNanoSpectrum(raw.left), predictedLines: predictedNanoLines(recipe) };
}
function nanoManifest(rendered) {
  return { format: "opensync-nano-audio", version: 1, renderer: "nanolab-v1", recipe: rendered.recipe, units: { samples: "dimensionless digital full-scale amplitude", frequency: "Hz", gain: "dBFS sample-amplitude ceiling" }, sampleRateHz: rendered.sampleRate, nyquistHz: rendered.sampleRate / 2, framesPerChannel: rendered.left.length, actualDurationSec: rendered.left.length / rendered.sampleRate, channels: "identical L/R (diotic)", masterGainDb: rendered.recipe.gainDb, samplePeakDbFs: rendered.peakDbFs, rmsDbFs: rendered.rmsDbFs, edgeFadeSec: NANO_FADE_SEC, wavEncoding: "PCM16 stereo", predictedLinesBeforeEdgeFades: rendered.predictedLines, analysis: { window: "periodic Hann, centered segment, coherent-gain corrected", fftSize: rendered.spectrum.fftSize, binSpacingHz: rendered.spectrum.binHz, observationSec: rendered.spectrum.observationSec, strongestBins: rendered.spectrum.strongestBins, warning: "Window leakage broadens lines. FFT bins are not exact component frequencies or reconstructed true peaks." }, physicalCalibration: null, scope: "Digital audio/acoustic analogy only. No magnetic field, optical exposure, nanoparticle response, dose or treatment is specified.", source: { synthesis: "src/engine/synth.ts", adapter: "src/nanolab/model.ts", encoder: "src/engine/wav.ts" } };
}
async function exportNanoSignal(rendered) {
  const wav = encodeWav(rendered.left, rendered.right, rendered.sampleRate, "pcm16");
  const digest = await crypto.subtle.digest("SHA-256", wav.buffer.slice(wav.byteOffset, wav.byteOffset + wav.byteLength));
  const sha256 = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
  return { wav, manifest: new TextEncoder().encode(JSON.stringify({ ...nanoManifest(rendered), wavBytes: wav.length, wavSha256: sha256 }, null, 2) + "\n") };
}
export {
  DEFAULT_NANO_RECIPE,
  NANO_FADE_SEC,
  NANO_KINDS,
  NANO_LABELS,
  NANO_SAMPLE_RATE,
  exportNanoSignal,
  inspectNanoSpectrum,
  nanoManifest,
  predictedNanoLines,
  renderNanoSignal,
  validateNanoRecipe
};
