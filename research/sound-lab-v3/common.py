"""Deterministic evidence output helpers. No acquisition or playback."""
from pathlib import Path
import hashlib, json, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent
plt.rcParams.update({'svg.hashsalt':'sound-lab-v3','font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.grid':True,'grid.alpha':0.2})
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def writejson(path, data): Path(path).write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
def csv(path, names, data): np.savetxt(path,np.asarray(data),delimiter=',',header=','.join(names),comments='',fmt='%.17g')
def savefig(fig, path): fig.tight_layout(); fig.savefig(path,metadata={'Date':None}); plt.close(fig)
def finish(folder, metrics, finding, failedcontrols, report, files, extra=None):
    folder=Path(folder); contract=json.loads((folder/'contract.json').read_text())
    result={'id':contract['id'],'round':contract['round'],'title':contract['title'],'status':'executed_pending_review','evidenceType':contract['evidenceType'],'question':contract['question'],'finding':finding,'metrics':metrics,'failedControls':failedcontrols,'limits':contract['limits'],'sources':contract['sources'],'contractSHA256':sha(folder/'contract.json'),'runtime':{'python':sys.version.split()[0],'numpy':np.__version__,'matplotlib':matplotlib.__version__}}
    if extra: result.update(extra)
    writejson(folder/'results.json',result); (folder/'report.md').write_text(report+'\n')
    artifacts=['contract.json','run.py','results.json','report.md',*files]
    manifest={'id':contract['id'],'artifacts':{p:sha(folder/p) for p in artifacts},'commonSHA256':sha(ROOT/'common.py')}
    writejson(folder/'manifest.json',manifest)
    loops=[]
    for p in sorted(ROOT.glob('S[1-5][AB]/results.json')):
        r=json.loads(p.read_text()); rel=p.parent.relative_to(ROOT.parent.parent).as_posix(); manifest=json.loads((p.parent/'manifest.json').read_text())
        loops.append({k:r[k] for k in ['id','round','title','status','evidenceType','question','finding','metrics','limits','sources']} | {'contractPath':rel+'/contract.json','resultsPath':rel+'/results.json','reportPath':rel+'/report.md','figurePaths':[rel+'/'+f for f in manifest['artifacts'] if f.endswith('.svg')],'rawPaths':[rel+'/'+f for f in manifest['artifacts'] if f.endswith(('.csv','.wav'))],'protocolPath':'research/sound-lab-v3/protocol.md'})
    writejson(ROOT/'summaries.json',{'schemaVersion':1,'program':'Low-material sound measurements','status':'in_progress' if len(loops)<10 else 'executed_pending_final_review','loops':loops})
    print(json.dumps({'id':result['id'],'metrics':metrics,'finding':finding},indent=2))
