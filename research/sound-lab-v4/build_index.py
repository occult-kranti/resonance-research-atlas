"""Create a convenience index; frozen producer/reviewer records remain authoritative."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rounds = []
    for folder in sorted(ROOT.glob("R[1-5]")):
        if not (folder / "manifest.json").is_file():
            continue
        r = json.loads((folder / "results.json").read_text())
        manifest = json.loads((folder / "manifest.json").read_text())
        review_path = ROOT / "reviews" / f"{folder.name}-review.json"
        review = json.loads(review_path.read_text()) if review_path.is_file() else {}
        accepted = review.get("verdict") == "accepted_narrow" and review.get("manifestSHA256") == sha(folder / "manifest.json")
        prefix = "research/sound-lab-v4/" + folder.name + "/"
        entry = {k:r[k] for k in ["id","round","title","question","finding","metrics","evidenceType","limits"]}
        entry.update({"status":"accepted_narrow" if accepted else "executed_pending_review",
                      "resultsPath":prefix+"results.json","contractPath":prefix+"contract.json",
                      "reportPath":prefix+"report.md","manifestPath":prefix+"manifest.json",
                      "figurePaths":[prefix+p for p in manifest["artifacts"] if p.endswith(".svg")],
                      "rawPaths":[prefix+p for p in manifest["artifacts"] if p.endswith((".csv",".csv.gz",".wav"))],
                      "reviewPath":"research/sound-lab-v4/reviews/"+review_path.name if review else None,
                      "contractSHA256":r["contractSHA256"],"manifestSHA256":sha(folder/"manifest.json")})
        rounds.append(entry)
    data = {"schemaVersion":1,"program":"Reference witnesses, electrical energy and force boundaries",
            "status":"complete_narrow" if len(rounds)==5 and all(r["status"]=="accepted_narrow" for r in rounds) else "in_progress",
            "rounds":rounds,"claimBoundary":"Synthetic models, not our physical experiments, extra energy, gravity modification or intrinsic material identification.",
            "scopeRevision":"After R2 the user prioritized electricity, magnetism and antigravity. Unadmitted sound R3 is parked separately and excluded from the five-round count."}
    (ROOT/"summaries.json").write_text(json.dumps(data,indent=2,allow_nan=False)+"\n")
    print(json.dumps({"roundsIndexed":len(rounds),"status":data["status"]}))


if __name__ == "__main__":
    main()
