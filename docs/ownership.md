# Ownership

`c3d_fracture.c3l` owns fracture algorithms and their authoring workflow. It consumes
c3d's public CPU data types. c3d owns the reusable rendering, asset and physics
capabilities that applications use around those algorithms.

| Standalone fracture project | Retained in c3d |
|---|---|
| Exact arithmetic, predicates, solid validation and topology | Geometry, bounds, math integration and generic faults |
| Boolean and volumetric Voronoi generation | AssetStore and ModelDocument ownership/publication |
| Surface construction, attribute transfer and collision reconstruction | glTF decoding, source inspection, material and texture vocabulary |
| Fracture recipes, site placement and sidecar formats | Rendering, picking, GUI and scene nodes |
| Future bake writer/loader, CLI and fracture authoring workflow | Box3D integration, body/collider ownership and generic multi-hull Breakable APIs |

The current kernel's direct dependency surface is small:

- `c3d::geometry::Geometry` and `Topology`, including the supported vertex streams,
  indices and bounds; `Geometry.finalize` updates output bounds.
- c3d's `INVALID_ARGUMENT`, `UNSUPPORTED` and `CAPACITY_EXCEEDED` faults.
- Standard-library math vectors, allocators, containers, sorting and clocks.

The package owns its fracture-specific faults, workspace and result types.
It imports no renderer, platform, GUI, Box3D binding or other add-on in `src/`.
The c3d package currently brings broader transitive build dependencies; that
packaging fact does not give the kernel ownership of those systems.

A caller supplies indexed triangle geometry and explicit topology/material labels.
The kernel borrows that data for the call and returns owned CPU arrays. It does
not insert assets, create nodes or bodies, assign live material IDs, or publish
a scene. Those steps belong to the application or an explicit consumer adapter.
The optional integration tests select c3d's physics add-on separately.

Generic multi-hull piece authoring, read-only Breakable views, pending preparation
and serialization stay in c3d. The glTF `SourceRecord`, shared supported-extension
vocabulary, source diagnostics and `ModelInstance.present_node` also remain generic
c3d APIs. A future bake layer consumes them; it does not duplicate their loaders,
encoded-image ownership or native physics implementation.

The former `c3d::physics::fracture` namespace is relocated to `fracture`. Consumers
select the `c3d_fracture` package explicitly. The pinned c3d dependency includes
[the generator removal](https://github.com/fesoliveira014/c3d.c3l/pull/328).
No reverse dependency from c3d to this project is introduced.

Feature development remains paused. The move preserves the existing checkpoint,
its known limitations and evidence; it does not authorize finishing the deferred
bake, collision or runtime work.
