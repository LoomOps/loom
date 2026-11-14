# recovery — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Rust recovery incidents, leases, rounds and recipient events in loom-ops.
- Sequence: 1 incident/lease model; 4 worker/queue cutover.
- Existing feature dependencies: identity, execution.

## Current source and authority

Recovery reservations, recipient events and retries. The implemented contract is in the linked source and [recovery feature specification](../../features/recovery.md).

| File | Planning treatment |
|---|---|
| [ops/recovery.py](../../../ops/recovery.py) | Inspect domain/consumer boundary; port only the selected core responsibility |

## Retained code and external dependencies

Keep caller-owned diagnosis and repair, existing MCP actions and user-facing recovery presentation. No resident repair model or new approval/ACK gate is introduced.

## Compatibility invariants

- The caller owns error repair. Preserve reservation deadlines, attempt limits and dependent-Job skipping. Event acknowledgments are recipient-specific.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Extract incident, reservation, lease and execution phase into separate types; Recovery executing must not replace the current Job execution phase.
2. Preserve persisted deadlines and shared recovery-round accounting from recovery.py and finish(): initial execution plus at most three shared repair rounds, with automatic attempts potentially reducing the budget.
3. Port claim/progress/resume/defer/reactivate with the exact actor scope and stable request fingerprint behavior.
4. Keep result-only recovery on the same Attempt and avoid re-running execution admission, mutable input resolution or training.
5. Preserve prior outcomes in attempt_results and job_revisions, while clearing only the current execution result when a new Attempt begins.
6. Use transactional clock-bound comparisons for concurrent claims and expiry; event ACK remains recipient receipt and never grants a lease.
7. Integrate recovery reservation changes with queue selection and returned-resource evidence in the same worker cutover.
8. Test through both MCP/HTTP and durable database restart fixtures, including old records that lack newer optional fields.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Two agents claim the same incident | One valid owner; the other gets the current conflict. |
| Progress after the maximum repair deadline | Do not extend beyond the original repair-round cap. |
| Automatic retry followed by manual recovery | Consume the same shared round budget. |
| Result-only failure | Reuse returned execution and the same Attempt. |
| Old failure beside a running repair | Display current execution; do not submit another repair automatically. |
| Deferred recovery reactivated | Assign the documented new queue order without preempting active work. |

### Existing regression sources

- [tests/ops/test_worker_recovery.py](../../../tests/ops/test_worker_recovery.py)
- [tests/ops/test_job_lifecycle.py](../../../tests/ops/test_job_lifecycle.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

Recovery must switch with its queue/worker consumers. Reuse existing incident/lease/round rows and recognize existing request hashes; no incident reset or fabricated ACK during rollback.

## Main risk and design review

Language types can separate lease and execution state, but expiry, retry budgets and resource evidence remain transactional business rules.

## Contracts and documentation to review

- [ops/recovery.py](../../../ops/recovery.py)
- [ops/access.py](../../../ops/access.py)

Change rule: When state transitions change, check queue dispatch, notification events, claim leases, concurrency and expiry tests. Authoritative transitions live in ops/ops.py worker/finish and ops/recovery.py.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
