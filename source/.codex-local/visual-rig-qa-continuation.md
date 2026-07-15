You are Codex 5.5 Agent Mode running with Max Reasoning inside the PosePuppet repository.

You are using Codex’s Goal feature. This is a long, multi-hour continuation task. Do not treat this as a quick report-generation pass. Do not stop after 25–30 minutes unless the completion checklist at the end is actually satisfied.

Canonical working machine:

```sh
ssh -i ~/.ssh/pinn_rtx3090 o@192.168.86.152
cd /home/o/Dev/posepuppet
```

Ubuntu is canonical. Do not run Blender conversion, VRM inspection, generated-avatar browser validation, screenshot/contact-sheet generation, or model visual QA on the Mac checkout.

## Immediate context

A previous Codex run completed and pushed:

```txt
5f3286c feat: complete generated avatar rig readiness pass
```

That run was useful, but it did **not** fully complete the original prompt.

It completed:

```txt
repo checkpoint
Batch B preservation/push
baseline validation
rig-readiness tooling
all-20-model classification
conversion attempts for spider-man-playstation, jack-sparrow, elsa, buzz-lightyear, teal-v2
browser-smoke acceptance for spider-man-playstation and jack-sparrow
reference/deferred classification for elsa, buzz-lightyear, teal-v2
expanded generated-avatar smoke suite: 12 passed
safe commit/push
```

It did **not** complete:

```txt
real screenshot/contact-sheet visual review
vision-based rig-quality judgment
full pose-suite deformation review
persistent multi-attempt rig-fix loops for failed/deferred models
deep wrist/palm/foot/face-touch repair attempts
hand-only preview for rigged-hand
creature/static-preview VRM/browser attempts
proof that the 10 browser-smoke-passing avatars actually look good in motion
```

Your job is to continue from `5f3286c` and complete the unfinished parts of the original prompt.

This is now a **visual rig-quality, persistent repair, pose-suite, screenshot/vision QA, and candidate-upgrade pass**.

Do not redo the whole previous report scaffolding unless necessary. Build on it.

## Current known state

Active query-param-only browser-smoke-passing generated candidates after `5f3286c`:

```txt
woody
darth-vader
fortnite-batman
iron-man
shrek
amazing-spider-man-2
terminator-t-800
spider-man-no-way-home
spider-man-playstation
jack-sparrow
```

Reference/deferred VRM candidates:

```txt
elsa
buzz-lightyear
teal-v2
```

Special categories:

```txt
rigged-hand: hand_only, not full avatar
baby-yoda: creature_profile_needed + static_preview_only
godzilla: creature_profile_needed
grogu: creature_profile_needed
king-kong: creature_profile_needed
olaf: creature_profile_needed
xenomorph: creature_profile_needed
```

Existing ignored generated VRM storage:

```txt
/home/o/posepuppet-working/generated-vrms/
```

Existing ignored public symlink/copy location:

```txt
/home/o/Dev/posepuppet/public/avatars/generated/
```

Reports and tooling already exist under:

```txt
model-audits/
model-audits/rig-prep/
tools/
```

## Core objective

Complete the missing part of the original prompt:

```txt
For every model that is active, partial, reference, deferred, hand-only, or creature/custom-profile:
  generate actual pose/screenshot/contact-sheet evidence where feasible
  use visual reasoning to judge rig quality
  make persistent targeted rig-fix attempts when visual/pose/browser evidence fails
  preserve failed attempts
  accept only candidates that are actually visually acceptable
  update reports honestly
```

The goal is not merely to classify models. The goal is to actively try to make each model as usable as possible for PosePuppet’s future website/game use.

Future target features:

```txt
better avatar rigging
expressive body movement
arms and wrists
hands and palms
fingers where possible
feet and ankles
leaning and turning
walking proxy
simple flying proxy
rowing proxy
hand-to-face / face-touch proxy
gesture-to-intent game controls
hand-only mode for rigged-hand
creature/custom-profile support
truthful avatar compatibility labels
```

Do not implement the final public gameplay system unless a small test-only harness is necessary for visual validation.

## Non-negotiable instruction: do not finish early

Do not conclude with “visual_review: not_available” for all models if screenshots/contact sheets can be generated.

