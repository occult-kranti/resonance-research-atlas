# S3A — protect evidence before interpreting it

This loop repairs a concrete defect found during root review rather than running the originally proposed geometry study. The historical fitter remains unchanged and hash-bound to S2A/S2B. The new intake_v2.py guards paths before analysis, rejects CSV channel selection other than zero, and uses exclusive file creation. Existing outputs cannot be overwritten; choose a new prefix. If creating the second output fails, only files created by this invocation are cleaned up.

Actual CLI runs demonstrate preserved raw-source and sentinel hashes for source, symlink and existing-output collisions. The valid decoded WAV and exact two-column CSV produce identical fit traces and fitted parameters under the frozen tolerances. Source hashes, provenance declarations and both implementation hashes appear in output JSON.

This is evidence-preserving software/metrology verification, not an acoustic discovery. The caller's provenance label is not independent authentication. The physical limitations established by S2B still hold. Next: malformed acquisition metadata and time-base calibration, including failures that file validation cannot detect.

