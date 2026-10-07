# c3d_fracture.c3l

CPU Boolean and three-dimensional Voronoi fracture generation for C3, using
[c3d](https://github.com/fesoliveira014/c3d.c3l) geometry types. The package provides
`c3d_fracture`; its C3 module is `fracture`.

**Status:** extraction checkpoint. Feature development is paused. Boolean/Voronoi
generation and collision reconstruction are preserved, with a known authored-point
retention defect in point-limited collision subdivision. See [status](docs/status.md)
before treating this checkpoint as complete fracture tooling.

The public operations are `create_boolean`, `create_voronoi_fracture` and
`create_fracture_collision`. A bounded workspace holds temporary data. Successful
surface and collision results own independent allocations and remain valid after
workspace reuse. The kernel creates no scene, rendering or native physics objects.
Applications publish its geometry through the c3d APIs they select.

Requires C3 0.8.3, Python 3.10 or newer for setup/build orchestration, and the tools
required by the pinned c3d dependency. Prepare dependencies and run the public
[two-site box example](examples/basic.c3):

```text
python scripts/setup.py
python scripts/build.py --run
```

The setup command prepares c3d's existing native libraries and shader embeds;
it does not run tests. Those are transitive package build requirements even for
this CPU consumer. The fracture package directly depends only on c3d.

Run a focused CPU test or the optional physics integration target:

```text
python scripts/build.py --target unit --test-filter test_voronoi_generation_public_sites
python scripts/build.py --target collision_integration --test-filter collision
```

The integration target additionally selects `c3d_physics` and its Box3D dependency.
Use strict floating-point settings at O0–O3. O4/O5 use the exact predicate path;
see the [numeric contract](docs/fracture.md) before overriding compiler settings.

- [Ownership and dependency boundary](docs/ownership.md)
- [Current status and outstanding work](docs/status.md)
- [Numeric and geometry contracts](docs/fracture.md)
- [Recorded kernel measurements](docs/fracture-measurements.md)
- [Inactive continuation drafts](docs/continuation/README.md)
- [Independent collision evidence](docs/evidence/README.md)

The bake writer/loader, sidecar/tool workflow and interactive authoring workflow
are not completed by this extraction. Generic Breakable support, glTF loading and
source inspection remain in c3d. See [LICENSE](LICENSE).
