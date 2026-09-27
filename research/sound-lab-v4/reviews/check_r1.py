"""Independent R1 check: carrier maxima, explicit kernels and same-PCM rivals.

No producer module is imported. This script is for the declared 8 kHz,
integer-period, zero-phase synthetic fixtures, not arbitrary recordings.
"""
from pathlib import Path
import hashlib
import json
import wave
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inspect_wav(path):
    with wave.open(str(path), "rb") as stream:
        fs = stream.getframerate()
        channels = stream.getnchannels()
        assert channels == 2 and stream.getsampwidth() == 2
        data = np.frombuffer(stream.readframes(stream.getnframes()), dtype="<i2").reshape(-1, 2)
    slopes = []
    for channel, frequency in enumerate([500, 1000]):
        period = fs // frequency
        assert period * frequency == fs
        indices = np.arange(0, len(data), period)
        amplitude = data[indices, channel].astype(float) / 32768
        if np.all(amplitude == 0):
            slopes.append(None)
            continue
        assert np.all(amplitude > 0), "Fixture is not declared zero-phase positive-envelope case"
        times = indices / fs
        centered = times - times.mean()
        slopes.append(float(centered @ np.log(amplitude) / (centered @ centered)))
    return {"sha256": digest(path), "sampleRate_Hz": fs, "samples": len(data),
            "maxAbsPCM": int(np.max(np.abs(data.astype(np.int32)))),
            "targetSlope_per_s": slopes[0], "referenceSlope_per_s": slopes[1],
            "correctedAlpha_per_s": None if None in slopes else slopes[1] - slopes[0]}


def pcm(alpha, beta_s, beta_r, alpha_r=0):
    t = np.arange(8000) / 8000
    x = np.column_stack((.2*np.exp((beta_s-alpha)*t)*np.cos(2*np.pi*500*t),
                         .05*np.exp((beta_r-alpha_r)*t)*np.cos(2*np.pi*1000*t)))
    return np.round(x*32767).astype("<i2")


def main():
    models = {
        "single_channel": ([[-1, 1]], [1, 1]),
        "shared_gain": ([[-1, 1], [0, 1]], None),
        "differential_gain": ([[-1, 1, 0], [0, 0, 1]], [1, 1, 0]),
        "unstable_reference": ([[-1, 0, 1], [0, -1, 1]], [1, 1, 1]),
    }
    structural = {}
    for name, (entries, kernel) in models.items():
        matrix = np.asarray(entries, dtype=float)
        rank = int(np.linalg.matrix_rank(matrix))
        residual = None if kernel is None else float(np.linalg.norm(matrix @ kernel))
        assert residual is None or residual == 0
        structural[name] = {"matrix": entries, "domainDimension": matrix.shape[1],
                            "rank": rank, "nullity": matrix.shape[1]-rank,
                            "kernelWitness": kernel, "kernelResidual": residual}
    baseline = pcm(4, 1, 1)
    differential_rival = pcm(5, 2, 1)
    unstable_rival = pcm(5, 2, 2, 1)
    rivals = {"different_alpha_differential_gain_PCM_identical": bool(np.array_equal(baseline, differential_rival)),
              "different_alpha_unstable_reference_PCM_identical": bool(np.array_equal(baseline, unstable_rival)),
              "baseline_alpha_per_s": 4, "rival_alpha_per_s": 5}
    assert all(v for k, v in rivals.items() if k.endswith("identical"))
    # Exact common gain cancels even if nonexponential. Noise and channel
    # mismatch do not share this cancellation and are not assumed absent in a bench.
    t = np.linspace(0, 1, 1001)
    gain = np.exp(.4*np.sin(8*t)+.2*t*t)
    log_ratio = np.log(.2*np.exp(-4*t)*gain)-np.log(.05*gain)
    centered = t-t.mean()
    ratio_alpha = float(-(centered @ log_ratio)/(centered @ centered))
    assert abs(ratio_alpha-4) < 1e-12
    files = {str(p.relative_to(ROOT)): inspect_wav(p) for p in sorted((ROOT/"R1").rglob("*.wav"))}
    assert files, "No R1 fixtures supplied"
    result = {"method": "Independent signed carrier-maxima regression; no producer code import",
              "models": structural, "exactRivals": rivals,
              "nonexponentialSharedGainRatioAlpha_per_s": ratio_alpha, "decodedFiles": files,
              "scriptSHA256": digest(__file__)}
    (HERE/"R1-independent-checks.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
