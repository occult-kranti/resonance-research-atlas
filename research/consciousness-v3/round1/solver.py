"""B1 exact synthetic state enumeration. No model API or human observations."""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import math
import platform
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
plt.rcParams.update({'svg.hashsalt': 'consciousness-v3-B1', 'font.family': 'DejaVu Sans', 'font.size': 10})


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def marginal(joint, axes):
    out = defaultdict(F)
    for key, p in joint.items():
        out[tuple(key[i] for i in axes)] += p
    return out


def information(joint):
    pt, pa, pb = (marginal(joint, (i,)) for i in range(3))
    pta, ptb, pab = (marginal(joint, axes) for axes in [(0, 1), (0, 2), (1, 2)])
    def mi(pxy, px, py):
        return sum(float(v) * math.log2(float(v / (px[(x,)] * py[(y,)])))
                   for (x, y), v in pxy.items() if v)
    ia, ib = mi(pta, pt, pa), mi(ptb, pt, pb)
    iab = sum(float(v) * math.log2(float(v / (pt[(t,)] * pab[(a, b)])))
              for (t, a, b), v in joint.items() if v)
    conditional = sum(float(v) * math.log2(float(v * pa[(a,)] / (pta[(t, a)] * pab[(a, b)])))
                      for (t, a, b), v in joint.items() if v)
    return {'I_T_A_bits': ia, 'I_T_B_bits': ib, 'I_T_AB_bits': iab,
            'I_T_B_given_A_bits': conditional, 'chain_error_bits': abs(iab - ia - conditional)}


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    c = json.loads((HERE / 'contract.json').read_text())
    biased = list(map(F, c['parameters']['biasedPrior']))
    uniform = list(map(F, c['parameters']['balancedPrior']))
    lam = F(c['parameters']['lambda'])
    states, summaries, joints = [], [], {}
    for scenario in c['parameters']['scenarios']:
        name = scenario['id']
        prior = biased if scenario['prior'] == 'biased' else uniform
        joint = {}
        for t, a, b in itertools.product(range(4), repeat=3):
            la = lam * (a == t) + (1 - lam) / 4
            lb = lam * (b == t) + (1 - lam) / 4
            if name.endswith('majority'):
                channel = F(a == 0 and b == 0)
            elif name == 'biased_common_random':
                channel = biased[a] * (a == b)
            elif name == 'balanced_independent_null':
                channel = F(1, 16)
            elif name == 'balanced_independent_leaks':
                channel = la * lb
            else:
                channel = la * (a == b)
            joint[(t, a, b)] = prior[t] * channel
            states.append([name, t, a, b, str(joint[(t, a, b)]), float(joint[(t, a, b)])])
        assert sum(joint.values()) == 1 and min(joint.values()) >= 0
        assert marginal(joint, (0,)) == {(i,): prior[i] for i in range(4)}
        info = information(joint)
        no_path = name in ['biased_majority', 'balanced_majority', 'biased_common_random', 'balanced_independent_null']
        if no_path:
            pab = marginal(joint, (1, 2))
            assert all(p == prior[t] * pab[(a, b)] for (t, a, b), p in joint.items())
            assert info['I_T_A_bits'] == info['I_T_AB_bits'] == 0
        copied = name != 'balanced_independent_null' and name != 'balanced_independent_leaks'
        if copied:
            assert info['I_T_B_given_A_bits'] == 0
        assert info['chain_error_bits'] < c['acceptance']['chainRuleTolerance_bits']
        hit_a = sum(p for (t, a, b), p in joint.items() if t == a)
        hit_b = sum(p for (t, a, b), p in joint.items() if t == b)
        agreement = sum(p for (t, a, b), p in joint.items() if a == b)
        summaries.append({'id': name, 'targetPrior': list(map(str, prior)), 'hit_A_exact': str(hit_a),
                          'hit_A': float(hit_a), 'hit_B_exact': str(hit_b), 'hit_B': float(hit_b),
                          'agreement_exact': str(agreement), 'agreement': float(agreement),
                          'no_path_by_construction': no_path, **info})
        joints[name] = joint
    assert len(states) == 448
    assert joints['balanced_copied_leak'] == joints['hypothetical_receiver_copy']
    by_id = {s['id']: s for s in summaries}
    assert by_id['balanced_independent_leaks']['I_T_B_given_A_bits'] > 0
    with (out / 'joint_states.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['scenario', 'target', 'report_A', 'report_B', 'probability_exact', 'probability']); w.writerows(states)

    n, alpha = c['parameters']['n'], F(c['parameters']['alpha'])
    distributions, calibration, rows = {}, [], []
    for p_string in c['parameters']['binomialNulls']:
        p = F(p_string)
        mass = [F(math.comb(n, k)) * p**k * (1-p)**(n-k) for k in range(n+1)]
        assert sum(mass) == 1 and min(mass) >= 0
        tails = [sum(mass[k:]) for k in range(n+1)]
        cutoff = next(k for k in range(n+1) if tails[k] <= alpha)
        assert tails[cutoff] <= alpha < tails[cutoff-1]
        assert all(tails[k] >= tails[k+1] for k in range(n))
        distributions[p_string] = (mass, tails, cutoff)
        calibration.append({'null_p_exact': str(p), 'critical_hits': cutoff, 'rejection_exact': str(tails[cutoff]),
                            'rejection_probability': float(tails[cutoff]), 'preceding_tail_exact': str(tails[cutoff-1])})
        rows.extend([str(p), n, k, str(mass[k]), float(mass[k]), str(tails[k]), float(tails[k]), cutoff] for k in range(n+1))
    wrong_cutoff = distributions['1/4'][2]
    wrong = {}
    for p_string in ['11/20', '37/100']:
        _, tails, correct_cutoff = distributions[p_string]
        assert tails[wrong_cutoff] > tails[correct_cutoff]
        wrong[p_string] = {'assumed_null_p_exact': '1/4', 'actual_null_p_exact': p_string,
                           'wrong_cutoff': wrong_cutoff, 'rejection_exact': str(tails[wrong_cutoff]),
                           'rejection_probability': float(tails[wrong_cutoff])}
    assert len(rows) == 243
    with (out / 'binomial_nulls.csv').open('w', newline='') as f:
        w = csv.writer(f); w.writerow(['p_exact', 'n', 'hits', 'mass_exact', 'mass', 'tail_exact', 'tail', 'critical_hits']); w.writerows(rows)

    metrics = {'weighted_joint_states': 448, 'binomial_states': 243,
               'biased_majority_hit_rate': by_id['biased_majority']['hit_A'],
               'biased_majority_agreement': by_id['biased_majority']['agreement'],
               'biased_majority_target_information_bits': by_id['biased_majority']['I_T_AB_bits'],
               'biased_common_random_hit_rate': by_id['biased_common_random']['hit_A'],
               'copied_leak_target_information_bits': by_id['balanced_copied_leak']['I_T_A_bits'],
               'copied_leak_added_information_bits': by_id['balanced_copied_leak']['I_T_B_given_A_bits'],
               'independent_leak_added_information_bits': by_id['balanced_independent_leaks']['I_T_B_given_A_bits'],
               'incorrect_uniform_cutoff': wrong_cutoff,
               'biased_majority_wrong_baseline_rejection': wrong['11/20']['rejection_probability'],
               'common_random_wrong_baseline_rejection': wrong['37/100']['rejection_probability'],
               'receiver_leak_total_variation': 0.0,
               'max_information_chain_error_bits': max(s['chain_error_bits'] for s in summaries)}
    result = {k: c[k] for k in ['id', 'round', 'title', 'question', 'model', 'incomingEvidence', 'sources', 'limits', 'evidenceType']}
    result.update(status='executed_pending_review', finding='Biased agreeing reporters can carry zero target information. A copied informative report adds zero conditional information; an independent informative report adds some. The conditional receiver and ordinary leak remain observationally identical.',
                  metrics=metrics, scenarios=summaries, calibratedNulls=calibration, incorrectBaseline=wrong,
                  controls=c['controls'], allAcceptanceGatesPassed=True, live_model_calls=0, human_observations=0,
                  contractSHA256=sha(HERE / 'contract.json'), runtime={'python': platform.python_version(), 'matplotlib': matplotlib.__version__})
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8), constrained_layout=True)
    names = ['Biased\nmajority', 'Balanced\nmajority', 'Shared\nrandom', 'Independent\nnull', 'Copied\nleak', 'Independent\nleaks', 'Conditional\nreceiver']
    x = list(range(7))
    ax[0].bar([v-.18 for v in x], [s['hit_A'] for s in summaries], .36, label='Report A hits', color='#0c7c86')
    ax[0].bar([v+.18 for v in x], [s['agreement'] for s in summaries], .36, label='A and B agree', color='#b87835')
    ax[0].set(xticks=x, xticklabels=names, ylim=(0, 1.14), ylabel='Exact model probability', title='Agreement can coexist with zero target information')
    ax[0].tick_params(axis='x', labelsize=8); ax[0].legend(fontsize=9)
    ax[1].bar(x, [s['I_T_A_bits'] for s in summaries], .65, color='#0c7c86', label='Information in A')
    ax[1].bar(x, [s['I_T_B_given_A_bits'] for s in summaries], .65, bottom=[s['I_T_A_bits'] for s in summaries], color='#b87835', label='Additional information in B')
    ax[1].set(xticks=x, xticklabels=names, ylabel='Target information (bits)', title='A second copy adds no information')
    ax[1].tick_params(axis='x', labelsize=8); ax[1].legend(fontsize=9)
    fig.suptitle('B1 · Exact synthetic joint distributions · 448 weighted states', fontsize=14)
    fig.savefig(out / 'figure.svg', metadata={'Date': None, 'Creator': 'Resonance Research Atlas B1 exact solver'})
    plt.close(fig)
    text = f'''# B1 — agreement is not additional information

Executed exact synthetic enumeration: 448 weighted joint states and 243 binomial states. No human observations or live model calls.

Two always-majority reporters score 55% with 100% agreement under the declared biased prior, while their target information is exactly 0 bits. The common-random pair scores 37% with the same absence of target information. Balancing the target prior changes the constant predictor's hit rate to 25%; it does not create information.

The copied ordinary-leak channel has {metrics['copied_leak_target_information_bits']:.9f} bits in A and exactly 0 additional bits in B. Giving B an independent conditional leak instead adds {metrics['independent_leak_added_information_bits']:.9f} bits. Agreement is therefore not an independent evidence count.

The binomial audit assumes 80 independent repetitions of the single-trial law. In the shared-random scenario, U is shared between A and B within a trial and redrawn independently on the next trial. A study-level shared U would be a different dependent model and is not tested here.

For n=80, the incorrect uniform-null cutoff is {wrong_cutoff} hits. Under the actual majority-prior null it rejects with probability {metrics['biased_majority_wrong_baseline_rejection']:.9f}; under the shared-random null it rejects with probability {metrics['common_random_wrong_baseline_rejection']:.9f}. Correct-prior cutoffs and all exact rational tails remain in the CSV/JSON.

Positive hypothesis H-RX assigns a target-to-report coupling kappa. At kappa=lambda=.1 it exactly matches the ordinary leak distribution (total variation 0). This is observational nonidentification, not evidence for or against higher consciousness. No-path independence is built into the null models. Consciousness alone does not entail hidden knowledge.

Incoming lesson: S5A/S5B showed that matching observations and metadata cannot certify a mechanism or custody. This round makes the corresponding information-map ambiguity explicit. Next candidate: after independent review, audit whether a flexible correspondence score can appear informative on balanced targets and fail on an untouched holdout.

The proposed human protocol is separate: concealed balanced blocks need a block-randomization analysis; these IID binomial tails are not its analysis. Source ledger: docs/panel-v3/sources-consciousness.json.
'''
    (out / 'report.md').write_text(text)
    files = ['joint_states.csv', 'binomial_nulls.csv', 'results.json', 'figure.svg', 'report.md']
    artifacts = {f: sha(out / f) for f in files}
    artifacts['contract.json'] = sha(HERE / 'contract.json')
    artifacts['solver.py'] = sha(HERE / 'solver.py')
    (out / 'manifest.json').write_text(json.dumps({'id': 'B1', 'artifacts': artifacts, 'sharedDependencies': [], 'dataKind': 'exact synthetic weighted states'}, indent=2) + '\n')
    print(json.dumps(metrics, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=HERE)
    run(parser.parse_args().output_dir)
