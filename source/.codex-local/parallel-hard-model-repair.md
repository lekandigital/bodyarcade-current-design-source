You are Codex 5.5 Agent Mode with Max Reasoning.

This is a parallel PosePuppet hard-model repair run. Another Codex task may still be running in `/home/o/Dev/posepuppet`. Do not touch, edit, stage, commit, reset, or clean that checkout.

Use this separate worktree only:

```sh
cd /home/o/Dev/posepuppet-hard-model-fix
```

This worktree was created from:

```txt
5f3286c feat: complete generated avatar rig readiness pass
```

This task is not a report pass. This is a persistent hard-model repair pass focused on models that converted or browser-smoked but failed real visual QA.

## Why this exists

The current visual QA continuation run discovered that some avatars passed conversion/validation/browser smoke but failed actual visual review. Smoke passing is not enough. This run should aggressively redo, repair, and revalidate the problematic models in isolation so it can run in parallel without corrupting the main active worktree.

Known visual/rig failures from the other run:

```txt
amazing-spider-man-2:
  browser smoke passed earlier, but visual/contact sheets are effectively empty/invisible after normalization/orientation attempts.

terminator-t-800:
  browser smoke passed earlier, but visual/contact sheets are effectively empty/invisible after normalization.

spider-man-no-way-home:
  browser smoke passed earlier, but visual QA showed orientation/root problems; body appears horizontal/prone or disappears after attempted Z-dominant correction.

spider-man-playstation:
  accepted in 5f3286c, but visual QA showed grounding/scale issues; later repair attempt overcorrected into close-up/occluded torso. Needs a more robust scale/grounding/camera/root fix.

jack-sparrow:
  accepted in 5f3286c, but visual QA showed huge/slow load and then duplicate figures side-by-side after normalization. Needs duplicate mesh/armature/scene cleanup investigation.

elsa:
  converted/validated in 5f3286c but failed browser smoke. Must investigate actual browser/load blocker and attempt fixes.

buzz-lightyear:
  converted as reference/deferred with weak/manual mapping. Must investigate beyond bone names.

teal-v2:
  converted as reference/deferred with weak/manual mapping/cleanup needs. Must investigate beyond bone names.
```

If the current running task produced evidence, it may be copied here:

```txt
/home/o/posepuppet-hard-fix-evidence/<slug>/
```

Use it as diagnostic input only. Do not depend on it as final evidence. Generate your own final evidence in this parallel worktree.

## Isolation rules

Do not use `/home/o/Dev/posepuppet` as a writable checkout.

Do not overwrite the other run’s `model-working/`.

Use separate ignored working locations:

```txt
/home/o/posepuppet-working-hard-fix/
model-working-hard-fix/
public/avatars/generated/
model-audits/rig-prep/hard-model-repair/
```

If existing tools assume `/home/o/posepuppet-working/generated-vrms`, either add a safe CLI/env override or copy needed inputs into the parallel working location. Do not mutate the original source assets.

Do not push directly to `main`. Commit to the current parallel branch only. Final response should say the branch name and commit hash. Merging can happen later after review.

## Absolute safety rules

Never overwrite source assets.

Never destructively edit:

```txt
ModelsForAnimation/
models_for_animation/
source zips
source .blend/.fbx/.glb/.gltf files
source textures
existing tracked runtime avatars
```

Do not commit:

```txt
*.vrm
*.blend
*.fbx
*.glb
*.gltf
*.zip
*.png
*.jpg
*.jpeg
*.webp
*.tga
*.bmp
*.tif
*.tiff
*.exr
model-working/
model-working-hard-fix/
public/avatars/generated/
source assets
textures
screenshots
contact sheets
large generated binaries
prompt files
```

Reports under `model-audits/**/*.md` and `model-audits/**/*.json` may be committed. Safe tooling/code/tests may be committed.

Do not public-promote any avatar. Generated candidates must remain query-param-only, experimental, and `enabledInUi: false`.

Do not mark `works_well` unless conversion, structural validation, browser smoke, pose-suite screenshots, and visual review strongly support it.

## Main objective

For each hard model, make persistent targeted repair attempts to produce the strongest safe generated candidate possible.

Target models:

```txt
amazing-spider-man-2
terminator-t-800
spider-man-no-way-home
spider-man-playstation
jack-sparrow
elsa
buzz-lightyear
teal-v2
```

Optional if time remains:

```txt
shrek
iron-man
```

Only touch Shrek/Iron Man if you need to compare normalization/material fixes or confirm that their repair class is solved.

## Baseline checkpoint

Start by running:

