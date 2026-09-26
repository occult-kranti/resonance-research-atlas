#!/usr/bin/env python3
"""Verify five nanoparticle rounds and their bound evidence.

Default: read-only hash/review/artifact verification (Python standard library).
--recompute: rerun existing solvers in a temporary copy, compare numeric evidence,
             and verify actual audio renderer regeneration; never rewrite originals.
Recomputation repeats existing benchmarks and does not select additional rounds.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("--recompute",action="store_true");args=parser.parse_args()
    manifest=json.loads((ROOT/"artifact-manifest.json").read_text())
    for name,item in manifest["files"].items():
        path=ROOT/name
        assert path.exists() and path.stat().st_size==item["bytes"] and sha(path)==item["sha256"],f"Bound artifact mismatch: {name}"
    rounds=[]
    for n in range(1,6):
        folder=ROOT/f"round{n}";result=json.loads((folder/"results.json").read_text());review=json.loads((folder/"independent-review.json").read_text())
        assert result["status"]=="passed" and all(c["passed"] for c in result["checks"]),f"Production gate failure N{n}"
        assert review["status"]=="accepted",f"Independent admission missing N{n}"
        for name,digest in result["hashes"].items():assert sha(folder/name)==digest,f"Result source mismatch N{n}/{name}"
        for name,digest in review["source_sha256"].items():assert sha(folder/name)==digest,f"Review binding mismatch N{n}/{name}"
        assert (folder/"interpretation.md").exists() and list(folder.glob("*.svg")) and list(folder.glob("*.png"))
        rounds.append(dict(round=n,production_checks=len(result["checks"]),independent_review="accepted",status="verified"))
    inputs=json.loads((ROOT/"round5"/"inputs.json").read_text())
    for name,item in inputs["files"].items():
        path=ROOT/"round5"/name
        assert sha(path)==item["sha256"] and path.stat().st_size==item["bytes"],f"Actual renderer input mismatch: {name}"
    recomputed=[]
    if args.recompute:
        with tempfile.TemporaryDirectory(prefix="nanoparticles-recompute-") as temporary:
            copy=Path(temporary)/"nanoparticles";shutil.copytree(ROOT,copy)
            for n in range(1,6):
                subprocess.run([sys.executable,str(copy/f"round{n}"/"solver.py")],check=True,stdout=subprocess.DEVNULL)
                # Exact numeric/source metadata equality is intentional; changed
                # dependency versions or outputs require review, not a hash refresh.
                names=["results.json"]+[path.name for path in (ROOT/f"round{n}").glob("*.csv")]
                for name in names:assert sha(copy/f"round{n}"/name)==sha(ROOT/f"round{n}"/name),f"Recomputation mismatch N{n}/{name}"
                recomputed.append(n)
            subprocess.run(["node",str(copy/"round5"/"regenerate_assets.mjs")],check=True)
    output=dict(status="verified",branch="nanoparticles",rounds=rounds,total_production_checks=sum(r["production_checks"] for r in rounds),
                bound_artifact_files=len(manifest["files"]),actual_production_audio_inputs_bound=len(inputs["files"]),recomputed_rounds=recomputed,
                scope="Five existing model benchmarks with separate accepted reviews. Hashes bind exact evidence; they are not scientific proof or measured physical effects.")
    print(json.dumps(output,indent=2))

if __name__=="__main__":main()
