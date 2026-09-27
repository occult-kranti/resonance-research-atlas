# A small sound bench — proposed, not yet measured

Use one phone capable of exporting unprocessed WAV, a familiar speaker for the transfer experiment, a pencil with eraser, a sound unbroken metal or wooden spoon, cotton thread, books and cardboard position marks. Do not use high voltage, powders, hot vessels, fragile glass or biological claims. These are optional household sound observations, not instructions for treatment.

Keep volume comfortable and brief. Digital −30 dBFS is a file amplitude, not a sound-pressure exposure limit. Start with playback volume low; manual stopping is always available. Generated examples do not autoplay. An ordinary microphone without calibration does not yield pascals or dB SPL.

Validation WAVs in the loop folders are data-analysis fixtures, not listening presets. Some deliberately contain full-scale clipped signals or silence to test rejection. Use ordinary quiet taps or the app's existing bounded manual audio controls for the proposed bench; do not play the negative-control files as probes.

## Recording-chain comparison

1. Mark the speaker and phone positions on cardboard; a candidate separation is 0.50 m, measured between the speaker face and microphone opening. Keep orientation, support, room and volume unchanged. Photograph or sketch the actual positions and note distances; drawings are plans only.
2. Record silence, then the same probe with no object, with the test object, and again with no object. Preserve raw files and acquisition order. Repeat the complete sequence three times. Log date, device/OS/app, sample rate, channel selection, exported format, volume setting and any processing controls.
3. Request fixed gain and disable automatic gain control, echo cancellation and noise suppression where available. Save both requested and reported settings; neither guarantees the underlying hardware is linear. If controls are unavailable, label the path uncontrolled.
4. A separate control intentionally moves the phone 1 cm, then restores it to its mark. A moved response shows how geometry can imitate an object change. Do not call its spectral peak a material resonance.
5. Compare reference repeats, report excluded weak bins and preserve the raw data. Stability checks can reject a recording; they cannot establish that the source/receiver factors are individually known. This program's synthetic thresholds are not universal phone-calibration limits.

## Gentle tap and ringdown

1. Suspend a spoon loosely by thread over a padded table so it cannot fall far. Place the phone microphone 0.20 m away without contact. Record 1 s before and at least 2 s after a gentle eraser tap; avoid striking the microphone or support.
2. For an exploratory pilot, record at least five separate taps without moving the phone. Before a condition comparison, select the mode frequency and fit window using this separate pilot, then freeze a new study plan. Preserve every file, including quiet or visibly clipped takes, and record exclusion reasons without selecting the most attractive spectrum.
3. Repeat with a finger lightly touching the spoon as a support/damping control. This changes a boundary and loading; it is not a test that material composition changed. Keep the microphone in place and repeat untouched reference taps afterwards.
4. Fit only a declared time window after the impact. Report frequency, exponential decay rate, residual fraction, window and channels. A good single-mode fit does not establish intrinsic material damping: receiver decay, support losses, radiation losses and automatic gain can all matter.
5. The command-line intake accepts WAV or `time_s,amplitude_FS` CSV and saves fit traces/flags. Synthetic validation files show the format; they are not recorded taps. Window times are absolute times from the beginning of the file: with a 1 s lead-in, a window starting .05 s after the tap might start at 1.05 s, depending on the actual event timestamp. Do not use the fixture's start time blindly.

The protected `intake_v2.py` wraps the frozen historical fitter. It rejects input/output collisions, existing output files, symlink collisions and unavailable CSV channels before writing. Keep `fit_recording.py` for historical reproduction only.

```sh
python research/sound-lab-v3/intake_v2.py path/to/tap.wav --frequency 500 --start 1.05 --stop 1.8 --output path/to/new-tap-fit
```

`--frequency` is the declared nominal mode frequency and creates a local ±50 Hz search; `--alpha-max` defaults to 20 s^-1. Choose both before comparing conditions, based on an independently saved pilot or declared object hypothesis. The tool reports local results and flags; it does not search every mode or establish uncertainty from a single take. It rejects silence, full-file clipping, malformed/nonuniform CSV, nonfinite samples, unavailable channels, files over 20 MB and records longer than 60 seconds. Stereo defaults to channel zero; set `--channel` explicitly if another microphone channel is intended. Keep original files; outputs are separate files chosen by the user.

The final synthetic preregistration and batch intake are in S5A and S5B. No laboratory or participant data are claimed here.

## Counterbalanced comparison

S5A supplies a public synthetic plan and a blank acquisition table. Its 16-trial sequence is `ABBA BAAB ABBA BAAB`, where A means untouched and B means light touch. This balances the declared linear order-drift model; it does not remove arbitrary drift or a gain change tied to condition. The public demonstration labels are not blinded. A future analyst can receive masked codes only if another custodian holds the condition key; the operator still knows whether they touched the object.

Record one raw file per trial, trial order/code, device/export settings, gain processing, geometry, clock/reference status and the raw-file SHA-256. Predeclare how impact time will be assigned before analysis—for example, an analyst marks the first impact onset while condition labels remain masked, without selecting it to improve a decay fit. Store that file-relative time for every trial. Keep the raw file with its pre-impact silence. The analysis window is relative to the recorded impact time; do not apply `.05–.8 s` from file start when the tap occurs after a 1 s lead-in. These numbers and 500 Hz are fixture choices; use the separately frozen pilot choices for an actual object.

Report every planned trial and exclusion, including silence, clipping, poor single-mode residual or failed metadata/integrity checks. The planned set is incomplete when a required trial is missing or ineligible. A descriptive contrast among remaining trials does not repair missing data or establish intrinsic material damping. No significance or participant-study inference is supplied by this bench.

```sh
python research/sound-lab-v3/batch_intake.py --plan path/to/frozen-plan.json --manifest path/to/acquisition-manifest.json --output path/to/new-analysis-directory
```

Use S5A's `trial-template.csv` to log acquisition and S5B's `complete-manifest.json` to see the JSON structure. Each trial's source hash, order, condition code and impact time must match its raw file and separately frozen plan. The batch output records every rejection. When any planned trial is missing or ineligible, `primaryContrast_per_s` is null; an optional surviving-trial contrast is explicitly descriptive. The first S5B fixture includes 1 s of silence before the impact to verify this alignment path.

## Spatial observation option

For an optional amplitude-only survey, keep the speaker fixed and mark microphone positions along a cardboard strip. Keep phone orientation and height constant and retain an unchanged-position reference recording between moved-position measurements. A position map describes the combined source/room/receiver response. It does not identify a material from a node pattern.

S4's two-complex-sample inversion is a synthetic benchmark, with assumed 500 Hz and sound speed 343 m/s, giving wavelength 0.686 m and quarter-wave spacing 0.1715 m. Its complex amplitudes require a shared phase reference independently maintained across positions. Ordinary separately started phone recordings do not automatically supply that reference. Without it, use the amplitude-survey interpretation and do not run an apparent complex inversion as a physical result. A real room is not automatically a one-dimensional two-wave field.
