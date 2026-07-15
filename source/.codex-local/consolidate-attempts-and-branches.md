You are Codex 5.5 Agent Mode with Max Reasoning.

This is a PosePuppet consolidation, preservation, and git-organization task. The goal is to save absolutely everything from the simultaneous runs, organize all attempts/results into clean labeled folders, create clean branches for comparison, and prepare a local demo website that can view all VRM attempts. Do not delete anything.

## Core objective

Take the outputs from the simultaneous PosePuppet runs and organize them into a single clean preservation structure, while also creating clean git branches/manifests so later prompts can compare, test, and choose the best work.

The runs may include:

```txt
Ubuntu canonical visual-QA run:
  /home/o/Dev/posepuppet
  /home/o/posepuppet-working/
  /home/o/Dev/posepuppet/model-working/

Ubuntu parallel hard-fix worktree, if present:
  /home/o/Dev/posepuppet-hard-model-fix
  /home/o/posepuppet-working-hard-fix/
  /home/o/posepuppet-hard-fix-evidence/

Mac main checkout:
  /Users/lekan/Dev/posepuppet

Mac parallel hard-fix checkout:
  /Users/lekan/Dev/posepuppet-hard-model-fix
  /Users/lekan/posepuppet-working-hard-fix/
  /Users/lekan/posepuppet-hard-fix-evidence/

Previous local archives:
  /Users/lekan/Downloads/PosePuppet_ALL_Attempts_Results_*
  /Users/lekan/Downloads/PosePuppet_Attempt_Preservation_*
  /Users/lekan/Downloads/PosePuppet_Model_Attempts_By_Model_*
```

## Non-negotiable safety rules

Do not delete, reset, clean, rebase, squash, force-push, or discard anything.

Do not run:

```sh
git reset
git clean
git checkout -- .
git restore .
rm -rf
git rebase
git merge
git push --force
```

unless explicitly asked later.

Do not modify or clean the original source asset folders.

Do not stage or commit generated binary/media artifacts into normal git history unless the user explicitly approves Git LFS or a release/archive strategy later.

Forbidden normal-git tracked artifacts include:

```txt
*.vrm
*.blend
*.fbx
*.glb
*.gltf
*.obj
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
public/avatars/generated/
model-working/
model-working-hard-fix/
.codex-local/
prompt files
source assets
textures
```

These files must be preserved in the external archive folder and referenced by manifests. Commit only safe code, Markdown, JSON, text reports, branch manifests, and viewer source code if appropriate.

## Desired final structure

Create one master local archive folder in Downloads:

```txt
/Users/lekan/Downloads/PosePuppet_Consolidated_Attempts_<timestamp>/
```

Inside it, organize all work like this:

```txt
PosePuppet_Consolidated_Attempts_<timestamp>/
  README.md
  INDEX.md
  branches/
    ubuntu-canonical/
    mac-parallel-hard-fix/
    mac-main/
    ubuntu-parallel-hard-fix-if-present/
  models/
    <model-slug>/
      README.md
      attempt-index.json
      attempt-index.md
      ubuntu-canonical/
        vrms/
        screenshots/
        contact-sheets/
        pose-suite/
        reports/
        logs/
        manifests/
        diffs/
      mac-parallel-hard-fix/
        vrms/
        screenshots/
        contact-sheets/
        pose-suite/
        reports/
        logs/
        manifests/
        diffs/
      other-sources/
        vrms/
        screenshots/
        contact-sheets/
        reports/
        logs/
  repositories/
    ubuntu-canonical/
      git/
      diffs/
      reports/
      changed-files/
    mac-parallel-hard-fix/
      git/
      diffs/
      reports/
      changed-files/
    mac-main/
      git/
      diffs/
      reports/
      changed-files/
  transcripts/
    ubuntu-canonical/
    mac-parallel-hard-fix/
  demo-site/
    README.md
    package.json
    src/
    public/
      manifest.json
      vrms/
      screenshots/
      contact-sheets/
  manifests/
    all-files.txt
    all-folders.txt
    sha256-all-files.txt
    models.txt
    attempts.txt
    branches.txt
    artifact-sources.txt
    do-not-delete.txt
```

