# R4 — magnetic force, source work, and balance boundaries

The finite model assumes L(z)=.01 H+(.1 H/m)z for 0≤z≤.02 m, where positive z is upward and increases inductance. A half-cosine path completes this motion in .2 s with zero endpoint velocities. The path is prescribed by an external motion controller, not predicted by free mechanical dynamics. Maintained current is .2 A through a 5 ohm resistance. No measured coil or claimed achievable geometry supplies this L(z).

Flux linkage is lambda=L(z)I. At fixed current, v=RI+d(lambda)/dt=RI+I L'(z) z_dot. Electrical power is RI²+I²L' z_dot. Field-energy rate is half the motion term, dU/dt=I² L' z_dot/2; the remaining half is mechanical power. Therefore Fz=+I² L'/2 and W_source=Delta U+W_mechanical+W_Joule. The sign equals the fixed-current coenergy derivative. Taking minus the field-energy gradient while silently holding current fixed omits source work and gives the opposite force; that wrong model and its failed budget are retained.

Trapezoidal source and force-power integrals are separately checked against endpoint formulas: Delta U=W_mechanical=I² Delta L/2, W_source=RI²T+I²Delta L. Refinement checks quantify their finite quadrature error. Reversing current changes voltage sign but leaves force and energy unchanged. Reversing the prescribed path keeps force upward while reversing field change and mechanical work. Zero current and zero gradient give zero magnetic force.

The auxiliary lossless fixed-flux case is a different electrical boundary: R=0, lambda=.002 Wb-turn constant, I=lambda/L(z), U=lambda²/(2L). Here Fz=−partial U/partial z at fixed lambda=+lambda²L'/(2L²), W_source=0, and W_mechanical=−Delta U. It is an ideal comparison, not a household persistent-current apparatus.

For a separate static 1 g test mass, N=mg−Fz with g=9.80665 m/s². Contact remains positive. The lower indicated mass N/g and its even-in-current symmetry occur with unchanged g. This readout assumes the magnetic reaction is supported externally; the total apparatus boundary is not yet resolved. The moving electromagnetic subsystem delivers F dz to its mechanical boundary; it does not solve the motion controller, total apparatus mechanics, or gravitational potential changes of a moved test mass.

Run: `python research/sound-lab-v4/R4/run.py`. This is a conditional classical actuator and support-force calculation, not a gravity modification or a physical experiment. Current reversal alone does not remove an ordinary quadratic magnetic force.
