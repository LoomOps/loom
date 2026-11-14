# observations — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Retained collectors initially; typed Rust observation readers and freshness model.
- Sequence: 3 read-only parity; optional later collector rewrite.
- Existing feature dependencies: none.

## Current source and authority

Host, GPU and Docker observations. The implemented contract is in the linked source and [observations feature specification](../../features/observations.md).

| File | Planning treatment |
|---|---|
| [deploy/collect-dashboard-gpus.py](../../../deploy/collect-dashboard-gpus.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/collect-observations.py](../../../deploy/collect-observations.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/docker_status.py](../../../ops/docker_status.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/host_metrics.py](../../../ops/host_metrics.py) | Retain interface/tooling; review exact bridge and packaging behavior |

## Retained code and external dependencies

Keep host/NVIDIA/Docker collectors and installed collection services initially. External driver/tool output and platform-specific probes are independent of the language of the Job core.

## Compatibility invariants

- Observations are read-only and do not affect queue dispatch. Preserve missing/stale/partial distinctions.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Enumerate collector inputs, files, observation timestamps and missing/stale/partial/error states from host_metrics.py and docker_status.py.
2. Port the reader/response model first, preserving source timestamps and bounded parsing of malformed or incomplete snapshots.
3. Keep actual driver/GPU inventory distinct from an executable Runtime grant or an available scheduler resource.
4. Preserve the read-only boundary: collection failure cannot change admission, cancel a Job or infer container return.
5. Retain existing mount ownership and collector timer/unit settings when installing a Rust consumer.
6. Only propose a collector rewrite after measured complexity/performance evidence; use bounded subprocess argv and existing privilege separation if it is later selected.
7. Exercise the unchanged Dashboard resource and Docker views with valid, stale and malformed observations.
8. Document actual hardware/tool acceptance separately from deterministic collector fixtures.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| GPU tool is absent or fails | Unavailable observation, not zero GPUs. |
| Snapshot is old or partial | Retain stale/partial status and source time. |
| Docker inspection fails | Do not release a scheduler ticket based on observation loss. |
| Collector file is malformed/oversized | Bound failure and preserve service availability. |
| Installed collector uses custom paths/UIDs | Read configured grants; do not hardcode another installation. |
| No observation available during a Job | Job ownership/state remains authoritative and unchanged. |

### Existing regression sources

- [tests/ops/test_docker_status.py](../../../tests/ops/test_docker_status.py)
- [tests/ops/test_host_metrics.py](../../../tests/ops/test_host_metrics.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

No collector/service replacement is required for the first Rust backend. Keep file formats and grants; rollback is a reader change only, with no hardware or queue mutation.

## Main risk and design review

Observations look similar to executor status but carry different authority. Sharing a convenient Rust status type across both would be dangerous.

## Contracts and documentation to review

- [ops/docker_status.py](../../../ops/docker_status.py)
- [ops/host_metrics.py](../../../ops/host_metrics.py)

Change rule: When collector fields change, check host mounts, collection services, API projections and UI rendering. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
