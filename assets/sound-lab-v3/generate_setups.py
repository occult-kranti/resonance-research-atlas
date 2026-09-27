#!/usr/bin/env python3
"""Regenerate proposed, unbuilt sound-lab apparatus plans and geometry renders.

Dimensions are nominal illustration coordinates. This is a drawing generator, not
an acoustic simulator or a record of measurements. Run from any directory.
"""

from __future__ import annotations

import json
from pathlib import Path
from xml.sax.saxutils import escape

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CATALOG = ROOT / "docs/panel-v3/setup-catalog.json"

INK = "#163044"
MUTED = "#506477"
BLUE = "#2563a6"
TEAL = "#087f73"
ORANGE = "#bc6836"
PAPER = "#f8fbfd"
FAINT = "#e2eaf0"


def text(x, y, value, size=18, color=INK, weight="normal", anchor="start"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
        f'font-weight="{weight}" text-anchor="{anchor}" '
        'font-family="Inter,Segoe UI,Arial,sans-serif">'
        f"{escape(value)}</text>"
    )


def line(x1, y1, x2, y2, color=INK, width=2, dash=None, marker=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ""
    extra += f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}"{extra}/>'
    )


def box(x, y, w, h, title, detail, fill="#fff", edge=FAINT):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" '
        f'fill="{fill}" stroke="{edge}" stroke-width="2"/>'
        + text(x + 16, y + 30, title, 16, INK, "bold")
        + text(x + 16, y + 56, detail, 14, MUTED)
    )


def svg(name, title, desc, body, height=760):
    data = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {height}" '
        f'width="1200" height="{height}" role="img" aria-labelledby="title desc">'
        f"<title id=\"title\">{escape(title)}</title><desc id=\"desc\">{escape(desc)}</desc>"
        '<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
        'orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#163044"/></marker>'
        '<marker id="blueArrow" markerWidth="9" markerHeight="9" refX="8" refY="4.5" '
        'orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#2563a6"/></marker></defs>'
        f'<rect width="1200" height="{height}" fill="{PAPER}"/>'
        + body
        + "</svg>"
    )
    (OUT / name).write_text(data, encoding="utf-8")


def common_header(kicker, title, subtitle):
    return (
        text(54, 48, kicker.upper(), 14, TEAL, "bold")
        + text(54, 86, title, 30, INK, "bold")
        + text(54, 115, subtitle, 16, MUTED)
        + line(54, 134, 1146, 134, FAINT, 2)
    )


def s1_plan():
    parts = [common_header("S1 proposed bench / top view", "Speaker · reflector · phone",
                           "Nominal placement in metres. Unbuilt; the synthetic S1A 5 ms path is not a room measurement.")]
    parts += [
        text(70, 177, "PLACEMENT", 17, INK, "bold"),
        line(130, 255, 685, 255, ORANGE, 12),
        text(408, 232, "movable stiff card, 0.90 m nominal width", 15, ORANGE, "bold", "middle"),
        line(252, 585, 552, 585, BLUE, 4),
        line(252, 585, 402, 255, TEAL, 3, "9 7"),
        line(402, 255, 552, 585, TEAL, 3, "9 7"),
        text(389, 442, "illustrative reflected path", 14, TEAL, "bold", "middle"),
        '<circle cx="252" cy="585" r="29" fill="#e7f1fc" stroke="#2563a6" stroke-width="3"/>',
        text(252, 591, "S", 19, BLUE, "bold", "middle"),
        '<rect x="525" y="558" width="54" height="54" rx="9" fill="#e5f5f2" stroke="#087f73" stroke-width="3"/>',
        text(552, 590, "M", 19, TEAL, "bold", "middle"),
        text(250, 631, "ordinary speaker", 15, INK, "bold", "middle"),
        text(551, 631, "phone mic port → S", 15, INK, "bold", "middle"),
        line(295, 585, 505, 585, BLUE, 3, None, "blueArrow"),
        text(402, 565, "direct path", 14, BLUE, "bold", "middle"),
        line(252, 666, 552, 666, INK, 1.5),
        line(252, 657, 252, 675, INK, 1.5),
        line(552, 657, 552, 675, INK, 1.5),
        text(402, 693, "S–M = 0.50 m", 16, INK, "bold", "middle"),
        line(718, 255, 718, 585, INK, 1.5),
        line(708, 255, 728, 255, INK, 1.5),
        line(708, 585, 728, 585, INK, 1.5),
        text(706, 429, "0.60 m to card", 15, INK, "bold", "end"),
        text(72, 720, "Coordinates: S (0, 0); M (0.50, 0); card line y = 0.60, x = −0.20…0.70 m.", 14, MUTED),
        line(785, 173, 785, 723, FAINT, 2),
        text(810, 180, "SIGNAL / READOUT", 17, INK, "bold"),
        box(810, 201, 330, 70, "Digital test signal", "output level logged"),
        line(974, 271, 974, 293, INK, 2, None, "arrow"),
        box(810, 303, 330, 70, "Speaker + room", "both are unknown transfer paths"),
        line(974, 373, 974, 395, INK, 2, None, "arrow"),
        box(810, 405, 330, 70, "Phone + recorder", "gain mode / rate documented"),
        text(810, 515, "Matched placements", 16, INK, "bold"),
        text(810, 544, "no card → card → no card", 15, MUTED),
        text(810, 566, "+1 cm phone move, then restore", 14, MUTED),
        text(810, 592, "A changed recording does not isolate", 15, INK),
        text(810, 616, "the card from speaker, microphone,", 15, INK),
        text(810, 640, "gain, and other room reflections.", 15, INK),
        text(810, 701, "Measure actual positions and room state.", 14, ORANGE, "bold"),
    ]
    svg("s1-bench-plan.svg", "Proposed speaker, card reflector and phone plan",
        "Top view: speaker S at (0,0) metres, phone microphone M at (0.50,0), a nominal 0.90-m-wide movable card on y=0.60 m. Direct and illustrative reflected paths, signal chain and placement controls. Proposed and unbuilt; no measured delay.", "".join(parts), 755)


