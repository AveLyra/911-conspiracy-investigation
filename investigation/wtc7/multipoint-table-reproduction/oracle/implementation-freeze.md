# Independent arithmetic implementation freeze

Frozen 2026-09-19 after synthetic tests and before historical calculations or
reading the producer's implementation/results. This agent independently coded
exact `Fraction` Gauss-Jordan normal equations from the shared protocol; it used
the separately source-reviewed transcription as its only historical numeric
input. No producer calculation code was read or imported.

- `exact_oracle.py`: SHA-256 `e4e76ab42ba94e0c6a47a8e09f1c6130bb8d26882738af74e72b49cb1c78cec2`
- `test_exact_oracle.py`: SHA-256 `901b7331a07becfc736793f914c69a5ceadbd81660eb51418de2e33dcf044ca3`
- `../PROTOCOL.md`: SHA-256 `85c1570d523fa8514e9596ecc36e85bc1299586f0a70b0211c38f3725eb59aac`
- `../reconciliation.json`: SHA-256 `2aba8ca61b1ef8461654cfcab4b4cd86847660259576a9038aa6015e4ccc0fe6`

Actual command, from this directory:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_exact_oracle
```

Result: 15 tests passed, 0.144 seconds, Python 3.14.0. Tests use synthetic data
only and never open historical tables. Coverage includes constant/linear/
quadratic histories, even/odd designs, exact normal-equation residual
orthogonality, time/value translation, hand-derived small-design weights,
basis-response weights, attained display-rounding extrema for both families
across sample counts 4–24, the 45 grid plus four contrast windows and matched
position/velocity memberships, centered-derivative and western arithmetic
boundary cases, invalid schema/token/missing-data failure, and exclusive-file
preservation.

Root confirmed that all 791 numeric tokens and 229 blanks matched across the
two independently frozen transcriptions, and released historical execution
after this implementation freeze and synthetic pass. That release is a
calculation dependency check, not independent source-measurement validation.

The implementation does not use NumPy, SciPy, external solver software, network
access, original video annotation, source edits, or any Sherlock case state.
Its fractions govern exact comparisons; floating values are display aids.
