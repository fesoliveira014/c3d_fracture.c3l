# Inactive continuation drafts

These files were preserved when feature work stopped. They are not included in
`src/`, `test/unit/` or any active build target. Their `.txt` suffix is intentional.
They have not passed the complete acceptance sequence and must not be described
as delivered fixes.

The completed implementation baseline is c3d checkpoint
`b3170d04bf4406b377c9a13d97514caeb8bd0cdf`. The drafts retain their historical
`c3d::physics::fracture` namespace; review and migrate them to `fracture` only if
the owner explicitly resumes this work.

| Draft | Purpose and state |
|---|---|
| collision_tetrahedra.c3.txt | Unfinished tetrahedral refinement helper for authored points omitted by hull facets. |
| collision_authored_test.c3.txt | Proposed public face-center, edge-midpoint and combined/permutation acceptance, with exact volume checks at hull limits 128/4. Not accepted after the paused fix. |
| collision_authored_probe.c3.txt | Minimal diagnostic that demonstrated 9/9 retained source positions at limit 128 and 8/9 at limit 4. |
| collision_reconstruction.c3.txt | Pending root wiring that calls the new tetrahedral helper; not the completed checkpoint version. |
| collision_retained.c3.txt | Pending protected-point helper/wiring additions beyond the completed checkpoint. |
| collision-rework-docs.md.txt | Draft explanation of the unaccepted tetrahedral change. |
| bake-contract-inventory.md | Paused read-only material, sidecar and ownership inventory. No bake implementation or finished public bake API is claimed; the historical namespace is labeled. |

Source retention must hold for all reported successes, not only the 96-case
rotation corpus. The known face-center defect remains open. Native cooking and
oracle checks for new authored-point cases were not completed before the pause.
The bake writer/loader and its public ownership APIs remain separate unfinished
work; no bake implementation is enabled by these drafts.

The planning inventory replaces its machine-local interview reference with the public discussion link. SHA256SUMS records the preserved artifact bytes. These snapshots are evidence for a
later deliberate continuation, not instructions to resume automatically.
