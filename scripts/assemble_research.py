#!/usr/bin/env python3
"""Normalize source-led panel records into the website dataset; do not infer execution."""
from pathlib import Path
import json, shutil
ROOT=Path(__file__).resolve().parents[1]
PANEL=ROOT/'docs/panel'

def sources():
    out=[]
    for p in sorted(PANEL.glob('*sources*.json')):
        d=json.loads(p.read_text());rows=d.get('sources',[]) if isinstance(d,dict) else d
        for s in rows:
            depth=s.get('reading_depth',s.get('readingDepth','Recorded in source packet'))
            category=s.get('claim_category',s.get('provenance',s.get('type','Source record')))
            lead=any(k in (depth+' '+category).lower() for k in ['unaccessed','not read','snippet only','catalogue only','lead','abstract only'])
            kind='Historical primary source'
            lower=(s.get('id','')+' '+category+' '+s.get('title','')).lower()
            if 'patent' in lower or s.get('id','').startswith('PAT'): kind='Patent proposal'
            elif 'fringe' in lower or 'reddit' in lower or s.get('id') in ['H14','H15']: kind='Discourse lead'
            elif any(x in lower for x in ['fda','nasa','fbi','government']): kind='Government record'
            elif any(x in lower for x in ['dataset','software','database','documentation']): kind='Data or tool'
            elif s.get('id','').startswith(('SR','BIO','PH','DREAM','DR-','SLP','OBE')) or s.get('id') in ['H10','H11','H12']: kind='Modern primary research'
            ev='hypothesis' if lead else 'documented'
            if kind=='Discourse lead': ev='unsupported'
            if kind=='Modern primary research' and not lead: ev='preliminary'
            out.append({'id':s['id'],'title':s['title'],'author':s.get('author',s.get('provenance','')),'year':s.get('date',s.get('year','')),'url':s['url'],'type':kind,'evidence':ev,'summary':s.get('summary',s.get('supports',s.get('claim','Source scope is recorded in the reading note.'))),'claim':category,'section':s.get('sections_read',s.get('passages_read',s.get('sections',''))),'readingDepth':depth,'verifiedAt':s.get('accessed','2026-09-26'),'limitations':s.get('unresolved',s.get('verification_remaining',s.get('limitations',s.get('does_not_support',''))))})
    unique={s['id']:s for s in out}
    return list(unique.values())

def result_round(n):
    folder=ROOT/'research'/f'round{n}'
    path=folder/'results.json'
    data=json.loads(path.read_text()) if path.exists() else {}
    review=folder/'independent-review.json'
    checked=json.loads(review.read_text()) if review.exists() else {}
    ledger=ROOT/'research/panel-decisions.json'
    decisions=json.loads(ledger.read_text()).get('rounds',[]) if ledger.exists() else []
    accepted=any(r.get('round')==n and r.get('status')=='accepted' for r in decisions)
    status='Executed; independent review accepted' if data and checked and accepted else ('Executed; review pending' if data else 'Planned')
    return status,data,checked

