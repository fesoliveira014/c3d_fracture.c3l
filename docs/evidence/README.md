# Independent collision evidence

[collision-oracle-evidence.zip](collision-oracle-evidence.zip) contains the
standalone standard-library Fraction oracle, its analytic tests, the exported
binary32 geometry, exact reports, baseline comparisons and CLI reproduction
instructions. The archive is analysis evidence; its Python is not library runtime.

SHA256: `244f2f14e768729a05cde571bde92e8ef165a2890d1ed30879922bb3eb0839d8`.

The corrected corpus passes 96/96 exact geometric-bound and source-bit-retention
checks, covering 9,877 hulls and 41,810 point entries. The baseline artifacts preserve
the earlier 28 missing source positions in 15 cases and the earlier native failures.
The corrected corpus does not include the separate authored face/edge subdivision
fix. That work is still incomplete; see [status](../status.md).

The bundle's internal SHA256SUMS identifies every preserved file. Its README gives
Python 3.11+ reproduction commands and distinguishes exact results from approximate
display values and runtime diagnostics.
