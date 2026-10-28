---
description: >-
  Merlin is a polynomial-time quantum simulator for non-Clifford quantum error
  correction. It simulates magic state distillation, magic state cultivation and
  code switching circuits built from CNOT, T and Pauli gates, in Python and Rust.
---

# Merlin Quantum Simulator

**Merlin** (`merlin-sim`) is a polynomial-time quantum simulator for **non-Clifford quantum error correction**. Unlike Clifford/stabilizer simulators such as stim, Merlin can simulate **magic state** protocols, including magic state distillation, magic state cultivation and code switching, at a cost polynomial in the circuit size rather than exponential in the number of T gates.

Merlin supports circuits that can be decomposed into CNOT, T, Paulis, Z-measurements and certain state-dependent *compatible* X-measurements. It can sample computational basis states and compute expectation values and amplitudes, all in polynomial time in the circuit depth and size. It is based on the paper [Polynomial-time simulation of non-Clifford quantum error correction](https://arxiv.org/abs/2610.06811) by Serban Cercelescu, Mark Koch and Arthur Pesah. The source code is on [GitHub](https://github.com/mark-koch/merlin-sim).


## Installation

Install merlin by running

```console
pip install merlin-sim
```


## Quick start

The `Simulator` class can be used to interactively apply gates and measurements:

```python
from merlin_sim import Simulator

sim = Simulator(seed=1234)
sim.reset_x(0, 1)
sim.t(0)
sim.t_dag(1)
sim.cnot(0, 1)

result = sim.measure(0)
p_true = sim.peek_z_probability(1)
parity = sim.measure_observable("-XX", flip_probability=0.001)
```

Note that merlin only supports certain kinds of X measurements such as flag or gauge measurements.
For unsupported measurements, the simulator will raise a `MeasurementError`:

```python
# Measuring CCZ|+++> in X is not supported
sim = Simulator()
sim.reset_x(0, 1, 2)
sim.ccz(0, 1, 2)
sim.measure_x(0)
```

Output:

```
MeasurementError: X measurement on qubit 0 is incompatible: non-affine zero set
```

The `CircuitSampler` class can be used to sample from circuits in an extended stim-like format:

```python
from merlin_sim import CircuitSampler

sampler = CircuitSampler("""
    RX 0
    T 0
    EXP_VAL X0 Z0
    MX 0
    R 0
    X_ERROR(0.01) 0
    M 0
    DETECTOR rec[-1]
    OBSERVABLE_INCLUDE(0) rec[-1]
""", seed=1234, postselect=[0])

result = sampler.sample(1000)
print(result.measurements)
print(result.exp_vals)
print(result.detectors)
print(result.observables)
```

The full circuit specification is described on the [Circuit Format](circuit-format.md) page.

## Citing

If you use Merlin in your research, please cite the paper:

```bibtex
@article{cercelescu2026polynomial,
  title   = {Polynomial-time simulation of non-Clifford quantum error correction},
  author  = {Cercelescu, Serban and Koch, Mark and Pesah, Arthur},
  journal = {arXiv preprint arXiv:2610.06811},
  year    = {2026},
  url     = {https://arxiv.org/abs/2610.06811}
}
```
