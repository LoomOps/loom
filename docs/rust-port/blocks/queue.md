# queue — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust queue eligibility, ordering, admission and operator pause within loom-ops.
- Sequence: 1 pure eligibility model; 4 atomic worker/queue cutover.
- Existing feature dependencies: identity, execution, recovery, results.

## Current source and authority

Shared queue ordering, admission and preparation pipelines. The implemented contract is in the linked source and [queue feature specification](../../features/queue.md).

| File | Planning treatment |
|---|---|
| [ops/queue_control.py](../../../ops/queue_control.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/dispatch_control.py](../../../ops/dispatch_control.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep the existing Dashboard queue UI and external queue-control clients. Retain deployment pause scripts until they can invoke the same stable operation contract.

## Compatibility invariants

- Do not preempt running Jobs. Respect dependencies, allow concurrent preparation and never reassign resources before their return.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Extract ordering and eligibility from queue_control.py and dispatch_control.py into explicit decisions, including dependencies, artifacts, lanes, holds, recovery reservations and global admission.
2. Model a presentation-level logical Job separately from each real scheduler node. Research filters must never remove resource consumers from scheduling.
3. Preserve prepare/run dependency differences, concurrent CPU preparation, one exclusive GPU owner and independent finalization/callback work.
4. Port reorder/hold/resume with stable operation receipts and BEGIN IMMEDIATE transaction boundaries; do not replace persisted order with an in-memory priority queue.
5. Port operator pause keys and maintenance interaction exactly. The same durable key must survive upgrades and older-worker rollback; unrelated fences remain intact.
6. Integrate claims and eligibility with the Rust worker in one ownership change. An async task must not launch from a stale eligibility snapshot.
7. Use a controlled clock to test reservation expiry, dependency readiness and hold/reorder races before executing any container.
8. Compare complete queue snapshots and subsequent chosen work against the Python implementation under the same recorded state and clock.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Failed dependency and independent later Job | Skip the dependency chain while eligible independent work proceeds. |
| Artifact verified during result indexing failure | Allow only consumers whose exact required artifact is ready. |
| Running Job reordered or another Job held | Never preempt or release a running owner. |
| Operator pause across update and old-worker rollback | Keep dispatch fenced until matching-key resume. |
| Recovery reservation expires | Release only its ordering reservation, not an unreturned resource. |
| Two concurrent claim/reorder requests | One durable consistent order and no duplicate claim. |

### Existing regression sources

- [tests/ops/test_queue_contract.py](../../../tests/ops/test_queue_contract.py)
- [tests/ops/test_queue_control.py](../../../tests/ops/test_queue_control.py)
- [tests/ops/test_job_lifecycle.py](../../../tests/ops/test_job_lifecycle.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Move eligibility and claiming with the single authoritative Ops writer. Preserve worker.lock, existing dispatch-control rows and maintenance mode; no shadow implementation may dispatch.

## Main risk and design review

Queue eligibility, resource ownership and UI grouping are separate. An async rewrite can accidentally turn a read model into admission authority.

## Contracts and documentation to review

- [ops/queue_control.py](../../../ops/queue_control.py)
- [ops/job_contract.py](../../../ops/job_contract.py)

Change rule: When queue policy changes, verify dispatch, catalog ordering and control capabilities with the same scenarios.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
