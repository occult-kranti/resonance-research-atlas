"""Overlay independent review status without editing any frozen producer artifact."""
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def finalize():
    index=json.loads((root/'summaries.json').read_text());ledger=json.loads((root.parent/'panel-v3-decisions.json').read_text());reviews={r['id']:r for r in ledger['reviews']}
    count=0
    for loop in index['loops']:
        producer=json.loads((root/loop['id']/'results.json').read_text());loop['producerStatus']=producer['status'];loop['status']=producer['status']
        review=reviews.get(loop['id'])
        if review and review['status']=='accepted_narrow':
            assert sha(root/loop['id']/'results.json')==review['resultSHA256'],(loop['id'],'review does not bind current result')
            loop['status']='accepted_narrow';loop['reviewPath']=review['reviewPath'];loop['reviewedFinding']=review['finding'];count+=1
    index.update({'status':'completed_reviewed_narrow' if count==10 else 'review_in_progress','completedLoops':count,'requiredLoops':10,'empiricalBoundary':'Generated simulations and WAV bytes only; no physical apparatus or participant measurements.','intakePath':'research/sound-lab-v3/intake_v2.py','batchIntakePath':'research/sound-lab-v3/batch_intake.py','preregistrationPath':'research/sound-lab-v3/S5A/preregistration.json','batchExampleManifestPath':'research/sound-lab-v3/S5B/complete-manifest.json'})
    (root/'summaries.json').write_text(json.dumps(index,indent=2,allow_nan=False)+'\n');return count
if __name__=='__main__':print(json.dumps({'reviewedSoundLoops':finalize()}))