Do not stop after generating reports.

Do not stop after browser-smoke tests.

Do not stop after one failed conversion or one failed visual attempt.

Do not mark the task complete until you have done the following:

```txt
1. Generated visual evidence for the 10 active smoke-passing candidates.
2. Used image/vision reasoning to inspect that evidence.
3. Produced model-specific visual-rig-review reports.
4. Run or generated pose-suite evidence for humanoid, hand-only, and creature categories where feasible.
5. Made targeted repair attempts for models that fail visual/pose/browser checks.
6. Re-tested repaired attempts.
7. Preserved rejected attempts with useful manifests.
8. Updated active/reference/deferred classifications.
9. Re-ran build, Playwright smoke, validation, registry invariant checks, and forbidden-file scans.
10. Committed and pushed only safe code/text/report changes.
```

If you cannot complete a phase because a tool is missing, create the missing tool if feasible. If not feasible, produce a blocker report explaining the exact missing technical capability and what command or tool would be needed.

## Strict safety rules

Never overwrite original downloaded assets.

Never destructively edit:

```txt
ModelsForAnimation/
models_for_animation/
source zips
source .blend files
source .fbx files
source .glb files
source .gltf files
source textures
Woody original source files
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
public/avatars/generated/
source assets
textures
screenshots
contact sheets
large generated binaries
```

Reports under `model-audits/**/*.md` and `model-audits/**/*.json` may be committed.

Code and tests may be committed if safe.

Do not public-promote any avatar in this task.

Do not add generated avatars to the normal public avatar registry.

Generated avatars must remain:

```txt
query_param_only
experimental
enabledInUi: false
not_public_ui
```

Do not mark `works_well` unless visual QA, pose-suite QA, VRM validation, and browser smoke all support it.

## Phase 0 — Checkpoint and confirm continuation state

Run:

```sh
cd /home/o/Dev/posepuppet
source .venv/bin/activate 2>/dev/null || true
source ~/.nvm/nvm.sh
nvm use 22

pwd
git status --short
git branch --show-current
git log --oneline -12
git rev-parse --short HEAD
git remote -v
git fetch origin main
git rev-parse --short origin/main

python3 --version
node --version
npm --version
which blender || true
~/.local/bin/blender --version || true

git ls-files --cached public/avatars/generated/ || true
git diff --check
```

Confirm:

```txt
HEAD is at or after 5f3286c
worktree is clean or only contains known ignored generated artifacts
no generated VRMs/images/source assets are staged
public avatar cycling remains unchanged
```

Run baseline checks:

```sh
npm run build
npx playwright test tests/generated-avatar-load.spec.ts --reporter=line
python3 tools/audit_model.py --self-test
python3 tools/validate_rig_readiness.py model-audits
python3 tools/update_generated_avatar_registry.py --validate-only
```

Write/update:

```txt
model-audits/rig-prep/visual-continuation-baseline.md
model-audits/rig-prep/visual-continuation-baseline.json
```

## Phase 1 — Read current reports and identify missing evidence

Read:

```txt
model-audits/rig-prep/full-rig-readiness-summary.md
model-audits/rig-prep/full-rig-readiness-summary.json
model-audits/rig-prep/vrm-candidate-summary.md
model-audits/rig-prep/vrm-candidate-summary.json
model-audits/rig-prep/attempts-summary.md
model-audits/rig-prep/attempts-summary.json
model-audits/rig-prep/runtime-blockers-for-next-phase.md
model-audits/rig-prep/runtime-blockers-for-next-phase.json
model-audits/*/runtime-capability-profile.json
model-audits/*/attempts-summary.json
model-audits/*/post-vrm-rig-validation.json
model-audits/*/visual-rig-review.json
model-audits/*/pose-suite-validation.json
```

Create:

```txt
model-audits/rig-prep/visual-qa-work-queue.md
model-audits/rig-prep/visual-qa-work-queue.json
```

The queue must group models as:

```txt
A. active_smoke_passing_needs_visual_review
B. active_smoke_passing_needs_pose_suite
C. active_smoke_passing_needs_targeted_tuning
D. reference_vrm_needs_repair_attempt
E. hand_only_needs_hand_preview
F. creature_needs_static_or_custom_preview
G. blocked_until_manual_artist_work
```

