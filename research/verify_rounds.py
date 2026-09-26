#!/usr/bin/env python3
"""Verify six completed rounds, or regenerate their existing benchmarks first.

python research/verify_rounds.py
python research/verify_rounds.py --regenerate

Regeneration repeats the declared experiments; it does not select new rounds.
Hash checks verify artifact identity and do not replace independent mathematics.
"""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument("--regenerate",action="store_true")
args=parser.parse_args()

def digest(data):return hashlib.sha256(data).hexdigest()
def payload(folder,name):
    path=folder/name
    if path.exists():return path.read_bytes()
    archive=folder/(name+".gz")
    if archive.exists():return gzip.decompress(archive.read_bytes())
    raise FileNotFoundError(path)

if args.regenerate:
    subprocess.run([sys.executable,"-m","unittest","discover","-s",str(ROOT/"round1"),"-p","test_solver.py","-v"],check=True)
    for number in range(1,7):
        subprocess.run([sys.executable,str(ROOT/f"round{number}"/"solver.py")],check=True,stdout=subprocess.DEVNULL)
    subprocess.run([sys.executable,str(ROOT/"compress_evidence.py")],check=True)

rounds=[]
for number in range(1,7):
    folder=ROOT/f"round{number}"
    result=json.loads((folder/"results.json").read_text())
    assert result["status"]=="passed" and all(check["passed"] for check in result["checks"]),folder
    pairs={"contract_sha256":"contract.md","solver_sha256":"solver.py",
           "test_source_sha256":"test_solver.py","clarification_sha256":"contract-clarification.md"}
    for key,name in pairs.items():
        if key in result:assert digest(payload(folder,name))==result[key],f"Result source mismatch: {folder.name}/{name}"
    review=json.loads((folder/"independent-review.json").read_text())
    reviewed_hashes=review.get("source_sha256",{}).copy()
    revision=folder/"independent-review-revision.json"
    if revision.exists():reviewed_hashes.update(json.loads(revision.read_text()).get("current_source_sha256",{}))
    assert reviewed_hashes,"Independent review has no source bindings"
    for name,expected in reviewed_hashes.items():
        assert digest(payload(folder,name))==expected,f"Independent review source mismatch: {folder.name}/{name}"
    manifest=json.loads((folder/"csv-manifest.json").read_text())
    for item in manifest["files"]:
        packed=(folder/item["gzip_filename"]).read_bytes();raw=gzip.decompress(packed)
        assert digest(raw)==item["raw_sha256"] and len(raw)==item["raw_bytes"],"Raw evidence mismatch"
        assert digest(packed)==item["gzip_sha256"] and len(packed)==item["gzip_bytes"],"Archive mismatch"
    assert (folder/"interpretation.md").exists()
    assert list(folder.glob("*.svg")) and list(folder.glob("*.png"))
    rounds.append(dict(round=number,production_checks=len(result["checks"]),independent_review_bound=True,
                       compressed_csv_files=len(manifest["files"]),status="verified"))

output=dict(status="verified",rounds=rounds,total_production_checks=sum(row["production_checks"] for row in rounds),
            focused_round1_unit_tests=4,regenerated=args.regenerate,
            scope="Source/result/review/archive binding; with --regenerate also reruns all existing production checks and the four focused tests. No new research round.")
(ROOT/"verification.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps(output,indent=2))
