# What the sound witnesses can identify

These are elementary model derivations and project-specific implementations. No priority claim is made for slope subtraction, linear inverse analysis, or interval propagation. Named historical methods motivate controls; they do not add unmeasured forces.

## Round 1: distinguish gain from decay under a stated witness

Let time be in seconds, amplitudes be digital full scale, and rates be s⁻¹. After ideal signal separation, let target and reference envelopes be

\[
a_s(t)=A_s e^{(-\alpha+\beta_s)t},\qquad a_r(t)=A_r e^{(-\alpha_r+\beta_r)t}.
\]

Their log slopes obey \(m_s=-\alpha+\beta_s\) and \(m_r=-\alpha_r+\beta_r\). Thus

\[
\widehat\alpha=m_r-m_s=\alpha-\alpha_r+(\beta_r-\beta_s).
\]

A stable independently known input reference means \(\alpha_r=0\); a common scalar receiver gain means \(\beta_r=\beta_s\). Both are needed for this subtraction to identify \(\alpha\). With only target data, the map from \((\alpha,\beta)\) to \(m_s\) has rank one and kernel spanned by \((1,1)\). Under both witness premises, adding \(m_r=\beta\) makes the two-by-two map full rank. Allowing an unknown reference decay restores a kernel spanned by \((1,1,1)\) in \((\alpha,\beta,\alpha_r)\). A fitted exponential and low residual do not establish either witness premise.

The implemented phase-aware carrier fit and the reviewer's independent carrier-maxima log regression inspect generated PCM. Physical timing remains a premise. Stereo channels already separate the signals; a practical mixed microphone response is a different inverse problem.

## Round 2: conditional bounds must include nuisance premises

For fixed times, define \(w_i=(t_i-\bar t)/\sum_j(t_j-\bar t)^2\). The fitted slope difference is \(C=\sum_i w_i[\log a_{r,i}-\log a_{s,i}]\). A supplied additive envelope error bound \(\delta_i\) gives an interval for each positive amplitude. If \(a_i-\delta_i\le0\), its logarithmic lower endpoint is not finite and the frozen-window log estimator must withhold a bounded result.

Where all endpoints are positive, set \(\ell_i=\log(a_i-\delta_i)\) and \(u_i=\log(a_i+\delta_i)\). Because \(C\) is linear in these logarithms, choose \(\ell_i\) for each positive coefficient and \(u_i\) for each negative coefficient to obtain its exact lower box endpoint; reverse those choices for the upper endpoint. This is a deterministic set bound, not a probability confidence statement. An arbitrary correlated or independent error inside the supplied box is covered.

If independently supported bounds give \(|\alpha_r|\le R\) and \(|\beta_r-\beta_s|\le D\), then

\[
\alpha\in[C_{\min}-R-D,\;C_{\max}+R+D].
\]

The box width grows by \(2(R+D)\). If either nuisance bound is unknown, a finite physical-alpha interval is not established. This program does not infer envelope-error or nuisance limits from the same low-residual fit. Unknown systematic error is not replaced by a small numerical tolerance.

## Electrical R3: a larger voltage is not a larger energy output

For charge q in coulombs and current I in amperes,

\[
\dot q=I,\qquad L\dot I=u-(R_i+R_l)I-q/C.
\]

Multiplying the second equation by I gives

\[
uI=\frac{d}{dt}\left(\tfrac12 LI^2+\frac{q^2}{2C}\right)+R_iI^2+R_lI^2.
\]

The complete finite-time boundary is signed source work equal to stored-energy change plus internal heat and load work. During source-off discharge, source work is zero but the stored-energy change is negative; positive load output is then expected without new energy production. At sinusoidal steady state the impedance is \(Z=R_i+R_l+i(\omega L-1/(\omega C))\). Capacitor voltage magnification at resonance is \(1/[\omega C(R_i+R_l)]\), while an ideal capacitor's average real power is zero over a period. Multiplying RMS voltage and current gives apparent volt-amperes, which must not be labeled dissipated watts without the phase factor. These are standard circuit relations, used here to generate deliberately misleading readouts and then repair their boundaries.

## Magnetic R4: source work changes the fixed-current energy derivative

For linear inductance L(z), flux linkage is λ = LI and terminal voltage is \(v=RI+\dot\lambda\). With maintained current, \(vI=RI^2+I^2L'(z)\dot z\), while \(\dot U=\tfrac12 I^2L'(z)\dot z\). The remainder is mechanical power, giving \(F_z=+\tfrac12 I^2L'(z)\). An unqualified \(-\partial U/\partial z\) at fixed current omits the source and has the wrong sign. At fixed flux in the separate ideal lossless control, \(U=\lambda^2/[2L(z)]\), so \(-\partial U/\partial z|_\lambda\) gives the same positive force. The constraints and energy reservoirs must be stated before differentiating.

If z is a relative test/stator coordinate, the internal forces are equal and opposite. A static test support can read \(mg-F\) while the source support reads \(Mg+F\). Their sum is \((m+M)g\); a smaller one-pan reading need not change g.

## Gravity-claim R5: a useful design still has an exact rival

Define baseline-subtracted force observations on two supports. Summing contemporaneous supports cancels modeled internal magnetic force. Averaging opposite-current conditions cancels the stipulated odd lead force. If the remaining even bias B is independent of test mass, four distinct masses identify the slope of \(S(m)=(m+M)\delta g+B\). At one mass the two-parameter map has rank one and kernel \((1,-(m+M))\).

For the selected masses, the OLS slope weights are \((-30,-10,10,30)\) kg⁻¹. A supplied bound ε on each baseline-subtracted support contrast becomes a 2ε bound on each paired, polarity-averaged value. Thus the slope error is at most \(2\epsilon\sum_i|w_i|=160\epsilon\), with units m s⁻². This deterministic bound does not gain an unjustified square-root reduction from repeated measurements.

Allowing mass-scaled bias c changes the observation to \(S=(m+M)(\delta g+c)+B\). The three-parameter map has rank two and kernel \((1,0,-1)\) in \((\delta g,B,c)\). An injected gravity-like signal and the corresponding ordinary instrument-bias rival can therefore produce identical records. An independent bound or distinguishing readout is needed before δg is identified physically.

The R5 implementation retains a reviewer-detected finite-precision endpoint failure and its repair. Its theoretical error halfwidth remains 0.00032 m s⁻²; the API adds a separately recorded outward arithmetic guard of 10⁻¹² m s⁻². Strict inclusion was checked at both saturation endpoints and all 65,536 vertices of the selected error box. The guard is not a universal floating-point enclosure certificate.