Initial expected grouping:

```txt
A/B:
  woody
  darth-vader
  fortnite-batman
  iron-man
  shrek
  amazing-spider-man-2
  terminator-t-800
  spider-man-no-way-home
  spider-man-playstation
  jack-sparrow

D:
  elsa
  buzz-lightyear
  teal-v2

E:
  rigged-hand

F:
  baby-yoda
  godzilla
  grogu
  king-kong
  olaf
  xenomorph
```

For each model, record:

```json
{
  "slug": "",
  "current_status": "",
  "vrm_path": "",
  "browser_smoke": "",
  "post_vrm_validation": "",
  "visual_review": "",
  "pose_suite": "",
  "missing_evidence": [],
  "repair_attempts_required": [],
  "acceptance_gates_remaining": []
}
```

## Phase 2 — Upgrade visual tooling if needed

Inspect the current visual/contact-sheet tools:

```txt
tools/generate_avatar_contact_sheet.py
tools/pose_suite_validate_model.py
tools/pose_suite_validate_all.py
tools/rig_attempt_model.py
tools/rig_attempt_all_models.py
tools/validate_rig_readiness.py
```

If these tools only write placeholder manifests and do not actually create screenshots/contact sheets, upgrade them.

You must produce real visual evidence where feasible.

Acceptable visual evidence methods:

```txt
Blender offscreen renders from generated VRM or cleaned source
Playwright browser screenshots of generated avatar load
Three.js/VRM test harness screenshots
Pose-suite rendered contact sheets from Blender
Pose-suite rendered contact sheets from browser harness
```

Preferred minimum output for each active candidate:

```txt
model-working/<slug>/visual-review/browser-load.png
model-working/<slug>/visual-review/neutral.png
model-working/<slug>/visual-review/contact-sheet.png
model-working/<slug>/visual-review/pose-suite.png
```

Do not commit images.

Commit only reports/manifests:

```txt
model-audits/<slug>/visual-rig-review.md
model-audits/<slug>/visual-rig-review.json
model-audits/<slug>/pose-suite-validation.md
model-audits/<slug>/pose-suite-validation.json
```

If you implement browser screenshot support, keep it test-only. Do not alter public UI behavior.

Possible safe approaches:

```txt
1. Add a Playwright visual test/helper that opens:
   /?generatedAvatar=<slug>&smoke=avatar-load-only
   then captures screenshot after loaded.

2. Add a test-only query param:
   ?generatedAvatar=<slug>&smoke=avatar-visual-review
   only if necessary.

3. Add a dev/test-only pose suite helper that applies fixed synthetic rotations to VRM bones
   without changing normal runtime behavior.

4. Use Blender to render source/VRM pose poses if browser rig driving is too complex.
```

Do not implement large gameplay features here. This is visual QA and rig-readiness tooling.

## Phase 3 — Required pose-suite definitions

For humanoid models, pose-suite must attempt these poses if bones exist:

```txt
neutral
arms_out
arms_up
arms_forward
elbow_bend_left
elbow_bend_right
wrist_rotate_left
wrist_rotate_right
palm_forward
lean_left
lean_right
torso_turn_left
torso_turn_right
walking_stride_proxy
foot_lift_left
foot_lift_right
foot_rotate_left
foot_rotate_right
rowing_stroke_start
rowing_stroke_pull
flying_arms_out
hand_to_mouth_proxy
hand_to_cheek_proxy
finger_curl_left_if_fingers_exist
finger_curl_right_if_fingers_exist
```

For hand-only model:

```txt
neutral_hand
open_hand
fist_or_curl
point_index
thumb_motion_if_available
wrist_rotate
palm_forward
palm_down
```

For creatures:

```txt
neutral
head_turn_left
head_turn_right
torso_lean_left
torso_lean_right
front_limb_raise_if_available
jaw_open_if_available
tail_swing_if_available
root_motion_proxy
gesture_to_intent_pose
```

For each pose, report:

```json
{
  "pose_name": "",
  "attempted": true,
  "skipped_reason": "",
  "bones_driven": [],
  "missing_bones": [],
  "result": "pass | partial | fail | not_tested",
  "visual_review": "visual_pass | visual_acceptable | visual_weird_but_usable | visual_partial | visual_reject | visual_not_available",
  "observed_issues": [],
  "repair_recommendation": ""
}
```