The `demo-site/` should be a local comparison viewer that can load the archived VRMs and show each attempt side by side with screenshots/contact sheets/reports. It does not need to be production PosePuppet UI. It should be an internal artifact browser.

## Git branch organization

Create clean labeled branches without merging them into main yet.

Suggested branches:

```txt
archive/ubuntu-canonical-visual-qa
archive/mac-parallel-hard-fix
archive/consolidated-attempt-index
compare/attempt-gallery
```

Use branches as labels and safe report/code containers, not as places to commit huge generated binaries.

For each branch, save:

```txt
branch name
base commit
current HEAD
remote tracking info
commit log
git status
changed files
diff stats
full patch where applicable
artifact archive path
models affected
attempts present
```

If a branch already exists, do not overwrite it. Create a timestamped variant.

Also create git bundles for preservation:

```txt
<archive>/repositories/<repo-label>/git/<repo-label>.bundle
```

Use `git bundle create ... --all` where safe.

## Phase 1 — Inventory all runs

Inspect these checkouts if they exist:

```txt
/home/o/Dev/posepuppet
/home/o/Dev/posepuppet-hard-model-fix
/Users/lekan/Dev/posepuppet
/Users/lekan/Dev/posepuppet-hard-model-fix
```

For remote Ubuntu paths, use:

```sh
ssh -i ~/.ssh/pinn_rtx3090 o@192.168.86.152
```

For every checkout, record:

```sh
pwd
git branch --show-current
git rev-parse HEAD
git rev-parse --short HEAD
git remote -v
git status --short --ignored
git diff --stat
git diff --cached --stat
git log --oneline -30
git ls-files --others --exclude-standard
git ls-files --ignored --others --exclude-standard
```

Save these into:

```txt
<archive>/repositories/<repo-label>/git/
<archive>/repositories/<repo-label>/diffs/
```

Do not rely on terminal output only. Everything must be written to files.

## Phase 2 — Copy all artifacts, do not move them

Copy all relevant artifacts into the archive. Preserve source paths in manifests.

Search and copy from:

```txt
public/avatars/generated/
dist/avatars/generated/
model-working/
model-working-hard-fix/
model-audits/
test-results/
playwright-report/
coverage/
logs/
reports/
screenshots/
contact-sheets/
/home/o/posepuppet-working/generated-vrms/
/home/o/posepuppet-working-hard-fix/generated-vrms/
/home/o/posepuppet-hard-fix-evidence/
/Users/lekan/posepuppet-working/generated-vrms/
/Users/lekan/posepuppet-working-hard-fix/generated-vrms/
/Users/lekan/posepuppet-hard-fix-evidence/
```

Also include previous preservation folders in Downloads if present:

```txt
/Users/lekan/Downloads/PosePuppet_ALL_Attempts_Results_*
/Users/lekan/Downloads/PosePuppet_Attempt_Preservation_*
/Users/lekan/Downloads/PosePuppet_Model_Attempts_By_Model_*
```

Copy, do not move. Never delete originals.

For every copied file, record:

```txt
original path
archive path
file size
sha256
source run label
model slug if known
attempt id if known
category: vrm / screenshot / contact-sheet / pose-suite / report / log / diff / manifest / source-copy / unknown
```

## Phase 3 — Build model attempt index

Create per-model folders for at least these model slugs if present:

```txt
amazing-spider-man-2
terminator-t-800
spider-man-no-way-home
spider-man-playstation
jack-sparrow
elsa
buzz-lightyear
teal-v2
shrek
iron-man
woody
darth-vader
fortnite-batman
baby-yoda
godzilla
grogu
king-kong
olaf
rigged-hand
xenomorph
```

For every model, create:

```txt
models/<model>/README.md
models/<model>/attempt-index.md
models/<model>/attempt-index.json
```

Each attempt entry must include:

```txt
model slug
attempt label
run source: ubuntu-canonical / mac-parallel-hard-fix / other
repo path
branch
commit
VRM path
screenshots path
contact sheet path
pose-suite path
capture-results path
validation report path
audit report path
browser smoke result
visual result
pose result
failure class
repair class
changed files
generated artifacts preserved: yes/no
safe to compare later: yes/no/unknown
safe to merge later: yes/no/unknown
notes
```

