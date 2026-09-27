"""Exact finite B2 score selection audit; no human data or model calls."""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import platform
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
plt.rcParams.update({'svg.hashsalt': 'consciousness-v3-B2', 'font.family': 'DejaVu Sans', 'font.size': 10})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def write_csv(path, header, rows):
    with path.open('w', newline='') as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    c = json.loads((HERE / 'contract.json').read_text())
    p = c['parameters']; reports = p['reports']; shifts = p['shifts']; alpha = F(p['alpha'])
    targets = sorted(set(itertools.permutations([k for k, n in enumerate(p['targetCounts']) for _ in range(n)])))
    n = len(targets)
    assert n == c['acceptance']['assignments']
    def scores(t):
        return [sum(p['scoreByCyclicDistance'][(b-a-m) % 4] for a, b in zip(reports, t)) for m in shifts]
    all_scores = [scores(t) for t in targets]
    distributions = [Counter(s[m] for s in all_scores) for m in shifts]
    assert all(d == distributions[0] for d in distributions)
    fixed = distributions[0]; maximum = Counter(max(s) for s in all_scores)
    support = list(range(2*p['n']+1))
    tail_fixed = {v: F(sum(count for score, count in fixed.items() if score >= v), n) for v in support}
    tail_max = {v: F(sum(count for score, count in maximum.items() if score >= v), n) for v in support}
    rows = []; selected_joint = Counter(); selected_counts = Counter()
    for i, (target, s) in enumerate(zip(targets, all_scores)):
        best = max(s); selected = s.index(best)
        selected_joint[(selected, best)] += 1; selected_counts[selected] += 1
        rows.append([i, ''.join(map(str, target)), *s, best, selected,
                     str(tail_fixed[s[0]]), str(tail_fixed[best]), str(tail_max[best])])
    fixed_count = sum(tail_fixed[s[0]] <= alpha for s in all_scores)
    naive_count = sum(tail_fixed[max(s)] <= alpha for s in all_scores)
    corrected_count = sum(tail_max[max(s)] <= alpha for s in all_scores)
    fixed_mean = F(sum(score*count for score, count in fixed.items()), n)
    discovery_mean = F(sum(score*count for score, count in maximum.items()), n)
    holdout = Counter(); pair_rows = []
    for (m, discovery), count in sorted(selected_joint.items()):
        for score, hcount in sorted(distributions[m].items()):
            weight = count*hcount
            holdout[score] += weight
            pair_rows.append([m, discovery, score, weight, str(F(weight,n*n)), float(F(weight,n*n))])
    assert sum(holdout.values()) == n*n
    assert all(F(holdout[s], n*n) == F(fixed[s],n) for s in support)
    holdout_mean = F(sum(s*count for s,count in holdout.items()), n*n)
    holdout_rejection = F(sum(count for s,count in holdout.items() if tail_fixed[s] <= alpha), n*n)
    assert fixed_mean == holdout_mean == c['acceptance']['holdoutMeanEqualsNullMean']
    assert discovery_mean > fixed_mean and naive_count > fixed_count
    assert F(corrected_count,n) <= alpha
    assert holdout_rejection == F(fixed_count,n)
    assert sum(fixed.values()) == sum(maximum.values()) == n
    positive_target = tuple((r+p['positiveControlShift'])%4 for r in reports)
    positive_scores = scores(positive_target)
    assert positive_scores[p['positiveControlShift']] == c['acceptance']['knownMappingScore']
    assert tail_max[max(positive_scores)] <= alpha
    write_csv(out/'assignments.csv', ['assignment','target_labels','score_m0','score_m1','score_m2','score_m3','max_score','selected_shift','fixed_p_exact','naive_selected_p_exact','max_corrected_p_exact'], rows)
    write_csv(out/'score_distribution.csv', ['score','fixed_count','maximum_count','fixed_mass_exact','maximum_mass_exact','fixed_tail_exact','maximum_tail_exact','holdout_count','holdout_mass_exact'],
              [[s,fixed[s],maximum[s],str(F(fixed[s],n)),str(F(maximum[s],n)),str(tail_fixed[s]),str(tail_max[s]),holdout[s],str(F(holdout[s],n*n))] for s in support])
    write_csv(out/'discovery_holdout.csv', ['selected_shift','discovery_max_score','holdout_score','pair_multiplicity','probability_exact','probability'], pair_rows)
    metrics = {'balanced_assignments':n,'independent_discovery_holdout_pairs':n*n,'fixed_rule_rejection':float(F(fixed_count,n)),
               'naive_selected_rejection':float(F(naive_count,n)),'max_corrected_rejection':float(F(corrected_count,n)),
               'holdout_rejection':float(holdout_rejection),'fixed_rule_mean_score':float(fixed_mean),
               'selected_discovery_mean_score':float(discovery_mean),'holdout_mean_score':float(holdout_mean),
               'selection_optimism_points':float(discovery_mean-holdout_mean),'positive_control_score':max(positive_scores),
               'positive_control_corrected_p':float(tail_max[max(positive_scores)])}
    exact = {'fixed_rejection':str(F(fixed_count,n)),'naive_selected_rejection':str(F(naive_count,n)),
             'max_corrected_rejection':str(F(corrected_count,n)),'holdout_rejection':str(holdout_rejection),
             'discovery_mean':str(discovery_mean),'holdout_mean':str(holdout_mean)}
    result = {k:c[k] for k in ['id','round','title','question','model','incomingEvidence','sources','limits','evidenceType']}
    result.update(status='executed_pending_review',finding='Selecting a correspondence rule increases discovery scores and rejection relative to the fixed rule. Exact maximum calibration controls the declared finite null; a frozen discovery mapping returns to the null mean on independent holdout.',metrics=metrics,exactResults=exact,selectedShiftCounts=dict(selected_counts),positiveControl={'targets':list(positive_target),'scores':positive_scores,'correctedPExact':str(tail_max[max(positive_scores)])},controls=c['controls'],allAcceptanceGatesPassed=True,live_model_calls=0,human_observations=0,contractSHA256=sha(HERE/'contract.json'),runtime={'python':platform.python_version(),'matplotlib':matplotlib.__version__})
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    fig, ax=plt.subplots(1,2,figsize=(11.5,4.6),constrained_layout=True)
    ax[0].plot(support,[float(F(fixed[s],n)) for s in support],'o-',label='Fixed rule / independent holdout',color='#0c7c86')
    ax[0].plot(support,[float(F(maximum[s],n)) for s in support],'s-',label='Best discovery rule',color='#b87835')
    ax[0].set(xlabel='Score (0–16 points)',ylabel='Exact probability',title='Selecting a rule shifts discovery scores');ax[0].legend(fontsize=9)
    labels=['Fixed\nrule','Selected\nnaive','Maximum\ncorrected','Frozen-rule\nholdout']
    values=[metrics[k] for k in ['fixed_rule_rejection','naive_selected_rejection','max_corrected_rejection','holdout_rejection']]
    ax[1].bar(labels,values,color=['#0c7c86','#b87835','#6a6f7b','#0c7c86']);ax[1].axhline(.05,ls='--',color='#404750',label='Nominal alpha .05')
    ax[1].set(ylabel='Exact null rejection probability',title='Report achieved discrete sizes');ax[1].legend(fontsize=9)
    fig.suptitle('B2 · Four frozen score rules · All 2,520 balanced assignments',fontsize=14)
    fig.savefig(out/'figure.svg',metadata={'Date':None,'Creator':'Resonance Research Atlas B2 exact solver'});plt.close(fig)
    report=f'''# B2 — freeze the correspondence before the holdout

All 2,520 balanced assignments were enumerated under four correlated cyclic score rules. Exact integer multiplicities represent all {n*n:,} independent discovery/holdout pairs. No people, events, text embeddings or live model calls were sampled.

The fixed rule rejects with probability {metrics['fixed_rule_rejection']:.9f}; retrospective rule selection with its uncorrected single-rule tail rejects with probability {metrics['naive_selected_rejection']:.9f}. This is inflation relative to the fixed rule's achieved size, not a claim that the nominal .05 threshold must be exceeded. Exact maximum-statistic calibration gives {metrics['max_corrected_rejection']:.9f}. Every achieved size is retained, including conservatism from discrete scores.

The mean selected discovery score is {metrics['selected_discovery_mean_score']:.9f} of 16, versus exactly 8 for a fixed rule and for the independent holdout scored with the discovery mapping frozen. Selection creates {metrics['selection_optimism_points']:.9f} points of discovery optimism under this declared null. The known inserted m=2 correspondence gives 16 points, with corrected p={metrics['positive_control_corrected_p']:.9f}; that positive control is ordinary known correspondence.

Conditional hypothesis H-MEANING proposes a reproducible relationship under a predeclared dictionary and time window. It predicts a held-out excess if the specified relationship exists; a failed holdout challenges that specified prediction. These synthetic labels neither test meaningful personal events nor identify a higher source. An unrestricted choice of dictionary, event window or interpretation after seeing results leaves the source unidentified.

B1 motivated balanced targets and separate information paths; B2 adds fixed scoring and a genuinely untouched holdout. Pauli's historical discussion of event windows motivates clear boundaries, not this model's probabilities. Next candidate after independent review: distinguish a scripted state's causal access from prompted self-description without assigning phenomenal-consciousness labels.
'''
    (out/'report.md').write_text(report)
    files=['contract.json','solver.py','assignments.csv','score_distribution.csv','discovery_holdout.csv','results.json','figure.svg','report.md']
    artifacts={f:sha((HERE if f in ['contract.json','solver.py'] else out)/f) for f in files}
    (out/'manifest.json').write_text(json.dumps({'id':'B2','artifacts':artifacts,'sharedDependencies':[],'dataKind':'exact synthetic finite assignments and weighted pairs'},indent=2)+'\n')
    print(json.dumps(metrics,indent=2))


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path,default=HERE)
    run(parser.parse_args().output_dir)