## Phase 4 — Use visual reasoning, not just file existence

For each generated screenshot/contact sheet, inspect it using available image/vision reasoning.

Do not merely record “screenshot generated.”

You must answer these questions for each active or reference candidate:

```txt
Does the avatar load visibly?
Is the avatar upright?
Is scale reasonable?
Is it facing expected direction?
Are textures/materials present?
Are limbs attached?
Are hands attached?
Are feet attached?
Do shoulders collapse?
Do elbows bend plausibly?
Do wrists/palms point plausibly?
Do knees/feet behave plausibly?
Do fingers curl plausibly if tested?
Does hand-to-mouth or hand-to-cheek look plausible?
Do cape/coat/hair/accessories detach or explode?
Does walking proxy look readable?
Does flying arms-out look readable?
Does rowing proxy look readable?
Would this be acceptable as query-param experimental website avatar?
Would this be embarrassing or broken if shown publicly?
Should the attempt remain active, become reference-only, or be rejected?
```

Write:

```txt
model-audits/<slug>/visual-rig-review.md
model-audits/<slug>/visual-rig-review.json
```

Use labels:

```txt
visual_pass
visual_acceptable
visual_weird_but_usable
visual_partial
visual_reject
visual_not_available
```

If visual reasoning is available, `visual_not_available` is not acceptable for the 10 active smoke-passing candidates unless screenshot generation is impossible and the blocker is documented.

If Codex cannot view images for some technical reason, still generate the images and write:

```txt
requires_external_visual_review: true
```

but do not mark the model visually accepted.

## Phase 5 — Persistent rig-fix protocol

Be very persistent.

Do not stop at the first failed conversion, bad pose, broken screenshot, missing bone map, bad orientation, failed browser smoke, or weak automatic mapping.

For each model, make serious targeted repair attempts before giving up.

The goal is not merely to classify models. The goal is to actively try to make each model usable for PosePuppet as much as safely possible.

Persistence must be paired with strict acceptance gates. A model may only become or remain an active accepted candidate if the result is actually good enough.

### Per-model attempt budget

For each standard humanoid or humanoid-with-offsets model, attempt up to:

```txt
1 baseline/reference attempt check
1 scale/orientation/root correction attempt
1 manual/suggested bone-map recovery attempt
1 wrist/palm correction attempt if hands exist
1 foot/ankle correction attempt if feet exist
1 accessory/material cleanup attempt if visual QA shows issues
1 face-touch anchor/proxy attempt if head + hands make it plausible
1 optimization attempt if the model is web-heavy
1 final-best consolidation attempt
```

For hard models, be especially persistent:

```txt
jack-sparrow
elsa
buzz-lightyear
teal-v2
spider-man-playstation
```

Do not dismiss these after one weak mapping.

For cleanup/manual mapping models, infer rig structure from:

```txt
bone hierarchy
bone positions
deform vertex groups
skin weights
left/right symmetry
mesh names
armature naming
relative body location
existing audit files
bone-tree.txt
visual screenshots
```

Do not rely only on bone names.

### Attempt loop

For each model, use this loop:

```txt
1. Create an attempt folder.
2. Make one targeted rig/prep/conversion change.
3. Export or generate candidate if possible.
4. Validate structurally.
5. Run pose-suite tests if possible.
6. Generate screenshot/contact-sheet evidence.
7. Use visual reasoning.
8. Browser-smoke if the candidate is valid enough.
9. Classify the attempt.
10. If it failed, identify the most likely cause and try a different targeted fix.
```

Attempt folders:

```txt
model-working/<slug>/attempts/
  attempt-001-baseline-or-current/
  attempt-002-scale-orientation-root/
  attempt-003-manual-bone-map/
  attempt-004-wrist-palm/
  attempt-005-foot-ankle/
  attempt-006-accessory-material/
  attempt-007-face-touch-anchor/
  attempt-008-optimization/
  attempt-009-final-best/
```

Only create attempt folders that are actually used.

Each attempt must include:

