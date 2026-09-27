"""Bind an advisor verdict to reviewed artifacts and update the decision ledger.
Internal recording helper; numeric checks live in reviewer.py.
"""
from pathlib import Path
import hashlib,json,inspect
ROOT=Path(__file__).resolve().parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def record(id, evidence, accepted, withheld, next_decision, method, folder=None):
    folder=ROOT/(folder or ('research/sound-lab-v3/'+id))
    c=json.loads((folder/'contract.json').read_text());r=json.loads((folder/'results.json').read_text())
    binding={p.relative_to(ROOT).as_posix():sha(p) for p in sorted(folder.iterdir()) if p.is_file()}
    manifest=folder/'manifest.json'
    if manifest.exists():
        for name in json.loads(manifest.read_text()).get('artifacts',{}):
            dependency=(folder/name).resolve();binding[dependency.relative_to(ROOT).as_posix()]=sha(dependency)
    common=folder.parent/'common.py'
    if common.exists():binding[common.relative_to(ROOT).as_posix()]=sha(common)
    order=[f'S{n}{x}' for n in range(1,6) for x in 'AB']+['B1','B2','B3']
    sequence=order.index(id)+1
    if sequence==1:
        predecessor={'id':'P3','record':'docs/panel-v3/planning-panels.md','status':'completed_before_S1A_execution'}
    else:
        prev=order[sequence-2];prevpath=ROOT/'docs/panel-v3/reviews'/f'{prev}-review.json'
        assert prevpath.exists(), f'Predecessor review missing: {prev}'
        predecessor={'id':prev,'reviewPath':prevpath.relative_to(ROOT).as_posix(),'reviewSHA256':sha(prevpath),'status':json.loads(prevpath.read_text())['status']}
    import reviewer
    checker=getattr(reviewer,'review_'+id.lower(),None)
    checker_sha=hashlib.sha256(inspect.getsource(checker).encode()).hexdigest() if checker else None
    review={'id':id,'sequence':sequence,'predecessor':predecessor,'checkerFunction':'review_'+id.lower(),'checkerFunctionSHA256':checker_sha,'status':'accepted_narrow','reviewer':'/root/advisor_v3 (correlated model agent; independent implementation/derivation, not human peer review)','reviewMethod':method,'independentChecks':evidence,'acceptedClaim':accepted,'withheld':withheld,'nextDecision':next_decision,'bindings':binding}
    out=ROOT/'docs/panel-v3/reviews'/f'{id}-review.json';out.write_text(json.dumps(review,indent=2)+'\n')
    ledger=ROOT/'research/panel-v3-decisions.json';d=json.loads(ledger.read_text())
    entry={'id':id,'sequence':sequence,'predecessor':predecessor,'round':r.get('round',id),'title':r.get('title',c.get('title',id)),'status':'accepted_narrow','evidenceType':r.get('evidenceType','synthetic'),'question':r.get('question',c.get('question','')),'finding':accepted,'scope':c.get('model',''),'withheld':withheld,'incomingEvidence':c.get('incomingEvidence',''),'nextDecision':next_decision,'metrics':r.get('metrics',{}),'sources':r.get('sources',c.get('sources',[])),'contractPath':(folder/'contract.json').relative_to(ROOT).as_posix(),'resultsPath':(folder/'results.json').relative_to(ROOT).as_posix(),'reviewPath':out.relative_to(ROOT).as_posix(),'reportPath':(folder/'report.md').relative_to(ROOT).as_posix(),'figurePaths':[p.relative_to(ROOT).as_posix() for p in folder.glob('*.svg')],'rawPaths':[p.relative_to(ROOT).as_posix() for p in folder.glob('*.csv')],'resultSHA256':sha(folder/'results.json'),'contractSHA256':sha(folder/'contract.json'),'independentChecks':evidence}
    d['reviews']=[e for e in d['reviews'] if e['id']!=id]+[entry];d['completedSoundLoops']=sum(e['id'].startswith('S') for e in d['reviews']);d['completedLaterRounds']=sum(e['id'].startswith('B') for e in d['reviews']);d['nextAuthorized']=next_decision;ledger.write_text(json.dumps(d,indent=2)+'\n');write_report(d);return review

