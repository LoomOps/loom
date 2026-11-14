# Rust compatibility and preservation contract

This is a cross-block implementation requirement, not a new Job admission gate.
Public behavior remains authoritative over preferred Rust library defaults.

## IDs and persisted representations

Keep Job/Attempt/ticket/entity/revision/storage/installation/user/credential IDs
unchanged. Use separate Rust types to prevent mixing them; do not impose a new
UUID-only parser on existing string identifiers. Logical workflow roots,
scheduler node Jobs, internal steps and execution Attempts are different records.

Persisted timestamps are Unix seconds with existing precision/meaning. Elapsed
logical Job time, unioned active execution intervals and receipt timestamps must
remain distinct. Recovery uses persisted wall-clock deadlines; elapsed process
waits use monotonic time. An async timeout never proves external resource return.

Preserve null versus omission, empty versus unrecorded, zero versus N/A, booleans
versus integers, integer precision, Unicode casefold/normalization and stable
ordering. Newly submitted requests remain strictly validated. Historical and
sealed JSON retains unknown accepted fields instead of being destructively
round-tripped through a smaller Rust struct.

## Canonical JSON is not one algorithm

Current source uses multiple encodings for different identities. Inventory the
actual call site before selecting a Rust serializer:

| Namespace | Current representation that must be captured |
|---|---|
| Ops dump/request comparisons | `json.dumps(sort_keys=True, allow_nan=False)` with Python defaults |
| Executor request fingerprint | sorted JSON with existing whitespace/escaping |
| Executor launch fingerprint | JSON encoding of the exact Docker argv |
| Runtime digest | sorted compact JSON, finite values, default ASCII escaping |
| Profile/source publication | existing pretty/compact/source-byte rules per registration path |
| Historical encoded snapshots | sorted finite JSON with `ensure_ascii=False` |
| Guide/projection/source manifests | exact source-specific serialization and ordering |

Python float exponents, large integers, negative zero, Unicode escaping, key order
and whitespace affect hashes. Rust semantic JSON equality is insufficient for a
stored digest. Keep legacy namespaces readable and verify old known-byte fixtures
before writing a new representation. Introduce a versioned digest only through a
separately designed migration; never silently recompute all stored pins.

## Public API and client boundary

Preserve six MCP groups and their advertised scope-filtered action schemas;
retain JSON/Streamable HTTP/SSE and notification semantics accepted by clients.
HTTP and MCP invoke the same domain operation. Existing public status and legacy
state aliases remain distinct from scheduling, recovery and resource ownership.

Match input/default/error behavior, stable submit-key semantics and bounded
responses. Keep compact summary fields and on-demand exact inventories so large
Profile/Runtime catalogs fit the pinned client. Public diagnostics contain only
validated opaque locators and product-defined safe messages.

Keep Dashboard route allowlists, trusted assertions, Origin/CSRF, browser session
invalidation and opaque iframe isolation. An HTTP framework or Rust SDK does not
supply those application decisions automatically.

## Transactions, effects and authority

SQLite stays the persisted authority. Preserve schema/user versions, constraints,
indexes, transaction/locking semantics, update fences and actual backup APIs.
Audit the effective SQLite pragmas per existing database; do not apply one blanket
WAL/synchronous policy without documenting its compatibility/durability impact.

Each state transition has one owner. A shadow implementation never launches,
cancels, indexes, registers or grants anything. When a mutation includes a file
publication or external call, record its intent/evidence and reconcile the same
identity after interruption. Lost replies are uncertain outcomes, not proof of
rejection. Stable keys permit exact replay only where the contract supports it.

Preserve worker.lock, schema locks, remote fencing, current Job/Attempt checks,
container labels/tickets, return receipts, result outbox, finalizer receipts,
callback IDs, reservation deadlines and operator pause keys. Existing resource
return evidence takes precedence over a future completing or being dropped.

## Filesystem and host contracts

Use configured roots and verified persistent store markers. Do not hardcode a
particular installation's `/dependencies`, data or component directory. Preserve
UID/GID, modes, ACL/traverse requirements, mount dependencies and protected socket
credentials. Keep canonical relative locator and symlink/path escape checks.

Atomic replacement must preserve intended service ownership and private modes,
flush content and retain required directory durability. Do not reproduce a
root-owned 0600 management journal unreadable by its service account. Do not
weaken sockets or add them to user Job containers to work around migration errors.

Keep typed locators and byte hashes distinct from scientific metadata validity.
No language port authorizes model loading, GPU work, dataset repair or adoption
of an unregistered dependency directory.

## Cutover and rollback

1. Build immutable source-qualified artifacts and compare contracts in isolation.
2. Wait for all affected executions, callbacks and Runtime validation owners to
   return; honor the official update/installation locks.
3. Fence all writers affected by shared helpers and take consistent DB/file/config
   snapshots without copying another installation's identities.
4. Switch one authoritative implementation with matching helper/protocol versions.
5. Verify actual native entry, storage parity, client/API behavior, retained state
   and an explicitly requested isolated/operational acceptance scope.
6. Retain previous executable/image/source and a concrete matching rollback plan.
   An unresolved owner stays fenced across rollback.

Planning/source tests do not authorize any of these operational mutations. A
rebuild preserves state rather than creating a fresh installation. Cumulative
updates collect every required migration when releases are skipped.

## Evidence levels

- Structural inventory/AST/schema/link checks establish review coverage.
- Pure Rust and differential contract tests establish the checked behavior only.
- SQLite/filesystem/process crash tests establish the tested recovery windows.
- Firefox establishes the rendered consumer paths and tested sizes/themes.
- CPU Docker acceptance establishes the tested container/return/storage path.
- GPU/driver, native client identity, Tailscale approval and actual power loss
  require their own appropriately isolated or explicitly authorized acceptance.

Record skipped, missing, failed and stale evidence separately. Do not add a new
platform feature-audit or agent ACK prerequisite to user Job execution.
