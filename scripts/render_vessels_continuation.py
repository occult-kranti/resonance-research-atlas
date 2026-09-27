#!/usr/bin/env python3
"""Render the companion archive summary from admitted V4 panel decisions."""
from pathlib import Path
import argparse
import html
import json

ROOT = Path(__file__).resolve().parents[1]
ATLAS = 'https://occult-kranti.github.io/resonance-research-atlas/'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vessels-root', required=True)
    args = parser.parse_args()
    destination = Path(args.vessels_root).resolve()
    if not (destination / 'research-corrections.html').is_file():
        raise ValueError('Expected the recovered Resonant Vessels checkout')
    ledger = json.loads((ROOT / 'research/panel-v4-decisions.json').read_text())
    accepted = [r for r in ledger['reviews'] if r.get('loop') == 'B' and r.get('status') == 'accepted_narrow']
    if len(accepted) != 5:
        raise ValueError('Only render the complete companion release after all five admissions')
    e = html.escape
    rows = []
    for r in accepted:
        limits = ''.join(f'<li>{e(v)}</li>' for v in r['withheld'])
        rows.append(f'''<article class="round" id="round-{r['round']}">
<p class="eyebrow">Round {r['round']} · production + independent review</p>
<h2>{e(r['title'])}</h2><p>{e(r['finding'])}</p>
<details><summary>Assumptions and limits</summary><p>{e(r['scope'])}</p><ul>{limits}</ul></details>
<p class="artifact-links"><a href="{ATLAS + r['contractPath']}">Frozen contract</a> ·
<a href="{ATLAS + r['resultsPath']}">Computed results</a> ·
<a href="{ATLAS + r['reviewPath']}">Independent review</a></p></article>''')
    document = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Reviewed electricity, magnetism and force-claim investigations, with the earlier sound checkpoint and source-bound historical material readings.">
<title>Electricity &amp; force claims · Resonant Vessels</title>
<style>
:root{{color-scheme:light;--paper:#f4ecd8;--ink:#252821;--green:#274a40;--muted:#55584d;--line:#bab59f}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.65 Georgia,serif}}
a{{color:var(--green);text-underline-offset:.2em}}a:focus-visible,summary:focus-visible{{outline:3px solid #9a5d23;outline-offset:5px}}
.skip{{position:absolute;left:1rem;top:-5rem;background:white;padding:.5rem}}.skip:focus{{top:1rem}}
header,main,footer{{max-width:1120px;margin:auto;padding:28px clamp(20px,5vw,64px)}}
header{{display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);font-family:system-ui,sans-serif}}
.brand{{font-family:Georgia,serif;font-size:1.2rem}}nav{{display:flex;gap:20px;flex-wrap:wrap}}
.eyebrow{{font:12px/1.5 system-ui,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 16px}}
h1{{font-size:clamp(2.5rem,7vw,4.7rem);line-height:1.08;max-width:15ch;font-weight:400;margin:0 0 30px}}h2{{font-size:clamp(1.5rem,3vw,2rem);line-height:1.2;font-weight:400}}
.intro{{font-size:1.2rem;max-width:65ch}}.primary{{display:inline-block;background:var(--green);color:white;padding:12px 22px;margin:12px 0;text-decoration:none;font-family:system-ui,sans-serif}}
.boundary{{border-left:3px solid var(--green);padding:8px 0 8px 22px;margin:30px 0;max-width:72ch}}
.index{{display:grid;grid-template-columns:1fr 1fr;gap:32px;border-block:1px solid var(--line);padding:26px 0;margin:40px 0}}.index h2{{margin-top:0}}
.round{{padding:28px 0;border-bottom:1px solid var(--line)}}.round p{{max-width:75ch}}summary{{cursor:pointer;font-family:system-ui,sans-serif;font-weight:600;padding:8px 0}}
li{{margin:8px 0}}.artifact-links,footer{{font:14px/1.6 system-ui,sans-serif}}footer{{color:var(--muted)}}
@media(max-width:620px){{header{{flex-direction:column}}.index{{grid-template-columns:1fr}}main{{padding-top:36px}}nav{{gap:12px}}}}
</style></head><body><a class="skip" href="#main">Skip to experiments</a>
<header><a class="brand" href="index.html">Resonant Vessels</a><nav aria-label="Research navigation"><a href="research-corrections.html">Source corrections</a><a href="{ATLAS}sound-lab/field-notes.html">Experiment bench ↗</a></nav></header>
<main id="main"><p class="eyebrow">Research continuation · 27 September 2026</p>
<h1>Energy flows.<br>Forces need a source.</h1>
<p class="intro">The user-directed continuation now focuses on electricity, magnetism and antigravity claims. Two completed sound rounds remain as a checkpoint; the remaining three test electrical and force models. Each round contains a production loop and a separate skeptical review.</p>
<a class="primary" href="{ATLAS}sound-lab/field-notes.html">Open the electricity &amp; force bench ↗</a>
<p class="boundary">The completed results are calculations and synthetic controls. The tabletop arrangements are proposed experiments. Magnetic lift, resonance amplification and a changed balance reading do not by themselves establish modified gravity or excess energy.</p>
<div class="index"><section><h2>Try the practical path</h2><ol><li>Read the proposed materials and coordinate drawings.</li><li>Use the calculator to inspect the assumptions.</li><li>Follow a frozen measurement plan and retain all raw records.</li><li>Account for inputs, stored energy, losses and ordinary forces before interpreting a change.</li></ol><a href="{ATLAS}docs/panel-v4/roadmap-v4.md">Detailed next-gate roadmap</a></section>
<section><h2>Read the historical path</h2><p>The material dictionary separates conventional element names from compounds, process terms and ambiguous cover-names. A symbol or visual pattern alone cannot determine a specimen's composition.</p><a href="{ATLAS}docs/panel-v4/alchemy-materials.md">Alchemy and modern materials</a><br><a href="{ATLAS}docs/panel-v4/source-review.md">Papers, patents, archives and discourse</a></section></div>
{''.join(rows)}
<section class="round"><h2>How this continues the archive</h2><p>The older six simulation families retain their inherited-report status because their cited implementations were absent from the recovered archive. These new, separately identified investigations provide executable artifacts; they do not retrospectively validate those older reports.</p><p>Historical figures provide documented research lenses. The advisor, producer and skeptic were separate model agents with correlated model-family authorship, not historical people or human peer reviewers.</p><a href="{ATLAS}research/panel-v4-decisions.json">Ten-loop decision ledger</a> · <a href="{ATLAS}docs/continuation-v4.md">Scope and provenance</a></section>
</main><footer>Resonant Vessels · Source-led research · <a href="README.md">Repository guide</a></footer></body></html>'''
    out = destination / 'research-continuation.html'
    out.write_text(document)
    print(json.dumps({'path': str(out), 'acceptedRounds': len(accepted)}))


if __name__ == '__main__':
    main()
