"""Verify exact synthetic round artifacts; optionally regenerate in temporary folders.

This checks reproducibility, not scientific validity or phenomenal consciousness.
Independent review is recorded separately in docs/panel-v3/reviews.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(regenerate=False, require_complete=False):
    rounds = sorted(HERE.glob('round[123]'))
    if require_complete:
        assert len(rounds) == 3, 'Three rounds required'
    checked = []
    summary = json.loads((HERE / 'summary.json').read_text())
    summary_rows = {r['id']: r for r in summary['rounds']}
    for folder in rounds:
        contract = json.loads((folder / 'contract.json').read_text())
        result = json.loads((folder / 'results.json').read_text())
        manifest = json.loads((folder / 'manifest.json').read_text())
        assert result['id'] == contract['id'] == manifest['id']
        assert result['evidenceType'] == 'synthetic'
        assert result['live_model_calls'] == result['human_observations'] == 0
        assert result['allAcceptanceGatesPassed'] is True
        assert result['contractSHA256'] == digest(folder / 'contract.json')
        for relative, expected in manifest['artifacts'].items():
            assert digest(folder / relative) == expected, (folder.name, relative, 'hash mismatch')
        for dependency in manifest.get('sharedDependencies', []):
            assert digest(REPO / dependency['path']) == dependency['sha256']
        predecessor = contract['predecessorReview']
        assert digest(REPO / predecessor['path']) == predecessor['sha256'], 'Predecessor review changed'
        review_path = REPO / 'docs/panel-v3/reviews' / f"{result['id']}-review.json"
        if require_complete:
            review = json.loads(review_path.read_text())
            assert review['status'].startswith('accepted'), (result['id'], 'not independently accepted')
            row = summary_rows[result['id']]
            assert row['reviewSHA256'] == digest(review_path), 'Bound round review changed'
            assert row['reviewStatus'] == row['status'] == review['status']
            for relative in [*manifest['artifacts'], 'manifest.json']:
                file_path = folder / relative
                assert review['bindings'][str(file_path.relative_to(REPO))] == digest(file_path), 'Reviewed artifact changed'
        if regenerate:
            with tempfile.TemporaryDirectory(prefix=f"{result['id']}-verify-") as tmp:
                proc = subprocess.run([sys.executable, str(folder / 'solver.py'), '--output-dir', tmp], capture_output=True, text=True)
                assert proc.returncode == 0, proc.stdout + proc.stderr
                for generated in Path(tmp).iterdir():
                    if generated.name == 'manifest.json':
                        continue  # input-only review notes are bound in the stored manifest
                    assert digest(generated) == digest(folder / generated.name), (result['id'], generated.name, 'regeneration differs')
        checked.append({'id': result['id'], 'boundArtifacts': len(manifest['artifacts']), 'regenerated': regenerate})
    print(json.dumps({'status': 'passed', 'rounds': checked, 'claim': 'Artifact integrity and declared synthetic-model reproducibility only'}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--regenerate', action='store_true')
    parser.add_argument('--require-complete', action='store_true')
    args = parser.parse_args()
    verify(args.regenerate, args.require_complete)
