# ssh — Rust transition plan

Status: proposed; no Loom Rust implementation or deployment is performed by this document.

Baseline: `4d93ab9bdcb5750f3d0be161925e834984492f89` (Loom alpha.60).

## Decision and sequence

- Target: Retained privileged Python SSH helper; Rust read-only connection discovery.
- Sequence: retain; 6 discovery and Admin relay acceptance.
- Existing feature dependencies: identity, network, installation.

## Current source and authority

Optional personal host SSH accounts and connection discovery. The implemented contract is in the linked source and [ssh feature specification](../../features/ssh.md).

| File | Planning treatment |
|---|---|
| [deploy/ssh_host.py](../../../deploy/ssh_host.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [deploy/ssh_setup.py](../../../deploy/ssh_setup.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [dashboard/ssh_access.py](../../../dashboard/ssh_access.py) | Retain interface/tooling; review exact bridge and packaging behavior |
| [ops/ssh_info.py](../../../ops/ssh_info.py) | Retain interface/tooling; review exact bridge and packaging behavior |

## Retained code and external dependencies

Keep the established host-account provisioning/helper and Dashboard Admin/CSRF boundary. Do not rebuild an SSH server, change user authentication or expand access as part of a Rust rewrite.

## Compatibility invariants

- Admin-only mutations; never adopt existing accounts or grant sudo/Docker. Disable blocks the personal UID before remote cleanup. Same-host clients require no SSH.
- Preserve existing IDs, authentication, configured roots, sealed bytes and operational history unless an explicit separate schema change is approved.
- Keep missing, null, false, zero, unknown, stale and unavailable distinctions required by this block.
- Development checks are evidence, not extra Job or agent-ACK execution gates.

## Detailed implementation work

1. Capture caller-specific SSH info/discovery results and optional/not-enabled/unavailable distinctions from ssh_info.py.
2. Keep Admin-only enable/disable mutations on the current protected host helper; ordinary MCP discovery remains read-only.
3. Preserve UID account ownership, group/ACL grants, storage/dependency paths and disable-before-cleanup ordering.
4. Ensure a Rust discovery consumer validates the same installed identity and does not infer credentials or another machine's path.
5. Keep same-host workflows on direct files; no new SSH dependency for local operations.
6. Test revocation/uninstall interactions with Sharing and unknown external host state, using isolated account/helper fixtures.
7. Verify Dashboard relay Origin/CSRF and trusted peer behavior before wiring discovery into the Rust system group.
8. If the helper is ever rewritten later, require separate privilege/path/cleanup review and keep its wire contract unchanged first.

## Acceptance matrix

| Scenario | Required observable result |
|---|---|
| Non-Admin attempts to enable an account | Reject before host mutation. |
| Existing unrelated host account has a matching name | Never adopt it. |
| Caller has no SSH grant | Report disabled/unavailable without inventing credentials. |
| Disable interrupted during cleanup | Personal UID is blocked before remote resource removal. |
| Same-host caller discovers a connection | Local access needs no SSH setup. |
| Other installation or user remains active | Preserve unrelated accounts and grants. |

### Existing regression sources

- [tests/deploy/test_ssh_host.py](../../../tests/deploy/test_ssh_host.py)
- [tests/dashboard/test_ssh_access.py](../../../tests/dashboard/test_ssh_access.py)
- [tests/ops/test_ssh_info.py](../../../tests/ops/test_ssh_info.py)

Existing Python-internal tests need boundary adaptation when their implementation moves. Passing the old implementation alone does not establish Rust parity. Add state/trace and crash cases from this matrix; keep actual external acceptance separately identified.

## State, cutover and rollback

No account or key migration is required. Keep the current helper and socket; the Rust reader can be rolled back without touching user permissions.

## Main risk and design review

Rust memory safety does not make an overprivileged account/helper policy correct. The privilege boundary must survive unchanged.

## Contracts and documentation to review

- [docs/SSH.md](../../../docs/SSH.md)

Change rule: Review host helper, private Admin CSRF routes, Sharing revocation, readonly MCP, installation/update/uninstall and Loom Use together.

Before implementation, apply the cross-block [compatibility contract](../COMPATIBILITY.md), [sequence and ownership rules](../README.md), and [whole-tree review findings](../REVIEW.md). Update the implementation source, public schema/guide, consumers and installation packaging together when an accepted contract changes.

## Exit criteria

- The implemented responsibilities and deliberately retained Python/external boundaries are explicit.
- Every acceptance row has a reproducible test or is named as an unverified external acceptance boundary.
- Affected consumers pass against the selected Rust implementation, including its error and restart paths.
- Preservation and rollback checks use the same state format/identities; no second writer or duplicated external action is introduced.
- Feature mappings and source-qualified verification evidence match the exact candidate build.
- No production activation, user-thread inference, credential rotation or research execution is inferred from source/test completion.
