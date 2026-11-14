# execution — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust loom-executor host service and Rust stage/worker state machine.
- Sequence: 2 host Executor; 4 worker/stage integration.
- Existing feature dependencies: extensions.

## Current source and authority

Job lifecycle, script execution and container ownership. The implemented contract is in the linked source and [execution feature specification](../../features/execution.md).

| File | Planning treatment |
|---|---|
| [executor/runtime_policy.py](../../../executor/runtime_policy.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [executor/server.py](../../../executor/server.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/execution.py](../../../ops/execution.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/hooks.py](../../../ops/hooks.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/runtime_client.py](../../../ops/runtime_client.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/runtime_contract.py](../../../ops/runtime_contract.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/job_work.py](../../../ops/job_work.py) | Inspect domain/consumer boundary; port only the selected core responsibility |
| [ops/workflows.py](../../../ops/workflows.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep registered Component/Tool source bytes, Python/Isaac/ML commands and their container images. Initially retain Docker CLI execution and its established policy semantics rather than simultaneously adopting a different Docker client API.

## Compatibility invariants

- Loom executes Jobs. Release resources based on executor-ticket, container and process return evidence. Never pass platform secrets or Docker sockets into Jobs.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Freeze the Unix-socket request/response envelopes and credential/instance grants exposed by executor/server.py. Preserve every configured UID/GID, image pin, store grant and resource limit.
2. Port ticket lookup, create-or-reuse and label/request fingerprints before launch. Persist the accepted ticket before start and reconcile a lost Docker reply against the same container identity.
3. Port container policy construction: non-root, read-only rootfs, dropped capabilities, explicit mounts, driver capabilities, network and output path validation. Keep Docker/native/API secrets outside Jobs.
4. Use typed Job, Attempt, stage and ticket identities; preserve ticket strings and old request/launch hashes. Unknown container state must remain resource-owned.
5. Port bounded cancellation and log/exit collection. Distinguish a requested stop, observed process/container return, natural successful return and successful artifact indexing.
6. Move worker restart reconciliation, return receipts, result outbox, finalizer receipts and callbacks together with their transaction/fence rules. Preserve fsync/rename and directory durability.
7. Keep one requested outcome as one logical Job; internal steps remain producer-reported evidence, while workflow nodes retain real independent scheduler ownership.
8. Execute CPU acceptance with exact input/output mounts and crash injection at create, ticket commit, start reply, return receipt and finalizer boundaries. GPU/driver acceptance is a later explicit test boundary.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Docker create succeeds and reply is lost | Recover only the matching unstarted container; no second launch. |
| Worker restarts with an active or uncertain ticket | Reconcile/cancel and prove return before assigning resources. |
| Late return receipt from an older Attempt | Ignore for the current Attempt; preserve original evidence. |
| Finalizer or callback fails after training returns | Retry that stage only, without retraining. |
| Job cancellation races successful return | Preserve cancellation and the actual return evidence consistently. |
| Secondary storage or granted Runtime changes identity | Reject launch; never fall back to another store/image. |

### Existing regression sources

- [tests/ops/test_executor_boundary.py](../../../tests/ops/test_executor_boundary.py)
- [tests/ops/test_job_work.py](../../../tests/ops/test_job_work.py)
- [tests/ops/test_job_lifecycle.py](../../../tests/ops/test_job_lifecycle.py)
- [tests/ops/test_research_workflows.py](../../../tests/ops/test_research_workflows.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Executor can be the first running Rust component only after wire/hash/ticket compatibility is proven. Drain/reconcile all attached instances before changing shared helpers; keep the old executor executable and existing databases for rollback.

## Main risk and design review

This is the highest-consequence block. Tokio task cancellation, process exit and Docker resource return are not equivalent and cannot share a single completion flag.

## Contracts and documentation to review

- [ops/execution.py](../../../ops/execution.py)
- [ops/runtime_contract.py](../../../ops/runtime_contract.py)
- [executor/runtime_policy.py](../../../executor/runtime_policy.py)

Change rule: When execution contracts change, verify the worker, executor, restart/idempotency behavior, cancellation, result collection and Compose mounts. Review the full installation doctor and step exit criteria when this feature changes; a local health response does not establish user-facing readiness.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
