# extensions — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust Component/Tool/Profile/Runtime catalog domain with retained administrator installers.
- Sequence: 1 sealed contracts; 3 reads; 5 registration writes.
- Existing feature dependencies: identity.

## Current source and authority

Components, Tools, Profiles and immutable Runtime environment contracts. The implemented contract is in the linked source and [extensions feature specification](../../features/extensions.md).

| File | Planning treatment |
|---|---|
| [ops/component_store.py](../../../ops/component_store.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/profile_store.py](../../../ops/profile_store.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/profiles.py](../../../ops/profiles.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/tool_store.py](../../../ops/tool_store.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/runtime_catalog.py](../../../ops/runtime_catalog.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [executor/runtime_store.py](../../../executor/runtime_store.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/profile_inventory.py](../../../ops/profile_inventory.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/software_metadata.py](../../../ops/software_metadata.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/runtime_hub.py](../../../ops/runtime_hub.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/dependency_catalog.py](../../../ops/dependency_catalog.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep research software and its dependencies in their original languages/images. Retain deploy/runtime.py/runtime_inventory.py and external validators initially; registered user configuration is not platform release source.

## Compatibility invariants

- Registering a new component must not require new MCP tools or platform redeployment. Preserve profile revision pins on submitted Jobs.
- Runtime metadata is separate from Job state; instance grants and exact revisions are verified, and dependency discovery does not authorize host installation.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Freeze the distinct identities for source namespace, current attribution, immutable software revision, execution Profile kind, Runtime revision/grant and derived Dependency unit.
2. Port source snapshot checking/publication and registration collision rules without overwriting a sealed revision or fabricating Built-in attribution.
3. Preserve each digest serialization namespace exactly: Component source pins, pretty-printed Profile content, Tool manifests and compact Runtime manifests are not one universal JSON hash.
4. Port Profile stage binding and exact Runtime/Tool pins, including requires/stage_requires and ambiguous interpreter scopes. Registration does not install a framework.
5. Port current/historical discovery and representative dependency projections. Dependencies remain derived from granted Runtime metadata; transitive inventories stay bounded in summaries.
6. Keep the configured dependency directory and administrator recipe/image validation workflow. New grants and installations remain explicit host actions, protected by the shared installation/validation fence.
7. Port curation/category/attribution overlays separately from sealed manifests and execution evidence. Preserve Python Unicode casefold/normalization behavior used in derived IDs.
8. Test existing records, legacy runtime_id/direct images and exact older revisions alongside new registrations and large package inventories.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Existing Profile pins an older Tool/Runtime | Launch/read the exact revision after a newer registration. |
| Two namespaces or Profile kinds collide | Reject publication without partial source state. |
| Same dependency version in different images/directories | Keep distinct physical origins and one software-unit identity. |
| 995 transitive package entries | Do not promote all entries or repeat the full inventory in every Profile. |
| Inventory metadata or image identity drifts | Do not silently bind the stale observation to a new launch. |
| Runtime installer holds a GPU validation fence | Block incompatible update/dispatch without killing validation. |

### Existing regression sources

- [tests/ops/test_components_platform.py](../../../tests/ops/test_components_platform.py)
- [tests/ops/test_independent_profiles.py](../../../tests/ops/test_independent_profiles.py)
- [tests/ops/test_research_tools.py](../../../tests/ops/test_research_tools.py)
- [tests/ops/test_runtime_catalog.py](../../../tests/ops/test_runtime_catalog.py)
- [tests/ops/test_profile_inventory.py](../../../tests/ops/test_profile_inventory.py)
- [tests/ops/test_runtime_hub.py](../../../tests/ops/test_runtime_hub.py)
- [tests/ops/test_dependency_catalog.py](../../../tests/ops/test_dependency_catalog.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Read-only catalog parity precedes registrations. Preserve runtimes.sqlite3, instance grants, configured roots, source snapshots and digest bytes; Runtime installers can stay Python while Rust serves the same executor contract.

## Main risk and design review

Rust structs must preserve opaque sealed/historical metadata. Strict new-input validation cannot be applied as a destructive schema rewrite to existing user manifests.

## Contracts and documentation to review

- [ops/runtime_contract.py](../../../ops/runtime_contract.py)
- [ops/profiles.py](../../../ops/profiles.py)
- [loom_use/runtimes.md](../../../loom_use/runtimes.md)
- [ops/execution.py](../../../ops/execution.py)

Change rule: When Profiles, Components, Tools or Runtimes change, review stage pins, dependency requirements, executor grants/policy, API/MCP discovery, Dashboard, configured installation directories and preservation.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