def s1_ambiguity():
    parts = [common_header("S1A synthetic inference", "One total transfer, multiple physical stories",
                           "The 5 ms branch belongs to an exact computational FIR contract, not an observed sound path.")]
    parts += [
        box(70, 198, 480, 92, "Decomposition A · model", "device = d; acoustic = e = δ[n] + 0.6 δ[n−40]", "#edf6fc"),
        box(650, 198, 480, 92, "Decomposition B · model", "device = d * e; acoustic = δ[n]", "#edf7f4"),
        line(312, 290, 312, 340, BLUE, 3, None, "blueArrow"),
        line(889, 290, 889, 340, TEAL, 3, None, "arrow"),
        box(240, 350, 720, 100, "Same observable output", "Y(ω)/X(ω) identifies total H, not a unique room or device factor.", "#fff5e9", "#e8c6a8"),
        text(70, 505, "PROPOSED PHYSICAL AUDIT", 18, INK, "bold"),
        box(70, 535, 245, 84, "1. Source", "playback file and level"),
        box(342, 535, 245, 84, "2. Device", "speaker / microphone"),
        box(614, 535, 245, 84, "3. Air + card", "room, paths, placement"),
        box(886, 535, 245, 84, "4. Readout", "gain / sample clock"),
        line(316, 577, 338, 577, INK, 2, None, "arrow"),
        line(588, 577, 610, 577, INK, 2, None, "arrow"),
        line(860, 577, 882, 577, INK, 2, None, "arrow"),
        text(70, 677, "d = [0.7, 0.2, 0.1]; 40 samples / 8 kHz = 5 ms only in the synthetic model.", 15, MUTED),
        text(70, 702, "No measured time zero, impulse response, or separate device calibration exists here.", 16, ORANGE, "bold"),
    ]
    svg("s1-identifiability.svg", "Synthetic two-path transfer identifiability",
        "Two exact factorisations of the same synthetic total transfer H: device d and acoustic delayed branch e, versus device d convolved with e and identity acoustic path. The branch is 40 samples at 8 kilohertz. Proposed source, device, air and readout audit is unbuilt.", "".join(parts), 730)


def chemical_identity_plate():
    parts = [common_header("Alchemy → elements / source-bound mapping", "A name is not an assay",
                           "Historically attested words and signs are context-sensitive; these are modern candidates, not tested specimens.")]
    parts += [
        text(67, 177, "HISTORICAL WITNESS", 16, TEAL, "bold"),
        text(405, 177, "CANDIDATE MODERN IDENTITY", 16, BLUE, "bold"),
        text(790, 177, "WHAT REMAINS UNKNOWN", 16, ORANGE, "bold"),
    ]
    rows = [
        ("☉ / gold · conventional sign", "Au · gold, if literal metal", "Manuscript context uncollated here"),
        ("♄ / Saturn · contextual term", "Pb · only if passage establishes lead", "Can also signify aqua fortis elsewhere"),
        ("antimony · ore or regulus", "Sb₂S₃ ore / Sb-rich metal candidate", "Ore, metal or alloy? Sample required"),
        ("arsenic · early-modern usage", "often As₂O₃, not elemental As", "Historical usage varies by passage"),
        ("vitriol · family label", "Fe / Cu sulfate family candidates", "Which cation, hydration and mixture?"),
    ]
    for idx, (old, candidate, unknown) in enumerate(rows):
        y = 195 + idx * 89
        parts += [
            f'<rect x="54" y="{y}" width="1092" height="76" rx="10" fill="{("#fff" if idx % 2 == 0 else "#eff5f8")}" stroke="{FAINT}"/>',
            text(70, y + 33, old, 17, INK, "bold"),
            text(405, y + 33, candidate, 17, BLUE, "bold"),
            text(790, y + 33, unknown, 16, MUTED),
            text(70, y + 57, "historical expression", 13, MUTED),
            text(405, y + 57, "editorial mapping, context-limited", 13, MUTED),
            text(790, y + 57, "element / phase / composition unresolved", 13, MUTED),
        ]
    parts += [
        line(54, 660, 1146, 660, FAINT, 2),
        text(65, 691, "A conventional symbol is a candidate reading; a primary passage must establish a literal substance.", 16, INK),
        text(65, 722, "Compound, phase and purity still require measurement. Color or code-word cannot establish transmutation.", 16, ORANGE, "bold"),
        text(65, 758, "Source trail: primary manuscript index; separate editorial symbols/glossary (V3-NEWTON-INDEX / SYMBOLS / GLOSSARY).", 13, MUTED),
    ]
    svg("alchemy-chemical-identity.svg", "Alchemy terms and uncertain modern chemical identity",
        "Conventional solar sign can indicate gold, Au, in literal metal context; Saturn can indicate lead, Pb, where a manuscript establishes it, but has other meanings. Antimony can refer to ore or regulus, arsenic often to trioxide, and vitriol to sulfate families. None identifies an actual specimen.", "".join(parts), 785)


