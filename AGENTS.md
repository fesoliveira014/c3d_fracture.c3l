# c3d_fracture.c3l

Read this file, README.md and docs/status.md before changing the project.

The package provides `c3d_fracture`; every kernel module is `fracture` or a child.
Use C3 0.8.3. Load `c3-expert` before reading or changing C3 or build manifests,
`c3-style` when writing/reviewing C3, and `c3-bindings` when crossing a C binding.
Consult the installed compiler and bundled language reference instead of assuming
syntax from another C3 version.

Feature development is paused at the owner's request. Preserve and verify the
extraction; do not finish deferred work without an explicit request to resume it
or perform that work. Known incomplete cases are tracked in docs/status.md.
Drafts in docs/continuation are inactive evidence, not build inputs.

## Boundaries

The kernel imports only the standard library and c3d CPU types. Rendering,
platform, GUI and native physics are explicit consumer integrations. Do not add
Box3D or another add-on to the kernel dependency surface.

Keep generic Geometry, assets, glTF loading/source inspection, rendering and
multi-hull Breakable capabilities in c3d. This project owns exact arithmetic,
solid validation, Boolean/Voronoi generation, surface/collision reconstruction
and the future fracture-specific recipe/site/bake/tool workflow. See
[ownership](docs/ownership.md).

Workspaces have fixed capacity. Results own independent allocations. Failures
return named faults, publish no partial result, preserve inputs and leave scratch
reusable. Do not introduce hidden growth, per-triangle heap allocations, silent repair,
point movement, dropped source vertices or unmeasured algorithm changes.

## Code and validation

Use descriptive names, short contracts and readable logical blocks. Separate
validation, preparation, computation and publication with blank lines; expand
complex chained loops. Follow the C3 style baseline in the pinned dependency's
`docs/style.md`, while keeping this project's `fracture` module root.

Use preconditions for programming errors and named faults for operational failures.
Keep ownership explicit and cleanup in defers. Document public APIs; avoid history,
ticket numbers and development narration in source comments.

Run new and directly affected tests locally, with selectors when appropriate.
Do not default to the entire c3d or physics suite for a local change. Use the
project's setup/build scripts and preserve the strict floating-point contract:
O0–O3 require strict math; O4/O5 compile out floating filters. Verify required
modes for numeric changes. Do not use c3fmt.

Distinguish compilation, geometry proofs, native cooking, runtime observations and
performance acceptance. A recorded checkpoint or passing subset is not completion
of the outstanding authoring workflow. Keep measurements reproducible, and do not
change scope or numerical policy merely to make a fixture pass.

Python under scripts/ is standard-library build orchestration only. Independent
analysis/oracle tools are preserved as evidence, outside active library runtime.
Preserve user changes and dependency pins unless their change is part of the task.
