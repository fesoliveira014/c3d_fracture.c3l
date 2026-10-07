# Bake contract inventory — paused checkpoint

Read-only preparation captured 2026-10-07. The user subsequently paused fracture feature work and chose extraction into standalone `c3d_fracture.c3l`, namespace `fracture`. No bake implementation, architecture edit, interview, or Notion write was performed. The old bake-module namespace below records the prior agreement; the new standalone boundary supersedes its location.

## Evidence and precedence

- Live merged `main` was verified through GitHub as `bd90264bf0b5c9bd8948d4d4cb0087efb2dc79da`. The inspected core asset/material/model source and named core tests match that commit. The primary checkout's local `origin/main` was older; it was not used as current evidence.
- [Live M84](https://app.notion.com/p/3eccb7903a5881a48cd5fec4ccf7a040), fetched with page-last-edited `2026-10-07T20:57:44.358Z`: Offline/runtime use, Contracts, completion criteria, source-inspection delivery and open bake work.
- [Geometry 04](https://app.notion.com/p/3cfcb7903a5881759af9db439c70105e): CPU Geometry and construction/ownership. [Asset Loading 11](https://app.notion.com/p/3cfcb7903a5881ec8c69c668f9dea6d8): decoded document, instantiation, glTF primitive children. [Physics 16](https://app.notion.com/p/3cfcb7903a588130b87dd600ff2373fe): cooking lifetime and Breakable boundaries. The latter two still contain older M78 one-mesh/one-hull wording; merged explicit-piece code and the later agreements control that point.
- Canonical interview history: [fracture tracking discussion](https://github.com/fesoliveira014/c3d.c3l/issues/267). Individual controlling answers are linked below.
- [Q3 answer 6035076526](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035076526): decoded material vocabulary, shared extension list, verbatim image bytes, scale units.
- [Q4 answer 6035125999](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035125999): interior selection, strict sidecar, float fidelity, staged publication.
- [Q5 answer 6035280988](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035280988): one owning bake document, publication ownership, same-read hash/decode, template-node mapping.
- [Q6 answer 6035372724](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035372724): opt-in independent source record.
- Later controlling corrections: [Q8 answer 6035618680](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035618680), [Q9 answer 6035685519](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035685519), [Q10 answer 6035753408](https://github.com/fesoliveira014/c3d.c3l/issues/267#issuecomment-6035753408).

## Existing public declarations

Excerpts from merged `src/c3d/asset/gltf/source.c3`; bodies omitted, signatures unchanged:

```c3
const usz NO_SOURCE_INDEX = usz::max;
const usz NO_TEMPLATE_NODE = usz::max;

struct SourceImage {
    char[] encoded;
    String declared_mime_type;
}
struct SourceSampler {
    int min_filter;
    int mag_filter;
    int wrap_s;
    int wrap_t;
}
struct SourceTexture {
    usz image;
    usz sampler;
    TextureId srgb;
    TextureId linear;
    String[] extensions;
}
struct SourceMaterial {
    String name;
    String[] extensions;
    usz[] textures;
}
struct SourceRecord {
    Allocator allocator;
    SourceImage[] images;
    SourceSampler[] samplers;
    SourceTexture[] textures;
    SourceMaterial[] materials;
    usz[] texture_images;
    usz[] template_nodes;
    String[] extensions_required;
}
struct SourceDiagnostic {
    usz material_index;
    usz texture_index;
}
fn ModelDocument? decode_model_with_source(
    Allocator allocator,
    String path,
    SourceRecord* source,
    LoadOptions options = asset::LOAD_OPTIONS_DEFAULT,
    SourceDiagnostic* diagnostic = null,
);
fn ModelDocument? decode_model_memory_with_source(
    Allocator allocator,
    char[] bytes,
    String base_dir,
    String key,
    SourceRecord* source,
    LoadOptions options = asset::LOAD_OPTIONS_DEFAULT,
    SourceDiagnostic* diagnostic = null,
);
fn void destroy_source_record(SourceRecord* source);
```

Both decode entry points name `ASSET_IO_ERROR`, `ASSET_FORMAT_ERROR`, `UNSUPPORTED`, `INVALID_ARGUMENT`. Memory bytes are borrowed for the call; allocator must not be `tmem`; source is assigned only on complete success. Diagnostics reset to `NO_SOURCE_INDEX` at entry and contain known indices only on failure. The source record survives document destruction or publication independently.

Other existing signatures:

```c3
fn ModelId? AssetStore.publish_document(&self, ModelDocument* document);
fn void destroy_model_document(ModelDocument* document);
fn Node* ModelInstance.present_node(&self, usz template_index);
```

`publish_document` requires the store/document allocator to match and not be temporary. It decides `CAPACITY_EXCEEDED` or `INVALID_ARGUMENT` before insertion. On success it transfers payload ownership, remaps references, and empties the document; on failure store and document are unchanged. `destroy_model_document` retains the allocator in the emptied value. A bake owner therefore destroys the remaining document state and its independent sidecar/hull/recipe storage after either successful or failed publication. `present_node` requires an in-range template index and returns null when the original node has been removed, including slot reuse.

No delivered or compiled public bake owner, writer or loader declaration was found in merged source or live M84. Ownership and behavior are agreed; exact names/layout/signatures remain unfinished. Do not invent an existing `load_bake` API.

## Material mapping

The writer serializes decoded `DocumentMaterial.data`, with source metadata only for provenance/resource mapping and extension acceptance. Compare decoded values after re-reading the staged GLB. Imported kinds are BASIC, STANDARD and PHYSICAL; this does not authorize exporting arbitrary TOON, CUSTOM, render-target references or application-only material state.

| Accepted content | Decoded field(s) | Export and round-trip requirement |
| --- | --- | --- |
| Common | `Material.kind`, `common.alpha_mode`, `alpha_cutoff`, `double_sided` | Preserve family and common values. Other common raster/blend fields remain importer defaults; no new extension is implied. |
| Core metallic-roughness | `standard.base_color`, `metallic`, `roughness` | Preserve factors and `base_color_map`, `metallic_roughness_map`. |
| Core emission | `standard.emissive`, `emissive_strength`, `emissive_map` | Preserve RGB and strength; strength uses `KHR_materials_emissive_strength`. |
| Normal/occlusion | `standard.normal_map`, `normal_scale`, `occlusion_map`, `occlusion_strength` | Preserve independent slots and scalar values, including signed normal scale. |
| Unlit | `basic.color`, `basic.map` | Emit `KHR_materials_unlit`; preserve the decoded BASIC vocabulary. |
| Clearcoat | `physical.clearcoat`, `clearcoat_roughness`, `clearcoat_normal_scale`; three clearcoat slots | Preserve factors and each independent slot. |
| Sheen | `physical.sheen_color`, `sheen_roughness`; two sheen slots | Preserve color/roughness and maps. |
| IOR | `physical.ior` | Dimensionless; unchanged by geometry scaling. |
| Specular | `physical.specular`, `specular_color`; two specular slots | Preserve both factors and maps. |
| Anisotropy | `physical.anisotropy`, `anisotropy_rotation`, `anisotropy_map` | Preserve strength, radians and map. |
| Transmission | `physical.transmission`, `transmission_map` | Preserve factor and map. |
| Volume | `physical.thickness`, `thickness_map`, `attenuation_distance`, `attenuation_color` | Uniform bake scale changes thickness only. Nonuniform scale on a volume material is `UNSUPPORTED`; attenuation distance is unchanged. Decoded distance zero represents unbounded attenuation and must decode back to zero. |
| Every texture slot | `TextureSlot.texture`, `sampler`, `uv_set`, `transform.offset/scale/rotation` | Preserve effective UV0/UV1, including a transform texCoord override. Texture transform remains above generated cut UVs. |
| Samplers | `DocumentSampler.desc` and `SourceSampler` | Preserve decoded behavior and source minification mode; zero source min/mag filter means unspecified. |
| Images | `SourceImage.encoded`, source-image indices | Copy referenced encodings verbatim and deduplicate by source-image identity, namespaced by input document. No re-encoding. Choose MIME from validated bytes, not the declared string. |

The shared `SUPPORTED_MATERIAL_EXTENSIONS` contains exactly clearcoat, sheen, transmission, volume, IOR, specular, anisotropy, emissive_strength, unlit and texture_transform (`KHR_` names). Ordinary required-extension validation already consumes this list. The baker must consume the same list and reject unknown optional selected material/texture/texture-info extensions with `UNSUPPORTED`, material index and extension name. Source inspection gathers nested names onto the owning `SourceMaterial.extensions`, sorted and deduplicated.

Q8 correction: decoded texture identity is **image + color space**, while samplers belong to slots. Resolve a slot to a referenced source texture matching its decoded image and decoded sampler behavior; choose the lowest source texture index among equivalent candidates. Preserve each slot's sampler even when two slots share one decoded image. The accepted fidelity limit is an explicit filter versus an unspecified filter that decodes identically. Source metadata is not a per-slot schema.

Only `thickness` and `attenuation_distance` are length-valued fields in the current imported material parameters; the former changes under uniform bake scale and the latter does not. UV transforms and normal/occlusion scalars are dimensionless; anisotropy rotation is angular. Preserve reflected geometry by correcting winding/normal transforms and regenerating tangents, with a normal-mapped reflected fixture.

## Sidecar and publication requirements

Exact wire field names and numeric version values are not yet specified. Required semantic fields are:

| Group | Required contents |
| --- | --- |
| Identity | SHA-256 of the written GLB; hashes of source document(s), cutter and optional interior document. |
| Recipe | Operation; ordered sites OR seed, sampler version and fixed attempt budget; resolved source/cutter node selections; resolved interior material index; interior UV density. |
| Limits/version | Every numerical, scratch/count/capacity setting; hull vertex limit; kernel and sidecar format versions. Platform/build target and compiler version are informational. |
| Pieces | Stable order, validated template-node mapping and piece-local hulls using the same hull-view vocabulary as runtime fracture. Each array count must match. |

Interior input is a glTF/GLB document, selected by index or unique name. Missing/out-of-range/ambiguous selection faults with the requested selector. Retain only that material and referenced resources. Default is base color `(0.5,0.5,0.5,1)`, metallic 0, roughness 1, UV density 1 repeat/meter.

The loader reads GLB bytes once, hashes and decodes that same buffer, then validates everything before returning its owner. Piece indices must exist, be distinct, have no ancestor relation and represent rigid, skin-free and morph-free pieces. Every piece has at least one hull; each hull has 4..recorded-limit finite points. Source GLB node indices and decoded template indices are not interchangeable: the importer inserts a child for every primitive; `SourceRecord.template_nodes` supplies the mapping.

| Failure | Agreed fault/behavior |
| --- | --- |
| Newer format version | `UNSUPPORTED` |
| Unknown field, malformed sidecar, nonfinite value, count/range/mapping/rigid-skin-morph violation | `ASSET_FORMAT_ERROR`; no bake owner exposed |
| GLB identity mismatch | `BAKE_MISMATCH`; no owner exposed |
| File failure | `ASSET_IO_ERROR`; no owner exposed |
| Unknown selected material/texture feature or unsupported validated image format | `UNSUPPORTED`, with required diagnostics |
| Fixed site-placement attempt budget exhausted | `SITE_GENERATION_FAILED` |
| Degenerate hull reaching native authoring | Native `DEGENERATE_GEOMETRY` propagates unchanged; the CPU loader does not cook native objects |

Use standard-library JSON and SHA-256. Hull floats must round-trip bitwise, including subnormals and fixture-range extremes. No proof of the float spelling/parser path was performed during this read-only task. Installed JSON number scanning accepts decimal notation and delegates float conversion to double; raw hexadecimal numeric tokens are not accepted. Signed zero must be part of the round-trip sweep. Strict unknown-field checks must be implemented explicitly.

Stage into a distinguishable sibling directory. Without `--replace`, reject an existing destination before work. With replace: move old output aside, move complete staged directory into place, then delete old output; restore the old output if a move fails. Clean staging on failure. Inject failure at the second move and assert the original GLB/sidecar pair remains intact. Never publish a mixed pair.

## Reusable implementation and acceptance mapping

| Existing evidence/code | Required bake coverage still to add |
| --- | --- |
| `asset/gltf/source.c3`, `source_extensions.c3`, `convert.c3` | Shared-list completeness; deterministic per-slot source-texture resolution; selected unknown material, texture, normalTexture and occlusionTexture extensions rejected with diagnostics. |
| `test/src/test_gltf_source.c3`: seven source tests; private `source_glb` builds padded JSON/BIN fixtures | Tiny synthetic GLB per accepted extension, combined physical fixture, both UV sets/transforms, shared image with different/equivalent samplers, MIME declaration mismatch, no downloaded assets. The private helper is a pattern, not a public writer. |
| Source tests cover plain/opt-in equality and allocation count, independent owners, all three encoded-image storage forms, unused image not loaded, node sentinel, exact metadata mismatch diagnostics | Bake owner destroy without publish / after publish / after failed publish: zero live allocations and no double free. |
| `asset/document.c3`, `test/src/test_document.c3` | Validate staged decode field-by-field; publish ownership paths; ordinary glTF load of baked GLB with expected node/primitive counts. |
| `asset/gltf/nodes.c3`, `scene/model_instance.c3`, `test/src/test_model.c3` | GLB/template mapping through `present_node`, distinct/no-ancestor piece records, rigid/no-skin/no-morph rejection, multi-material render children remaining one physical piece. |
| `test/src/test_gltf.c3`: reflection, vertex color, primitive normalization, hierarchy and core conversion cases | Reflected normal-mapped bake; preserved exterior seams/channels; scale-dependent volume thickness and unchanged attenuation distance; nonuniform volume rejection. |
| `std::encoding::json`, `std::hash::sha256` | Float bit sweep; unknown/version/hash/range corruption; same-read hash/decode; I/O and second-move rollback injection. |

## Genuine unfinished contract details

1. Exact bake owner/entry-point declarations, wire names/version and selection/round-trip-check writer fault signatures have not been compiled or agreed in the inspected sources. Do not present guessed APIs as delivered.
2. Float round-trip behavior remains unmeasured; JSON's decimal-to-double path and signed zero need the required bitwise sweep before selecting the final spelling.
3. Conditional selected-content issue: `convert_model` converts all source materials and geometries; `LoadOptions` has no selected-node/material filter. If "other interior content is ignored" also means invalid/unloadable unselected content must not block decoding, the existing public decoder does not establish that stronger guarantee. The recorded contract does not resolve this distinction; do not invent a second importer or silently relax it.
4. M84's illustrative `--interior cut_material.json` and older architecture one-mesh/one-piece text are stale relative to the accepted interviews and merged source. Updating them was outside this read-only task.

Feature work remains paused for extraction. No bake implementation should begin until the user reauthorizes it under the standalone project and the measurement gate is explicitly accepted.