```txt
model-working/<slug>/attempts/<attempt-id>/manifest.json
model-working/<slug>/attempts/<attempt-id>/notes.md
model-working/<slug>/attempts/<attempt-id>/logs/
model-working/<slug>/attempts/<attempt-id>/exports/
model-working/<slug>/attempts/<attempt-id>/snapshots/
```

Committed attempt report:

```txt
model-audits/<slug>/attempts-summary.md
model-audits/<slug>/attempts-summary.json
```

Each attempt report must include:

```txt
what was attempted
why it was attempted
what changed
what command ran
what file was produced
whether conversion passed
whether validation passed
whether pose-suite passed
whether visual review passed
whether browser smoke passed
why it was accepted or rejected
what next repair was attempted after failure
```

### Do not give up too early

For humanoids, before giving up, try at least:

```txt
baseline/current candidate review
scale/orientation/root fix if any visual issue exists
manual/suggested bone-map recovery if mapping is weak
post-VRM validation
pose/contact-sheet visual review
```

For models with hands, try at least:

```txt
wrist/palm detection
hand bone preservation check
palm-only classification
curl-preset feasibility if finger chains exist
```

For models with feet, try at least:

```txt
foot bone detection
ankle anchor detection
foot orientation check
walking/foot-lift proxy pose
```

For face-touch, try at least:

```txt
head target estimation
mouth/cheek/chin/forehead target estimation
hand-to-mouth or hand-to-cheek proxy pose
visual plausibility review
```

Do not mark face-touch as supported unless the visual result is plausible.

For creatures, before giving up, try at least:

```txt
static-preview feasibility
creature rig profile
head/torso/limb detection
gesture-to-intent mapping
VRM/static container if safe
browser-load test if converted
visual screenshot/contact-sheet if loaded
```

Do not force creatures into humanoid mode.

For rigged-hand, before giving up, try at least:

```txt
hand-only rig inspection
finger-chain detection
open/close/point pose test
hand-only control plan
static or VRM hand preview if safe
browser-load test if preview exists
visual screenshot/contact-sheet if loaded
```

Do not make rigged-hand a normal full-body avatar.

### Repair based on evidence

After every failed attempt, inspect the failure and choose the next fix based on evidence.

If browser smoke fails:

```txt
inspect console error
inspect VRM path
inspect file size
inspect generated registry entry
inspect VRM validation report
fix the actual load blocker and retry
```

If pose-suite shows exploded limbs:

```txt
inspect bone mapping
inspect rest pose
inspect scale
inspect parent/local axes
try manual bone-map or axis correction
```

If hands detach:

```txt
inspect leftHand/rightHand mapping
inspect wrist orientation
inspect hand vertex groups
try wrist/palm correction or downgrade to palm_only
```

If fingers look broken:

```txt
inspect finger chains
inspect VRM preservation
try curl presets only if visually acceptable
otherwise mark palm_only
```

If feet are wrong:

```txt
inspect foot bones
inspect ankle anchors
inspect lower leg to foot direction
try foot/ankle correction
otherwise mark ankle_anchor_only or feet_disabled
```

If face-touch looks bad:

```txt
inspect target placement
inspect arm reach
inspect hand orientation
try estimated targets or mark ik_required
do not mark supported
```

If textures/materials break:

```txt
inspect texture paths
inspect material count
inspect browser screenshot
try material/texture survival fix
otherwise preserve candidate but mark visual_partial or visual_reject
```

If accessories detach:

```txt
identify accessory
determine nearest safe parent bone
reparent only if obvious and non-destructive
otherwise mark manual accessory cleanup needed
```

### Persistence limits

Be persistent, but do not loop forever.

For each model, stop after:

```txt
all relevant repair paths have been tried
or 8 serious attempts have been made
or the model clearly requires manual artist work
or the source cannot be opened/imported safely
or continuing would risk corrupting source assets
```

When stopping, write a clear blocker report.

Do not treat stopping as failure if the model is truthfully classified and useful attempts are preserved.

Bad final report:

```txt
Model failed. Skipped.
```

Good final report:

```txt
Model failed after baseline, scale/root, manual bone-map, and visual repair attempts.
Best attempt saved here.
Failure reason: wrists detach during elbow bend because hand vertex groups are absent.
Recommended next step: manual weight paint or external re-rig.
Runtime classification: partial / palm_only unavailable / not public UI.
```

