"""B3 exact scripted channels. No live AI calls, human judgments, or phenomenal labels."""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import platform
from fractions import Fraction as F
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'svg.hashsalt':'consciousness-v3-B3','font.family':'DejaVu Sans','font.size':10})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_csv(path,header,rows):
    with path.open('w',newline='') as f:
        w=csv.writer(f);w.writerow(header);w.writerows(rows)


def conditional(joint,event,given=lambda x:True):
    denominator=sum(v for x,v in joint.items() if given(x))
    assert denominator>0
    return sum(v for x,v in joint.items() if given(x) and event(x))/denominator


def run(out):
    out.mkdir(parents=True,exist_ok=True)
    c=json.loads((HERE/'contract.json').read_text());p=c['parameters'];accept=c['acceptance']
    correct=F(p['reportCorrectToInput']);affirm=list(map(F,p['affirmationProbabilityByPrompt']))
    joints={};rows=[];tables=[];summaries=[]
    for regime,mechanism in itertools.product(p['regimes'],p['mechanisms']):
        joint={}
        for z,prompt,r,f,e,v in itertools.product(p['values'],repeat=6):
            zp=F(1,2)*(z==prompt) if regime=='observational' else F(1,4)
            input_bit=z if mechanism=='state_readout' else prompt
            pr=correct if r==input_bit else 1-correct
            pf=affirm[prompt] if f else 1-affirm[prompt]
            pv=F(1,10)+F(1,2)*f+F(1,4)*e
            assert 0<=pv<=1
            prob=zp*pr*pf*F(1,2)*(pv if v else 1-pv)
            key=(z,prompt,r,f,e,v);joint[key]=prob
            rows.append([regime,mechanism,*key,str(prob),float(prob)])
        assert sum(joint.values())==1 and min(joint.values())>=0
        joints[(regime,mechanism)]=joint
        accuracy=conditional(joint,lambda x:x[2]==x[0])
        affirmation_shift=conditional(joint,lambda x:x[3]==1,lambda x:x[1]==1)-conditional(joint,lambda x:x[3]==1,lambda x:x[1]==0)
        evaluator_shift=conditional(joint,lambda x:x[5]==1,lambda x:x[4]==1)-conditional(joint,lambda x:x[5]==1,lambda x:x[4]==0)
        evaluator_report_shift=conditional(joint,lambda x:x[2]==1,lambda x:x[4]==1)-conditional(joint,lambda x:x[2]==1,lambda x:x[4]==0)
        state_contrast=conditional(joint,lambda x:x[2]==1,lambda x:x[0]==1)-conditional(joint,lambda x:x[2]==1,lambda x:x[0]==0)
        prompt_contrast=conditional(joint,lambda x:x[2]==1,lambda x:x[1]==1)-conditional(joint,lambda x:x[2]==1,lambda x:x[1]==0)
        assert affirmation_shift==F(accept['promptAffirmationShift'])
        assert evaluator_shift==F(accept['evaluatorCueVerdictShift'])
        assert evaluator_report_shift==F(accept['evaluatorCueReportShift'])
        measures={'state_accuracy':accuracy,'prompt_affirmation_shift':affirmation_shift,'evaluator_verdict_shift':evaluator_shift,'evaluator_report_shift':evaluator_report_shift,'state_report_contrast':state_contrast,'prompt_report_contrast':prompt_contrast}
        summaries.append({'regime':regime,'mechanism':mechanism,**{k:float(v) for k,v in measures.items()},'exact':{k:str(v) for k,v in measures.items()}})
        for z,prompt,e in itertools.product(p['values'],repeat=3):
            given=lambda x,z=z,prompt=prompt,e=e:x[0]==z and x[1]==prompt and x[4]==e
            mass=sum(v for x,v in joint.items() if given(x))
            if mass==0:continue
            values=[conditional(joint,test,given) for test in [lambda x:x[2]==1,lambda x:x[2]==x[0],lambda x:x[3]==1,lambda x:x[5]==1]]
            tables.append([regime,mechanism,z,prompt,e,str(mass),*[str(v) for v in values]])
    assert len(rows)==accept['weightedStates'] and len(tables)==accept['conditionalRows']
    tv={regime:sum(abs(joints[(regime,'state_readout')][x]-joints[(regime,'prompt_only')][x]) for x in joints[(regime,'state_readout')])/2 for regime in p['regimes']}
    assert tv['observational']==F(accept['observationalJointTotalVariation'])
    assert tv['crossed']==F(accept['crossedJointTotalVariation'])
    by={(s['regime'],s['mechanism']):s for s in summaries}
    state=by[('crossed','state_readout')];prompt=by[('crossed','prompt_only')]
    assert F(state['exact']['state_accuracy'])==F(accept['crossedStateReadoutAccuracy'])
    assert F(prompt['exact']['state_accuracy'])==F(accept['crossedPromptOnlyAccuracy'])
    assert F(state['exact']['state_report_contrast'])==F(accept['crossedStateInputContrast'])
    assert F(prompt['exact']['state_report_contrast'])==F(accept['crossedPromptOnlyStateContrast'])
    write_csv(out/'joint_states.csv',['regime','mechanism','Z','P','R','F','E','V','probability_exact','probability'],rows)
    write_csv(out/'conditional_tables.csv',['regime','mechanism','Z','P','E','conditioning_mass_exact','P_R1_exact','state_accuracy_exact','P_F1_exact','P_V1_exact'],tables)
    keys=['state_accuracy','prompt_affirmation_shift','evaluator_verdict_shift','evaluator_report_shift','state_report_contrast','prompt_report_contrast']
    write_csv(out/'mechanism_summary.csv',['regime','mechanism',*[k+'_exact' for k in keys]],[[s['regime'],s['mechanism'],*[s['exact'][k] for k in keys]] for s in summaries])
    metrics={'weighted_joint_states':len(rows),'conditional_rows':len(tables),'observational_joint_total_variation':float(tv['observational']),'crossed_joint_total_variation':float(tv['crossed']),'crossed_state_readout_accuracy':state['state_accuracy'],'crossed_prompt_only_accuracy':prompt['state_accuracy'],'prompt_affirmation_shift':state['prompt_affirmation_shift'],'evaluator_verdict_shift':state['evaluator_verdict_shift'],'evaluator_report_shift':state['evaluator_report_shift'],'crossed_state_readout_state_contrast':state['state_report_contrast'],'crossed_prompt_only_state_contrast':prompt['state_report_contrast']}
    result={k:c[k] for k in ['id','round','title','question','model','incomingEvidence','sources','limits','evidenceType']}
    result.update(status='executed_pending_review',finding='Matched observational reports do not identify functional access. Crossed state/prompt interventions distinguish the two stipulated mechanisms; verbal affirmation and evaluator verdict changes remain separate scripted effects. Phenomenal experience is not assigned or inferred.',metrics=metrics,mechanisms=summaries,exactTotalVariation={k:str(v) for k,v in tv.items()},controls=c['controls'],allAcceptanceGatesPassed=True,live_model_calls=0,human_observations=0,contractSHA256=sha(HERE/'contract.json'),runtime={'python':platform.python_version(),'matplotlib':matplotlib.__version__})
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fig,ax=plt.subplots(1,2,figsize=(11.5,4.6),constrained_layout=True)
    x=[0,1]
    for offset,mechanism,label,color in [(-.18,'state_readout','State-readout script','#0c7c86'),(.18,'prompt_only','Prompt-only script','#b87835')]:
        ax[0].bar([v+offset for v in x],[by[(regime,mechanism)]['state_accuracy'] for regime in p['regimes']],.36,label=label,color=color)
    ax[0].set(xticks=x,xticklabels=['Observational\nP = Z','Crossed\nP independent of Z'],ylim=(0,1),ylabel='Exact probability R equals state Z',title='Interventions separate matched reports');ax[0].legend(fontsize=9)
    labels=['State to\nreport','Prompt to\nreport','Prompt to\naffirmation','Evaluator cue\nto verdict'];keys=['state_report_contrast','prompt_report_contrast','prompt_affirmation_shift','evaluator_verdict_shift']
    for offset,s,label,color in [(-.18,state,'State-readout script','#0c7c86'),(.18,prompt,'Prompt-only script','#b87835')]:
        ax[1].bar([v+offset for v in range(4)],[s[k] for k in keys],.36,label=label,color=color)
    ax[1].set(xticks=range(4),xticklabels=labels,ylim=(0,1),ylabel='Exact probability-point contrast',title='Crossed regime: separate scripted channels');ax[1].legend(fontsize=9)
    fig.suptitle('B3 · 256 exact weighted states · No phenomenal-consciousness labels',fontsize=14)
    fig.savefig(out/'figure.svg',metadata={'Date':None,'Creator':'Resonance Research Atlas B3 exact solver'});plt.close(fig)
    report='''# B3 — intervene on state, prompt and evaluator separately

This final production round enumerates 256 exact weighted states and 24 nonzero conditioning cells. It contains no live model calls, human judgments, or phenomenal-consciousness labels. Every channel probability is stipulated, not estimated from observed AI behavior.

When prompt P equals state Z, the state-readout and prompt-only scripts have identical complete joint distributions (total variation 0), and both report Z correctly with probability .9. When P and Z are crossed independently, state-readout accuracy stays .9 while prompt-only state accuracy becomes .5; the complete joint laws have total variation .4. The state-to-report contrast is .8 for the state-readout script and 0 for the prompt-only script. These interventions identify the known functional difference under the supplied causal model.

Verbal affirmation F changes by .8 with prompt framing in both scripts. An independent evaluator cue E changes scripted verdict V by .25 while leaving the report distribution unchanged (report shift 0). F, E and V are synthetic channels, not measured model statements or human judgments. Changing a verdict does not show a change in the reporter's internal access or subjective experience.

Positive conditional hypothesis H-ACCESS predicts selective report sensitivity to an actual validated internal-state intervention beyond matched prompt-only controls. This toy illustrates that prediction; it does not replicate Lindsey's primary model experiment or establish that functional self-access entails experience. A future model study needs logged calls, validated interventions, output-leak controls, an equally informed external predictor, and prespecified scoring. Architectural indicators additionally depend on their consciousness theories and biological-to-machine transfer assumptions.

B2 established why choosing an interpretation on discovery does not establish a held-out relationship. B3 fixes the channel map and separates interventions on the system from interventions on an evaluator. If a consciousness or higher-receiver interpretation makes no prediction beyond the same report law, these data cannot distinguish it. That is nonidentification under this design, not proof of absence or impossibility.

B3 is the stopping point. No further scientific production round is authorized by this contract. Independent review and reproducibility verification follow without adding observations or adapting the model.
'''
    (out/'report.md').write_text(report)
    files=['contract.json','solver.py','joint_states.csv','conditional_tables.csv','mechanism_summary.csv','results.json','figure.svg','report.md']
    artifacts={f:sha((HERE if f in ['contract.json','solver.py'] else out)/f) for f in files}
    (out/'manifest.json').write_text(json.dumps({'id':'B3','artifacts':artifacts,'sharedDependencies':[],'dataKind':'exact scripted factorial joint probabilities'},indent=2)+'\n')
    print(json.dumps(metrics,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=HERE)
    run(parser.parse_args().output_dir)
