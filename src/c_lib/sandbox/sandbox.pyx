cimport sandbox as clib

cimport numpy as np
import numpy as np
import cython

__author__ = "Deepansh J. Srivastava"
__email__ = "deepansh2012@gmail.com"

# @cython.boundscheck(False)
# @cython.wraparound(False)
# def MRS_plan(int geodesic_polyhedron_frequency,
#         int number_of_sidebands)

cdef class AveragingScheme:
    cdef clib.MRS_averaging_scheme *scheme

    def __init__(self, integration_density, integration_volume='octant', allow_fourth_rank=False):
        """Create the averaging scheme for the simulation.

        Args:
            integration_density: The number of triangles along the edge of the octahedron face.
            integration_volume: An enumeration literal, 'octant', 'hemisphere'.
            allow_fourth_rank: Boolean, If True, pre-calculates tables for computing fourth rank tensors.
        """
        allow_fourth_rank_ = 0
        integration_volume_ = 0
        if allow_fourth_rank:
            allow_fourth_rank_=1
        if integration_volume == 'hemisphere':
            integration_volume_=1
        self.scheme = clib.MRS_create_averaging_scheme(integration_density,
                                        allow_fourth_rank_, integration_volume_)

    @property
    def total_orientations(self):
        return self.scheme.total_orientations


cdef class MRSPlan:
    cdef clib.MRS_plan *plan

    def __init__(self, AveragingScheme averaging_scheme, number_of_sidebands,
                sample_rotation_frequency_in_Hz, rotor_angle_in_rad,
                increment, allow_fourth_rank):
        self.plan = clib.MRS_create_plan(averaging_scheme.scheme,
                        number_of_sidebands, sample_rotation_frequency_in_Hz,
                        rotor_angle_in_rad, increment, allow_fourth_rank)

    @property
    def number_of_sidebands(self):
        return self.plan.number_of_sidebands

    @property
    def sample_rotation_frequency_in_Hz(self):
        return self.plan.sample_rotation_frequency_in_Hz

    @property
    def rotor_angle_in_rad(self):
        return self.plan.rotor_angle_in_rad

    # @property
    # def increment(self):
    #     return self.plan.increment

    # @property
    # def allow_fourth_rank(self):
    #     return self.plan.allow_fourth_rank

    # def evaluate(self, R0, R2, R4):
    #     cdef np.ndarray[double complex] R2_c = np.asarray(R2, dtype=np.complex128)
    #     cdef np.ndarray[double complex] R4_c = np.asarray(R4, dtype=np.complex128)
    #     cdef np.ndarray[double complex] output
    #     clib.MRS_get_amplitudes_from_plan(self.plan, &R2_c[0], &R4_c[0])
    #     clib.MRS_get_frequencies_from_plan(self.plan, R0)
    #     # side_band = np.
    #     output = self.plan.vector
    #     return output[::2].reshape(self.plan.number_of_sidebands,
    #                                 self.plan.averaging_scheme.total_orientations)
