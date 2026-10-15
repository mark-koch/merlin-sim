"""Deprecated compatibility alias for :mod:`merlin_sim`."""

import warnings as _warnings

_warnings.warn(
    "merlin is deprecated; import merlin_sim instead.",
    DeprecationWarning,
    stacklevel=2,
)

from merlin_sim import (
    CircuitSampler as CircuitSampler,
    MeasurementError as MeasurementError,
    SampleResult as SampleResult,
    Simulator as Simulator,
    __all__ as __all__,
)