def b1_blind_target():
    parts = [common_header("B1–B3 proposed human/AI protocol", "Concealed target · locked reports · independent scoring",
                           "Information custody only; no higher-consciousness field or subjective-experience sensor is measured.")]
    parts += [
        '<rect x="53" y="158" width="298" height="570" rx="14" fill="#edf6fc"/>',
        '<rect x="370" y="158" width="449" height="570" rx="14" fill="#f0f8f6"/>',
        '<rect x="837" y="158" width="309" height="570" rx="14" fill="#fff6ed"/>',
        text(70, 187, "1 · INDEPENDENT CUSTODIAN", 16, BLUE, "bold"),
        text(388, 187, "2 · TARGET-BLIND RESPONSE STATIONS", 16, TEAL, "bold"),
        text(854, 187, "3 · ANALYST AFTER FREEZE", 16, ORANGE, "bold"),
        box(68, 214, 265, 84, "Offline target schedule", "80 trials; 20 shuffled 4-symbol blocks"),
        box(68, 341, 265, 86, "Opaque target store", "targets + secret high-entropy salts"),
        line(201, 298, 201, 337, INK, 2, None, "arrow"),
        box(68, 464, 265, 86, "Public commitment", "trial ID + salted target hash"),
        line(201, 427, 201, 460, INK, 2, None, "arrow"),
        '<path d="M333 506 H363 V312 H795" fill="none" stroke="#2563a6" stroke-width="2"/>',
        line(405, 312, 405, 342, BLUE, 2, None, "blueArrow"),
        line(795, 312, 795, 342, BLUE, 2, None, "blueArrow"),
        text(605, 332, "ID + salted hash + four labels only", 13, BLUE, "bold", "middle"),
        box(435, 214, 318, 78, "Ordinary shared prior U", "same category set / prompt conventions", "#f6faf8"),
        line(453, 292, 453, 339, TEAL, 2, None, "arrow"),
        line(749, 292, 749, 339, TEAL, 2, None, "arrow"),
        box(391, 345, 202, 95, "Human station", "one choice + optional text"),
        box(607, 345, 202, 95, "AI station", "fresh context; raw output"),
        text(600, 459, "guesses hidden until lock", 13, TEAL, "bold", "middle"),
        line(490, 440, 490, 501, TEAL, 2, None, "arrow"),
        line(707, 440, 707, 501, TEAL, 2, None, "arrow"),
        box(446, 506, 318, 90, "Frozen response export", "both choices, UTC times, hashes, logs"),
        line(764, 551, 851, 551, TEAL, 2.5, None, "arrow"),
        box(852, 479, 278, 144, "Verify and score", "commitments; all 80 trials"),
        text(868, 575, "exact within-block randomization", 13, MUTED),
        text(868, 597, "agreement / added information", 13, MUTED),
        line(333, 390, 352, 390, ORANGE, 2),
        line(352, 390, 352, 676, ORANGE, 2),
        line(352, 676, 988, 676, ORANGE, 2, "7 7", "arrow"),
        line(988, 676, 988, 626, ORANGE, 2, "7 7", "arrow"),
        text(599, 665, "targets + salts released only after BOTH reports and entire main run freeze", 14, ORANGE, "bold", "middle"),
        text(391, 630, "Designed to exclude target paths; custody audit required.", 14, TEAL, "bold"),
        line(54, 759, 1146, 759, FAINT, 2),
        text(66, 789, "SEPARATE POSITIVE CONTROL", 16, ORANGE, "bold"),
        box(65, 805, 270, 70, "Disclosed target", "ordinary information path", "#fff0e2", "#e9bd91"),
        line(336, 839, 445, 839, ORANGE, 2, "7 6", "arrow"),
        box(450, 805, 315, 70, "Response with known target", "validates data path and scoring", "#fff0e2", "#e9bd91"),
        line(766, 839, 875, 839, ORANGE, 2, "7 6", "arrow"),
        box(879, 805, 253, 70, "Score separately", "excluded from concealed 80", "#fff0e2", "#e9bd91"),
    ]
    svg("b1-blind-target-flow.svg", "Proposed concealed-target human and AI information-custody protocol",
        "Three lanes show offline custodian generating 80 targets in twenty shuffled four-symbol blocks, target storage and salted commitments; independent human and AI target-blind stations with an ordinary shared category prior; both timestamped guesses locked before all targets and salts reach an analyst. A separate disclosed positive-control path is excluded from the concealed phase. Protocol only, not run.", "".join(parts), 900)