Use consistent status labels:

```txt
accepted_active_candidate
accepted_reference
deferred_with_blocker
rejected_all_attempts
unknown_needs_review
```

Use consistent failure/repair labels:

```txt
browser_smoke_fail
visual_invisible
material_visibility_blocker
camera_framing_blocker
scale_grounding_blocker
orientation_blocker
duplicate_mesh_blocker
manual_mapping_needed
source_reexport_attempt
runtime_normalization_attempt
visual_capture_tooling_attempt
pose_suite_attempt
bone_map_recovery_attempt
unknown
```

## Phase 4 — Create a local comparison demo website

Create a local static demo website inside:

```txt
<archive>/demo-site/
```

Purpose: compare every VRM attempt and its evidence. This is not production PosePuppet.

The site should include:

```txt
model list
attempt list per model
source run label
VRM viewer panel if feasible
contact sheet display
pose screenshot gallery
validation/report links
JSON manifest display
notes/blockers
side-by-side comparison mode
```

If building a fully functional VRM viewer takes too long, create a static HTML/JS gallery first with links to VRMs/contact sheets/reports, then clearly mark viewer as future work. Do not skip the manifest/gallery.

Generate:

```txt
demo-site/public/manifest.json
demo-site/README.md
demo-site/index.html
```

If using npm/Vite/Three is practical, set it up locally in the archive folder. Do not contaminate the production app unless needed.

## Phase 5 — Create tracked lightweight repo reports

In the appropriate PosePuppet checkout, create a safe tracked report folder:

```txt
model-audits/rig-prep/consolidated-attempts/
```

Write:

```txt
summary.md
summary.json
branches.md
branches.json
attempt-ledger.md
attempt-ledger.json
artifact-archive.md
artifact-archive.json
demo-site.md
demo-site.json
git-triage-notes.md
git-triage-notes.json
next-evaluation-plan.md
next-evaluation-plan.json
```

These tracked files should point to the external archive location and summarize what was preserved. They should not include binary files.

## Phase 6 — Create clean branches

Create a clean branch for the consolidation reports:

```txt
archive/consolidated-attempt-index-<timestamp>
```

Commit only safe Markdown/JSON/text files and any safe viewer source code if intentionally kept in repo. Do not commit the external archive binaries.

If existing work from the Mac hard-fix branch has safe code/report changes, preserve it on its own branch:

```txt
archive/mac-parallel-hard-fix-<timestamp>
```

If existing work from Ubuntu canonical has safe code/report changes, preserve it on its own branch:

```txt
archive/ubuntu-canonical-visual-qa-<timestamp>
```

Do not merge these branches together yet. The next prompt will evaluate and test candidates.

Before every commit, run:

```sh
git diff --check
git diff --cached --check
git diff --cached --name-only | grep -Ei '\.(vrm|blend|fbx|glb|gltf|obj|zip|png|jpg|jpeg|webp|tga|bmp|tif|tiff|exr)$|public/avatars/generated|model-working|model-working-hard-fix|\.codex-local|prompt|codex-goals' || true
```

If the forbidden-file scan prints anything, unstage those files and do not commit until clean.

## Phase 7 — Do not choose winners

Do not decide which model attempt is best in this task.

Instead, prepare:

```txt
model-audits/rig-prep/consolidated-attempts/next-evaluation-plan.md
```

It should say what the next prompt should test:

```txt
which attempts compete per model
which must be re-tested on Ubuntu
which must be compared visually
which have missing evidence
which are unsafe to merge
which need source-level repair
which can be considered runtime-only fixes
which branches contain which changes
```

## Final response

When finished, report:

```txt
master archive folder path
all branches created
all commits created
whether anything was pushed
all checkouts inspected
artifact counts
VRM count
screenshot/contact-sheet count
model count
attempt count
demo-site path
tracked report folder path
forbidden-file scan result
dirty state remaining per checkout
what was not copied and why
recommended next prompt: evaluation/testing/best-candidate selection
```

Remember: save everything, label everything, delete nothing, merge nothing, choose nothing yet.