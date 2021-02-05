# -*- coding: utf-8 -*-
"""Base Site class."""
from typing import ClassVar
from typing import Dict
from typing import List

from mrsimulator.utils.parseable import Parseable
from pydantic import validator

from .tensors import AntisymmetricTensor
from .tensors import SymmetricTensor

__author__ = "Deepansh Srivastava"
__email__ = "srivastava.89@osu.edu"


class Coupling(Parseable):
    """
    Base class representing a single-site nuclear spin interaction tensor parameters.
    The single-site nuclear spin interaction tensors include the nuclear shielding
    and the electric quadrupolar tensor.

    .. rubric:: Attribute Documentation

    Attributes
    ----------

    site_index: list of int (required).
        A list of two integers, each corresponding to the index of the coupled sites.
        expressed as an atomic number followed by an isotope symbol, eg.,
        `'13C'`, `'17O'`. The default value is `'1H'`.

        Example
        -------

        >>> coupling = Coupling(site_index=[0, 1])

    isotropic_j: float (optional).
        The value is the isotropic j-coupling between the coupled sites in the unit of
        Hz. The default value is 0.

        Example
        -------

        >>> coupling.isotropic_j = 43.3

    j_symmetric: :ref:`sy_api` or equivalent dict object (optional).
        The value of this attribute represents the irreducible second-rank traceless
        symmetric part of the J-coupling tensor. The default value is None.

        The allowed attributes of the :ref:`sy_api` class for `j_symmetric` are
        ``zeta``, ``eta``, ``alpha``, ``beta``, and ``gamma``, where ``zeta`` is the
        J anisotropy, in Hz, and ``eta`` is the J asymmetry parameter defined using the
        Haeberlen convention. The Euler angles ``alpha``, ``beta``, and ``gamma`` are
        in radians.

        Example
        -------

        >>> coupling.j_symmetric = {'zeta': 10, 'eta': 0.5}
        >>> # or equivalently
        >>> coupling.j_symmetric = SymmetricTensor(zeta=10, eta=0.5)

    j_antisymmetric: :ref:`asy_api` or equivalent dict object (optional).
        The value of this attribute represents the irreducible first-rank antisymmetric
        part of the J tensor. The default value is None.

        The allowed attributes of the :ref:`asy_api` class for `j_antisymmetric` are
        ``zeta``, ``alpha``, and ``beta``, where ``zeta`` is the anisotropy parameter
        of the anti-symmetric first-rank tensor given in Hz. The angles ``alpha`` and
        ``beta`` are in radians.

        Example
        -------

        >>> coupling.j_antisymmetric = {'zeta': 20}
        >>> # or equivalently
        >>> coupling.j_antisymmetric = AntisymmetricTensor(zeta=20)

    dipolar: :ref:`sy_api` or equivalent dict object (optional).
        The value of this attribute represents the irreducible second-rank traceless
        symmetric part of the direct dipolar coupling tensor. The default value is
        None.

        The allowed attributes of the :ref:`sy_api` class for `dipolar` are ``zeta``,
        ``eta``, ``alpha``, ``beta``, and ``gamma``, where ``zeta`` is the dipolar
        coupling constant, in Hz, and ``eta`` is the dipolar asymmetry parameter,
        which is usually zero. The Euler angles ``alpha``, ``beta``, and ``gamma``
        are in radians.

        Example
        -------

        >>> coupling.dipolar = {'zeta': 320}
        >>> # or equivalently
        >>> coupling.dipolar = SymmetricTensor(zeta=320)

    name: str (optional).
        The value is the name or id of the coupling. The default value is None.

        Example
        -------

        >>> coupling.name = '1H-1H'
        >>> coupling.name
        '1H-1H'

    label: str (optional).
        The value is a label for the coupling. The default value is None.

        Example
        -------

        >>> coupling.label = 'Weak coupling'
        >>> coupling.label
        'Weak coupling'

    description: str (optional).
        The value is a description of the coupling. The default value is None.

        Example
        -------

        >>> coupling.description = 'An example coupled sites.'
        >>> coupling.description
        'An example coupled sites.'

    Example
    -------

    The following are a few examples of setting the site object.

    >>> coupling1 = Coupling(
    ...     site_index=[0, 1],
    ...     isotropic_j=20, # in Hz
    ...     j_symmetric={
    ...         "zeta": 10, # in Hz
    ...         "eta": 0.5
    ...     },
    ...     dipolar={"zeta": 5.1e3}, # in Hz
    ... )

    Using SymmetricTensor objects.

    >>> coupling1 = Coupling(
    ...     site_index=[0, 1],
    ...     isotropic_j=20, # in Hz
    ...     j_symmetric=SymmetricTensor(zeta=10, eta=0.5),
    ... )
    """

    name: str = None
    label: str = None
    description: str = None
    site_index: List[int]
    isotropic_j: float = 0
    j_symmetric: SymmetricTensor = None
    j_antisymmetric: AntisymmetricTensor = None
    dipolar: SymmetricTensor = None

    property_unit_types: ClassVar = {"isotropic_j": "frequency"}
    property_default_units: ClassVar = {"isotropic_j": "Hz"}
    property_units: Dict = {"isotropic_j": "Hz"}

    @validator("j_symmetric", "j_antisymmetric", "dipolar")
    def couplings_symmetric_must_not_contain_Cq(cls, v, values):
        if v is None:
            return v
        if "Cq" in v.property_units:
            v.property_units.pop("Cq")
        v.property_units["zeta"] = "Hz"
        return v

    @validator("site_index", always=True)
    def validate_site_index(cls, v, *, values, **kwargs):
        if len(v) != 2:
            raise ValueError("Site index must a list of two integers.")
        if v[0] == v[1]:
            raise ValueError("The two site indexes must be unique integers.")
        return v

    class Config:
        validate_assignment = True

    @classmethod
    def parse_dict_with_units(cls, py_dict):
        """
        Parse the physical quantity from a dictionary representation of the Coupling
        object, where the physical quantity is expressed as a string with a number and
        a unit.

        Args:
            dict py_dict: A required python dict object.

        Returns:
            :ref:`site_api` object.

        Example
        -------

        >>> coupling_dict = {
        ...    "site_index": [1, 2],
        ...    "isotropic_j": "20 Hz",
        ...    "j_symmetric": {"zeta": "10 Hz", "eta":0.5}
        ... }
        >>> coupling1 = Coupling.parse_dict_with_units(coupling_dict)
        """
        prop_mapping = {
            "j_symmetric": SymmetricTensor,
            "j_antisymmetric": AntisymmetricTensor,
            "dipolar": SymmetricTensor,
        }

        for k, v in prop_mapping.items():
            if k in py_dict:
                py_dict[k] = v.parse_dict_with_units(py_dict[k])
                if py_dict[k].property_units["zeta"] == "ppm":
                    raise ValueError(
                        f"Error enforcing units for {k}.zeta: ppm. Use frequency units."
                    )
        return super().parse_dict_with_units(py_dict)