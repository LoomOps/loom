# results — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust result indexing, storage selection and lineage domain.
- Sequence: 1 locator/provenance contracts; 5 result writer cutover.
- Existing feature dependencies: identity, extensions.

## Current source and authority

Artifact registration, indexing, lineage and metadata contracts. The implemented contract is in the linked source and [results feature specification](../../features/results.md).

| File | Planning treatment |
|---|---|
| [ops/registry.py](../../../ops/registry.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/retain-artifact.py](../../../ops/retain-artifact.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/storage.py](../../../ops/storage.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep producer result.json contracts, research file bytes and specialized scientific validators. Do not import scientific runtime dependencies into the platform or rewrite dataset metadata as a side effect of the port.

## Compatibility invariants

- Distinguish execution completion from indexing completion. Ownership changes must not overwrite original artifact or execution provenance.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Inventory registry entity/revision/location schemas and storage marker behavior; distinguish execution return, artifact readiness and indexing completion.
2. Port bounded result parsing and exact profile/producer provenance checks with explicit path, symlink, size, MIME and content-hash behavior.
3. Preserve named store IDs and frozen output_storage selection through every stage, retry and downstream input. Host paths come from installed grants, not user-supplied locators.
4. Port indexing and result_outbox consumption atomically, preserving duplicate retry behavior and separate callback output handling.
5. Retain large-file streaming hashes and safe atomic file publication. Keep ownership overlays distinct from original producer/execution identities.
6. Port upstream consumes relations and cross-storage resolution without duplicating bytes or inflating research Job/dataset counts.
7. Keep profile-specific semantic validation external; a valid hash/schema does not establish episode counts, physics or model acceptance.
8. Test index/reindex/reconnect and a real CPU cross-storage producer/consumer chain in isolated stores.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Execution complete but indexing fails | Keep the returned execution and retry indexing only. |
| Selected store missing/replaced/unreadable | Fail specifically; do not publish to primary implicitly. |
| Artifact path escapes through a symlink | Reject without reading another Job or host secret. |
| Same verified artifact reindexed | Preserve identity and lineage without duplicate production. |
| Downstream Job consumes a secondary-store output | Resolve the exact storage ID and immutable artifact. |
| Metadata claims disagree with actual scientific content | Do not equate generic indexing success with semantic acceptance. |

### Existing regression sources

- [tests/ops/test_result_pipeline.py](../../../tests/ops/test_result_pipeline.py)
- [tests/ops/test_output_contract.py](../../../tests/ops/test_output_contract.py)
- [tests/ops/test_installation_smoke.py](../../../tests/ops/test_installation_smoke.py)
- [tests/ops/test_storage_results.py](../../../tests/ops/test_storage_results.py)
- [tests/ops/test_job_lifecycle.py](../../../tests/ops/test_job_lifecycle.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Use preserved DB/file snapshots and exact row/hash comparisons. Switch the result writer with its outbox consumer only after old execution/finalizer tickets return; retain original data and locators throughout rollback.

## Main risk and design review

Storage identity, file existence, byte integrity and scientific validity are four different claims. Replacing them with one Rust Available enum would lose evidence.

## Contracts and documentation to review

- [ops/registry.py](../../../ops/registry.py)
- [ops/mcp_groups.py](../../../ops/mcp_groups.py)

Change rule: When artifact schemas change, check producers, API/MCP schemas, queue dependency readiness, catalog projections and detail views together.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
