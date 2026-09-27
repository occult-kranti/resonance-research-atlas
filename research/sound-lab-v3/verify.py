"""Verify exact output bindings; --regenerate executes each existing frozen runner first."""
from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
records=[]
for folder in sorted(root.glob('S[1-5][AB]')):
    path=folder/'manifest.json'
    if not path.exists(): continue
    frozen=json.loads(path.read_text())
    if '--regenerate' in sys.argv: subprocess.run([sys.executable,str(folder/'run.py')],check=True,stdout=subprocess.DEVNULL)
    for name,digest in frozen['artifacts'].items():
        assert sha(folder/name)==digest,(folder.name,name,'hash mismatch')
    assert sha(root/'common.py')==frozen['commonSHA256'],(folder.name,'common helper changed')
    assert json.loads((folder/'results.json').read_text())['contractSHA256']==sha(folder/'contract.json')
    records.append({'id':folder.name,'boundArtifacts':len(frozen['artifacts']),'manifestSHA256':sha(path)})
from finalize_index import finalize
reviewed=finalize()
print(json.dumps({'status':'passed','loopsVerified':len(records),'reviewedLoops':reviewed,'loops':records,'scope':'Byte reproducibility and contract binding; independent scientific reviews live in docs/panel-v3/reviews.'},indent=2))
