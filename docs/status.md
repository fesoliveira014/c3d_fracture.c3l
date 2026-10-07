# Status

Feature development was paused on 2026-10-07 at the owner's request. The active
work is extracting the preserved implementation into this standalone project.
The standalone checks below passed on Windows; removal of the in-tree copy from
c3d is still pending. This does not complete the former fracture milestone.

The implementation checkpoint is
[`b3170d04bf4406b377c9a13d97514caeb8bd0cdf`](https://github.com/fesoliveira014/c3d.c3l/commit/b3170d04bf4406b377c9a13d97514caeb8bd0cdf).
The pinned c3d dependency is `bd90264bf0b5c9bd8948d4d4cb0087efb2dc79da`.
The namespace move to `fracture` changes package ownership, not the geometry
algorithms. The [checkpoint record](fracture-checkpoint-status.md) distinguishes
completed checks from unfinished acceptance.

| Area | Preserved state |
|---|---|
| Exact arithmetic and solid validation | Implemented, including bounded scratch, raw/quantized validity, shell nesting and named faults. |
| Boolean/Voronoi generation | Implemented with shared cuts, source attributes, independent surface ownership and deterministic output. |
| Collision reconstruction | Implemented checkpoint with source-protected generated-point omission and final geometric witnesses; authored subdivision retention remains incomplete. |
| Native integration | Existing diagnostic and physics test evidence is preserved; fixture equivalence still needs correction. |
| Measurements | 105 cases completed a warmup and three measurements; the owner paused before final performance acceptance. |
| Bake writer/loader and interactive workflow | Not completed. Designs and unfinished work remain inactive. |

The checkpoint's 36 selected collision groups passed O0, O3, O4 and explicit O4
fast math. The independent rational oracle passed geometric bounds and raw source
position retention for 96 quaternion-rotated exported cases: 9,877 hulls and
41,810 point entries. All those hulls passed the isolated native construction
diagnostic. The ordinary physics cooking tests use Rodrigues rotations and are
additional coverage, not a byte-identical rerun of that exported corpus.

The known authored-point defect is outside those 96 fixtures. A valid cube with
an authored face-center vertex retains all nine source positions at hull limit
128, but its current limit-4 output omits the face-center position. Authored edge
and interior points need the same retention contract. A refinement draft and
public regression drafts are preserved under [continuation](continuation/README.md),
outside the active source and test paths. They are not accepted fixes.

## Standalone extraction checks

| Check | Observed result on Windows with C3 0.8.3 |
|---|---|
| Public `basic` consumer | Builds and runs; reports two pieces and two hulls. |
| Focused `unit` target | One selected group passed; 194 unrelated groups skipped. |
| `collision_integration` | Both existing ordinary physics cooking groups passed. Their Rodrigues fixture distinction above still applies. |
| Manual `kernel_bench` | Built; concave and wall single-pass checks passed. These runs are not a new performance acceptance decision. |
| Manual `collision_oracle` exporter | Box-only export produced 24 cases with no reconstruction failures. |
| Build-script FP guard | Rejects relaxed/fast math below O4. |

The local setup initialized the real pinned submodules and generated the required
shader embeds, while reusing pin-matched native artifacts. A fresh-download setup
and Linux standalone run were not performed. These checks verify the extraction
consumer/build wiring; they do not resolve the authored-point defect or complete
baking and interactive acceptance.

Before resuming the remaining feature work:

1. Correct authored-point retention and verify closure, coverage, source bits,
   native cooking and deterministic output for the new cases.
2. Align the ordinary cooking fixtures with the exact quaternion export corpus.
3. Complete the postponed measurement/acceptance decision.
4. Implement the bake writer/loader, sidecar validation, transactional publication
   and runtime demonstration only when the owner explicitly resumes that scope.

The decision and discussion history is retained in the
[original tracking issue](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6047780415).
The old in-tree [collision PR](https://github.com/fesoliveira014/c3d.c3l/pull/326)
preserves a draft checkpoint; it is not a claim that the remaining milestone
acceptance passed. New standalone build checks will be recorded separately.
