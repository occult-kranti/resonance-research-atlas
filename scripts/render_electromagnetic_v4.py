#!/usr/bin/env python3
"""Draw the frozen R3 electrical topology and a proposed magnetic force bench.

No empirical data are rendered. Numerical RLC values belong to the synthetic
contract. Bench dimensions are proposed coordinates, not optimized hardware.
Keeps the earlier sound apparatus and its manifest unchanged.
"""
from pathlib import Path
import hashlib
import importlib.util
import json
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"assets/sound-lab-v4"
spec=importlib.util.spec_from_file_location("sound_apparatus",ROOT/"scripts/render_apparatus_v4.py")
geo=importlib.util.module_from_spec(spec); spec.loader.exec_module(geo)
PAPER,INK,TEAL,MUTED,GOLD,LINE=geo.PAPER,geo.INK,geo.TEAL,geo.MUTED,geo.GOLD,geo.LINE
t,l,r,c=geo.txt,geo.seg,geo.rect,geo.circle
TEST=np.array([.36,.30,.074])
MAGNET=np.array([.36,.30,.161])
TEST_TOP=.078
MAGNET_BOTTOM=.158
MAGNET_TOP=.164


def save_svg(name,title,desc,body,height=1100):
    data=(f'<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="{height}" viewBox="0 0 1500 {height}" '
          f'role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>'
          '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
          f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>'+r(0,0,1500,height,PAPER,PAPER)+''.join(body)+'</svg>')
    (OUT/name).write_text(data)
    ET.parse(OUT/name)


def arrow(x1,y1,x2,y2,color=INK,width=3):
    return f'<path d="M{x1},{y1} L{x2},{y2}" fill="none" stroke="{color}" stroke-width="{width}" marker-end="url(#arrow)"/>'


def node(x,y):
    return c(x,y,5,INK,INK)


def resistor(x1,y1,x2,y2,label,vertical=False):
    if vertical:
        return [l((x1,y1),(x1,y1+20),INK,3),r(x1-18,y1+20,36,y2-y1-40,PAPER,INK),l((x1,y2-20),(x1,y2),INK,3),t(x1+35,(y1+y2)/2,label,20,INK,"bold")]
    return [l((x1,y1),(x1+20,y1),INK,3),r(x1+20,y1-18,x2-x1-40,36,PAPER,INK),l((x2-20,y1),(x2,y1),INK,3),t((x1+x2)/2,y1+54,label,20,INK,"bold","middle")]


def electrical():
    b=[t(55,50,"ELECTRICITY / R3 MODEL TOPOLOGY + PROPOSED MEASUREMENT BOUNDARY",16,TEAL,"bold"),
       t(55,99,"Voltage gain is not an energy surplus",38,INK,"bold"),
       t(55,136,"Exact series RLC topology; numerical values below belong to the frozen simulation, not a component kit.",19,MUTED),l((55,165),(1445,165),LINE)]
    # Passive branch boundary excludes the source. Meter parasitics are outside
    # this ideal model and must be included in a later hardware budget.
    b += [r(370,220,915,480,"#e9eee2",LINE,12),t(395,250,"PASSIVE LOAD + STORAGE BOUNDARY",16,TEAL,"bold")]
    # Source and return.
    b += [l((220,350),(220,435),INK,3),l((220,545),(220,665),INK,3),c(220,490,55,PAPER,INK,3),
          '<path d="M182,490 C194,462 206,462 220,490 S246,518 258,490" fill="none" stroke="#183c3a" stroke-width="3"/>',
          t(275,471,"+",24,INK,"bold"),t(275,529,"−",24,INK,"bold"),
          t(220,601,"vₛ(t)",23,INK,"bold","middle"),t(220,631,"isolated source",16,MUTED,"normal","middle"),
          l((220,350),(390,350),INK,3),l((220,665),(1190,665),INK,3)]
    # Current transducer is series, before every passive element.
    b += [c(390,350,30,PAPER,INK,2),t(390,357,"I",21,INK,"bold","middle"),l((420,350),(475,350),INK,3),
          t(390,303,"waveform current probe",16,MUTED,"normal","middle"),arrow(250,312,320,312),t(281,291,"i(t)",19,INK,"bold","middle")]
    b += resistor(475,350,585,350,"Rᵢ = 1 Ω")
    b += [l((585,350),(650,350),INK,3)]
    # Four coil turns; exact conventional topology, not a coil build drawing.
    coil='M650,350 '
    for k in range(4):
        x=650+27*k; coil+=f'C{x},322 {x+27},322 {x+27},350 '
    b += [f'<path d="{coil}" fill="none" stroke="{INK}" stroke-width="3"/>',l((758,350),(875,350),INK,3),
          t(704,404,"L = 10 mH",20,INK,"bold","middle")]
    # Capacitor positive plate is on the incoming-current side.
    b += [l((875,315),(875,385),INK,4),l((901,315),(901,385),INK,4),l((901,350),(1190,350),INK,3),
          t(863,306,"+",21,INK,"bold"),t(895,306,"−",21,INK,"bold"),t(888,404,"C = 100 µF",20,INK,"bold","middle"),
          l((1190,350),(1190,445),INK,3)]
    b += resistor(1190,445,1190,590,"Rₗ = 4 Ω",True)
    b += [l((1190,590),(1190,665),INK,3)]
    # Voltage acquisition probes are explicitly high impedance and are wired
    # across nodes; a common return is not silently used for capacitor voltage.
    for pts in [[(220,350),(105,350),(105,460)],[(105,520),(105,665),(220,665)],
                [(848,350),(848,465),(858,465)],[(918,465),(940,465),(940,350)],
                [(1190,445),(1370,445),(1370,485)],[(1370,545),(1370,590),(1190,590)]]:
        b += [l(a,z,TEAL,2) for a,z in zip(pts,pts[1:])]
    for x,y,label in [(105,490,"Vₛ"),(888,465,"Vc"),(1370,515,"Vₗ")]:
        b += [c(x,y,30,PAPER,TEAL,2),t(x,y+7,label,21,TEAL,"bold","middle")]
    b += [t(82,377,"+",20,TEAL,"bold"),t(82,650,"−",20,TEAL,"bold"),
          t(826,445,"+",20,TEAL,"bold"),t(943,445,"−",20,TEAL,"bold"),
          t(1385,472,"+",20,TEAL,"bold"),t(1385,581,"−",20,TEAL,"bold")]
    for x,y in [(220,350),(220,665),(848,350),(940,350),(1190,445),(1190,590)]: b += [node(x,y)]
    b += [t(440,532,"Same i(t) through Rᵢ, L, C and Rₗ",20,INK,"bold"),
          t(440,566,"V probes connect across the labelled node pairs.",18,MUTED),
          t(440,598,"Differential / isolated voltage acquisition assumed.",18,MUTED),
          t(440,629,"No earth connection is shown or required by this model.",17,MUTED)]
    b += [r(55,730,1390,113,"#fffdf8",LINE,10),
          t(80,764,"SYNCHRONIZED WAVEFORM RECORDER · KNOWN BANDWIDTH REQUIRED",16,TEAL,"bold"),
          t(80,796,"Log vₛ(t), i(t), Vc(t), vₗ(t) and initial / final state; check polarity, timing, loading and sensor loss.",20,INK),
          t(80,825,"Symbols mark probe locations, not slow-meter readings. Real probe burden, bandwidth and wiring losses need a separate budget.",17,MUTED)]
    b += [r(55,869,1390,164,"#e4ece1",LINE,10),
          t(80,908,"ENERGY ACCOUNTING",16,TEAL,"bold"),
          t(80,947,"∫ vₛ i dt = ∫ Rₗ i² dt + ∫ Rᵢ i² dt + Δ(½ L i² + ½ C Vc²)",26,INK,"bold"),
          t(80,984,"Source work = load heat + internal loss + change in stored magnetic and electric energy.",16,MUTED),
          t(80,1014,"At vₛ = 0 with the series loop still closed, a charged capacitor can deliver its initial stored energy to the load.",18,MUTED)]
    b += [t(55,1070,"Model drive: 1 V peak, ω = 1000 rad/s (159.155 Hz); 10 driven cycles, then 5 with vₛ = 0 and loop closed. No physical measurements.",17,MUTED)]
    save_svg("electrical-energy-boundary.svg","Series RLC energy boundary and voltage/current observation points",
             "An isolated low-voltage source drives a series current sensor, 1 ohm internal resistor, 10 millihenry inductor, 100 microfarad capacitor and 4 ohm load. Voltage probes measure source, capacitor and load with explicit polarities. Values belong to a synthetic contract. Source work equals load heat plus resistor loss plus electric and magnetic storage change. No physical measurements.",b)


def magnetic_plan():
    # Side elevation: equal 1200 px/m scale for both x and z.
    scale=1200; ox=75; oz=770
    pt=lambda x,z:(ox+x*scale,oz-z*scale)
    box=lambda x,z,dx,dz,fill:r(*pt(x,z+dz),dx*scale,dz*scale,fill,LINE,2)
    b=[t(55,50,"MAGNETISM / PROPOSED CONTACT-FORCE CONTROL",16,TEAL,"bold"),
       t(55,99,"A changed scale reading is not changed gravity",37,INK,"bold"),
       t(55,136,"The steel test piece stays on the pan. Magnet and its support are mechanically outside the balance.",19,MUTED),l((55,165),(1445,165),LINE)]
    b += [t(75,218,"SIDE ELEVATION · x–z PLANE",17,TEAL,"bold"),
          r(75,253,950,93,"#fffdf8",LINE,8),t(95,288,"The magnet's opposite reaction is carried by the external stand.",19,INK,"bold"),
          t(95,319,"Ordinary-force illustration only: this is not a quantitative solenoid L(x) model or an antigravity rig.",16,MUTED),
          box(.17,0,.41,.015,"#d2ddce"),box(.24,.015,.24,.045,"#b3cbbb"),box(.325,.060,.07,.005,"#889f90"),box(.27,.065,.18,.005,"#d9e1d6"),
          box(.345,.070,.03,.008,"#9da9a6"),box(.345,.158,.03,.006,GOLD),
          box(.645,0,.13,.015,"#d0c7af"),box(.695,.015,.022,.26,"#c8c7b4"),
          box(.35,.255,.367,.016,"#c8c7b4"),box(.356,.164,.008,.091,"#c8c7b4")]
    b += [t(*pt(.245,.027),"BALANCE",16,INK,"bold"),t(*pt(.275,.094),"steel test piece",17,INK,"bold"),
          t(*pt(.39,.163),"small permanent magnet",17,GOLD,"bold"),arrow(536,523,536,599,GOLD,2),t(550,520,"−Fₘ on magnet",17,GOLD,"bold"),
          t(*pt(.55,.29),"nonmagnetic stand",17,INK,"bold"),
          t(*pt(.58,.312),"feet off the balance",16,MUTED),
          geo.dimension(pt(.31,.078),pt(.31,.158),"8 cm gap",(-52,4)),
          t(78,820,"Nominal geometry only: pan top z = 7 cm; test top z = 7.8 cm; magnet bottom z = 15.8 cm.",17,MUTED)]
    # Explicitly schematic isolated-body force diagram, separate from geometry.
    b += [l((1075,212),(1075,807),LINE),t(1120,238,"FORCES ON TEST PIECE",16,TEAL,"bold"),
          c(1225,475,28,"#abb7ac",INK),arrow(1194,458,1194,345,TEAL),t(1176,328,"N",21,TEAL,"bold"),
          arrow(1257,458,1257,290,GOLD),t(1290,305,"Fₘ",21,GOLD,"bold"),
          arrow(1225,504,1225,640),t(1247,627,"mg",21,INK,"bold"),
          t(1115,692,"Static contact model",19,INK,"bold"),t(1115,731,"N = mg − Fₘ",27,INK,"bold"),
          t(1115,769,"Only while N ≥ 0.",17,MUTED),t(1115,798,"Arrows are not to scale.",16,MUTED)]
    b += [r(55,870,1390,180,"#e4ece1",LINE,10),t(80,907,"WHAT MUST BE CONTROLLED",16,TEAL,"bold"),
          t(80,946,"Record baseline → fixed magnet gap → baseline; preserve all readings and the external magnet support.",19,INK),
          t(80,980,"Field response of the balance itself, drift, table coupling and magnet forces on nearby parts can imitate a mass change.",18,MUTED),
          t(80,1013,"A lighter contact-force reading does not by itself distinguish magnetic force from gravity change. No lift or antigravity is demonstrated.",18,MUTED)]
    save_svg("magnetic-force-plan.svg","Magnet above a contacting test piece on an independently supported balance",
             "Proposed side elevation: a small magnet on an off-balance stand sits 8 centimetres above a steel test piece that remains on the balance pan. An independent force diagram shows upward support N, upward magnetic force F m and downward weight mg. N equals mg minus F m in static contact. No physical measurements or antigravity.",b)


def cylinder(ax,centre,radius,z0,z1,color):
    theta=np.linspace(0,2*np.pi,65)
    theta_grid,height=np.meshgrid(theta,[z0,z1])
    geo.surface(centre[0]+radius*np.cos(theta_grid),centre[1]+radius*np.sin(theta_grid),height,color)
    rad,th=np.meshgrid(np.linspace(0,radius,8),theta)
    geo.surface(centre[0]+rad*np.cos(th),centre[1]+rad*np.sin(th),np.full_like(rad,z1),color)


def magnetic_3d():
    geo.SCENE_FACES.clear(); geo.SCENE_COLORS.clear()
    fig=plt.figure(figsize=(15,10),facecolor=PAPER)
    ax=fig.add_axes([.005,.15,.735,.71],projection="3d",facecolor=PAPER)
    points=np.array([[0,0,0],[1,0,0],[1,.65,0],[0,.65,0],[0,0,0]])
    ax.plot(points[:,0],points[:,1],points[:,2],color=LINE,lw=2)
    # Scale body rests on its own levelling support. External magnet support is
    # on the same table, so vibration coupling is explicitly not removed.
    geo.cuboid(ax,(.17,.16,0),(.41,.28,.015),"#d2ddce")
    geo.cuboid(ax,(.24,.19,.015),(.24,.22,.045),"#b3cbbb")
    geo.cuboid(ax,(.27,.22,.065),(.18,.16,.005),"#d9e1d6")
    geo.cuboid(ax,(.325,.29,.06),(.07,.02,.005),"#889f90")
    cylinder(ax,TEST,.015,.070,.078,"#9da9a6")
    cylinder(ax,MAGNET,.015,.158,.164,GOLD)
    geo.cuboid(ax,(.645,.225,0),(.13,.15,.015),"#d0c7af")
    geo.cuboid(ax,(.695,.289,.015),(.022,.022,.26),"#c8c7b4")
    geo.cuboid(ax,(.35,.289,.255),(.367,.022,.016),"#c8c7b4")
    geo.cuboid(ax,(.356,.296,.164),(.008,.008,.091),"#c8c7b4")
    # Ruler is beside the gap, not an extra load on the pan.
    geo.cuboid(ax,(.60,.35,0),(.015,.008,.23),"#d9b982")
    for z in np.arange(.01,.231,.01):
        ax.plot([.598,.616],[.348,.348],[z,z],c=MUTED,lw=.8)
    # A manually maintained logbook has no implied electronic sensor path.
    geo.cuboid(ax,(.79,.42,0),(.16,.15,.005),"#fffaf0")
    for y in np.arange(.445,.56,.02):
        ax.plot([.80,.94],[y,y],[.006,.006],color=LINE,lw=1)
    ax.add_collection3d(Poly3DCollection(geo.SCENE_FACES,facecolors=geo.SCENE_COLORS,edgecolors="none",linewidths=0,zsort="average"))
    ax.plot([.33,.33],[.30,.30],[TEST_TOP,MAGNET_BOTTOM],c=TEAL,lw=2,ls="--")
    labels=[((.31,.15,.09),"1"),((.35,.28,.10),"2"),((.33,.29,.19),"3"),((.69,.31,.30),"4"),((.84,.46,.025),"5")]
    for p,n in labels:
        ax.text(*p,n,color=PAPER,ha="center",va="center",fontsize=12,zorder=999,bbox=dict(boxstyle="circle,pad=.3",fc=INK,ec=PAPER,lw=1))
    ax.set(xlim=(0,1),ylim=(0,.65),zlim=(0,.36),xlabel="x / m",ylabel="y / m",zlabel="z / m")
    ax.set_box_aspect((1,.65,.36)); ax.view_init(elev=30,azim=-62)
    ax.set_xticks(np.arange(0,1.01,.2)); ax.set_yticks([0,.2,.4,.6]); ax.set_zticks([0,.1,.2,.3])
    for axis in (ax.xaxis,ax.yaxis,ax.zaxis):
        axis.pane.set_alpha(0); axis._axinfo["grid"]["color"]="#d8ded2"
    fig.text(.055,.946,"MAGNETIC FORCE CONTROL / DETERMINISTIC 3D GEOMETRY",fontsize=12,weight="bold",color=TEAL)
    fig.text(.055,.897,"Contact force, magnetic force and weight",fontsize=27,weight="bold",color=INK)
    fig.text(.055,.860,"Proposed and unbuilt. No physical measurements. All axes are metres (m).",fontsize=13,color=MUTED)
    legend=[("1","Balance + levelling support","No numerical reading is depicted."),("2","Steel test piece on the pan","Contact remains; no levitation."),
            ("3","Fixed small magnet","8 cm nominal air gap, not optimized."),("4","Independent magnet stand","Carries opposite reaction off-scale."),("5","Manual acquisition log","All readings, positions and controls.")]
    y=.73
    for n,a,b in legend:
        fig.text(.745,y,n,color=PAPER,fontsize=10,bbox=dict(boxstyle="circle,pad=.3",fc=INK,ec=INK))
        fig.text(.775,y,a,fontsize=12,weight="bold",color=INK)
        fig.text(.775,y-.027,b,fontsize=10.5,color=MUTED)
        y-=.086
    fig.text(.055,.118,"In static contact, the ideal pan force is N = mg − Fₘ.",fontsize=15,weight="bold",color=INK)
    fig.text(.055,.079,"A change in apparent weight can come from ordinary magnetic force or instrument bias.",fontsize=13,color=MUTED)
    fig.text(.055,.046,"Ordinary-force illustration, not a solenoid model or validated antigravity apparatus. Balance-field interference needs controls.",fontsize=11.5,color=MUTED)
    fig.savefig(OUT/"magnetic-force-3d.png",dpi=160,facecolor=PAPER); plt.close(fig)


def magnetic_work():
    b=[t(55,50,"MAGNETISM / R4 IDEAL ELECTROMECHANICAL MODEL",16,TEAL,"bold"),
       t(55,99,"Current, stored field energy and mechanical work",35,INK,"bold"),
       t(55,136,"Hypothetical L(z) law with externally imposed motion; not a measured coil, free dynamics or the permanent-magnet bench.",18,MUTED),l((55,165),(1445,165),LINE)]
    # The current regulator supplies whatever port voltage this stipulated
    # motion and ideal constitutive law require; no energy source is omitted.
    b += [t(80,215,"CLOSED ELECTRICAL PATH",16,TEAL,"bold"),c(190,465,54,PAPER,INK,3),arrow(190,495,190,436),
          l((190,411),(190,300),INK,3),l((190,300),(320,300),INK,3),
          l((190,519),(190,650),INK,3),l((190,650),(620,650),INK,3),
          t(75,556,"Maintained I = 0.2 A",20,INK,"bold"),t(75,587,"source must supply v(t) I",17,MUTED)]
    b += resistor(320,300,450,300,"R = 5 Ω")
    b += [l((450,300),(620,300),INK,3),l((620,300),(620,365),INK,3)]
    coil='M620,365 '
    for k in range(4):
        y=365+34*k; coil+=f'C590,{y} 590,{y+34} 620,{y+34} '
    b += [f'<path d="{coil}" fill="none" stroke="{INK}" stroke-width="3"/>',l((620,501),(620,650),INK,3),
          t(646,365,"L(z) = 0.01 + 0.1z H",21,INK,"bold"),t(646,397,"z in m; 0 ≤ z ≤ 0.02 m",17,MUTED),
          t(646,446,"F = ½ I² dL/dz = 2 mN",20,TEAL,"bold"),
          t(646,480,"v(t) = RI + I (dL/dz) ż",20,INK,"bold"),
          arrow(651,568,836,568,TEAL),t(717,600,"mechanical work",16,TEAL,"normal","middle"),
          r(865,495,570,185,"#e9eee2",LINE,10),t(890,528,"PRESCRIBED MOTION",16,TEAL,"bold"),
          t(890,559,"z(t) = 0.01 [1 − cos(πt / 0.2)] m",21,INK,"bold"),
          t(890,590,"0 ≤ t ≤ 0.2 s; starts and ends at rest.",18,MUTED),
          t(890,622,"External constraint selects this trajectory.",18,MUTED),
          t(890,653,"No claim that the model freely lifts a mass.",18,MUTED)]
    b += [r(55,695,1390,195,"#e4ece1",LINE,10),t(80,734,"COMPLETE PORT ENERGY IDENTITY AT MAINTAINED CURRENT",16,TEAL,"bold"),
          t(80,779,"vI = RI² + d(½ L I²)/dt + F ż",29,INK,"bold"),
          t(80,821,"source power = resistive heat + stored-field rate + mechanical output",20,MUTED),
          t(80,858,"For Δz = 2 cm: magnetic storage increases by 40 µJ and mechanical work is 40 µJ; both come from the source.",18,INK)]
    b += [r(55,916,1390,114,"#fffdf8",LINE,10),t(80,952,"SEPARATE STATIC CONTACT COMPARISON · STATOR REACTION SUPPORTED OFF BALANCE",16,TEAL,"bold"),
          t(80,990,"At fixed g = 9.80665 m/s², a 1 g mass and upward 2 mN force give N = 7.80665 mN while contact holds.",20,INK)]
    b += [t(55,1070,"Analytic model schematic only. Coil law, current control, trajectory and force are stipulated; no device or gravity change was measured.",17,MUTED)]
    save_svg("magnetic-work-boundary.svg","Maintained-current variable-inductance source, storage and work identity",
             "Closed ideal circuit with maintained 0.2 ampere current, 5 ohm resistance and hypothetical inductance 0.01 plus 0.1z henries. An externally prescribed half-cosine motion moves z from zero to two centimetres over 0.2 seconds. Source work supplies resistor heat, stored magnetic energy increase and mechanical output. The source supplies forty microjoules to storage and forty microjoules to mechanical work. No measured coil or free levitation model.",b)


def main():
    assert np.isclose(MAGNET_BOTTOM-TEST_TOP,.08)
    electrical(); magnetic_plan(); magnetic_3d(); magnetic_work()
    data={"schemaVersion":1,"status":"proposed/unbuilt; no physical measurements","coordinateUnit":"m","displayDimensionUnit":"cm in magnetic SVG; m in 3D axes",
          "generator":"scripts/render_electromagnetic_v4.py","soundGeometryDependency":"scripts/render_apparatus_v4.py",
          "electrical":{"topology":"isolated source -> series current sensor -> Rinternal -> L -> C -> Rload -> source return",
              "contractPath":"docs/panel-v4/contracts/R3.json","parameterOrigin":"frozen electrical R3 simulation, not a hardware kit",
              "Rinternal_ohm":1,"L_H":.01,"C_F":.0001,"Rload_ohm":4,"sourcePeak_V":1,"sourceAngularFrequency_rad_s":1000,
              "sourceOffMeaning":"zero ideal source voltage while the series circuit remains closed, not an open switch",
              "voltageObservations":["source positive node minus return","capacitor incoming-current node minus outgoing node","load incoming-current node minus return"],
              "currentSign":"leaves source positive terminal; enters positive terminal of each passive element",
              "idealBudget":"integral(vs*i dt) = integral(Rload*i^2 dt) + integral(Rinternal*i^2 dt) + delta(0.5*L*i^2 + 0.5*C*Vc^2)",
              "instrumentAssumption":"high-impedance differential voltage probes and same synchronized series current; real instrument losses/loading excluded from fixture"},
          "variableInductanceModel":{"contractPath":"docs/panel-v4/contracts/R4.json","status":"analytic schematic of stipulated model; not the permanent-magnet apparatus",
              "L_H":"0.01 + 0.1*z_m","I_A":.2,"R_ohm":5,"zSpan_m":[0,.02],"duration_s":.2,"prescribedTrajectory_m":"0.01*(1-cos(pi*t/0.2))",
              "force_N":.002,"storageChange_J":.00004,"mechanicalWork_J":.00004,"forceAndWorkMeasured":False},
          "magnetic":{"frame":"tabletop z=0; 1m x .65m plan","testCenter_m":TEST.tolist(),"magnetCenter_m":MAGNET.tolist(),
              "testTop_m":TEST_TOP,"magnetBottom_m":MAGNET_BOTTOM,"magnetTop_m":MAGNET_TOP,"airGap_m":.08,"testRadius_m":.015,"magnetRadius_m":.015,
              "balanceFootprint_m":{"origin":[.24,.19,.015],"size":[.24,.22,.045]},"panTop_m":.070,
              "externalSupportFootprint_m":{"origin":[.645,.225,0],"size":[.13,.15,.015]},"standHeight_m":.275,
              "observable":"change in apparent support force, not direct gravity measurement","contactModel":"N = mg - Fmag provided N >= 0",
              "externalReaction":"magnet experiences opposite magnetic force; off-balance stand carries that reaction to the tabletop",
              "limitations":["balance instrument may respond directly to field","common table transmits vibration","all hardware geometry is unoptimized","no quantitative mapping to a solenoid L(x) model","no magnetic field or force simulation implied by drawing","no lift or antigravity demonstrated"]}}
    (OUT/"electromagnetic-coordinates.json").write_text(json.dumps(data,indent=2)+"\n")
    names=["electrical-energy-boundary.svg","magnetic-force-plan.svg","magnetic-force-3d.png","magnetic-work-boundary.svg","electromagnetic-coordinates.json"]
    manifest={"generatorSha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"dependencySha256":hashlib.sha256((ROOT/"scripts/render_apparatus_v4.py").read_bytes()).hexdigest(),
              "filesSha256":{name:hashlib.sha256((OUT/name).read_bytes()).hexdigest() for name in names}}
    (OUT/"electromagnetic-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print("Rendered exact RLC topology, magnetic force plan and deterministic 3D geometry; gap and SVG XML verified.")


if __name__=="__main__": main()