```sh
cd /home/o/Dev/posepuppet-hard-model-fix
source .venv/bin/activate 2>/dev/null || true
source ~/.nvm/nvm.sh
nvm use 22

pwd
git status --short
git branch --show-current
git rev-parse --short HEAD
git log --oneline -8
git remote -v

python3 --version
node --version
npm --version
which blender || true
~/.local/bin/blender --version || true

npm run build
npx playwright test tests/generated-avatar-load.spec.ts --reporter=line
python3 tools/audit_model.py --self-test
python3 tools/validate_rig_readiness.py model-audits || true
```

Write:

```txt
model-audits/rig-prep/hard-model-repair/baseline.md
model-audits/rig-prep/hard-model-repair/baseline.json
```

## Required tooling

Inspect current tools before changing them:

```txt
tools/convert_avatar_to_vrm.py
tools/validate_vrm_candidate.py
tools/rig_attempt_model.py
tools/pose_suite_validate_model.py
tools/generate_avatar_contact_sheet.py
tests/generated-avatar-load.spec.ts
src/main.ts
src/rig/vrm.ts
src/rig/generatedAvatarRegistry.ts
```

If visual capture tooling is absent in this worktree, add a narrow test-only visual QA harness. It may expose loaded generated avatar diagnostics and pose controls only behind smoke/test query params.

Allowed test-only behavior:

```txt
?generatedAvatar=<slug>&smoke=avatar-visual-review
```

or equivalent.

Do not alter normal public UI behavior.

The visual harness must generate:

```txt
model-working-hard-fix/<slug>/visual-review/browser-load.png
model-working-hard-fix/<slug>/visual-review/neutral.png
model-working-hard-fix/<slug>/visual-review/pose-suite/*.png
model-working-hard-fix/<slug>/visual-review/contact-sheet.png
model-working-hard-fix/<slug>/visual-review/capture-results.json
```

Images are ignored and not committed.

Commit only reports/manifests.

## Persistent attempt loop

For every target model, use this loop:

```txt
1. Create attempt folder.
2. Identify the exact observed failure.
3. Make one targeted repair.
4. Export/generate candidate if possible.
5. Run structural validation.
6. Run browser smoke if structurally valid enough.
7. Generate screenshots/contact sheet.
8. Use visual reasoning to inspect the sheet.
9. Run/generate pose-suite evidence.
10. Classify the attempt.
11. If failed, choose the next repair based on evidence.
```

Attempt folders:

```txt
model-working-hard-fix/<slug>/attempts/
  attempt-001-current-baseline/
  attempt-002-scale-ground-camera/
  attempt-003-root-orientation/
  attempt-004-material-visibility/
  attempt-005-bone-map-recovery/
  attempt-006-wrist-palm-feet/
  attempt-007-duplicate-mesh-armature-cleanup/
  attempt-008-source-level-reexport/
  attempt-009-final-best/
```

Only create folders that are actually used.

Each attempt must write:

```txt
manifest.json
notes.md
commands.log
validation.json
browser-smoke.json
visual-review.json
pose-suite-validation.json
```

## Attempt budget

Be very persistent, but do not loop forever.

For each model, try up to 8 serious repair attempts, plus a final-best consolidation if one attempt is usable.

Do not defer a model until all relevant repair paths have been attempted or the source clearly requires manual artist work.

Minimum attempts by failure type:

### Invisible/empty contact sheet

For:

```txt
amazing-spider-man-2
terminator-t-800
```

Try:

```txt
camera/framing diagnostics
bounding-box diagnostics
scale-down-only normalization
grounding/centering without upscaling
material lighting fix
texture/material survival check
mesh visibility / hidden object check
skinned mesh world matrix update
source-level re-export if safe
browser screenshot rerun
Blender/offscreen render comparison
```

If browser render is invisible but Blender render is visible, classify as browser/material/runtime display blocker. If both are invisible, classify as source/export geometry blocker.

### Orientation/root failure

For:

```txt
spider-man-no-way-home
```

Try:

```txt
root axis diagnostics
Z-dominant vs Y-dominant bounds
+90 and -90 root rotation attempts
apply rotation before grounding
recompute bounds after skeleton update
source-level rest-pose correction if safe
camera-only diagnostic to separate orientation from visibility
```

Do not accept it unless final screenshot shows a visible upright readable avatar.

### Scale/grounding/camera failure

For:

```txt
spider-man-playstation
```

Try:

```txt
no-upscale normalization
scale-down-only normalization
camera framing without model scaling
grounding using skinned bounds not raw root bounds
root Y offset correction
stage-floor offset correction
pose visibility check
```

Do not accept a close-up torso as active. It must show a readable full or near-full body.

### Duplicate figure failure

For:

```txt
jack-sparrow
```

Try:

```txt
scene graph inspection
armature count
skinned mesh count
duplicate mesh/collection detection
multiple avatar root detection
visibility flags
mesh names and hierarchy
safe duplicate suppression only if objectively duplicated
single-armature export attempt
source-level cleanup copy if safe
material/texture survival check
large-file timeout handling
```