def write_report(d):
    reviews=sorted(d['reviews'],key=lambda r:r['sequence'])
    lines=['# Advisor review: sound and conditional consciousness continuation','',f"Accepted narrow computational reviews: **{len(reviews)} of 13**. Sound loops: {sum(r['id'].startswith('S') for r in reviews)} of 10; later conditional rounds: {sum(r['id'].startswith('B') for r in reviews)} of 3. The three actual planning panels are recorded in [planning-panels.md](planning-panels.md).",'',
    'The work uses separate producer, source and advisor model agents with correlated model-family provenance. Historical names denote documented methodological lenses, not participation, endorsement or human peer review. The original six rounds and five nanoparticle rounds remain frozen.','',
    'Accepted means the bounded model, generated-file calculation or software admission claim survived its specified independent check. Generated PCM is real file data produced by code; it is not a physical microphone recording. No hardware study, live-AI experiment, subjective-experience measurement, healing effect or metaphysical connection is established.','',
    '| ID | Accepted narrow finding | Review |','|---|---|---|']
    for r in reviews: lines.append(f"| {r['id']} | {r['finding']} | [Independent check](reviews/{r['id']}-review.json) |")
    lines += ['', '## Adaptive decisions and retained failures','',
    '- P2 removed unsupported H1 terminology and physical factor identification, added exact equivalent factorizations, and kept the later reporter study distinct from original R6.',
    '- S1B followed the missing stable-chain premise in S1A; S2 added generated recording intake and an exact gain/decay ambiguity.',
    '- Amendment A1 changed the original post-S2B spatial suggestion to S3A protected intake after a coordinator found potential raw-CSV overwrite and an ignored channel argument. The frozen historical fitter is a reproduction dependency; the current intake wrapper protects original files.',
    '- S3B retained a syntax-failure attempt and a substantive failed control: its first nonuniform-timestamp test accidentally hit an output-collision gate. The producer preserved the prior artifacts, used a separate output path, asserted the actual reason and reran the unchanged contract. The advisor independently exercised the corrected timestamp gate.',
    '- S4 returned to spatial information only after intake and timebase checks. Its hardware phase requirement led S5 to a feasible scalar tap comparison with counterbalanced order and a complete batch dry run.',
    '- S5B first admitted empty or one-condition plans as complete. The coordinator rejected that admission claim; the initial implementation/evidence were preserved, nonempty A/B/count guards were added before output creation, and independent actual CLI controls verified the repair under the same scientific contract.',
    '- Future selections are permitted only after the preceding verdict. The machine ledger records predecessor hashes and the explicit amendment; supporting source searches, images and release checks are not additional research loops.','',
    '## Evidence and limits','',
    'Each review binds exact producer contract, code, result, raw artifacts and shared dependencies. The advisor checker uses separate polynomial, algebraic, cycle-shift, counting or data-path checks rather than merely trusting a passing producer assertion. Whole-checker and source-ledger identities are frozen at final completion. Code and data bindings establish which computation was reviewed; they do not establish source authenticity or empirical calibration.','',
    'Reading depth and source category are explicit in [historical sources](sources-history.json), [modern sources](sources-modern.json) and [consciousness sources](sources-consciousness.json). Selected full-text passages, abstracts, catalog entries and cultural discourse remain distinct. A patent or archived proposal is evidence that a proposal exists, not that it works.','',
    'The detailed [next-gates roadmap](next-gates.md) lists prerequisites, discriminating observations and stop rules; those proposed gates are not additional executed rounds.', '',
    'Future physical work needs an independent pilot, a new locked plan, raw recordings, declared impact alignment, device/processing/clock information, reference repeats and retained exclusions. Future live-AI work needs actual logged model calls, independent target custody, fixed scoring and controls for ordinary information paths. Neither future program has been performed here.','']
    if len(reviews)==13:
        lines.insert(4,'The finite program is complete: three actual planning panels, ten sequential sound loops and three later conditional rounds. Research stopped after B3; publication verification is a separate integration gate.')
        lines.insert(5,'')
        lines=[line.replace('Future selections are permitted only after the preceding verdict.', 'Every selection followed the preceding verdict; no further research round is selected.').replace('Whole-checker and source-ledger identities are frozen at final completion.', 'Whole-checker and source-ledger identities are frozen in the completed decision ledger.') for line in lines]
    (ROOT/'docs/panel-v3/advisor-review.md').write_text('\n'.join(lines))
