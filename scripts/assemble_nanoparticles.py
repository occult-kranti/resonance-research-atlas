"""Append the five-round extension without reclassifying the original six rounds."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / 'docs/panel-nanoparticles'

def text(value):
    if isinstance(value, list):
        return '; '.join(map(str, value))
    return str(value or '')

def attach(data):
    ledger_path = ROOT / 'research/nanoparticle-panel-decisions.json'
    if not ledger_path.exists():
        return data
    ledger = json.loads(ledger_path.read_text())
    added = []
    for path in sorted(PANEL.glob('sources-*.json')):
        packet = json.loads(path.read_text())
        for s in packet['sources']:
            depth = text(s.get('reading_depth'))
            kind = s['type']
            limited = any(x in depth.lower() for x in ['abstract', 'not read', 'blocked', 'lead', 'catalog'])
            evidence = 'unsupported' if kind == 'Discourse lead' else ('hypothesis' if limited else 'documented')
            if kind == 'Modern primary research' and not limited:
                evidence = 'preliminary'
            added.append(dict(id=s['id'],title=s['title'],author=s.get('author',s.get('provenance','')),
                year=s.get('date',''),url=s['url'],type=kind,evidence=evidence,
                summary=text(s.get('summary',s.get('supports'))),claim=text(s.get('claim_category',kind)),
                section=text(s.get('sections_read')),readingDepth=depth,verifiedAt=s.get('accessed','2026-09-26'),
                limitations=text(s.get('does_not_support',s.get('limitations')))))
    existing = {s['id'] for s in data['sources']}
    assert not existing.intersection(s['id'] for s in added), 'Source IDs must be unique'
    data['sources'].extend(added)
    source_ids = {s['id'] for s in data['sources']}
    specs = json.loads((PANEL / 'round-specifications.json').read_text())
    rounds = []
    for d in ledger['rounds']:
        n = d['round']; spec = specs.get(str(n), {})
        folder = ROOT / f'research/nanoparticles/round{n}'
        results = folder / 'results.json'; review = folder / 'independent-review.json'
        accepted = d['status'] == 'accepted' and results.exists() and review.exists()
        status = 'Executed; independent review accepted' if accepted else ('Executed; review pending' if results.exists() else d['status'].capitalize())
        artifacts = []
        labels = {'contract.md':'Frozen contract','results.json':'Numerical results','interpretation.md':'Derivation and limits',
                  'independent-review.json':'Independent model-agent review','solver.py':'Reproducible solver','sources.md':'Source reading record',
                  'bibliographic-erratum.md':'Transparent bibliography correction','inputs.json':'Frozen production input hashes'}
        if folder.exists():
            for name,label in labels.items():
                if (folder/name).exists(): artifacts.append(dict(label=label,url=f'research/nanoparticles/round{n}/{name}'))
            for p in sorted(folder.glob('*.svg')):
                artifacts.append(dict(label=p.stem.replace('_',' ').title(),url=f'research/nanoparticles/round{n}/{p.name}'))
            for p in sorted(folder.glob('*.csv*')):
                artifacts.append(dict(label=p.name+' · data',url=f'research/nanoparticles/round{n}/{p.name}'))
            for p in sorted((folder/'assets').glob('*')):
                if p.suffix in ['.wav','.json']:
                    artifacts.append(dict(label=p.stem.replace('-',' ').title()+(' · actual WAV' if p.suffix=='.wav' else ' · export manifest'),url=f'research/nanoparticles/round{n}/assets/{p.name}'))
        refs = d.get('sourceIds',spec.get('sourceIds',[]))
        assert set(refs) <= source_ids, f'Unknown source in N{n}'
        rounds.append(dict(id=f'N{n}',title=spec.get('title',d['scope']),status=status,
            evidence='computed within model' if accepted else 'hypothesis',question=spec.get('question',d['scope']),
            hypothesis=d.get('projectHypothesis',spec.get('hypothesis','Awaiting the preceding review.')),
            rivals=spec.get('rivals',[]),falsifiers=spec.get('falsifiers',[]),method=d['scope'],
            findings=[d['finding']] if d.get('finding') else [],
            decisions=[x for x in [d.get('designImprovement'),d.get('novelty'),d.get('nextReason')] if x],
            limitations=[x for x in [d.get('empiricalWork'),('Not established: '+d['withheld']) if d.get('withheld') else None,spec.get('limitations')] if x],
            sourceIds=refs,artifacts=artifacts,modelId=spec.get('modelId','')))
    roadmap = [dict(id=r['id'],title=r['title'],status=r['status'],owner='Producer + independent advisor',
        dependsOn=[f'N{i}'] if i else [],detail=r['question']) for i,r in enumerate(rounds)]
    roadmap.extend([
        dict(id='NS',title='Historical and modern source lanes',status='Selected passages reviewed; incomplete leads retained',owner='Two source agents',dependsOn=[],detail='Primary manuscripts, empirical papers, patents and fringe-to-primary trails; publish reading depth and disagreements.'),
        dict(id='NA',title='OpenSync digital calibration bench',status='Completed implementation; digital outputs only',owner='Audio coder + verification',dependsOn=['N1','N2'],detail='Compare two-tone, AM, baseband and carrier controls; measure rendered samples and export WAV plus manifest.'),
        dict(id='NH',title='Qualified sealed-reference measurements',status='Proposed; not performed',owner='Future laboratory collaborators',dependsOn=['N5'],detail='Select one falsifiable proposal, characterize its sample and apparatus, preregister uncertainty and acquire independent measurements.'),
        dict(id='NR',title='External replication and peer review',status='Not started',owner='Independent human researchers',dependsOn=['NH'],detail='Model-agent agreement is not external scientific replication.'),
    ])
    cards = [
        dict(id='nano-code',title='Reproduce the five numerical rounds',kind='code',status='See per-round acceptance',summary='Frozen contracts, source-bound equations, raw data, scientific plots and independent reviews.',sourceIds=[],artifacts=[dict(label='Research program and reproduction',url='research/nanoparticles/README.md'),dict(label='Panel decisions',url='docs/nanoparticles-panel-review.md')]),
        dict(id='nano-hardware',title='Four nonclinical measurement stations',kind='hardware-proposal',status='Proposed; not built',summary='Magnetic phase, calibrated thermal response, optical absorption and acoustic mechanism controls.',sourceIds=['NANO-ROS2002','NANO-SKIN2025','NANO-PAVL2025'],artifacts=[dict(label='Observables, controls and apparatus logic',url='docs/panel-nanoparticles/hardware-concepts.md'),dict(label='Source-grounded mechanism derivations',url='docs/panel-nanoparticles/modern-mechanisms.md')]),
        dict(id='nano-history',title='Six historical ideas made testable',kind='hardware-proposal',status='New project proposals; no physical execution',summary='Color and material ambiguity, particle-count bias, harmonic rank, and complete energy/momentum boundaries.',sourceIds=['NH01','NH02','NH03','NH10','NH17','NH20','NH21'],artifacts=[dict(label='Hypotheses, alternatives and falsifiers',url='docs/panel-nanoparticles/historical-hypotheses.md')]),
    ]
    for p in sorted((ROOT/'assets/diagrams').glob('history-nano-*.svg')):
        cards[-1]['artifacts'].append(dict(label=p.stem.replace('history-nano-','').replace('-',' ').title(),url=f'assets/diagrams/{p.name}'))
    for s in added:
        data['network']['nodes'].append(dict(id=s['id'],label=s['title'],type='source',summary=s['summary'],sourceIds=[s['id']],program='nanoparticles'))
    for r in rounds:
        data['network']['nodes'].append(dict(id=r['id'],label=r['title'],type='experiment',summary=r['hypothesis'],sourceIds=r['sourceIds'],program='nanoparticles'))
        data['network']['edges'].extend(dict(source=s,target=r['id'],type='informs',label='Source informs a declared model; does not establish a measured result',sourceIds=[s]) for s in r['sourceIds'])
    for i in range(1,5):
        data['network']['edges'].append(dict(source=f'N{i}',target=f'N{i+1}',type='motivates',label='Preceding review selects the next question',sourceIds=[]))
    for c in cards[1:]:
        data['network']['nodes'].append(dict(id=c['id'],label=c['title'],type='experiment',summary=c['summary'],sourceIds=c['sourceIds'],program='nanoparticles'))
        data['network']['edges'].extend(dict(source=s,target=c['id'],type='inspires',label='Proposed test, not performed experiment',sourceIds=[s]) for s in c['sourceIds'])
    historical_proposals = [
        ('A','Loss per cycle versus heating per time','Compare energy per cycle and power under the same declared drive constraint; actual field transfer is a rival explanation.',['NH22','NH09'],'N1'),
        ('B','Particle count needs the correct size moment','Compare the number-weighted mean volume with the volume of a mean diameter; density and distribution weighting require independent checks.',['NH17','NH18'],'N4'),
        ('C','Optical strength can hide radius and contrast','A second independently sensitive measurement must distinguish the declared radius/contrast ambiguity; RGB alone does not identify a material.',['NH01','NH04','NH07','NH19'],None),
        ('D','Color change has competing material causes','Joint elemental recovery, dissolved fraction and count/size measurements distinguish aggregation, dissolution, deposition and medium effects.',['NH02','NH04','NH05','NH17'],None),
        ('E','Additional harmonics need independent information','At equal resources, compare noise-whitened sensitivities and held-out predictions with duplicate and miscalibrated channels.',['NH20'],None),
        ('F','Audit force and energy boundaries','Separate powered suspension from gravity change, and stored-energy release from source-free output; include environmental forces and uncertainty.',['NH10','NH11','NH21'],None),
    ]
    for key,title,summary,refs,round_id in historical_proposals:
        nid='nano-HN-'+key
        data['network']['nodes'].append(dict(id=nid,label=title,type='interpretation',summary='Modern proposal: '+summary,sourceIds=refs,program='nanoparticles'))
        data['network']['edges'].extend(dict(source=s,target=nid,type='informs',label='Selected source motivates an operational hypothesis',sourceIds=[s]) for s in refs)
        if round_id:
            data['network']['edges'].append(dict(source=nid,target=round_id,type='motivates',label='A restricted synthetic case is tested; physical proposal remains unexecuted',sourceIds=refs))
    data['nanoparticles'] = dict(summary='Five additional adaptive investigations turn frequency claims into specified fields, particle models and calibrated measurements. Six earlier investigations remain intact.',
        updated='2026-09-26',status=ledger['status'],sourceIds=[s['id'] for s in added],rounds=rounds,roadmap=roadmap,
        models=[dict(id=r['modelId'],title=r['title'],status=r['status'],sourceIds=r['sourceIds'],assumptions=[r['method']],limitations=r['limitations']) for r in rounds if r['modelId']],
        labCards=cards,links=[dict(label='OpenSync audible NanoLab',url='https://occult-kranti.github.io/brainwave_opensync/nano-lab/'),dict(label='Parallel roadmap and methods',url='docs/nanoparticle-roadmap.md'),dict(label='Source and review packets',url='docs/panel-nanoparticles/historical-hypotheses.md')])
    data['meta']['status']='Six original investigations plus five nanoparticle and frequency rounds; computation and source review only'
    return data
