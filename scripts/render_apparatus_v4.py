#!/usr/bin/env python3
"""Render proposed V4 apparatus from declared metre coordinates; no measured data.

Only Python, numpy and matplotlib are needed. All SVG geometry uses the same
coordinate constants as the three-dimensional surfaces and coordinate export.
Run: python scripts/render_apparatus_v4.py
"""
from pathlib import Path
import hashlib
import json
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/sound-lab-v4"
PAPER, INK, TEAL, MUTED = "#f6f1e7", "#183c3a", "#237b73", "#61736d"
GOLD, LINE, METAL = "#b57535", "#cbd7cc", "#a9b8b3"
BOWL = np.array([.32, .26, .08])  # center of rim circle
MIC = np.array([.59, .26, .08])
PILOT = np.array([.59, .61, .08])  # emitting port, facing -y
MONITOR = np.array([.59, .53, .08])
RADIUS, TABLE_X, TABLE_Y = .07, 1., .70
SX, SY, SCALE = 100, 265, 750
SCENE_FACES, SCENE_COLORS = [], []


def xy(p):
    return SX + SCALE*p[0], SY + SCALE*(TABLE_Y-p[1])


def txt(x, y, s, size=18, color=INK, weight="normal", anchor="start"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}" '
            f'font-family="Inter,Arial,sans-serif">{escape(s)}</text>')


