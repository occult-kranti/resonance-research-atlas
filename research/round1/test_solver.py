"""Focused independent identities and bad-input guards; production gates in solver.py."""
import math
import unittest
from dataclasses import replace

import numpy as np

from solver import Parameters, derivative, simulate, steady_response


class PhysicsChecks(unittest.TestCase):
    def test_instantaneous_energy_identity(self):
        p = Parameters()
        # Direct matrix energy gradient independently checks the scalar RHS signs.
        m = np.diag([p.mass_kg,p.mass_kg])
        k = p.ground_stiffness_N_per_m*np.eye(2)+p.coupling_stiffness_N_per_m*np.array([[1,-1],[-1,1]])
        for t in (0.0,0.123,1.37):
            for values in ((.02,-.01,.3,-.2),(-.03,.015,-.1,.4),(0,0,0,0)):
                q,v = np.asarray(values[:2]),np.asarray(values[2:])
                dy = derivative(t,(*values,0.,0.),p)
                energy_derivative = float(v @ m @ np.asarray(dy[2:4])+q @ k @ v)
                self.assertAlmostEqual(energy_derivative,dy[4]-dy[5],places=13)

    def test_passive_parameter_rejection(self):
        for overrides in ({"mass_kg":0},{"ground_stiffness_N_per_m":-1},
                          {"damping_kg_per_s":-.1},{"coupling_stiffness_N_per_m":-1},
                          {"force_N":math.nan}):
            with self.assertRaises(ValueError):
                simulate(replace(Parameters(),**overrides),duration_s=.01,dt_s=.001)

    def test_uncoupled_response_independent_scalar_formula(self):
        p = replace(Parameters(),coupling_stiffness_N_per_m=0)
        for frequency in (0.5,2.0,3.5):
            q,pin,loss = steady_response(p,frequency)
            omega = 2*math.pi*frequency
            scalar = p.force_N/complex(p.ground_stiffness_N_per_m-p.mass_kg*omega**2,
                                      omega*p.damping_kg_per_s)
            self.assertAlmostEqual(abs(q[0]-scalar),0.,places=15)
            self.assertEqual(q[1],0.)
            self.assertAlmostEqual(pin,loss,places=14)

    def test_incompatible_step_rejected(self):
        with self.assertRaises(ValueError):
            simulate(duration_s=1.,dt_s=.3)


if __name__ == "__main__":
    unittest.main()