## Phase 6 — Active smoke-passing visual review and tuning

Process the 10 active candidates first.

```txt
woody
darth-vader
fortnite-batman
iron-man
shrek
amazing-spider-man-2
terminator-t-800
spider-man-no-way-home
spider-man-playstation
jack-sparrow
```

For each:

```txt
confirm VRM exists
confirm registry entry
confirm browser smoke passes
generate browser-load screenshot
generate pose-suite/contact-sheet
inspect visually
write visual-rig-review
write pose-suite-validation
update runtime-capability-profile
update hand/finger readiness
update feet/leg readiness
update face-touch readiness
update game-control readiness
```

If visual review reveals a serious issue:

```txt
do not leave the candidate as active without noting the issue
make targeted repair attempt if safe
re-export/revalidate/resmoke/review
if repair fails, downgrade to reference/deferred or keep active only with explicit visual_partial warning
```

For each active candidate, final status must be one of:

```txt
active_visual_accepted
active_visual_partial_with_warning
active_downgraded_to_reference
active_rejected
```

## Phase 7 — Repair/retry deferred humanoids

Models:

```txt
elsa
buzz-lightyear
teal-v2
```

For `elsa`:

```txt
It already converted/validated but failed browser smoke.
Do not simply leave it deferred.
Inspect browser smoke error and console logs.
Inspect VRM validation.
Inspect path/size/material issue.
Try to fix the browser-load blocker.
If fixed, re-add as test-only generated candidate and run smoke.
Generate contact sheet and visual review.
If still fails, preserve best attempt and write exact blocker.
```

For `buzz-lightyear` and `teal-v2`:

```txt
They converted as reference candidates but mapping was weak.
Do not stop at “manual_mapping_needed” until you have tried evidence-based mapping recovery.
Infer from hierarchy, bone positions, vertex groups, skin weights, symmetry, source audit, and bone-tree.
Try manual/suggested bone-map recovery.
Try scale/orientation/root correction.
Try wrist/palm and foot/ankle if bones exist.
Re-export/revalidate.
If acceptable partial, browser-smoke and visually review.
If not, preserve best attempt and write exact blocker.
```

## Phase 8 — Hand-only rigged-hand pass

Model:

```txt
rigged-hand
```

Do not make this a full-body avatar.

Do:

```txt
inspect source
detect wrist/palm/finger chains
create or update hand-only control plan
attempt hand-only VRM/static preview if safe
generate hand pose contact sheet:
  neutral/open
  fist or curl
  index point
  wrist rotate
  palm forward
  palm down
inspect visually
write hand-only visual review
```

If browser preview is possible without pretending it is a body avatar:

```txt
add generated registry entry with profile: hand_only
enabledInUi: false
warningLabel: experimental
source: generated-vrm-smoke-test
```

Otherwise, do not add to registry.

## Phase 9 — Creature/custom-profile pass

Models:

```txt
baby-yoda
godzilla
grogu
king-kong
olaf
xenomorph
```

Do not force standard humanoid.

For each:

```txt
inspect source and prior reports
identify whether static-preview or creature-profile VRM container is feasible
attempt conversion/static preview if safe
validate if converted
browser-smoke if converted
generate screenshot/contact sheet if browser-loadable or renderable
inspect visually
write creature-rig-profile
write visual-rig-review
write game-control readiness
```

Creature visual review should focus on:

```txt
static visual correctness
texture/material survival
scale/orientation
head/torso readability
limb readability
jaw/tail/claw availability where relevant
gesture-to-intent potential
whether it should be static_preview_only, creature_profile_candidate, or deferred
```

If a creature is browser-loadable, it may be added as:

```txt
profile: creature
enabledInUi: false
warningLabel: experimental
source: generated-vrm-smoke-test
```

Do not mark creature as humanoid unless the rig objectively supports it.

## Phase 10 — Candidate selection rules

At the end of all attempts for each model, choose exactly one:

```txt
accepted_active_candidate
accepted_reference
deferred_with_blocker
rejected_all_attempts
```

An `accepted_active_candidate` must pass:

```txt
conversion pass or acceptable partial
post-VRM validation pass or acceptable partial
pose-suite pass or acceptable partial
visual review pass / acceptable / weird-but-usable
browser smoke pass
no public UI promotion
no generated VRM committed
```

