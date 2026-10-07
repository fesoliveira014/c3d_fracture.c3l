module fracture_example;

import c3d;
import fracture;
import std::io;
import std::math;

const usz SCRATCH_BYTES @local = 8 * 1024 * 1024; // One reusable arena for the two-site box.
const uint TRIANGLE_CORNERS @local = 3;
const uint HULL_VERTEX_LIMIT @local = 128;

<* Generate two box fragments and their convex collision hulls. *>
fn int main() {
    if (catch failure = fracture_box()) {
        io::eprintfn("Fracture failed: %s", failure);
        return 1;
    }
    return 0;
}

fn void? fracture_box() @local {
    Geometry geometry = geometry::box(
        allocator: mem,
        width: 2,
        height: 2,
        depth: 2,
    );
    defer asset::free_geometry(mem, &geometry);

    uint[] topology = alloc::new_array(mem, uint, geometry.positions.len);
    defer alloc::free(mem, topology.ptr);

    uint[] materials = alloc::new_array(mem, uint, geometry.indices.len / TRIANGLE_CORNERS);
    defer alloc::free(mem, materials.ptr);

    foreach (uint vertex, position : geometry.positions) {
        topology[vertex] = (position.x > 0 ? 4 : 0)
            | (position.y > 0 ? 2 : 0)
            | (position.z > 0 ? 1 : 0);
    }

    SolidMeshView source = {
        .geometry = geometry,
        .topology_vertices = topology,
        .triangle_materials = materials,
    };
    Vec3[2] sites = { { -0.5f, 0, 0 }, { 0.5f, 0, 0 } };

    FractureWorkspace workspace = fracture::create_fracture_workspace(mem, {
        .scratch_bytes = SCRATCH_BYTES,
        .max_vertices = 4096,
        .max_triangles = 8192,
        .max_pieces = 8,
        .max_sites = 2,
        .max_hulls = 128,
        .resolution_m = 0.0001f,
    })!;
    defer fracture::destroy_fracture_workspace(&workspace);

    FractureResult fragments = fracture::create_voronoi_fracture(
        allocator: mem,
        workspace: &workspace,
        source: source,
        sites: sites[..],
        cut: { .material_slot = 1, .uv_repeats_per_meter = 1 },
    )!;
    defer fracture::destroy_fracture_result(&fragments);

    FractureCollision collision = fracture::create_fracture_collision(
        allocator: mem,
        workspace: &workspace,
        fragments: &fragments,
        max_hull_vertices: HULL_VERTEX_LIMIT,
    )!;
    defer fracture::destroy_fracture_collision(&collision);

    io::printfn("Pieces: %s; hulls: %s", fragments.pieces.len, collision.hulls.len);
    return;
}
