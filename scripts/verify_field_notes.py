#!/usr/bin/env python3
"""Verify the V4 release record and the exact admitted research artifacts.

This gate checks completed work and reproducible provenance, not physical truth.
Numerical replay is a separate command in research/sound-lab-v4/verify.py.
"""
from datetime import datetime
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


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
    ledger = read('research/panel-v4-decisions.json')
    source_entries = read('data/sources-v4.json')['sources']
    source_ids = {source['id'] for source in source_entries}
    require(len(source_ids) == len(source_entries), 'Source IDs must be unique')
    expected = [f'R{r}{loop}' for r in range(1, 6) for loop in 'AB']
    entries = ledger.get('reviews', [])
    require([e.get('id') for e in entries] == expected, 'Exactly five ordered two-loop rounds required')
    require(ledger.get('completedRounds') == 5 and ledger.get('completedLoops') == 10,
            'Completed counts must agree with the ten records')
    bindings = set()
    previous_review_time = None
    for round_number in range(1, 6):
        producer, verdict = entries[(round_number - 1) * 2:round_number * 2]
        require(producer.get('status') == 'completed_producer', 'Production not complete')
        require(verdict.get('status') == 'accepted_narrow', 'Skeptical gate not accepted')
        for entry in (producer, verdict):
            require(entry.get('sequence') == expected.index(entry['id']) + 1, 'Loop sequence mismatch')
            for path_key, sha_key in [('contractPath', 'contractSHA256'),
                                     ('resultsPath', 'resultSHA256'),
                                     ('reviewPath', 'reviewSHA256')]:
                require(digest(entry[path_key]) == entry[sha_key], f'Stale binding: {entry["id"]} {path_key}')
                bindings.add(entry[path_key])
            require(entry.get('finding') and entry.get('withheld') and entry.get('nextDecision'),
                    'Each loop needs its result, limit and changed next question')
            for figure in entry.get('figurePaths', []):
                artifact(figure)
        contract = read(verdict['contractPath'])
        require(all(source in source_ids for source in contract.get('sources', [])),
                f'Unresolved source ID in round {round_number}')
        review = read(verdict['reviewPath'])
        require(review.get('verdict') == 'accepted_narrow', 'Review file verdict differs')
        independent_script = 'check_r3_electrical.py' if round_number == 3 else f'check_r{round_number}.py'
        for relative, key in [
            (f'research/sound-lab-v4/R{round_number}/manifest.json', 'manifestSHA256'),
            (f'research/sound-lab-v4/reviews/{independent_script}', 'independentScriptSHA256'),
            (f'research/sound-lab-v4/reviews/R{round_number}-independent-checks.json', 'independentResultsSHA256')]:
            require(digest(relative) == review[key], f'Stale independent review binding: {relative}')
            bindings.add(relative)
        require(review['contractSHA256'] == verdict['contractSHA256'], 'Reviewer contract differs')
        require(all(review.get('checks', {}).values()), 'Independent review contains a failed check')
        require(review.get('checks'), 'Independent checks missing')
        freeze_time = datetime.fromisoformat(contract['frozenAt'])
        review_time = datetime.fromisoformat(review['reviewedAt'])
        require(freeze_time < review_time, 'Contract must precede admission')
        if previous_review_time:
            require(freeze_time > previous_review_time, 'Later contract predates previous skeptical verdict')
        previous_review_time = review_time
    for group in ('sourceLedgerBindings', 'finalDocumentBindings'):
        require(ledger.get(group), f'Missing final provenance group: {group}')
        for relative, expected_sha in ledger[group].items():
            require(digest(relative) == expected_sha, f'Stale final provenance binding: {relative}')
            bindings.add(relative)
    for relative in ['sound-lab/field-notes.html', 'sound-lab/field-notes.js',
                     'sound-lab/field-notes.css', 'docs/continuation-v4.md',
                     'docs/panel-v4/roadmap-v4.md', 'docs/panel-v4/source-review.md',
                     'docs/panel-v4/alchemy-materials.md', 'data/sources-v4.json',
                     'docs/panel-v4/apparatus.md', 'scripts/render_apparatus_v4.py',
                     'scripts/render_electromagnetic_v4.py',
                     'assets/sound-lab-v4/electrical-energy-boundary.svg',
                     'assets/sound-lab-v4/magnetic-force-plan.svg',
                     'assets/sound-lab-v4/magnetic-force-3d.png',
                     'assets/sound-lab-v4/magnetic-balance-concept.png',
                     'assets/sound-lab-v4/tabletop-concept.png']:
        artifact(relative)
    geometry = read('assets/sound-lab-v4/electromagnetic-manifest.json')
    require(digest('scripts/render_electromagnetic_v4.py') == geometry['generatorSha256'],
            'Electrical / magnetic geometry generator changed')
    require(digest('scripts/render_apparatus_v4.py') == geometry['dependencySha256'],
            'Shared geometry renderer changed')
    for name, expected_sha in geometry['filesSha256'].items():
        require(digest('assets/sound-lab-v4/' + name) == expected_sha, 'Geometry artifact changed: ' + name)
    print(json.dumps({'status': 'passed', 'rounds': 5, 'loops': len(entries),
                      'coreBoundArtifacts': len(bindings),
                      'scope': 'Ordered completion and artifact identity; no physical validation.'}, indent=2))


if __name__ == '__main__':
    main()