def s2_spoon_plan():
    parts = [common_header("S2 proposed bench / side elevation", "Suspended spoon · gentle tap · noncontact phone",
                           "Nominal metre coordinates above padded tabletop. S2 synthetic decay is not an observed spoon response.")]
    parts += [
        text(66, 176, "GEOMETRY", 17, INK, "bold"),
        '<rect x="82" y="630" width="650" height="22" fill="#dae6ed" stroke="#879cad"/>',
        text(90, 682, "padded table  z = 0", 15, MUTED),
        line(241, 211, 460, 211, INK, 8),
        text(350, 190, "crossbar  z = 0.42 m", 15, INK, "bold", "middle"),
        line(350, 211, 350, 319, MUTED, 2, "5 4"),
        text(366, 280, "loose thread", 14, MUTED),
        line(350, 318, 350, 486, BLUE, 8),
        '<ellipse cx="350" cy="512" rx="30" ry="26" fill="#9ebce1" stroke="#2563a6" stroke-width="3"/>',
        text(273, 506, "spoon bowl", 15, BLUE, "bold", "end"),
        text(273, 531, "centre z = 0.12 m", 13, MUTED, "end"),
        '<rect x="577" y="455" width="20" height="109" rx="5" fill="#e5f5f2" stroke="#087f73" stroke-width="3"/>',
        line(587, 564, 587, 630, MUTED, 3),
        '<rect x="555" y="620" width="65" height="10" fill="#b9cbd3"/>',
        '<circle cx="577" cy="511" r="4" fill="#087f73"/>',
        text(610, 503, "phone mic → spoon", 15, TEAL, "bold"),
        text(610, 528, "M = (0.20, 0, 0.12) m", 14, MUTED),
        line(382, 512, 565, 512, TEAL, 2, "7 5", "arrow"),
        line(350, 581, 577, 581, INK, 1.5),
        line(350, 574, 350, 589, INK, 1.5),
        line(577, 574, 577, 589, INK, 1.5),
        text(463, 607, "bowl–mic = 0.20 m", 15, INK, "bold", "middle"),
        line(300, 492, 325, 507, ORANGE, 5),
        text(175, 465, "pencil eraser", 14, ORANGE, "bold"),
        line(170, 470, 294, 493, ORANGE, 2, None, "arrow"),
        line(785, 173, 785, 706, FAINT, 2),
        text(810, 178, "CAPTURE AND CONTROLS", 17, INK, "bold"),
        box(811, 206, 325, 80, "Quiet → tap → ringdown", "≥1 s before; ≥2 s after impact"),
        line(972, 286, 972, 312, INK, 2, None, "arrow"),
        box(811, 324, 325, 80, "At least five separate taps", "retain all WAV files and clipping flags"),
        line(972, 404, 972, 430, INK, 2, None, "arrow"),
        box(811, 443, 325, 83, "Matched touch control", "light finger loading; phone stays fixed"),
        text(811, 567, "Then repeat untouched references.", 15, INK),
        text(811, 612, "Fit a declared post-impact window;", 15, INK),
        text(811, 637, "log event time, processing and gain.", 15, INK),
        text(811, 684, "No intrinsic material damping inferred.", 15, ORANGE, "bold"),
        text(72, 725, "3D coordinates: thread and spoon at (0,0); bowl (0,0,0.12); phone mic (0.20,0,0.12) m.", 14, MUTED),
    ]
    svg("s2-spoon-plan.svg", "Proposed suspended spoon noncontact ringdown setup",
        "Side elevation shows an unbroken spoon hanging loosely from thread under a crossbar 0.42 m above a padded table. Spoon bowl centre is 0.12 m high and phone mic faces it 0.20 m away without contact. A pencil eraser gives a gentle tap; capture quiet pre-roll, five separate events, a light-touch loading control and return reference.", "".join(parts), 750)


def s3b_clock_plan():
    parts = [common_header("S3B exact generated-PCM fixture", "One sample series · two time axes",
                           "Metadata can stretch inferred frequency and decay. No physical phone clock was measured.")]
    parts += [
        box(72, 198, 325, 138, "Generated PCM16 samples", "n = 0…16031; 16032 samples", "#eef5fb"),
        text(89, 292, "fixture: 500 Hz, decay α = 4 s⁻¹", 15, BLUE, "bold"),
        text(89, 314, "true sampling interval = 1/8016 s", 14, MUTED),
        line(397, 258, 445, 258, INK, 2),
        line(445, 258, 445, 450, INK, 2),
        line(445, 257, 491, 257, INK, 2, None, "arrow"),
        line(445, 450, 491, 450, INK, 2, None, "arrow"),
        box(495, 191, 335, 142, "WAV header says 8000 Hz", "same quantized sample amplitudes", "#fff5ed", "#e5c6ac"),
        text(511, 286, "declared times tₕ = n / 8000 s", 15, ORANGE, "bold"),
        text(511, 311, "header is wrong for this fixture", 14, MUTED),
        box(495, 388, 335, 142, "Corrected-time CSV", "same decoded sample amplitudes", "#eaf8f4", "#b9dcd2"),
        text(511, 483, "external times tₑ = n / 8016 s", 15, TEAL, "bold"),
        text(511, 508, "external here = known simulation grid", 14, MUTED),
        line(830, 263, 869, 263, ORANGE, 2, None, "arrow"),
        line(830, 461, 869, 461, TEAL, 2, None, "arrow"),
        box(875, 191, 270, 142, "Predicted header-time fit", "499.001996 Hz", "#fff5ed", "#e5c6ac"),
        text(890, 288, "α = 3.992016 s⁻¹", 15, ORANGE, "bold"),
        box(875, 388, 270, 142, "Predicted corrected-time fit", "500 Hz", "#eaf8f4", "#b9dcd2"),
        text(890, 486, "α = 4 s⁻¹", 15, TEAL, "bold"),
        line(72, 566, 1146, 566, FAINT, 2),
        text(75, 598, "CONDITIONAL FUTURE CLOCK CHECK", 17, INK, "bold"),
        box(76, 613, 339, 76, "Independent 1000 Hz reference", "must have verified external timing"),
        line(415, 651, 463, 651, INK, 2, None, "arrow"),
        box(469, 613, 320, 76, "Capture through same recorder", "compare measured reference to 1000 Hz"),
        line(789, 651, 837, 651, INK, 2, None, "arrow"),
        box(843, 613, 299, 76, "Infer clock scale, conditionally", "same-clock file is circular"),
        text(75, 729, "Control: true 8000 Hz null plus invalid-file, window and channel refusals. Raw bytes and acquisition metadata stay preserved.", 14, MUTED),
    ]
    svg("s3b-clock-reference.svg", "Synthetic timebase ambiguity and conditional independent clock reference",
        "Exact generated fixture has 16032 PCM16 samples at true times n divided by 8016 seconds. The WAV header labels those same amplitudes n divided by 8000, producing apparent 499.001996 hertz and decay 3.992016 per second. A corrected-time CSV recovers 500 hertz and 4 per second. A future 1000-hertz calibration source must be independently timed; no physical clock has been measured.", "".join(parts), 760)


