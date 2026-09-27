"""Deterministic evidence helpers; no acquisition, playback, or physical claims."""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import scipy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
plt.rcParams.update({"svg.hashsalt": "sound-lab-v4", "font.family": "DejaVu Sans",
                     "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.alpha": .2})


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def writejson(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def csv(path, names, data):
    np.savetxt(path, np.asarray(data), delimiter=",", header=",".join(names),
               comments="", fmt="%.17g")


def savefig(fig, path):
    fig.tight_layout()
    fig.savefig(path, metadata={"Date": None})
    plt.close(fig)


def finish(folder, metrics, finding, controls, report, files, checks, extra=None):
    """Record checks even when false. A producer pass is not scientific acceptance."""
    folder = Path(folder)
    contract = json.loads((folder / "contract.json").read_text())
    result = {"id": contract["id"], "round": contract.get("round", int(contract["id"][1])),
              "title": contract["title"], "status": "executed_pending_review",
              "evidenceType": "synthetic_model", "question": contract["question"],
              "finding": finding, "metrics": metrics, "controls": controls,
              "checks": checks, "producerChecksPassed": all(checks.values()),
              "limits": contract.get("limits", [contract["claimCeiling"]]), "contractSHA256": sha(folder / "contract.json"),
              "runtime": {"python": sys.version.split()[0], "numpy": np.__version__,
                          "scipy": scipy.__version__, "matplotlib": matplotlib.__version__}}
    if extra:
        result.update(extra)
    writejson(folder / "results.json", result)
    (folder / "report.md").write_text(report.rstrip() + "\n")
    artifacts = ["contract.json", "run.py", "results.json", "report.md", *files]
    writejson(folder / "manifest.json", {"id": contract["id"],
              "artifacts": {p: sha(folder / p) for p in artifacts},
              "commonSHA256": sha(ROOT / "common.py")})
    print(json.dumps({"id": result["id"], "metrics": metrics,
                      "checks": checks, "finding": finding}, indent=2))
    return result