If no attempt passes these gates, do not select an active candidate.

Preserve the best attempt as:

```txt
accepted_reference
```

or classify:

```txt
manual_mapping_needed
cleanup_needed
creature_profile_needed
hand_only
static_preview_only
visual_reject
conversion_failed
defer
```

## Phase 11 — Report updates

Update per-model reports:

```txt
model-audits/<slug>/visual-rig-review.md
model-audits/<slug>/visual-rig-review.json
model-audits/<slug>/pose-suite-validation.md
model-audits/<slug>/pose-suite-validation.json
model-audits/<slug>/attempts-summary.md
model-audits/<slug>/attempts-summary.json
model-audits/<slug>/runtime-capability-profile.md
model-audits/<slug>/runtime-capability-profile.json
model-audits/<slug>/hand-and-finger-readiness.md
model-audits/<slug>/hand-and-finger-readiness.json
model-audits/<slug>/feet-and-leg-readiness.md
model-audits/<slug>/feet-and-leg-readiness.json
model-audits/<slug>/face-touch-rig-plan.md
model-audits/<slug>/face-touch-rig-plan.json
model-audits/<slug>/game-control-readiness.md
model-audits/<slug>/game-control-readiness.json
model-audits/<slug>/web-optimization-review.md
model-audits/<slug>/web-optimization-review.json
model-audits/<slug>/manual-fix-checklist.md
model-audits/<slug>/manual-fix-checklist.json
```

Update aggregate reports:

```txt
model-audits/rig-prep/visual-qa-summary.md
model-audits/rig-prep/visual-qa-summary.json
model-audits/rig-prep/pose-suite-summary.md
model-audits/rig-prep/pose-suite-summary.json
model-audits/rig-prep/full-rig-readiness-summary.md
model-audits/rig-prep/full-rig-readiness-summary.json
model-audits/rig-prep/attempts-summary.md
model-audits/rig-prep/attempts-summary.json
model-audits/rig-prep/vrm-candidate-summary.md
model-audits/rig-prep/vrm-candidate-summary.json
model-audits/rig-prep/game-control-readiness-summary.md
model-audits/rig-prep/game-control-readiness-summary.json
model-audits/rig-prep/hand-and-finger-readiness-summary.md
model-audits/rig-prep/hand-and-finger-readiness-summary.json
model-audits/rig-prep/feet-and-leg-readiness-summary.md
model-audits/rig-prep/feet-and-leg-readiness-summary.json
model-audits/rig-prep/face-touch-readiness-summary.md
model-audits/rig-prep/face-touch-readiness-summary.json
model-audits/rig-prep/creature-profile-summary.md
model-audits/rig-prep/creature-profile-summary.json
model-audits/rig-prep/runtime-blockers-for-next-phase.md
model-audits/rig-prep/runtime-blockers-for-next-phase.json
```

Update:

```txt
COMBINED_MODEL_AUDIT_LLM_HANDOFF_COMPACT_V2.md
```

Do not overwrite rich older dossiers or adapter specs with flattened summaries. If you need companion files, create:

```txt
rig-readiness-dossier.*
rig-readiness-adapter-spec.*
```

## Phase 12 — Strengthen validation

Update `tools/validate_rig_readiness.py` so the previous loophole is closed.

It must fail if:

```txt
an active smoke-passing candidate lacks visual-rig-review
an active smoke-passing candidate lacks pose-suite-validation
an active candidate has visual_review: not_available without documented screenshot-generation blocker
an active candidate has browser_smoke pass but visual_reject
a model is marked works_well without visual pass and pose-suite pass
rigged-hand is marked normal humanoid
creature is marked humanoid without explicit justification
generated VRM/image/source asset is tracked
public UI promotion occurred
normal avatar cycling guard was removed
```

Add or update a validation command:

```sh
python3 tools/validate_rig_readiness.py model-audits --require-visual-for-active
```

If you choose a different flag name, document it.

## Phase 13 — Final tests

Run all final checks:

