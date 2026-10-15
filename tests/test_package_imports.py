"""Canonical imports and the deprecated Python compatibility package."""

import subprocess
import sys

import merlin_sim


def test_canonical_class_modules():
    for name in ("Simulator", "CircuitSampler", "SampleResult"):
        assert getattr(merlin_sim, name).__module__ == "merlin_sim._core"


def test_legacy_imports_forward_to_canonical_objects():
    # A fresh process observes the warning regardless of prior import order.
    subprocess.run(
        [sys.executable, "-c", """
import warnings

with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always", DeprecationWarning)
    import merlin
    import merlin._core as legacy_core

import merlin_sim
assert len(caught) == 1, caught
assert caught[0].category is DeprecationWarning
assert "import merlin_sim" in str(caught[0].message)
assert caught[0].filename == "<string>"
assert merlin.__all__ == merlin_sim.__all__
for name in merlin_sim.__all__:
    assert getattr(merlin, name) is getattr(merlin_sim, name)
    assert getattr(legacy_core, name) is getattr(merlin_sim, name)
sim = merlin.Simulator(seed=1)
sim.x(0)
assert sim.measure(0) == 1
result = merlin.CircuitSampler("R 0\\nM 0", seed=1).sample(2)
assert type(result) is merlin_sim.SampleResult
assert result.accepted_shots == 2
"""],
        check=True,
    )