Do not delete anything from original source. Operate on working copies only. If duplicate removal is ambiguous, preserve as reference and mark manual cleanup needed.

### Browser-smoke failure

For:

```txt
elsa
```

Try:

```txt
exact browser console error
network/path status
VRM file existence and size
VRM metadata/extension validation
loader exception stack
texture path issue
material issue
avatar registry profile issue
fallback generated path issue
safe re-export/reconvert
re-smoke after each plausible fix
```

Do not leave Elsa deferred without at least one real browser-load fix attempt and a clear blocker.

### Weak/manual mapping

For:

```txt
buzz-lightyear
teal-v2
```

Do not rely on bone names alone.

Infer bone map from:

```txt
bone hierarchy
bone positions
deform vertex groups
skin weights
left/right symmetry
mesh names
armature names
relative body location
existing audits
bone-tree.txt
visual screenshots
```

Try:

```txt
manual bone-map recovery
root/hips/chest/head inference
upper/lower arm inference
hand/wrist inference
upper/lower leg inference
foot/ankle inference
scale/orientation correction
post-VRM validation
pose-suite/contact-sheet evidence
browser smoke if structurally valid
```

If still not usable, write exactly why manual artist work is required.

## Acceptance gates

An `accepted_active_candidate` must have:

```txt
conversion pass or acceptable partial
post-VRM validation pass or acceptable partial
browser smoke pass
visible screenshot/contact sheet
pose-suite pass or acceptable partial
visual review pass / acceptable / weird-but-usable
no public UI promotion
no generated binary committed
```

If any of these fail, do not call it active.

Final per-model outcome must be exactly one of:

```txt
accepted_active_candidate
accepted_reference
deferred_with_blocker
rejected_all_attempts
```

Use truthful labels:

```txt
visual_pass
visual_acceptable
visual_weird_but_usable
visual_partial
visual_reject
browser_smoke_fail
manual_mapping_needed
cleanup_needed
material_visibility_blocker
orientation_blocker
duplicate_mesh_blocker
source_reexport_needed
manual_artist_work_needed
```

## Reports to write

Per model:

```txt
model-audits/<slug>/hard-model-repair-plan.md
model-audits/<slug>/hard-model-repair-plan.json
model-audits/<slug>/hard-model-repair-attempts.md
model-audits/<slug>/hard-model-repair-attempts.json
model-audits/<slug>/visual-rig-review.md
model-audits/<slug>/visual-rig-review.json
model-audits/<slug>/pose-suite-validation.md
model-audits/<slug>/pose-suite-validation.json
model-audits/<slug>/runtime-capability-profile.md
model-audits/<slug>/runtime-capability-profile.json
model-audits/<slug>/manual-fix-checklist.md
model-audits/<slug>/manual-fix-checklist.json
```

Aggregate:

```txt
model-audits/rig-prep/hard-model-repair/summary.md
model-audits/rig-prep/hard-model-repair/summary.json
model-audits/rig-prep/hard-model-repair/active-candidate-decisions.md
model-audits/rig-prep/hard-model-repair/active-candidate-decisions.json
model-audits/rig-prep/hard-model-repair/manual-blockers.md
model-audits/rig-prep/hard-model-repair/manual-blockers.json
```

## Final validation

Run:

```sh
npm run build
npx playwright test tests/generated-avatar-load.spec.ts --reporter=line
python3 tools/audit_model.py --self-test
python3 tools/validate_rig_readiness.py model-audits || true
git diff --check
git diff --cached --check
git status --short
git ls-files --cached public/avatars/generated/
git diff --cached --name-only | grep -Ei '\.(vrm|blend|fbx|glb|gltf|zip|png|jpg|jpeg|webp|tga|bmp|tif|tiff|exr)$' || true
git diff --cached --name-only | grep -Ei '(^|/)model-working|(^|/)model-working-hard-fix|prompt|codex-goals|\.codex-local' || true
```

Do not commit forbidden files.

## Commit rules

Commit only safe code/text/report changes to the parallel branch.

Suggested commit message:

```txt
fix: repair hard generated avatar visual QA blockers
```

If most models remain blocked but reports are valuable:

```txt
docs: document hard generated avatar visual repair blockers
```

Do not push to main. Push the parallel branch only if all safe:

```sh
git push origin HEAD
```

## Final response

Report:

```txt
branch name
commit hash
whether pushed
models attempted
attempt count per model
which models became active candidates
which stayed reference
which were downgraded/rejected
exact blocker per failed model
screenshots/contact-sheet paths
VRM candidate paths
build result
smoke result
validation result
forbidden-file scan result
whether public UI stayed unchanged
whether any generated binaries/images/source assets/prompt files were staged
recommended merge/cherry-pick strategy
```

Be extremely persistent. The goal is to make the models usable, not merely to explain that they failed. But do not fake readiness.