```sh
npm run build
npx playwright test tests/generated-avatar-load.spec.ts --reporter=line
python3 tools/audit_model.py --self-test
python3 tools/validate_rig_readiness.py model-audits --require-visual-for-active
python3 tools/update_generated_avatar_registry.py --validate-only
git diff --check
git diff --cached --check
git status --short
git ls-files --cached public/avatars/generated/
git diff --cached --name-only | grep -Ei '\.(vrm|blend|fbx|glb|gltf|zip|png|jpg|jpeg|webp|tga|bmp|tif|tiff|exr)$' || true
git ls-files --others --exclude-standard | grep -Ei '\.(vrm|blend|fbx|glb|gltf|zip|png|jpg|jpeg|webp|tga|bmp|tif|tiff|exr)$' || true
```

No generated binaries/images/source assets may be staged.

The ignored screenshots/contact sheets may exist locally, but must not be committed.

## Phase 14 — Commit safe changes only

Stage only safe code/text/report changes:

```txt
tools/*.py
src/rig/generatedAvatarRegistry.ts
tests/*.ts
model-audits/**/*.md
model-audits/**/*.json
COMBINED_MODEL_AUDIT_LLM_HANDOFF_COMPACT_V2.md
.gitignore if legitimately changed
package/npm files only if legitimately changed
```

Before commit:

```sh
git diff --cached --stat
git diff --cached --check
git diff --cached --name-only | grep -Ei '\.(vrm|blend|fbx|glb|gltf|zip|png|jpg|jpeg|webp|tga|bmp|tif|tiff|exr)$' || true
git ls-files --cached public/avatars/generated/
```

Suggested commit message:

```txt
feat: add visual rig QA and persistent avatar repair pass
```

If many models remain blocked but reports and tools are valuable, use:

```txt
docs: add visual rig QA results and avatar repair blockers
```

Push normally. Do not force-push.

## Final response requirements

When finished, report:

```txt
commit hash
whether pushed
baseline status
number of models processed
visual review coverage
pose-suite coverage
models visually accepted
models visually partial
models visually rejected
active candidates kept active
active candidates downgraded
new active candidates added
reference candidates preserved
failed/deferred candidates and exact blockers
models where repair attempts were made
number of attempts per hard model
best attempt per hard model
screenshots/contact sheets generated locally
whether screenshots/images were committed
browser smoke results
build result
validation result
registry invariant result
forbidden-file scan result
whether public UI remains unchanged
top models now closest to website use
best for walking
best for flying
best for rowing
best for hand/palm control
best for finger experimentation
best for face-touch experimentation
creature preview/control recommendations
rigged-hand status
runtime blockers for next phase
next recommended implementation step
```

## Completion checklist

Do not claim done unless all are true:

```txt
[ ] Started from or after commit 5f3286c.
[ ] Baseline build/smoke/validation passed before changes.
[ ] Visual evidence was generated for all 10 active smoke-passing candidates, or a specific blocker exists.
[ ] Vision/image reasoning was used to inspect active candidate evidence, or external-visual-review blockers are documented.
[ ] Pose-suite validation exists for all active humanoid candidates, or a specific blocker exists.
[ ] Elsa browser-smoke failure was investigated and at least one targeted fix attempt was made.
[ ] Buzz-Lightyear mapping was investigated beyond bone names and at least one mapping repair attempt was made.
[ ] Teal-v2 mapping was investigated beyond bone names and at least one mapping repair attempt was made.
[ ] Rigged-hand received a hand-only visual/pose attempt or a precise blocker.
[ ] Each creature received static/creature preview feasibility work or a precise blocker.
[ ] Failed attempts were preserved and explained.
[ ] Active candidates are not marked works_well without visual and pose evidence.
[ ] No generated VRMs/images/source assets were committed.
[ ] Public UI promotion did not happen.
[ ] Expanded validation now requires visual review for active candidates.
[ ] Final build passed.
[ ] Final Playwright generated-avatar smoke suite passed, or failures were truthfully documented and failing candidates downgraded.
[ ] Final rig-readiness validation passed.
[ ] Commit was created and pushed, or a clear reason was given.
```

Be ambitious, persistent, evidence-driven, and conservative in acceptance.

Make the strongest safe attempt for every model.

Use visual reasoning to decide whether the rig actually looks good.

Accept only results that are actually good enough.

Do not fake readiness.