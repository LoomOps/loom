# Whole-tree review and findings

Baseline: alpha.60, commit `4d93ab9bdcb5750f3d0be161925e834984492f89`.
This review prepares a Rust variant; it is not an operational incident diagnosis
or a claim that Rust code already exists in Loom.

## Review coverage and method

The inventory reads every baseline tracked file and records its SHA-256, language,
size, line count, feature ownership and proposed disposition. It includes source,
all tests/instructions, generated frontend and build/service configuration rather
than limiting the review to the feature verification blocks.

The structural pass parses all 169 Python modules and seven JSON documents,
checks repository Markdown links, and records source declarations/imports and
persistence boundaries. Semantic review is organized by all 17 feature domains,
with focused inspection of execution/return/recovery, hashing/publication,
authorization, projection, maintenance/update and ownership boundaries. Frontend
and external integration files are retained and reviewed as consumers/packaging
boundaries, not translated line-for-line. The manifest explicitly distinguishes
structural coverage from the depth of semantic review; passing syntax or an
existing feature block is not equivalent to proving a Rust port correct.

The baseline contains 297 tracked files / 46,423 lines, including 65 Markdown
files and 36 cross-cutting files not assigned directly by the feature catalog's
source/test/contract lists. Those files are included by the additional ledger;
this is a planning coverage extension, not a claim that all unlisted documents
are broken. New plan documents are outside that frozen baseline inventory.

## Findings and required decisions

| ID | Finding from current source/instructions | Consequence and planned action |
|---|---|---|
| R01 | `ops/ops.py` combines HTTP/MCP routing, schema initialization, submit, worker, return/finish, results and CPU execution. Feature ownership already warns about this cross-domain file. | Extract explicit internal Rust modules and transition ownership; a file-by-file translation would preserve coupling. See API/execution/queue/recovery plans. |
| R02 | JSON identity encodings differ between `ops.dump`, `executor/server.py`, `executor/runtime_store.py`, Profile publication and `history_store.encoded`. | Capture byte-level fixtures per namespace. Do not replace them all with a default Rust serializer. |
| R03 | Job/public status, compatibility state, scheduling, recovery, logical roots/nodes, Steps and Attempts are distinct. | Use separate types/read models. Preserve underlying executions and UI timelines rather than flattening them into one status/count. |
| R04 | Worker/Executor correctness depends on ticket/request/launch fingerprints, returned receipts, fsync, finalizer receipts and current Attempt fences. | Port the resource/transaction protocol, not only async process launching. Preserve unknown ownership on every failed observation. |
| R05 | Dashboard contains substantial existing UI/generated-template/parent-iframe behavior and separate SSO/CSRF/trusted-relay logic. | Retain web source and its Python integration; require unchanged browser consumer acceptance against Rust responses. |
| R06 | `deploy/PLATFORM.md` manually enumerates an older subset of MCP actions, while `mcp_groups.py` advertises current workflow/curation/runtime/dependency actions. The root README's final Runtimes list also omits the new Dependencies tab. | Treat the executable registry and current feature/guide contracts as authority. Correct/generate static enumerations during contract documentation work; do not use stale overview lists as a Rust API specification. |
| R07 | `docs/features/catalog.md` lists `test_job_history.py` twice. Several overview files summarize an installation rather than listing every mandatory installer exit criterion. | Remove duplicate references when updating those specifications; retain root INSTALL/numbered steps as the complete installation contract. No bypass path should be created from an abbreviated overview. |
| R08 | Much of the current suite imports Python functions or patches Python internals. | Keep independent Python clients/harnesses, but adapt moved behavior to real Rust service/process/DB fault boundaries. Existing counts alone cannot validate a new implementation. |
| R09 | Runtime installation and all-instance helper replacement have active execution/validation locks and separate metadata ownership. | Keep Python recipe/build tooling and the lock contract initially. Transfer a metadata writer only as one deliberate registrar change, with compatible read/hash semantics. |
| R10 | Dependencies is a representative catalog derived from granted Runtime manifests; it is not a scan of every installed directory or proof of actual scientific use. | Preserve this exact evidence boundary. A general reconciler or independent installation database is a separate future feature, not silently bundled into the rewrite. |
| R11 | Historical originals and their current availability/presentation overlays coexist; large files can remain present_unverified. | Preserve originals, typed locators, thresholds and differing evidence claims. A Rust migration does not repair or promote records automatically. |
| R12 | Managed-resource files have explicit no-symlink checks, ownership selection, private modes, intent journaling and atomic replacement. | Retain these protections; language change must not regress service-account readability or external-write reconciliation. |
| R13 | Snapshots/installer HOST_FILES/source manifests enumerate packaged files and helper versions. | Extend all packaging paths for native binaries and provenance; merely adding Cargo source cannot make an installed service use it. |
| R14 | Some large dependencies belong to web/authentication, validation or scientific Runtime images rather than core scheduling. | Retain them behind explicit boundaries. Do not import user scientific environments into the Rust platform or rewrite external packages. |

These are migration design findings. No production DB, user software, account,
permission, network resource or Job has been changed to demonstrate them.

## Instruction review

The review includes AGENTS.md, root/new-install/update guides, all feature specs,
server-owned Loom Use guides/Skill, host/network/SSH/diagnostics instructions,
platform overviews and testing documentation. Their constraints are carried into
the block plans:

- Root INSTALL and numbered steps govern new-machine success; updates use the
  existing cumulative update/rebuild/preservation contract.
- A server guide and live action schema are authoritative for clients; historical
  examples or static action lists cannot override them.
- No prescribed resident agent hierarchy or extra agent completion/ACK gate is
  added to Loom Job execution.
- One requested research outcome remains one logical Job. Parallel/vectorized
  work can be internal; root grouping does not fabricate execution history.
- Profile/Runtime/Tool pins and user-owned source/configuration survive platform
  upgrades; no silent rewrite or new permission grant.
- Native Tailscale identity/Sharing/Gateway and protected SSH boundaries remain;
  local health or a token-only shortcut does not establish complete installation.
- Configured storage/dependency roots, marker identities and filesystem ownership
  must agree across effective API/worker/Executor/Explorer access.
- Private host instructions and operational evidence are never release source.
- Feature checks/tests aid development and do not become execution gates.

## Review limitations and implementation follow-up

This is source/contract planning, not a performance benchmark, formal proof or
new host/GPU/Tailscale acceptance run. No throughput gain or implementation date
is inferred from language choice. Large external dependencies are classified for
retention rather than audited as if their full upstream source lived here.

Before porting a block, capture its exact behavioral fixtures and resolve the
findings tied to that boundary. Record any new source/contract change against a
new baseline hash rather than treating this inventory as permanent evidence.
The plans' acceptance matrices are proposed tests; they are not reported passes.