def seg(a, b, color=INK, width=2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="M{a[0]:.2f},{a[1]:.2f} L{b[0]:.2f},{b[1]:.2f}" fill="none" stroke="{color}" stroke-width="{width}"{d}/>'


def rect(x, y, w, h, fill=PAPER, stroke=LINE, radius=0):
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def physical_rect(x0, y0, dx, dy, fill, stroke=LINE):
    x, y = xy([x0, y0+dy])
    return rect(x, y, dx*SCALE, dy*SCALE, fill, stroke, 4)


def circle(x, y, r, fill, stroke=TEAL, width=2):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def number(p, n, dx=0, dy=0):
    x, y = xy(p)
    return circle(x+dx, y+dy, 16, INK, PAPER)+txt(x+dx, y+dy+6, str(n), 16, PAPER, "bold", "middle")


def dimension(a, b, label, text_offset=(0, -10)):
    # Already screen coordinates, so text never depends on Matplotlib fonts.
    out = seg(a, b, MUTED, 1.5)
    d = np.array(b)-a
    n = np.array([-d[1], d[0]])/np.linalg.norm(d)*6
    out += seg(np.array(a)-n, np.array(a)+n, MUTED, 1.5)
    out += seg(np.array(b)-n, np.array(b)+n, MUTED, 1.5)
    mid = (np.array(a)+b)/2 + text_offset
    return out+txt(*mid, label, 17, INK, "bold", "middle")


def note(y, number_, title, lines):
    out = circle(930, y-5, 15, INK, INK)+txt(930, y+1, str(number_), 15, PAPER, "bold", "middle")
    out += txt(958, y, title, 19, INK, "bold")
    for i, line in enumerate(lines):
        out += txt(958, y+26+23*i, line, 16, MUTED)
    return out


def plan(upgrade):
    id_ = "dual-channel" if upgrade else "phone-witness"
    title = "Two microphones, one recorder" if upgrade else "Two phones, one mixed recording"
    out = [rect(0, 0, 1500, 1120, PAPER, PAPER)]
    out += [txt(55, 51, "PROPOSED SOUND BENCH / " + ("B · OPTIONAL UPGRADE" if upgrade else "A · LEAST MATERIALS"), 16, TEAL, "bold"),
            txt(55, 100, title, 38, INK, "bold"),
            txt(55, 137, "Construction coordinates only · no physical measurements · all dimensions in centimetres (cm)", 19, MUTED),
            seg((55, 165), (1445, 165), LINE),
            txt(100, 214, "TOP VIEW", 16, TEAL, "bold"),
            dimension((100, 240), (850, 240), "100 cm tabletop"),
            dimension((73, 265), (73, 790), "70 cm", (-30, 0)),
            rect(100, 265, 750, 525, "#fffdf8", LINE, 9)]
    # A physical 10 cm reference scale; grid is deliberately subtle.
    for x in np.arange(.1, 1., .1):
        out += [seg(xy([x, 0]), xy([x, .7]), "#e7e9de", 1)]
    for y in np.arange(.1, .7, .1):
        out += [seg(xy([0, y]), xy([1., y]), "#e7e9de", 1)]
    out += [physical_rect(.24, .18, .16, .16, "#e6dbc5", "#c3b499")]
    cx, cy = xy(BOWL)
    out += [circle(cx, cy, RADIUS*SCALE, METAL, INK), circle(cx, cy, (RADIUS-.004)*SCALE, "#e2e8df", "#83958b"),
            circle(cx, cy, .025*SCALE, "#c9d3c9", "#83958b", 1), number(BOWL, 1, -68, -20)]
    # Pilot phone elevated on a book/soft pad, port at exact declared coordinate.
    out += [physical_rect(.55, .60, .08, .09, "#e6dbc5", "#c3b499"),
            physical_rect(.5525, .61, .075, .012, "#bad0c4", TEAL)]
    px, py = xy(PILOT)
    out += [seg((px-10, py), (px+10, py), TEAL, 6), number(PILOT, 3, -53, -32)]
    # Source-to-mic acoustic route is a connector, not a calculated ray/field.
    out += [seg(xy([.39, .26]), xy(MIC), TEAL, 3, "8 7"),
            seg(xy(PILOT), xy(MIC), GOLD, 3, "8 7")]
    if upgrade:
        # Microphone capsules at front (left for sample, back for monitor).
        out += [physical_rect(.59, .252, .055, .016, TEAL, INK),
                physical_rect(.582, .48, .016, .05, GOLD, INK),
                physical_rect(.57, .23, .085, .06, "none", "#9eb5aa"),
                physical_rect(.56, .465, .06, .065, "none", "#9eb5aa"),
                physical_rect(.75, .30, .18, .15, "#dbe6dc", TEAL),
                physical_rect(.77, .35, .11, .065, "#294c46", TEAL)]
        mx, my = xy(MONITOR)
        out += [circle(mx, my, 5, GOLD, INK), number(MONITOR, 4, -39, 5), number([.85, .375], 5, 5, 44)]
        # Distinct analog cables join numbered inputs; no promise of equal gains.
        pts1 = [MIC+np.array([.055, 0, 0]), [.70, .26], [.70, .33], [.75, .33]]
        pts2 = [[.59, .48], [.69, .48], [.69, .42], [.75, .42]]
        for pts, color in [(pts1, TEAL), (pts2, GOLD)]:
            out += [seg(xy(a), xy(b), color, 3) for a, b in zip(pts, pts[1:])]
        out += [txt(*xy([.79, .31]), "CH 1", 13, TEAL, "bold"), txt(*xy([.79, .43]), "CH 2", 13, GOLD, "bold"),
                dimension((650, py), (650, my), "8 cm", (36, 4))]
    else:
        out += [physical_rect(.64, .21, .11, .10, "#e6dbc5", "#c3b499"),
                physical_rect(.59, .2225, .15, .075, "#bad0c4", TEAL),
                physical_rect(.61, .2325, .11, .055, "#294c46", TEAL)]
    mx, my = xy(MIC)
    out += [circle(mx, my, 6, TEAL, PAPER), number(MIC, 2, 6, 55),
            dimension((xy([.39, .18])[0], 703), (mx, 703), "20 cm rim–mic"),
            dimension((cx-RADIUS*SCALE, 525), (cx+RADIUS*SCALE, 525), "Ø14 cm"),
            dimension((450, py), (450, my), "35 cm", (37, 4))]
    # Tap pencil parked clear of vessel after impact.
    out += [seg(xy([.15, .40]), xy([.25, .36]), GOLD, 10), circle(*xy([.25, .36]), 6, "#c99278", GOLD),
            number([.15, .40], 6, -23, -19),
            txt(110, 824, "Grid = 10 cm. All microphone / emitting ports: z = 8 cm above tabletop.", 17, MUTED),
            txt(110, 850, "Bowl height 7 cm + soft support 1 cm. Port openings stay unobstructed.", 17, MUTED)]
    out += [note(212, 1, "Empty metal bowl + soft pad", ["Known intact household vessel; Ø14 × 7 cm", "is a drawing choice, not a tuned resonator."]),
            note(305, 2, "Sample microphone", ["Face the rim; keep location and orientation.", "A: phone records both sources in one track."]),
            note(398, 3, "Steady pilot source", ["A second phone can use its own speaker.", "Speaker port faces the sample microphone."])]
    if upgrade:
        out += [note(491, 4, "Optional source-monitor microphone", ["8 cm from pilot port; contains room sound.", "Cross-talk and source drift remain possible."]),
                note(584, 5, "Recorder + two analogue inputs", ["Both channels share a sample clock.", "That does not prove common gain."]),
                note(677, 6, "Gentle tap → withdraw pencil", ["Pencil eraser gives a brief impact.", "Do not keep tapper in contact during decay."])]
    else:
        out += [note(491, 6, "Gentle tap → withdraw pencil", ["Pencil eraser gives a brief impact.", "Save quiet pre-roll and every raw take."]),
                txt(916, 617, "Two phones are sufficient to explore", 20, INK, "bold"),
                txt(916, 646, "this geometry. A separate speaker is optional.", 17, MUTED),
                txt(916, 695, "Log gain, noise suppression, echo cancellation,", 17, MUTED),
                txt(916, 720, "volume, supports, timing and actual positions.", 17, MUTED)]
    out += [rect(55, 895, 1390, 180, "#e4ece1", LINE, 12),
            txt(80, 931, "WHAT THIS ARRANGEMENT CAN TEST", 16, TEAL, "bold")]
    if upgrade:
        lines = ["Save sample and monitor channels together; compare pilot changes across channels and repeated source-only controls.",
                 "R1 corrects a synthetic target slope only if the reference is stable and both gains follow the same drift.",
                 "Two microphones add observations. They do not establish stable paths, equal gains, isolated modes or intrinsic damping."]
    else:
        lines = ["Explore whether a steady pilot and a tap decay can be captured without clipping at fixed positions.",
                 "R1 validates ideally separated model channels. This single-microphone mixture needs its own separation checks.",
                 "A drifting pilot can reflect source, room or recorder changes; a stable pilot is not a calibration certificate."]
    for i, s in enumerate(lines):
        out += [txt(80, 968+i*32, s, 20 if i==0 else 18, INK if i==0 else MUTED)]
    desc = ("Proposed, unbuilt top-view plan, not measurements. A 100 by 70 centimetre tabletop holds a "
            "14-centimetre-diameter bowl on a 1-centimetre pad. The sample microphone is 20 centimetres "
            "from the rim; the pilot emitting port is 35 centimetres from the sample microphone. All "
            "ports are 8 centimetres above tabletop. " + ("Two wired microphone channels share a recorder; "
            "the monitor capsule is 8 centimetres from the source. Common gain is unproven." if upgrade else
            "One phone records a mixture; a second phone supplies pilot sound. R1 does not validate mono separation."))
    data = ('<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1120" viewBox="0 0 1500 1120" '
            'role="img" aria-labelledby="title desc"><title id="title">'+escape(title)+'</title><desc id="desc">'+escape(desc)+'</desc>'+"".join(out)+"</svg>")
    (OUT/f"{id_}-plan.svg").write_text(data)


def cuboid(ax, origin, size, color, alpha=1):
    x,y,z = origin; dx,dy,dz=size
    v=np.array([[x,y,z],[x+dx,y,z],[x+dx,y+dy,z],[x,y+dy,z],
                [x,y,z+dz],[x+dx,y,z+dz],[x+dx,y+dy,z+dz],[x,y+dy,z+dz]])
    faces=[[v[i] for i in face] for face in [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]]
    # Fine surface quads prevent a broad support face from occluding a higher
    # phone or bowl face in the painter's depth sort of this static renderer.
    for face in faces:
        a,b,c,d=np.asarray(face)
        nu=max(1,int(np.ceil(np.linalg.norm(b-a)/.012)))
        nv=max(1,int(np.ceil(np.linalg.norm(d-a)/.012)))
        for i in range(nu):
            for j in range(nv):
                add_face([a+u*(b-a)+v*(d-a) for u,v in [(i/nu,j/nv),((i+1)/nu,j/nv),((i+1)/nu,(j+1)/nv),(i/nu,(j+1)/nv)]],color)


def add_face(face, color):
    face=np.asarray(face)
    normal=np.cross(face[1]-face[0],face[2]-face[0])
    norm=np.linalg.norm(normal)
    light=np.array([-.5,-.8,1.]); light/=np.linalg.norm(light)
    shade=.7+.3*abs(np.dot(normal/norm,light)) if norm else .9
    SCENE_FACES.append(face)
    SCENE_COLORS.append(tuple(np.clip(np.array(to_rgb(color))*shade,0,1)))


def surface(x, y, z, color):
    for i in range(x.shape[0]-1):
        for j in range(x.shape[1]-1):
            add_face([[x[a,b],y[a,b],z[a,b]] for a,b in [(i,j),(i+1,j),(i+1,j+1),(i,j+1)]],color)


def render3d(upgrade):
    SCENE_FACES.clear(); SCENE_COLORS.clear()
    plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":11, "text.color":INK, "axes.labelcolor":MUTED, "xtick.color":MUTED, "ytick.color":MUTED, "svg.hashsalt":"apparatus-v4"})
    fig=plt.figure(figsize=(15,10),facecolor=PAPER)
    ax=fig.add_axes([.015,.19,.70,.67],projection="3d",facecolor=PAPER)
    # Outline only: mplot3d's collection-level depth sorter can otherwise paint
    # a large opaque tabletop over smaller objects even when their z is higher.
    boundary=np.array([[0,0,0],[1,0,0],[1,.7,0],[0,.7,0],[0,0,0]])
    ax.plot(boundary[:,0],boundary[:,1],boundary[:,2],color="#b8c7ba",lw=1.8)
    cuboid(ax,(.24,.18,0),(.16,.16,.01),"#d3be99")
    # Open bowl: revolved outer/inner wall joined by rim annulus, plus bottom.
    theta=np.linspace(0,2*np.pi,129)
    h=np.linspace(0,1,50)
    t,u=np.meshgrid(theta,h)
    z=.01+.07*u
    r=.024+.046*np.sqrt(u)
    surface(BOWL[0]+r*np.cos(t),BOWL[1]+r*np.sin(t),z,METAL)
    ri=np.maximum(.001,r-.004)
    surface(BOWL[0]+ri*np.cos(t),BOWL[1]+ri*np.sin(t),z+.002*(1-u),"#cdd5cf")
    rt, tt=np.meshgrid(np.linspace(.066,.07,3),theta)
    surface(BOWL[0]+rt*np.cos(tt),BOWL[1]+rt*np.sin(tt),np.full_like(rt,.08),"#e2e8df")
    rb,tb=np.meshgrid(np.linspace(0,.022,12),theta)
    surface(BOWL[0]+rb*np.cos(tb),BOWL[1]+rb*np.sin(tb),np.full_like(rb,.012),"#c2cec4")
    cuboid(ax,(.55,.60,0),(.08,.09,.075),"#ddcfb5")
    cuboid(ax,(.5525,.61,.075),(.075,.012,.15),TEAL)
    if upgrade:
        cuboid(ax,(.57,.23,0),(.085,.06,.015),"#b8c7ba")
        cuboid(ax,(.625,.251,.015),(.012,.018,.065),METAL)
        cuboid(ax,(.59,.252,.072),(.055,.016,.016),TEAL)
        cuboid(ax,(.56,.465,0),(.06,.065,.015),"#b8c7ba")
        cuboid(ax,(.583,.484,.015),(.014,.014,.065),METAL)
        cuboid(ax,(.582,.48,.072),(.016,.05,.016),GOLD)
        cuboid(ax,(.75,.30,.005),(.18,.15,.035),"#b5cdbd")
        for pts,c in [([[.645,.26,.08],[.70,.26,.005],[.70,.33,.005],[.75,.33,.025]],TEAL),
                      ([[.59,.48,.08],[.69,.48,.005],[.69,.42,.005],[.75,.42,.025]],GOLD)]:
            a=np.array(pts); ax.plot(a[:,0],a[:,1],a[:,2],color=c,lw=2)
        ax.scatter(*MONITOR,c=GOLD,s=35,depthshade=False)
    else:
        cuboid(ax,(.64,.21,0),(.11,.10,.075),"#ddcfb5")
        cuboid(ax,(.59,.2225,.075),(.15,.075,.01),TEAL)
    ax.add_collection3d(Poly3DCollection(SCENE_FACES,facecolors=SCENE_COLORS,edgecolors="none",linewidths=0,zsort="average"))
    ax.scatter(*MIC,c=TEAL,s=35,depthshade=False)
    ax.scatter(*PILOT,c=GOLD,s=35,depthshade=False)
    ax.plot([.15,.25],[.40,.36],[.008,.008],color=GOLD,lw=6)
    ax.scatter(.25,.36,.008,c="#c99278",s=50)
    for a,b,c in [(np.array([.39,.26,.08]),MIC,TEAL),(PILOT,MIC,GOLD)]:
        ax.plot([a[0],b[0]],[a[1],b[1]],[a[2],b[2]],ls="--",lw=1.8,c=c)
    labels=[(BOWL,"1",(-.04,0,.045)),(MIC,"2",(0,-.02,.035)),(PILOT,"3",(0,.01,.07)),
            (np.array([.16,.40,.008]),"6",(-.01,0,.04))]
    if upgrade:
        labels += [(MONITOR,"4",(.035,0,.055)),(np.array([.84,.37,.04]),"5",(.02,0,.06))]
    for p,t,d in labels:
        q=p+d; ax.text(*q,t,color=PAPER,fontsize=12,ha="center",va="center",zorder=999,bbox=dict(boxstyle="circle,pad=.25",fc=INK,ec=PAPER,lw=1))
    ax.set(xlim=(0,1),ylim=(0,.7),zlim=(0,.3),xlabel="x / m",ylabel="y / m",zlabel="z / m")
    ax.set_box_aspect((1,.7,.3)); ax.view_init(elev=34,azim=-57)
    ax.set_xticks(np.arange(0,1.01,.2)); ax.set_yticks(np.arange(0,.71,.2)); ax.set_zticks([0,.1,.2,.3])
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.pane.set_alpha(0); axis._axinfo["grid"]["color"]="#d8ded2"
    title="B · Two-channel observation" if upgrade else "A · The least-material bench"
    fig.text(.055,.945,"DETERMINISTIC 3D GEOMETRY / PROPOSED",fontsize=12,weight="bold",color=TEAL)
    fig.text(.055,.897,title,fontsize=27,weight="bold")
    fig.text(.055,.86,"No physical apparatus or measurements are claimed. Axes are metres (m).",fontsize=13,color=MUTED)
    x,y=.73,.76
    legend=[("1", "Empty bowl", "Soft 1 cm pad; rim height 8 cm."),
            ("2", "Sample microphone", "20 cm from nearest bowl rim."),
            ("3", "Pilot phone speaker", "35 cm from sample microphone.")]
    if upgrade:
        legend += [("4","Monitor microphone","8 cm from pilot emitting port."),("5","Dual-input recorder","Shared clock ≠ proven equal gains.")]
    legend += [("6","Pencil eraser","Gentle tap, then withdraw.")]
    for n,a,b in legend:
        fig.text(x,y,n,color=PAPER,fontsize=10,bbox=dict(boxstyle="circle,pad=.3",fc=INK,ec=INK))
        fig.text(x+.033,y,a,fontsize=13,weight="bold")
        fig.text(x+.033,y-.028,b,fontsize=10.8,color=MUTED)
        y-=.083
    fig.text(.055,.115,"Dashed connectors show signal routes, not calculated sound fields.",fontsize=13,weight="bold")
    fig.text(.055,.083,"Solid cables appear only in B. Both rigs need source, placement, gain and cross-talk checks.",fontsize=12,color=MUTED)
    fig.text(.055,.052,"Generated from metre coordinates; perspective changes apparent lengths. Use the paired dimensioned plan.",fontsize=11,color=MUTED)
    fig.savefig(OUT/("dual-channel-3d.png" if upgrade else "phone-witness-3d.png"),dpi=160,facecolor=PAPER)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    assert np.isclose(np.linalg.norm(MIC[:2]-BOWL[:2])-RADIUS,.20)
    assert np.isclose(np.linalg.norm(PILOT-MIC),.35)
    assert np.isclose(np.linalg.norm(PILOT-MONITOR),.08)
    for upgrade in [False, True]:
        plan(upgrade); render3d(upgrade)
    data={
        "schemaVersion":1,"coordinateUnit":"m","displayDimensionUnit":"cm",
        "status":"proposed, unbuilt; no physical measurements",
        "generatedBy":"scripts/render_apparatus_v4.py",
        "coordinateFrame":"tabletop upper surface z=0; x across 1.00 m width; y along 0.70 m depth",
        "tabletop":{"extent_m":[1,.7],"z_m":0},
        "bowl":{"rimCenter_m":BOWL.tolist(),"outerRadius_m":RADIUS,"height_m":.07,"supportThickness_m":.01,
                "wallThicknessIllustration_m":.004,"note":"generic revolved drawing, not a particular material or measured specimen"},
        "sampleMicrophonePort_m":MIC.tolist(),"pilotEmittingPort_m":PILOT.tolist(),"optionalMonitorPort_m":MONITOR.tolist(),
        "dimensions_m":{"nearestBowlRimToSampleMicrophone":.20,"pilotToSampleMicrophone":.35,"pilotToMonitor":.08},
        "alternatives":[
            {"id":"phone-witness","files":["phone-witness-plan.svg","phone-witness-3d.png"],
             "parts":["intact metal bowl","soft support","pencil eraser","recording phone","second phone with speaker for pilot","stable supports and marked ruler"],
             "recording":"one microphone records target plus reference; mono separation not validated by R1",
             "optionalSubstitution":"An available small speaker/player can replace the pilot phone; no purchase is required by this proposal."},
            {"id":"dual-channel","files":["dual-channel-plan.svg","dual-channel-3d.png"],
             "parts":["same bowl, pilot and soft supports","sample microphone","source-monitor microphone","stable low microphone stands","two analogue cables","two-input recorder with common sampling clock"],
             "recording":"two input tracks, neither ideal separated nor proven to share gain; cross-talk and processing must be characterized"}],
        "r1ClaimBoundary":"R1 ideal separated stereo fixtures do not establish mono extraction, source stability, common hardware gain or intrinsic damping.",
        "signalConnectorMeaning":"schematic acoustic or cable routing, no calibrated field, loss, phase or propagation model",
        "verification":{"distancesComputedFromCoordinates":True,"physicalApparatusBuilt":False,"physicalMeasurementClaimed":False},
    }
    (OUT/"apparatus-coordinates.json").write_text(json.dumps(data,indent=2)+"\n")
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.iterdir()) if p.name in ["phone-witness-plan.svg","phone-witness-3d.png","dual-channel-plan.svg","dual-channel-3d.png","apparatus-coordinates.json"]}
    (OUT/"apparatus-manifest.json").write_text(json.dumps({"generatorSha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"filesSha256":hashes},indent=2)+"\n")
    print("Rendered 2 dimensioned SVG plans and 2 3D geometry images; coordinate distances verified.")


if __name__=="__main__":
    main()
