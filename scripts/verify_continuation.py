#!/usr/bin/env python3
"""Release gate for the completed V3 program; uses only the standard library.

This checks completeness and reviewed artifact identity, not new scientific truth.
Individual producer and reviewer runners supply the numerical checks.
"""
from pathlib import Path
import hashlib
import ast
import json

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [f'S{round_}{loop}' for round_ in range(1, 6) for loop in 'AB'] + ['B1', 'B2', 'B3']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def artifact(relative):
    path = (ROOT / relative).resolve()
    require(path.is_relative_to(ROOT), f'Artifact outside repository: {relative}')
    require(path.is_file(), f'Missing artifact: {relative}')
    return path


def digest(relative):
    return hashlib.sha256(artifact(relative).read_bytes()).hexdigest()


def read(relative):
    return json.loads(artifact(relative).read_text())


def main():
    ledger = read('research/panel-v3-decisions.json')
    panels = ledger.get('planningPanels', [])
    require([p['id'] for p in panels] == ['P1', 'P2', 'P3'], 'Three ordered planning panels required')
    for panel in panels:
        require(panel.get('status') == 'completed', f'Planning panel incomplete: {panel["id"]}')
        artifact(panel['record'])
    reviews = ledger.get('reviews', [])
    require([review['id'] for review in reviews] == EXPECTED, 'Exactly ten ordered sound loops, then three later rounds required')
    reviewer_text = artifact(ledger.get('reviewerSourcePath', 'docs/panel-v3/reviewer.py')).read_text()
    reviewer_lines = reviewer_text.splitlines(keepends=True)
    checker_hashes = {node.name: hashlib.sha256(''.join(reviewer_lines[node.lineno - 1:node.end_lineno]).encode()).hexdigest()
                      for node in ast.parse(reviewer_text).body if isinstance(node, ast.FunctionDef)}
    bindings = set()
    for index, entry in enumerate(reviews):
        require(entry.get('status') == 'accepted_narrow', f'Unaccepted loop: {entry["id"]}')
        review = read(entry['reviewPath'])
        require(review.get('id') == entry['id'], 'Review ID mismatch')
        require(review.get('status') == 'accepted_narrow', 'Review verdict mismatch')
        require(checker_hashes.get(review.get('checkerFunction')) == review.get('checkerFunctionSHA256'), 'Reviewed checker function changed')
        require(review.get('sequence') == index + 1, 'Review order mismatch')
        if index:
            predecessor = review.get('predecessor', {})
            previous = reviews[index - 1]
            require(predecessor.get('id') == previous['id'], 'Wrong review predecessor')
            require(predecessor.get('reviewPath') == previous['reviewPath'], 'Wrong predecessor artifact')
            require(predecessor.get('reviewSHA256') == digest(previous['reviewPath']), 'Predecessor review changed')
        require(bool(review.get('independentChecks')), f'Missing independent checks: {entry["id"]}')
        require(bool(review.get('bindings')), f'Missing reviewed bindings: {entry["id"]}')
        for relative, expected in review['bindings'].items():
            require(digest(relative) == expected, f'Reviewed artifact changed: {relative}')
            bindings.add(relative)
        for key, hash_key in [('contractPath', 'contractSHA256'), ('resultsPath', 'resultSHA256')]:
            require(digest(entry[key]) == entry[hash_key], f'Ledger binding differs: {entry["id"]} {key}')
            require(entry[key] in review['bindings'], f'Unreviewed core artifact: {entry[key]}')
        for key in ['figurePaths', 'rawPaths']:
            for relative in entry.get(key, []):
                artifact(relative)
        artifact(entry['reportPath'])
        if 'sequenceIndex' in entry:
            require(entry['sequenceIndex'] == index + 1, 'Review sequence index mismatch')
    for path_key, hash_key in [('reviewerSourcePath', 'reviewerSourceSHA256'), ('recordReviewSourcePath', 'recordReviewSourceSHA256')]:
        require(bool(ledger.get(path_key)) and bool(ledger.get(hash_key)), f'Missing final reviewer binding: {path_key}')
        require(digest(ledger[path_key]) == ledger[hash_key], f'Final review tool changed: {path_key}')
    for group in ['sourceLedgerBindings', 'finalDocumentBindings']:
        require(bool(ledger.get(group)), f'Missing final bindings: {group}')
        for relative, expected in ledger[group].items():
            require(digest(relative) == expected, f'Final source or document changed: {relative}')
    catalog = read('docs/panel-v3/setup-catalog.json')
    require(len(catalog.get('entries', [])) == 9, 'Nine setup/catalog visuals required')
    summary = read('research/consciousness-v3/summary.json')
    require([r.get('id') for r in summary.get('rounds', [])] == ['B1', 'B2', 'B3'], 'Consciousness wrapper incomplete')
    require(all(r.get('status') == 'accepted_narrow' for r in summary['rounds']), 'Consciousness wrapper has stale verdicts')
    require(summary.get('live_model_calls') == 0 and summary.get('human_observations') == 0, 'Synthetic study provenance changed')
    require(ledger.get('completedSoundLoops') == 10 and ledger.get('completedLaterRounds') == 3, 'Ledger completion counts differ')
    for setup in catalog['entries']:
        artifact(setup['file'])
        require(bool(setup.get('caption')) and bool(setup.get('alt')), 'Setup needs a caption and text alternative')
    for relative in ['sound-lab/index.html', 'sound-lab/app.js', 'sound-lab/styles.css',
                     'docs/panel-v3/sources-history.json', 'docs/panel-v3/sources-modern.json',
                     'docs/panel-v3/sources-consciousness.json', 'docs/panel-v3/alchemy-dictionary.json',
                     'docs/panel-v3/bashar-perspective.md', 'assets/sound-lab-v3/concept.png']:
        artifact(relative)
    print(json.dumps({'status': 'passed', 'planningPanels': len(panels), 'reviewedLoops': len(reviews),
                      'uniqueReviewedArtifacts': len(bindings), 'setupEntries': len(catalog['entries']),
                      'scope': 'Release completeness and exact reviewed bytes; no physical or consciousness claim.'}, indent=2))


if __name__ == '__main__':
    main()
