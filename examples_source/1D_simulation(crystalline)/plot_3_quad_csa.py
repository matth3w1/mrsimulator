#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Potassium Sulfate, 33S (I=3/2)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

33S (I=3/2) quadrupolar spectrum simulation.
"""
# %%
# The following example is the :math:`^{33}\text{S}` NMR spectrum simulation of
# potassium sulfate (:math:`\text{K}_2\text{SO}_4`). The quadrupole tensor parameters
# for :math:`^{33}\text{S}` is obtained from Moudrakovski `et. al.` [#f3]_
import matplotlib as mpl
import matplotlib.pyplot as plt
from mrsimulator import Simulator, SpinSystem, Site
from mrsimulator.methods import BlochDecayCentralTransitionSpectrum
import numpy as np

# global plot configuration
mpl.rcParams["figure.figsize"] = [4.5, 3.0]
# sphinx_gallery_thumbnail_number = 1

# %%
# **Step 1:** Create the spin system.
site = Site(
    isotope="17O",
    isotropic_chemical_shift=320,  # in ppm
    shielding_symmetric={"zeta": 376.667, "eta": 0.345},
    quadrupolar={
        "Cq": 8.97e6,  # in Hz
        "eta": 0.15,
        "alpha": 5 * np.pi / 180,
        "beta": np.pi / 2,
        "gamma": 70 * np.pi / 180,
    },
)
spin_system = SpinSystem(sites=[site])

# %%
# **Step 2:** Create a central transition selective Bloch decay spectrum method.
method = BlochDecayCentralTransitionSpectrum(
    channels=["17O"],
    magnetic_flux_density=11.74,  # in T
    rotor_frequency=0,  # in Hz
    spectral_dimensions=[
        {
            "count": 1024,
            "spectral_width": 1e5,  # in Hz
            "reference_offset": 22500,  # in Hz
            "label": r"$^{17}$O resonances",
        }
    ],
)

# %%
# **Step 3:** Create the Simulator object and add method and spin system objects.
sim = Simulator()
sim.spin_systems = [spin_system]  # add the spin system
sim.methods = [method]  # add the method

# Since the spin system have non-zero Euler angles, set the integration_volume to
# hemisphere.
sim.config.integration_volume = "hemisphere"

# %%
# **Step 4:** Simulate the spectrum.
sim.run()

# The plot of the simulation before signal processing.
ax = plt.subplot(projection="csdm")
ax.plot(sim.methods[0].simulation.real, color="black", linewidth=1)
ax.invert_xaxis()
plt.tight_layout()
plt.show()