def _style_3d(ax, xlim, ylim, zlim):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)
    ax.set_box_aspect((xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0]), zoom=0.88)
    ax.set_xlabel("x (m)", labelpad=8)
    ax.set_ylabel("y (m)", labelpad=8)
    ax.set_zlabel("z (m)", labelpad=8)
    ax.tick_params(labelsize=8)
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
    ax.grid(True, alpha=0.2)


def cuboid(ax, a, b, color, edge=INK, alpha=1):
    x0, y0, z0 = a
    x1, y1, z1 = b
    p = [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),
         (x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    faces = [[p[i] for i in ids] for ids in ((0,1,2,3),(4,5,6,7),(0,1,5,4),
                                             (1,2,6,5),(2,3,7,6),(3,0,4,7))]
    ax.add_collection3d(Poly3DCollection(faces, facecolors=color, edgecolors=edge,
                                          linewidths=.8, alpha=alpha))


def s1_render():
    fig = plt.figure(figsize=(11, 8), facecolor=PAPER)
    ax = fig.add_subplot(111, projection="3d", facecolor=PAPER)
    ax.view_init(elev=25, azim=-64)
    # Tabletop at z=.63 m; all coordinate dimensions are nominal, not observations.
    table_x = [-.30, .80, .80, -.30, -.30]
    table_y = [-.30, -.30, .82, .82, -.30]
    ax.plot(table_x, table_y, [.63] * len(table_x), color="#b8c8d4", linewidth=1.4)
    ax.text(.48, -.27, .635, "tabletop z=0.63 m", fontsize=9, color=MUTED)
    # Movable 0.90 m-wide, 0.42 m-high rigid card on the tabletop.
    panel = [[(-.20, .60, .63), (.70, .60, .63), (.70, .60, 1.05), (-.20, .60, 1.05)]]
    ax.add_collection3d(Poly3DCollection(panel, facecolors="#cf9b72", edgecolors=ORANGE, alpha=.66, linewidths=1.5))
    cuboid(ax, (-.06, -.05, .65), (.06, .05, .82), "#9ebce1", BLUE)
    cuboid(ax, (.475, -.042, .665), (.525, .042, .82), "#adddd4", TEAL)
    cuboid(ax, (-.26, -.24, .635), (-.11, -.11, .66), "#c9d2db", MUTED)
    ax.scatter([0, .5], [0, 0], [.75, .75], color=[BLUE, TEAL], s=55, depthshade=False)
    ax.text(0, -.12, .85, "speaker S", color=BLUE, fontsize=10, weight="bold")
    ax.text(.5, -.13, .85, "phone mic M", color=TEAL, fontsize=10, weight="bold")
    # Audio-output cable; phone stores its own recording locally.
    ax.plot([-.17,-.13,-.10,-.04], [-.18,-.14,-.08,-.04], [.665,.665,.665,.69],
            color="#33485d", linewidth=2)
    ax.text(-.26, -.27, .70, "playback device", fontsize=9, color=MUTED)
    ax.plot([0, .5], [0, 0], [.75, .75], color=BLUE, linewidth=3, label="direct geometric path")
    ax.plot([0, .25, .5], [0, .60, 0], [.75, .75, .75], color=TEAL, linestyle="--", linewidth=2,
            label="illustrative specular ray")
    ax.plot([0, .5], [-.18, -.18], [.75, .75], color=INK, linewidth=1.5)
    ax.text(.25, -.18, .79, "0.50 m", color=INK, fontsize=9)
    ax.text(.72, .60, .76, "card at y=0.60 m", color=ORANGE, fontsize=9)
    _style_3d(ax, (-.30, .80), (-.30, .85), (.60, 1.10))
    ax.legend(loc="upper left", bbox_to_anchor=(.02, .88), fontsize=9)
    fig.suptitle("S1 proposed bench geometry · unbuilt", x=.06, y=.96, ha="left", fontsize=19, weight="bold", color=INK)
    fig.text(.06, .055, "Metre coordinates are nominal placement marks. Dashed ray is geometric only; card response and total transfer are unmeasured.",
             fontsize=10, color=MUTED)
    fig.savefig(OUT / "s1-bench-3d.png", dpi=180, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


def s2_render():
    fig = plt.figure(figsize=(11, 8), facecolor=PAPER)
    ax = fig.add_subplot(111, projection="3d", facecolor=PAPER)
    ax.view_init(elev=22, azim=-59)
    # Padded table top is the z=0 reference. Two book stacks carry the crossbar.
    ax.plot([-.10,.31,.31,-.10,-.10], [-.29,-.29,.29,.29,-.29], [0]*5,
            color="#9badb9", linewidth=1.4)
    cuboid(ax, (-.065,-.23,0), (.065,-.16,.42), "#cad9e3", MUTED, .7)
    cuboid(ax, (-.065,.16,0), (.065,.23,.42), "#cad9e3", MUTED, .7)
    ax.plot([0,0],[-.22,.22],[.42,.42], color=INK, linewidth=5)
    ax.plot([0,0],[0,0],[.42,.31], color="#8496a4", linestyle="--", linewidth=2)
    # Spoon handle and bowl: outline geometry, not a vibration-mode prediction.
    ax.plot([0,0],[0,0],[.31,.15], color=BLUE, linewidth=7)
    theta = np.linspace(0,2*np.pi,72)
    ax.plot(.032*np.cos(theta), .023*np.sin(theta), .12+0*theta,
            color=BLUE, linewidth=2.5)
    ax.scatter([0],[0],[.12], s=280, color="#89b3df", edgecolor=BLUE, depthshade=False)
    cuboid(ax, (.185,-.039,.045), (.215,.039,.19), "#aadbd2", TEAL)
    cuboid(ax, (.18,-.05,0), (.22,.05,.03), "#c4d2d9", MUTED)
    ax.scatter([.185],[0],[.12], s=55, color=TEAL, depthshade=False)
    ax.plot([0,.20],[0,0],[.12,.12], color=TEAL, linestyle="--", linewidth=2,
            label="0.20 m noncontact acoustic path")
    # A pencil with soft eraser is held near the strike point only for the tap.
    ax.plot([-.17,-.045],[-.13,-.017],[.22,.13], color=ORANGE, linewidth=4)
    ax.scatter([-.045],[-.017],[.13], color="#d9b89e", s=55, depthshade=False)
    ax.text(-.19,-.20,.26,"eraser tap",fontsize=9,color=ORANGE)
    ax.text(-.015,-.06,.20,"spoon",fontsize=10,color=BLUE,weight="bold")
    ax.text(.22,-.08,.21,"phone mic",fontsize=10,color=TEAL,weight="bold")
    ax.text(.05,.23,.44,"crossbar z=0.42 m",fontsize=9,color=INK)
    _style_3d(ax, (-.22,.34), (-.30,.32), (0,.47))
    ax.legend(loc="upper left", bbox_to_anchor=(.02,.88), fontsize=9)
    fig.suptitle("S2 proposed spoon ringdown geometry · unbuilt", x=.06, y=.96,
                 ha="left", fontsize=19, weight="bold", color=INK)
    fig.text(.06,.055,"Nominal metre coordinates. Gentle tap is withdrawn for decay; phone does not touch the spoon. No measured spectrum or damping.",
             fontsize=10,color=MUTED)
    fig.savefig(OUT / "s2-spoon-3d.png", dpi=180, bbox_inches="tight", facecolor=PAPER)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    CATALOG.parent.mkdir(exist_ok=True, parents=True)
    s1_plan()
    s1_ambiguity()
    chemical_identity_plate()
    b1_blind_target()
    s2_spoon_plan()
    s3b_clock_plan()
    s1_render()
    s2_render()
    entries = [
        {
            "id": "S1-bench-plan",
            "kind": "vector apparatus plan",
            "title": "Speaker, movable card and phone: proposed bench",
            "file": "assets/sound-lab-v3/s1-bench-plan.svg",
            "alt": "Top view: ordinary speaker at (0,0) m and phone microphone at (0.50,0) m, with a nominal 0.90 m wide movable card at y=0.60 m. Direct and illustrative reflected paths connect source to microphone. Separate digital output, speaker and room, and phone readout blocks show unknown factors.",
            "caption": "Unbuilt nominal setup for the S1 total-transfer question. Record no-card, card, no-card at fixed marks, then a separate 1 cm phone displacement and restoration control; document gain mode, geometry and room state. A card's reflection strength depends on wavelength and has not been measured. No physical 5 ms delay is asserted.",
            "units": "metres (m); positions relative to speaker S",
            "coordinates": {"speaker": [0, 0, .75], "phone_microphone": [.5, 0, .75], "tabletop_z": .63, "card_plane_y": .60, "card_x_span": [-.20, .70], "card_z_span": [.63, 1.05]},
            "materials": ["ordinary small speaker", "recording phone", "stiff card", "table and books or cardboard positioning jigs", "tape measure or marked paper", "playback device and audio-output cable"],
            "sourceIds": ["V3-SMITH-COMB", "V3-W3C-CAPTURE"], "hypothesisIds": ["S1A"], "status": "proposed, unbuilt; no physical measurements",
        },
        {
            "id": "S1-identifiability",
            "kind": "exact vector inference diagram",
            "title": "S1 synthetic total-transfer ambiguity",
            "file": "assets/sound-lab-v3/s1-identifiability.svg",
            "alt": "Two exact factorisations of the identical synthetic transfer: device d with three taps and acoustic e with a 40-sample delayed branch; or device d convolved with e and acoustic identity. Both yield the same total H. A source, device, air plus card, readout chain is proposed for a future physical audit.",
            "caption": "S1A is an exact synthetic computation: Y/X determines total H but does not uniquely attribute a delayed branch to the room. The model's 5 ms delay is not a measured physical reflection.",
            "units": "milliseconds (ms), synthetic model only",
            "coordinates": None, "sourceIds": ["V3-FARINA2000", "V3-SMITH-COMB"], "hypothesisIds": ["S1A"], "status": "computed model illustration; physical audit unbuilt",
        },
        {
            "id": "S1-bench-3d",
            "kind": "deterministic 3D geometry render",
            "title": "Proposed speaker, card and phone geometry",
            "file": "assets/sound-lab-v3/s1-bench-3d.png",
            "alt": "Three-dimensional metre-axis drawing of speaker and phone on short supports, 0.50 m apart at height 0.75 m, facing a stiff card at y=0.60 m. A solid direct ray and dashed illustrative specular ray are geometry only.",
            "caption": "Deterministic geometry from nominal coordinates; not a photograph or evidence of a built apparatus. The ray does not establish card reflectance or an isolated recorded echo.",
            "units": "metres (m)",
            "coordinates": {"speaker": [0, 0, .75], "phone_microphone": [.5, 0, .75], "tabletop_z": .63, "card_plane_y": .60, "card_x_span": [-.20, .70], "card_z_span": [.63, 1.05]},
            "sourceIds": ["V3-SMITH-COMB"], "hypothesisIds": ["S1A"], "status": "proposed, unbuilt; no physical measurements",
        },
        {
            "id": "alchemy-chemical-identity",
            "kind": "historical and chemical identity vector plate",
            "title": "Alchemy terms and modern candidate identities",
            "file": "assets/sound-lab-v3/alchemy-chemical-identity.svg",
            "alt": "Five context-dependent mappings: the conventional solar sign can indicate gold Au in literal context; Saturn can indicate lead Pb when a passage establishes it, but also means something else elsewhere; antimony may be sulfide ore or metallic regulus, arsenic often trioxide, and vitriol iron or copper sulfate family. Every candidate is unassayed.",
            "caption": "Newton Chymistry's primary manuscript index and its separate editorial symbols/glossary support conditional readings, not universal symbol decoding. The guide's conventional solar symbol has not been checked against a particular manuscript in this plate. Actual sample identity, phase and isotopes need independent analysis; no sample or preparation is supplied.",
            "units": "chemical symbols/formulae; no physical scale",
            "coordinates": None,
            "sourceIds": ["V3-NEWTON-INDEX", "V3-NEWTON-SYMBOLS", "V3-NEWTON-GLOSSARY"],
            "mappingFile": "docs/panel-v3/alchemy-dictionary.json",
            "hypothesisIds": ["alchemy-identity"],
            "status": "source-grounded candidate mapping; no specimen or assay",
        },
        {
            "id": "B1-blind-target-flow",
            "kind": "exact vector information-custody protocol",
            "title": "Human and AI concealed-target protocol",
            "file": "assets/sound-lab-v3/b1-blind-target-flow.svg",
            "alt": "Three lanes: an independent offline custodian shuffles 80 concealed four-symbol targets in twenty balanced blocks and distributes trial IDs plus salted commitments; a human and target-blind AI lock independent timestamped guesses without seeing one another; only after all reports freeze does the analyst receive targets and salts to verify and score. Separate disclosed positive control is excluded.",
            "caption": "Proposed, unrun human/AI information-access test. Four neutral categories are each used once within each concealed block. A shared category/prompt prior can make reporters agree without target information. The actual analysis needs an exact within-block randomization test; a salted hash is an integrity aid, not a replacement for independent custody. No consciousness apparatus or effect is claimed.",
            "units": "80 main trials; 20 blocks × 4 categories; UTC timestamps",
            "coordinates": {"lanes": ["independent custodian", "human and AI target-blind stations", "analyst after all response records freeze"], "physicalSeparation": "distinct custody and station devices or opaque target envelopes; no specified metre spacing"},
            "materials": ["independent offline laptop or opaque envelopes", "four neutral symbol cards", "participant form and clock", "separate target-blind AI interface", "response export and sealed target log"],
            "sourceIds": ["C-BASHAR-ANKA2014", "C-GATEWAY1983", "C-AIR1995", "C-AI-INDICATORS2023"],
            "hypothesisIds": ["B1", "B2", "B3"],
            "protocolFile": "research/consciousness-v3/human-ai-protocol.md",
            "status": "proposed protocol only; zero participants or live AI trials",
        },
        {
            "id": "S2-spoon-plan",
            "kind": "vector apparatus side elevation",
            "title": "Suspended spoon and noncontact microphone",
            "file": "assets/sound-lab-v3/s2-spoon-plan.svg",
            "alt": "Side elevation of a spoon suspended from loose thread below a crossbar 0.42 m above a padded table. Bowl center at 0.12 m; phone microphone 0.20 m horizontally away at the same height. Pencil eraser provides a gentle tap, then is withdrawn; recording includes quiet pre-roll and ringdown, five repeats, a light-touch control and return references.",
            "caption": "Unbuilt low-material ringdown candidate for S2. Preserve at least one second before and two seconds after each impact, all takes and clipping flags; record impact time and choose a stated post-impact fit window. The touched spoon changes loading and boundary conditions. S2's generated-PCM single-mode fit does not establish a real spoon's material damping.",
            "units": "metres (m); seconds (s)",
            "coordinates": {"spoon_bowl": [0,0,.12], "phone_microphone": [.20,0,.12], "crossbar_center": [0,0,.42], "padded_tabletop_z": 0},
            "materials": ["unbroken metal or wooden spoon", "cotton thread", "books and short crossbar", "padded table", "phone recording WAV", "pencil with eraser", "tape measure"],
            "sourceIds": ["V3-FEYN23", "V3-W3C-CAPTURE"], "hypothesisIds": ["S2A", "S2B"],
            "protocolFile": "research/sound-lab-v3/protocol.md",
            "status": "proposed, unbuilt; synthetic S2 model separate",
        },
        {
            "id": "S2-spoon-3d",
            "kind": "deterministic 3D geometry render",
            "title": "Suspended spoon and phone geometry",
            "file": "assets/sound-lab-v3/s2-spoon-3d.png",
            "alt": "Three-dimensional metre-axis drawing of a spoon on thread below a crossbar supported by books above padded tabletop, an eraser-tipped pencil nearby, and a phone microphone 0.20 m from the bowl with a dashed noncontact acoustic path.",
            "caption": "Deterministic render of the nominal, unbuilt S2 setup; not a photograph of a tap or evidence for a mode or decay constant. The eraser is withdrawn after the gentle tap and the phone stays fixed for touch and reference controls.",
            "units": "metres (m)",
            "coordinates": {"spoon_bowl": [0,0,.12], "phone_microphone": [.20,0,.12], "crossbar_center": [0,0,.42], "padded_tabletop_z": 0},
            "sourceIds": ["V3-FEYN23"], "hypothesisIds": ["S2A", "S2B"],
            "status": "proposed, unbuilt; no physical measurements",
        },
        {
            "id": "S3B-clock-reference",
            "kind": "exact vector sample and timing-flow plan",
            "title": "Sample clock and corrected-time reference",
            "file": "assets/sound-lab-v3/s3b-clock-reference.svg",
            "alt": "The identical 16032 generated PCM16 samples fork into a WAV carrying a false 8000 hertz header and a corrected-time CSV with timestamps n divided by 8016 seconds. Fits shift from 499.001996 hertz and 3.992016 inverse seconds to the fixture's 500 hertz and 4 inverse seconds. A separate proposed independent 1000-hertz timing reference is conditional and unmeasured.",
            "caption": "S3B frozen model prediction: wrong declared sample rate changes inferred frequency and decay without changing sample amplitudes. The corrected axis is known only because the fixture constructs samples at 8016 samples/s. A real recorder would need a genuinely external verified time reference; a same-clock file is circular. The 8000 Hz null and invalid-input refusals are controls, not hardware results. A constant calibration tone may fit at the α = 0 boundary, which must remain flagged.",
            "units": "sample index n; sample rate Hz; time s; decay s⁻¹",
            "coordinates": {"sample_indices": [0,16031], "sample_count": 16032, "header_time_s": "n/8000", "fixture_time_s": "n/8016", "conditional_external_reference_Hz": 1000},
            "materials": ["generated PCM16 WAV", "header metadata", "corrected-time CSV", "immutable source file", "conditional independently timed 1000 Hz reference source for future hardware check"],
            "sourceIds": ["V3-FARINA2000", "V3-W3C-CAPTURE"], "hypothesisIds": ["S3B"],
            "contractFile": "research/sound-lab-v3/S3B/contract.json",
            "status": "exact synthetic fixture; independent physical reference only proposed, not measured",
        },
    ]
    if (OUT / "concept.png").exists():
        entries.append({
            "id": "sound-bench-concept",
            "kind": "generated concept image",
            "title": "Possible tabletop sound-lab components",
            "file": "assets/sound-lab-v3/concept.png",
            "alt": "Illustrative tabletop scene with speaker, board, phones, a laptop, a metal bowl and soft mallet. The board is pictured between speaker and phone, unlike the separately specified side-reflector geometry.",
            "caption": "Generated visual concept only. Component placement, cables, screen waveforms and board orientation are not the experiment specification or observed data. Use the dimensioned vector plans for the proposed setups.",
            "units": "none; image not dimensioned",
            "coordinates": None,
            "sourceIds": [], "hypothesisIds": [],
            "status": "illustrative generation; not dimensioned, built or measured",
        })
    for entry in entries:
        entry["physicalApparatusBuilt"] = False
        entry["physicalMeasurementClaimed"] = False
    CATALOG.write_text(json.dumps({
        "schemaVersion": 1,
        "generatedBy": "assets/sound-lab-v3/generate_setups.py",
        "empiricalBoundary": "Geometry and information-flow drawings are proposals. Synthetic computations and generated imagery are labeled separately; no physical apparatus, target study, specimen assay or physiological measurement was performed.",
        "entries": entries,
    }, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
