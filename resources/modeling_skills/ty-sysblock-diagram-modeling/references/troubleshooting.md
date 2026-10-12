# Sysblock Troubleshooting Index

Use the first matching symptom. Collect the stated evidence, take one action, then return to the authoritative rule instead of repeating a broad diagnostic loop.

| Symptom | First evidence | First action | Authority |
|---|---|---|---|
| API name/signature unknown | exact requested API and installed version | run contract resolver, then one exact documentation lookup | `runtime-contracts.md` |
| API returned false/empty | direct return, exception, `GetLastErrors()` | stop dependent calls and fix the first error | `runtime-contracts.md` |
| Same-name model/file conflict | project target, loaded class, `GetDirectory()` file | resolve ownership; touch only task-owned assets | `runtime-contracts.md` |
| `SaveModelAs` rejects target | absolute current and target paths | use `SaveModel` for an existing confirmed target | `runtime-contracts.md` |
| Top-level load succeeds but internal fragments fail | load result, intended library, `check_model` result | ignore unrelated unqualified fragments only if the real model checks | `runtime-contracts.md` |
| Component add fails | full class path, model path, return/error | verify library/class and model ownership; do not guess variants | `block-reference.md` |
| Connection fails | source/target full ports and refreshed port list | configure variable ports first; retry the one connection | `modeling-workflow.md` |
| Route has unexpected endpoint duplication | requested grip points and saved `Points` | remove endpoints from grip points | `layout-workflow.md` |
| Route crosses a block/text region | final readback points and no-crossing regions | adjust placement, reroute once, then use explicit bends if needed | `layout-workflow.md` |
| Feedback leaves interface envelope | declared feedback path and route bounds | reserve/move the feedback return region inside boundaries | `layout-workflow.md` |
| State transition cannot be straight | source/target rectangles and x/y overlap | translate state, then bounded scale/push before routing | `state-machine.md` |
| Repeated corner attempts do not work | geometry-adjustment record | stop routing attempts; fail `STATE_GEOMETRY_ADJUSTMENT_FAILED` or redesign hierarchy | `layout-workflow.md` |
| Chart label is misplaced | route shape, label field/value | relative offset only for two-point orthogonal routes; otherwise absolute midpoint coordinate | `state-machine.md` |
| Chart port unconnected | final Chart ports and parent-level connections | repair containing Sysblock topology and rerun final readback | `modeling-workflow.md` |
| Check passes but evidence audit fails | audit report failure codes | fix the first missing/stale/layout/test section | `modeling-workflow.md` |
| Simulation boundary appears one tick late | integer-tick table and boundary tests | distinguish scheduling semantics from model defect | `modeling-workflow.md` |
| Results cannot be read | simulation return, result location, requested variables | resolve result handling; do not substitute screenshots | `modeling-workflow.md` |
| Audit-only target hash changed | before/after SHA-256 | report writeback failure; do not claim read-only audit | `runtime-contracts.md` |

When a symptom is absent, do not load the entire troubleshooting history. Start from the failing validation and one associated authority.
