"""Verify frozen evidence bytes; optionally reproduce existing rounds in a temp copy."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--regenerate", action="store_true")
    args = parser.parse_args()
    records = []
    with tempfile.TemporaryDirectory(prefix="sound-v4-verify-") as temporary:
        destination = Path(temporary) / ROOT.name
        if args.regenerate:
            shutil.copytree(ROOT, destination, ignore=shutil.ignore_patterns("__pycache__"))
        for folder in sorted(ROOT.glob("R[1-5]")):
            if not (folder / "manifest.json").is_file():
                continue
            manifest = json.loads((folder / "manifest.json").read_text())
            if sha(ROOT / "common.py") != manifest["commonSHA256"]:
                raise RuntimeError(f"{folder.name}: common helper drift")
            for name, expected in manifest["artifacts"].items():
                if sha(folder / name) != expected:
                    raise RuntimeError(f"{folder.name}/{name}: artifact drift")
            result = json.loads((folder / "results.json").read_text())
            if result["contractSHA256"] != sha(folder / "contract.json"):
                raise RuntimeError(f"{folder.name}: contract mismatch")
            if not result["producerChecksPassed"]:
                raise RuntimeError(f"{folder.name}: retained producer failure requires review")
            if args.regenerate:
                target = destination / folder.name
                subprocess.run([sys.executable, str(target / "run.py")], check=True, stdout=subprocess.DEVNULL)
                for name, expected in manifest["artifacts"].items():
                    if sha(target / name) != expected:
                        raise RuntimeError(f"{folder.name}/{name}: regeneration differs")
            records.append({"id":folder.name,"artifacts":len(manifest["artifacts"]),
                            "manifestSHA256":sha(folder / "manifest.json")})
    print(json.dumps({"status":"passed","mode":"regenerated_in_temporary_copy" if args.regenerate else "bound_bytes",
                      "rounds":records,"claim":"Byte and producer-gate verification; independent scientific review remains separate."}, indent=2))


if __name__ == "__main__":
    main()