specs=[
 ('R1','Resonance and complete energy accounting','Tesla · mechanics','Can passive resonance amplify displacement while every joule remains accounted for?','Two coupled damped masses. Multiply the equation of motion by velocity and compare the exact energy identity with numerical quadrature.','Zero input, zero coupling, damping, detuning and timestep refinement.','Finite linear mechanical model only; not clinical efficacy, a physical prototype or a new law.',['TES-1898','TES-1901'],'resonance'),
 ('R2','A peak is not a pole','Tesla · Schumann interpretation','Can changing the readout move a spectral maximum without changing the oscillator?','Compare displacement and velocity transfer functions, source compensation and a calibrated positive control.','Fixed poles; alternative source and detector; recover the pole only under declared calibration.','A lossy single-mode surrogate, not an Earth–ionosphere propagation solver.',['TES-1905','SR-2011','SR-2026'],'schumann'),
 ('R3','Decipherment needs an identifying measurement','Newton · alchemy','Can different compositions give identical observable signs?','A synthetic linear observation map with two channels and three unknown relative amounts. Exhibit the entire nonnegative ambiguity family.','Duplicate third assay versus an independent assay. Report domain dimension, rank and nullity.','Synthetic components are not identified with Newton reagents; no historical compound is recovered.',['H01','H02','H16'],'mixture'),
 ('R4','How independent is an added assay?','Newton · measurement design','Does formal full rank remain useful under measurement noise?','Extend the previous inverse problem with controlled near-dependent assays and declared perturbation scales.','Compare duplicate, nearly dependent and genuinely independent measurements.','Toy measurement uncertainty does not calibrate a real spectrometer or historical manuscript.',['H01','H13'],'mixture'),
 ('R5','Patterns selected after looking','Jung · prophecy · statistical controls','How does choosing the most striking result change a false-positive claim?','Freeze a search family and compare single-test and family-level null behavior with a prespecified correction.','Report every tested candidate and failed match; separate exploratory selection from held-out assessment.','Tests a declared statistical toy model, not all symbolic interpretation or the truth of a prophecy.',['H04','H05','H13'],'selection'),
 ('R6','Lucid dreaming and astral-travel claims','Dream research · final session','Which observations distinguish dream awareness, an out-of-body report and correct hidden-target information?','Source-led normal-sleep observation protocol plus a fixed four-choice chance model for a separately preregistered target experiment.','No feedback before recording; independent target handling; fixed trial count; no selective scoring or optional stopping.','No human trial or astral travel is demonstrated. Laboratory dream communication does not establish extracorporeal perception.',[],'dreams'),
]

