#!/usr/bin/env python3
"""Reproduce Round 1. Model and thresholds are frozen in contract.md.

Run: python research/round1/solver.py
Dependencies: Python >=3.10, numpy, matplotlib. No network access or random seed.
All dynamical calculations use SI units. This is not a biological/device model.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Parameters:
    mass_kg: float = 1.0
    ground_stiffness_N_per_m: float = (2.0 * math.pi * 2.0) ** 2
    coupling_stiffness_N_per_m: float = 40.0
    damping_kg_per_s: float = 0.4
    force_N: float = 0.1
    drive_Hz: float = 2.0

    def validate(self):
        values = list(asdict(self).values())
        if not all(math.isfinite(x) for x in values):
            raise ValueError("Parameters must be finite")
        if self.mass_kg <= 0 or self.ground_stiffness_N_per_m <= 0:
            raise ValueError("Mass and ground stiffness must be positive")
        if self.coupling_stiffness_N_per_m < 0 or self.damping_kg_per_s < 0:
            raise ValueError("This passive spring family requires kc,c >= 0")
        if self.drive_Hz < 0:
            raise ValueError("Drive frequency must be nonnegative")


def derivative(t, y, p):
    q1, q2, v1, v2, _, _ = y
    force = p.force_N * math.sin(2 * math.pi * p.drive_Hz * t)
    coupling = p.coupling_stiffness_N_per_m * (q1 - q2)
    a1 = (force - p.damping_kg_per_s*v1
          - p.ground_stiffness_N_per_m*q1 - coupling) / p.mass_kg
    a2 = (-p.damping_kg_per_s*v2
          - p.ground_stiffness_N_per_m*q2 + coupling) / p.mass_kg
    return (v1, v2, a1, a2, force*v1,
            p.damping_kg_per_s*(v1*v1 + v2*v2))


def rk4_step(t, y, h, p):
    a = derivative(t, y, p)
    b = derivative(t+h/2, tuple(yj+h*aj/2 for yj, aj in zip(y, a)), p)
    c = derivative(t+h/2, tuple(yj+h*bj/2 for yj, bj in zip(y, b)), p)
    d = derivative(t+h, tuple(yj+h*cj for yj, cj in zip(y, c)), p)
    return tuple(yj+h*(aj+2*bj+2*cj+dj)/6
                 for yj, aj, bj, cj, dj in zip(y, a, b, c, d))


def simulate(p=Parameters(), duration_s=20.0, dt_s=0.002,
             initial=(0.0, 0.0, 0.0, 0.0)):
    p.validate()
    if not math.isfinite(dt_s) or dt_s <= 0 or duration_s <= 0:
        raise ValueError("Duration and timestep must be positive and finite")
    steps = round(duration_s/dt_s)
    if not math.isclose(steps*dt_s, duration_s, rel_tol=0, abs_tol=1e-10):
        raise ValueError("Duration must be an integer number of timesteps")
    if len(initial) != 4 or not all(math.isfinite(v) for v in initial):
        raise ValueError("Initial state requires four finite SI coordinates")
    state = tuple(float(x) for x in initial)+(0.0, 0.0)
    states = np.empty((steps+1, 6))
    states[0] = state
    for n in range(steps):
        state = rk4_step(n*dt_s, state, dt_s, p)
        states[n+1] = state
    times = np.arange(steps+1)*dt_s
    q1, q2, v1, v2, work, loss = states.T
    energy = (0.5*p.mass_kg*(v1*v1+v2*v2)
              + 0.5*p.ground_stiffness_N_per_m*(q1*q1+q2*q2)
              + 0.5*p.coupling_stiffness_N_per_m*(q1-q2)**2)
    force = p.force_N*np.sin(2*np.pi*p.drive_Hz*times)
    pin = force*v1
    ploss = p.damping_kg_per_s*(v1*v1+v2*v2)
    residual = energy-energy[0]-work+loss
    return dict(t_s=times, states=states, energy_J=energy, input_force_N=force,
                input_power_W=pin, loss_power_W=ploss, residual_J=residual)


def summarize(trace):
    states = trace["states"]
    energy = trace["energy_J"]
    work, loss = states[-1, 4:6]
    scale = max(abs(work), energy[0], energy[-1], loss, 1e-12)
    return {
        "initial_energy_J": float(energy[0]),
        "final_energy_J": float(energy[-1]),
        "input_work_J": float(work),
        "dissipated_energy_J": float(loss),
        "endpoint_residual_J": float(trace["residual_J"][-1]),
        "max_abs_residual_J": float(np.max(abs(trace["residual_J"]))),
        "endpoint_residual_scale_J": float(scale),
        "relative_endpoint_residual": float(abs(trace["residual_J"][-1])/scale),
        "endpoint_state_SI": [float(x) for x in states[-1, :4]],
    }


def steady_response(p, frequency_Hz):
    """Independent 2x2 complex formulation, q=Re(Q) sin(wt)+Im(Q) cos(wt)."""
    p.validate()
    omega = 2*np.pi*frequency_Hz
    m = p.mass_kg*np.eye(2)
    k = np.array([[p.ground_stiffness_N_per_m+p.coupling_stiffness_N_per_m,
                   -p.coupling_stiffness_N_per_m],
                  [-p.coupling_stiffness_N_per_m,
                   p.ground_stiffness_N_per_m+p.coupling_stiffness_N_per_m]])
    r = p.damping_kg_per_s*np.eye(2)
    q = np.linalg.solve(k-omega**2*m+1j*omega*r, np.array([p.force_N, 0.0]))
    velocity = 1j*omega*q
    mean_pin = 0.5*float(np.real(p.force_N*np.conjugate(velocity[0])))
    mean_loss = 0.5*float(np.real(np.vdot(velocity, r@velocity)))
    return q, mean_pin, mean_loss


def conservative_exact(t, p):
    """Analytic solution for q(0)=(0.01,0), v(0)=0 only."""
    low = math.sqrt(p.ground_stiffness_N_per_m/p.mass_kg)
    high = math.sqrt((p.ground_stiffness_N_per_m
                      + 2*p.coupling_stiffness_N_per_m)/p.mass_kg)
    return np.column_stack((0.005*(np.cos(low*t)+np.cos(high*t)),
                            0.005*(np.cos(low*t)-np.cos(high*t))))


def save_trace(filename, trace, stride=1):
    names = ["time_s", "q1_m", "q2_m", "v1_m_per_s", "v2_m_per_s",
             "input_work_J", "dissipated_energy_J", "stored_energy_J",
             "input_force_N", "input_power_W", "loss_power_W", "residual_J"]
    data = np.column_stack((trace["t_s"], trace["states"], trace["energy_J"],
                            trace["input_force_N"], trace["input_power_W"],
                            trace["loss_power_W"], trace["residual_J"]))
    np.savetxt(ROOT/filename, data[::stride], delimiter=",", header=",".join(names),
               comments="", fmt="%.17g")


def add_check(checks, name, passed, observed, criterion):
    checks.append(dict(name=name, passed=bool(passed), observed=observed,
                       criterion=criterion))


def run_round():
    checks = []
    base = Parameters()
    baseline = simulate(base)
    stats = {"baseline": summarize(baseline)}
    add_check(checks, "baseline_energy_budget", stats["baseline"]["max_abs_residual_J"] < 1e-6,
              stats["baseline"]["max_abs_residual_J"], "max absolute residual < 1e-6 J")
    save_trace("baseline.csv", baseline)

    lossless_p = replace(base, damping_kg_per_s=0, force_N=0)
    lossless = simulate(lossless_p, initial=(0.01, 0, 0, 0))
    exact = conservative_exact(lossless["t_s"], lossless_p)
    analytic_error = float(np.max(abs(exact-lossless["states"][:, :2])))
    drift = float(np.max(abs(lossless["energy_J"]-lossless["energy_J"][0]))
                  / lossless["energy_J"][0])
    stats["undriven_lossless"] = summarize(lossless)
    stats["undriven_lossless"].update(relative_energy_drift=drift,
                                     max_analytic_displacement_error_m=analytic_error)
    add_check(checks, "undriven_conservation", drift < 1e-5, drift, "relative drift < 1e-5")
    add_check(checks, "analytic_normal_modes", analytic_error < 1e-7, analytic_error,
              "maximum displacement error < 1e-7 m")
    save_trace("undriven_lossless.csv", lossless, stride=10)

    damped = simulate(replace(base, force_N=0), initial=(0.01, 0, 0, 0))
    max_rise = float(np.max(np.diff(damped["energy_J"])))
    stats["undriven_damped"] = summarize(damped)
    stats["undriven_damped"]["maximum_step_energy_increase_J"] = max_rise
    add_check(checks, "passive_decay", max_rise <= 1e-12 and damped["energy_J"][-1] < damped["energy_J"][0],
              max_rise, "maximum step increase <= 1e-12 J and final energy below initial")
    save_trace("undriven_damped.csv", damped, stride=10)

    uncoupled = simulate(replace(base, coupling_stiffness_N_per_m=0))
    receiver_max = float(np.max(abs(uncoupled["states"][:, [1, 3]])))
    stats["zero_coupling"] = summarize(uncoupled)
    add_check(checks, "zero_coupling_receiver", receiver_max < 1e-14, receiver_max,
              "receiver displacement and velocity < 1e-14 in SI units")
    save_trace("zero_coupling.csv", uncoupled, stride=10)

    zero = simulate(replace(base, force_N=0))
    zero_max = float(np.max(abs(zero["states"])))
    stats["zero_input_rest"] = summarize(zero)
    add_check(checks, "zero_input_rest", zero_max == 0, zero_max, "all augmented states exactly zero")

    off = simulate(replace(base, drive_Hz=3.5))
    baseline_rms = float(np.sqrt(np.mean(baseline["states"][baseline["t_s"] >= 15, 0]**2)))
    off_rms = float(np.sqrt(np.mean(off["states"][off["t_s"] >= 15, 0]**2)))
    stats["off_resonance"] = summarize(off)
    stats["off_resonance"].update(final_5s_rms_q1_m=off_rms, baseline_final_5s_rms_q1_m=baseline_rms)
    add_check(checks, "off_resonance_control", off_rms < baseline_rms,
              {"off_rms_m": off_rms, "baseline_rms_m": baseline_rms}, "off resonance RMS < baseline RMS")
    save_trace("off_resonance.csv", off, stride=10)

    convergence_traces = [simulate(base, dt_s=h) for h in (0.004, 0.002, 0.001, 0.0005)]
    reference = convergence_traces[-1]["states"][-1, :4]
    convergence = []
    for h, trace in zip((0.004, 0.002, 0.001, 0.0005), convergence_traces):
        error = trace["states"][-1, :4]-reference
        convergence.append(dict(dt_s=h, max_abs_budget_residual_J=summarize(trace)["max_abs_residual_J"],
                                endpoint_q_error_m=float(np.linalg.norm(error[:2])),
                                endpoint_v_error_m_per_s=float(np.linalg.norm(error[2:]))))
    residuals = [v["max_abs_budget_residual_J"] for v in convergence]
    q_errors = [v["endpoint_q_error_m"] for v in convergence]
    v_errors = [v["endpoint_v_error_m_per_s"] for v in convergence]
    add_check(checks, "timestep_budget_convergence", all(a>b for a,b in zip(residuals, residuals[1:])),
              residuals, "strictly decreasing max closure residual with timestep refinement")
    add_check(checks, "timestep_state_convergence",
              all(a>b for a,b in zip(q_errors, q_errors[1:])) and all(a>b for a,b in zip(v_errors, v_errors[1:])),
              {"q_errors_m": q_errors, "v_errors_m_per_s": v_errors}, "strictly decreasing endpoint errors against finest run")
    with (ROOT/"convergence.csv").open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(convergence[0]))
        writer.writeheader(); writer.writerows(convergence)

    initial = np.array([0.01, -0.004, 0.03, -0.02])
    forward = simulate(lossless_p, duration_s=5, initial=initial)
    turning = forward["states"][-1, :4].copy(); turning[2:] *= -1
    backward = simulate(lossless_p, duration_s=5, initial=turning)
    target = initial.copy(); target[2:] *= -1
    reversal_error = abs(backward["states"][-1, :4]-target)
    stats["lossless_reversal"] = {"q_error_m": float(np.max(reversal_error[:2])),
                                  "v_error_m_per_s": float(np.max(reversal_error[2:]))}
    add_check(checks, "lossless_time_reversal", np.max(reversal_error) < 1e-7,
              stats["lossless_reversal"], "max q and v errors < 1e-7 in respective SI units")

    sign_positive = simulate(base, initial=initial)
    sign_negative = simulate(replace(base, force_N=-base.force_N), initial=-initial)
    parity_state = float(np.max(abs(sign_positive["states"][:, :4]+sign_negative["states"][:, :4])))
    parity_integrals = float(np.max(abs(sign_positive["states"][:, 4:]-sign_negative["states"][:, 4:])))
    parity_energy = float(np.max(abs(sign_positive["energy_J"]-sign_negative["energy_J"])))
    stats["sign_reversal"] = dict(state_error_SI=parity_state, work_loss_error_J=parity_integrals, energy_error_J=parity_energy)
    add_check(checks, "linear_sign_symmetry", max(parity_state, parity_integrals, parity_energy) < 1e-12,
              stats["sign_reversal"], "state negation and energy/work/loss agreement < 1e-12 in SI units")

    steady_checks = []
    for frequency in (2.0, 3.5):
        p = replace(base, drive_Hz=frequency)
        trace = simulate(p, duration_s=60)
        mask = trace["t_s"] >= 50
        phase = 2*np.pi*frequency*trace["t_s"][mask]
        design = np.column_stack((np.sin(phase), np.cos(phase), np.ones(len(phase))))
        fitted = np.linalg.lstsq(design, trace["states"][mask, :2], rcond=None)[0]
        fit_amplitudes = np.sqrt(fitted[0]**2+fitted[1]**2)
        exact_q, mean_pin, mean_loss = steady_response(p, frequency)
        relative_error = abs(fit_amplitudes-abs(exact_q))/abs(exact_q)
        entry = dict(frequency_Hz=frequency, time_fit_amplitude_m=fit_amplitudes.tolist(),
                     exact_amplitude_m=abs(exact_q).tolist(), relative_amplitude_error=relative_error.tolist(),
                     exact_mean_input_power_W=mean_pin, exact_mean_loss_power_W=mean_loss)
        steady_checks.append(entry)
        add_check(checks, f"steady_state_{frequency:g}_Hz", np.max(relative_error) < 1e-3,
                  entry, "both oscillator relative amplitude errors < 1e-3")

    sweep = []
    for damping in (0.2, 0.4, 0.8, 2.0):
        p = replace(base, damping_kg_per_s=damping)
        for frequency in np.linspace(0.5, 4.0, 701):
            q, pin, loss = steady_response(p, frequency)
            sweep.append([frequency, damping, abs(q[0]), abs(q[1]), pin, loss, pin-loss])
    sweep = np.asarray(sweep)
    np.savetxt(ROOT/"frequency_sweep.csv", sweep, delimiter=",", comments="", fmt="%.17g",
               header="frequency_Hz,damping_kg_per_s,q1_amplitude_m,q2_amplitude_m,mean_input_power_W,mean_loss_power_W,power_residual_W")
    power_residual = float(np.max(abs(sweep[:, 6])))
    add_check(checks, "steady_mean_power_identity", np.isfinite(sweep).all() and np.all(sweep[:, 5] >= 0) and power_residual < 1e-12,
              power_residual, "all values finite; dissipation >= 0; max power residual < 1e-12 W")

    omitted_loss = float(baseline["energy_J"][-1]-baseline["energy_J"][0]-baseline["states"][-1, 4])
    full_residual = abs(float(baseline["residual_J"][-1]))
    wrong = dict(omitted_dissipation_endpoint_residual_J=omitted_loss,
                 correct_endpoint_abs_residual_J=full_residual,
                 wrong_to_correct_abs_ratio=abs(omitted_loss)/max(full_residual, 1e-300))
    add_check(checks, "wrong_model_omitted_dissipation", abs(omitted_loss) > 1e-4 and abs(omitted_loss) > 1000*full_residual,
              wrong, "wrong residual > 1e-4 J and >1000 times correct residual")

    plots(baseline, lossless, exact, damped, convergence, sweep, base)
    output = dict(round=1, status="passed" if all(c["passed"] for c in checks) else "failed",
                  scope="Classical passive mechanical analogy only; no empirical or clinical inference.",
                  contract_sha256=hashlib.sha256((ROOT/"contract.md").read_bytes()).hexdigest(),
                  solver_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  test_source_sha256=hashlib.sha256((ROOT/"test_solver.py").read_bytes()).hexdigest(),
                  runtime={"python":platform.python_version(), "numpy":np.__version__},
                  parameters=asdict(base), duration_s=20, baseline_dt_s=0.002,
                  undamped_modes_Hz=[math.sqrt(base.ground_stiffness_N_per_m/base.mass_kg)/(2*math.pi),
                                     math.sqrt((base.ground_stiffness_N_per_m+2*base.coupling_stiffness_N_per_m)/base.mass_kg)/(2*math.pi)],
                  controls=stats, convergence=convergence, steady_state_checks=steady_checks,
                  sweep={"points_per_damping":701,"damping_kg_per_s":[0.2,0.4,0.8,2.0],
                         "range_Hz":[0.5,4],"max_abs_mean_power_residual_W":power_residual},
                  wrong_model_control=wrong, checks=checks)
    (ROOT/"results.json").write_text(json.dumps(output, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status":output["status"],"checks":len(checks),
                      "baseline":stats["baseline"],"failed":[c["name"] for c in checks if not c["passed"]]}, indent=2))
    if output["status"] != "passed":
        raise SystemExit(1)
    return output


def plots(baseline, lossless, exact, damped, convergence, sweep, p):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator
    matplotlib.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False,
                                "svg.hashsalt":"round1-passive-resonators", "savefig.dpi":180})
    def save(fig, name):
        for extension in ("svg", "png"):
            fig.savefig(ROOT/f"{name}.{extension}", bbox_inches="tight",
                        metadata={"Date":None} if extension == "svg" else {})
        plt.close(fig)
    fig, axes = plt.subplots(2, 1, figsize=(9, 6.5), sharex=True,
                             gridspec_kw={"height_ratios":[3,1]}, layout="constrained")
    t = baseline["t_s"]
    axes[0].plot(t, baseline["states"][:,4],label="Input work W",color="#3659b8")
    axes[0].plot(t, baseline["states"][:,5],label="Dissipated energy D",color="#bc4b37")
    axes[0].plot(t, baseline["energy_J"],label="Stored energy E",color="#16766c")
    axes[0].plot(t, baseline["states"][:,4]-baseline["states"][:,5],label="W − D (E₀ = 0)",
                 color="black",ls="--",lw=.9)
    axes[0].set(ylabel="Energy (J)",title="Driven passive pair: input work accounts for storage and loss")
    axes[0].legend(ncol=2,loc="upper left")
    axes[1].plot(t, baseline["residual_J"]*1e9,color="#6d468c")
    axes[1].set(xlabel="Time (s)",ylabel="Closure error (nJ)")
    for ax in axes: ax.grid(alpha=.2)
    save(fig,"energy_budget")

    fig, ax = plt.subplots(figsize=(9,4.8),layout="constrained")
    for damping in (0.2,0.4,0.8,2.0):
        rows = sweep[sweep[:,1] == damping]
        ax.plot(rows[:,0], rows[:,3]*1000, label=f"c = {damping:g} kg/s")
    frequencies = [math.sqrt(p.ground_stiffness_N_per_m/p.mass_kg)/(2*np.pi),
                   math.sqrt((p.ground_stiffness_N_per_m+2*p.coupling_stiffness_N_per_m)/p.mass_kg)/(2*np.pi)]
    for i,f in enumerate(frequencies):
        ax.axvline(f,color="#666666",lw=.8,ls="--",label="Undamped modes" if i == 0 else None)
    ax.set(xlabel="Driving frequency (Hz)",ylabel="Receiver displacement amplitude (mm)",
           title="Steady sinusoidal response: damping limits resonant amplitude",xlim=(.5,4))
    ax.legend(ncol=2); ax.grid(alpha=.2)
    save(fig,"frequency_response")

    fig, axes = plt.subplots(1,2,figsize=(10,4),layout="constrained")
    h = [v["dt_s"] for v in convergence]
    errors = [v["max_abs_budget_residual_J"] for v in convergence]
    axes[0].loglog(h, errors,"o-",color="#3659b8")
    axes[0].set(xlabel="Timestep (s)",ylabel="Maximum budget residual (J)",title="Energy budget convergence")
    axes[1].loglog(h[:-1],[v["endpoint_q_error_m"] for v in convergence[:-1]],"o-",color="#16766c")
    axes[1].set(xlabel="Timestep (s)",ylabel="Endpoint displacement error (m)",
                title="Against dt = 0.0005 s reference")
    for index, ax in enumerate(axes):
        ax.xaxis.set_major_locator(FixedLocator(h if index == 0 else h[:-1]))
        ax.xaxis.set_major_formatter(FuncFormatter(lambda value, position: f"{value:g}"))
        ax.xaxis.set_minor_locator(NullLocator())
        ax.grid(which="both",alpha=.2)
    save(fig,"convergence")

    fig, axes = plt.subplots(2,1,figsize=(9,6),layout="constrained")
    mask = lossless["t_s"] <= 2
    axes[0].plot(lossless["t_s"][mask],lossless["states"][mask,0]*1000,label="RK4 mass 1",color="#3659b8")
    axes[0].plot(lossless["t_s"][mask],exact[mask,0]*1000,"--",lw=1,color="black",label="Exact normal modes")
    axes[0].set(xlabel="Time (s)",ylabel="Displacement (mm)",title="Undriven control checked against an exact solution")
    axes[0].legend()
    axes[1].plot(lossless["t_s"],lossless["energy_J"]*1000,label="c = 0",color="#3659b8")
    axes[1].plot(damped["t_s"],damped["energy_J"]*1000,label="c = 0.4 kg/s",color="#bc4b37")
    axes[1].set(xlabel="Time (s)",ylabel="Stored energy (mJ)",title="Lossless conservation and damped decay from the same initial state")
    axes[1].legend()
    for ax in axes: ax.grid(alpha=.2)
    save(fig,"controls")


if __name__ == "__main__":
    run_round()