def main():
    S=sources();ids={s['id'] for s in S}
    ledger=ROOT/'research/panel-decisions.json'
    decisions={r['round']:r for r in json.loads(ledger.read_text()).get('rounds',[])} if ledger.exists() else {}
    experiments=[];rounds=[]
    for i,(rid,title,domain,q,m,ctrl,lim,src,model) in enumerate(specs,1):
        status,data,review=result_round(i)
        artifacts=[]
        folder=ROOT/'research'/f'round{i}'
        for name,label in [('contract.md','Frozen contract'),('results.json','Numerical results'),('interpretation.md','Derivation and limits'),('independent-review.json','Independent model-agent review')]:
            if (folder/name).exists(): artifacts.append({'label':label,'url':f'research/round{i}/{name}'})
        svgs=sorted(folder.glob('*.svg')) if folder.exists() else []
        for p in svgs[:3]:artifacts.append({'label':p.stem.replace('_',' ').title(),'url':f'research/round{i}/{p.name}'})
        src=[x for x in src if x in ids]
        if i==6:src=[s['id'] for s in S if s['id'].startswith(('DREAM','DR-','SLP','OBE','LUC'))]
        experiments.append({'id':rid,'title':title,'domain':domain,'status':status,'evidence':'computed within model' if 'accepted' in status else 'hypothesis','summary':q,'question':q,'method':m,'prediction':ctrl,'limitations':lim,'safety':'Computational investigation; no human exposure or hazardous chemical recreation.','sourceIds':src,'modelId':model,'artifacts':artifacts})
        decision=decisions.get(i,{})
        findings=[decision.get('finding','Read the linked result and review files for numerical values and tolerances.')] if data else ['Execution follows the previous round’s review.']
        rounds.append({'id':rid,'title':title,'status':status,'participants':['Advisor / independent skeptic','Research producer','Source researcher'],'question':q,'artifacts':artifacts,'findings':findings,'decisions':[decision.get('scope',lim),lim],'next':[decision.get('nextReason','The next round is selected from the unresolved measurement or inference limitation.')] if i<6 else ['Final focused session; subsequent human research remains unexecuted.']})
    experiments.extend([
      {'id':'P1','title':'Frequency-dependent coupling in an inert phantom','domain':'Tesla · proposed nonclinical study','status':'Protocol only; not executed','evidence':'hypothesis','summary':'Separate deposited energy and heating from a claim of healing.','question':'Does a preregistered load model predict changes in absorbed energy after accounting for accepted input power?','method':'Characterized inert phantom and instrument transfer model; source-off, dummy-load and heat-only controls.','prediction':'Normalized energy deposition should follow the stated coupling model; instrumentation artifacts must fail validity gates.','limitations':'A phantom has no clinical endpoint. Frequency-dependent absorption is not healing.','safety':'Computational/nonclinical specification only, with no human-exposure construction procedure.','sourceIds':[x for x in ['TES-1898','PH-FDA-MDDT','PH-SIMNIBS','PH-AE2026'] if x in ids],'artifacts':[{'label':'Protocol and apparatus map','url':'docs/panel/tesla-phantom-protocol.md'}]},
      {'id':'P2','title':'Audit a purported reactionless device','domain':'Tesla · momentum / antigravity','status':'Next research candidate; not executed','evidence':'hypothesis','summary':'Include the apparatus, environment and fields in the momentum budget.','question':'Does measured thrust persist when ion flow, cables, vibration and external-field forces are controlled?','method':'Source and momentum audit of a concrete patent, then a complete mechanical or electromagnetic model.','prediction':'An internal-mass model conserves total momentum; atmospheric ion motion provides an alternative to gravity reduction.','limitations':'The selected NASA experiment and patent descriptions do not establish a blanket verdict on every device.','safety':'No high-voltage build instructions or human exposures.','sourceIds':[x for x in ['NASA-ACT2004','PAT-PAIS2018','PAT-2026'] if x in ids]},
    ])
    history=[
      {'id':'N1','title':'Clavis: copied authority, not original authorship','person':'Newton / Starkey','summary':'The inherited dossier misattributed Clavis. Scholarly source criticism identifies it as part of Starkey’s letter to Boyle, copied by Newton. Authorship must be resolved before building an interpretation.','evidence':'documented','sourceIds':[x for x in ['H16','H17'] if x in ids]},
      {'id':'N2','title':'Star, net, tree: compare mechanisms','person':'Newton','summary':'Crystalline facets, reticular alloy surfaces and branching growth need their own textual contexts and diagnostic measurements. A similar shape does not uniquely identify a composition or cause.','evidence':'hypothesis','sourceIds':[x for x in ['H01','H02','H16'] if x in ids]},
      {'id':'N3','title':'Why 2060 appears in a manuscript','person':'Newton','summary':'The date follows a conditional theological chronology: 800 + 1260. The passage allows a later end and argues against rash date-setting; it is not a calibrated physical forecast.','evidence':'documented','sourceIds':['H05']},
      {'id':'T1','title':'Tesla’s electrotherapy observations','person':'Tesla','summary':'The historical lecture describes coupling, retuning, personal effects and uncertainty. Its useful engineering questions can be modeled without converting anecdote into clinical evidence.','evidence':'documented','sourceIds':['TES-1898']},
      {'id':'J1','title':'Symbols as a declared dictionary','person':'Jung / Pauli','summary':'Treat meaningful symbolic patterns as interpretations. Declare coding rules and preserve misses before testing an external predictive claim. Individual Jung–Pauli correspondence remains an incompletely accessed reading lead.','evidence':'hypothesis','sourceIds':[x for x in ['H06','H07','H08','H09'] if x in ids]},
      {'id':'PEN','title':'Geometry and model-specific limits','person':'Penrose','summary':'Gravitational state-reduction proposals require an explicit model and model-specific experimental bounds. Abstract-level reading does not verify the full derivation, and these proposals do not define a universal human frequency.','evidence':'preliminary','sourceIds':[x for x in ['H10','H11','H12'] if x in ids]},
      {'id':'FEY','title':'Publish the damaging control','person':'Feynman','summary':'Keep the duplicate-assay failure, source-off result and alternative explanations beside successful predictions. Repeated execution of one implementation is not independent reasoning.','evidence':'documented','sourceIds':['H13']},
    ]
    roadmap=[{'id':f'G{i}','title':x[1],'status':rounds[i-1]['status'],'owner':'Advisor + assigned researcher','dependsOn':[f'G{i-1}'] if i>1 else [],'detail':x[3]} for i,x in enumerate(specs,1)]
    roadmap += [
      {'id':'G7','title':'Trace primary alchemical cover-names across manuscripts','status':'Planned','owner':'Historical source team','dependsOn':['G3','G4'],'detail':'Collate original images, dated textual context and specialist modern reconstructions. Retain contradictory meanings; do not infer identity from a symbol alone.'},
      {'id':'G8','title':'Analyze a licensed multichannel physiological dataset','status':'Planned; no patient data analyzed','owner':'Measurement researcher','dependsOn':['G2','G4'],'detail':'Freeze channels, time windows, sensor units, filtering, artifact exclusions and held-out prediction before analysis.'},
      {'id':'G9','title':'Complete source scans and patent-family audits','status':'Planned','owner':'Source researchers','dependsOn':['G1','G5'],'detail':'Authenticate Tesla magazine facsimiles, inspect government scans and distinguish granted claims from performance records.'},
      {'id':'G10','title':'Independent external replication','status':'Not started','owner':'Qualified external reviewers','dependsOn':['G6'],'detail':'Model-agent review is not human peer review or a performed biological experiment.'},
    ]
    nodes=[{'id':s['id'],'label':s['title'],'type':'source','summary':s['summary'],'sourceIds':[s['id']]} for s in S]
    edges=[]
    for ex in experiments:
        nodes.append({'id':ex['id'],'label':ex['title'],'type':'experiment','summary':ex['limitations'],'sourceIds':ex['sourceIds']})
        edges += [{'source':sid,'target':ex['id'],'type':'inspires','label':'Motivates a question; does not prove the result','sourceIds':[sid]} for sid in ex['sourceIds']]
    for h in history:
        nid='history-'+h['id'];nodes.append({'id':nid,'label':h['title'],'type':'interpretation','summary':h['summary'],'sourceIds':h['sourceIds']})
        edges += [{'source':sid,'target':nid,'type':'documents' if h['evidence']=='documented' else 'informs','label':'Source scope and reading depth remain applicable','sourceIds':[sid]} for sid in h['sourceIds']]
    edges += [{'source':f'R{i}','target':f'R{i+1}','type':'motivates','label':'Unresolved limitation selects next investigation','sourceIds':[]} for i in range(1,6)]
    projects=[
      {'name':'OpenSync · primary audio laboratory','url':'https://occult-kranti.github.io/brainwave_opensync/','role':'Presets, harmonic composition, analysis and shared audio safety controls.','status':'Existing app, extended in this release'},
      {'name':'Open Sync · imported sound suite','url':'https://occult-kranti.github.io/brainwave_opensync/open-sync/','role':'Complete second application preserved under the primary deployment.','status':'Integrated subapp'},
      {'name':'Resonant Vessels · corrected research','url':'projects/resonant-vessels/research-corrections.html','role':'Start with source corrections, then explore the amended original folios and concept plates.','status':'Corrected first-draft exhibit'},
      {'name':'Historical astronomy & astrology workbench','url':'projects/astrology-sim-ant/index.html','role':'Astronomical calculations and historical interpretive systems. Calculation accuracy does not validate astrology predictions.','status':'Pinned complete import'},
      {'name':'Newton–Tesla archive · original dossiers','url':'archive/newton-tesla-alchemy/README.md','role':'Original owner-supplied research, retained for comparison with this release’s corrections.','status':'Inherited source archive, not fully revalidated'},
    ]
    D={'meta':{'title':'Resonance Research Atlas','subtitle':'Historical ideas. Explicit models. Observable tests.','updated':'2026-09-26','status':'Six adaptive investigations; computation and source review only'},'experiments':experiments,'sources':S,'dreams':{'summary':'Round 6 examines dream awareness, out-of-body reports and concealed-target claims as distinct endpoints. No human trial was performed.','sourceIds':[s['id'] for s in S if s['id'].startswith(('DREAM','DR-','SLP','OBE','LUC'))],'protocol':['Keep an ordinary sleep schedule; choose one neutral intention to remember a dream.','On spontaneous waking, record the report before viewing prompts, targets or interpretations.','Record whether you knew you were dreaming and any sense of body location as separate observations.','Keep failed recall and uneventful nights; review the complete record without selecting only striking matches.','A concealed-target study needs a separate controlled protocol and independent target handling; this static site demonstrates the null only.'],'limitations':['No sleep deprivation, forced awakenings or stimulation schedule is prescribed.','A vivid or meaningful experience does not by itself verify information obtained outside the body.','Diary content remains on the device and is exported only on request.']},'history':history,'rounds':rounds,'roadmap':roadmap,'network':{'nodes':nodes,'edges':edges},'projects':projects}
    from assemble_nanoparticles import attach
    D = attach(D)
    (ROOT/'data').mkdir(exist_ok=True)
    (ROOT/'data/research.json').write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'sources':len(S),'experiments':len(experiments),'rounds':len(rounds),'network_nodes':len(nodes),'network_edges':len(edges)}))
if __name__=='__main__': main()
