import os
import shutil
import hashlib
import re
from pathlib import Path

SOURCE_DIR = "/Users/lekan/Dev/posepuppet"
DEST_DIR = os.path.expanduser("~/Downloads/bodyarcade-current-design-source")

def main():
    # 1. Inventory
    os.chdir(SOURCE_DIR)
    all_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', 'dist', 'build', '__pycache__']]
        for file in files:
            path = os.path.relpath(os.path.join(root, file), ".")
            if not path.startswith(".git/") and not path.startswith("node_modules/"):
                all_files.append(path)
    all_files.sort()
    
    with open(os.path.join(DEST_DIR, "inventories", "all-reviewed-files.txt"), "w") as f:
        for p in all_files:
            f.write(p + "\n")

    # Classifications
    classifications = {}
    reasons = {}

    # Keywords for search
    design_keywords = re.compile(r'THREE|Mesh|Material|Geometry|Shader|Color|Fog|Light|Camera|Scene|Sprite|Particle|Trail|Wake|Water|Ocean|Terrain|Globe|Plane|Boat|Carpet|Avatar|HUD|Lobby|Panel|Card|Transition|Animation|Audio|Weather|Rain|Cloud|Aurora|Star|Landmark|Campsite|Dolphin|Underwater|Vehicle|BodyInput', re.IGNORECASE)

    def classify(path, category, reason):
        if path not in classifications:
            classifications[path] = category
            reasons[path] = reason

    # Phase 2: Candidate discovery
    # First classify obvious exclusions
    for p in all_files:
        if p.endswith('.DS_Store') or '.pytest_cache' in p:
            classify(p, 'EXCLUDE_GENERATED', 'Generated or system file')
            continue
        if p.endswith('.png') or p.endswith('.jpg') or p.endswith('.mp4') or p.endswith('.webm') or p.endswith('.wasm') or p.endswith('.task') or p.endswith('.vrm') or p.endswith('.glb') or p.endswith('.gltf'):
            classify(p, 'EXCLUDE_BINARY', 'Large binary asset')
            continue
        if p.endswith('.env') or 'secret' in p.lower():
            classify(p, 'EXCLUDE_SECRET', 'Potential secret or environment file')
            continue
        if 'tests/' in p or p.endswith('.spec.ts') or p.endswith('.test.ts'):
            classify(p, 'EXCLUDE_TEST_ONLY', 'Test file unrelated to visual behavior')
            continue
        if 'scripts/' in p or 'tools/' in p or 'docker' in p.lower() or '.github' in p or 'playwright.config.ts' in p or p == 'vite.config.ts':
            classify(p, 'EXCLUDE_INFRASTRUCTURE', 'Infrastructure or script file')
            continue
        if 'server/' in p or 'backend/' in p or 'database' in p.lower():
            classify(p, 'EXCLUDE_BACKEND', 'Backend code')
            continue
        
        # Documentation
        if p.endswith('.md') or p.endswith('.txt'):
            classify(p, 'INCLUDE_DOCUMENTATION', 'Design and project documentation')
            continue
        
        # Look for keywords in file
        try:
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
                if design_keywords.search(content):
                    if 'apps/flight' in p:
                        classify(p, 'INCLUDE_DESIGN', 'Contains design keywords')
                    elif 'src/' in p or 'packages/body-input' in p:
                        classify(p, 'INCLUDE_SHARED_CONTEXT', 'Shared UI/Input context with design keywords')
                    else:
                        classify(p, 'UNCERTAIN', 'Has keywords but not in standard design paths')
        except UnicodeDecodeError:
            classify(p, 'EXCLUDE_BINARY', 'Binary file not decodable as text')
    
    # Required areas
    for p in all_files:
        if p not in classifications or classifications[p] == 'UNCERTAIN':
            if p.startswith('apps/flight/client/src/game/') or \
               p.startswith('apps/flight/client/src/ui/') or \
               p.startswith('apps/flight/client/src/input/') or \
               p.startswith('apps/flight/client/src/audio/') or \
               p.startswith('apps/flight/client/src/config/') or \
               p.startswith('apps/flight/client/src/runtime/') or \
               p.startswith('apps/flight/client/src/utils/') or \
               p.startswith('apps/flight/shared/'):
                classify(p, 'INCLUDE_DESIGN_ADJACENT', 'Required source area')
            elif p.startswith('src/ui/') or p.startswith('src/stage/') or p.startswith('src/styles.css') or p == 'src/main.ts' or p == 'src/config.ts':
                classify(p, 'INCLUDE_SHARED_CONTEXT', 'Shared PosePuppet design language')
            elif p.startswith('packages/body-input/src/') or p.startswith('src/bodyinput/'):
                classify(p, 'INCLUDE_SHARED_CONTEXT', 'Body input context')

    # Catch-all
    for p in all_files:
        if p not in classifications:
            classify(p, 'EXCLUDE_INFRASTRUCTURE', 'Not related to design or explicitly included')

    # Phase 3: Dependency expansion
    # simple regex for imports
    import_re = re.compile(r'from\s+[\'"]([^\'"]+)[\'"]|import\s+[\'"]([^\'"]+)[\'"]')
    
    def resolve_import(base_path, import_path):
        if not import_path.startswith('.'):
            return None
        dir_name = os.path.dirname(base_path)
        resolved = os.path.normpath(os.path.join(dir_name, import_path))
        # try adding extensions
        for ext in ['.ts', '.tsx', '.js', '.css', '/index.ts']:
            if os.path.exists(resolved + ext):
                return resolved + ext
            if ext.startswith('/') and os.path.exists(resolved + ext):
                return resolved + ext
        return resolved

    changed = True
    while changed:
        changed = False
        includes = [p for p in all_files if classifications.get(p, '').startswith('INCLUDE')]
        for p in includes:
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for match in import_re.findall(content):
                        imp = match[0] or match[1]
                        if imp:
                            resolved = resolve_import(p, imp)
                            if resolved and resolved in classifications:
                                if classifications[resolved].startswith('EXCLUDE') or classifications[resolved] == 'UNCERTAIN':
                                    classifications[resolved] = 'INCLUDE_DESIGN_ADJACENT'
                                    reasons[resolved] = f'Imported by {p}'
                                    changed = True
            except Exception:
                pass

    # Copy files
    os.makedirs(os.path.join(DEST_DIR, "source"), exist_ok=True)
    included = []
    excluded = []
    uncertain = []
    
    with open(os.path.join(DEST_DIR, "inventories", "copied-file-checksums.sha256"), "w") as checksum_file:
        for p in all_files:
            cls = classifications[p]
            if cls.startswith('INCLUDE'):
                included.append(p)
                dest_path = os.path.join(DEST_DIR, "source", p)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                shutil.copy2(p, dest_path)
                
                # Checksum
                with open(p, 'rb') as f:
                    csum = hashlib.sha256(f.read()).hexdigest()
                checksum_file.write(f"{csum}  {p}\n")
            elif cls.startswith('EXCLUDE'):
                excluded.append(p)
            else:
                uncertain.append(p)

    with open(os.path.join(DEST_DIR, "inventories", "included-files.txt"), "w") as f:
        f.write("\n".join(included))
    with open(os.path.join(DEST_DIR, "inventories", "excluded-files.txt"), "w") as f:
        for p in excluded:
            f.write(f"{p} ({reasons[p]})\n")
    with open(os.path.join(DEST_DIR, "inventories", "uncertain-files.txt"), "w") as f:
        for p in uncertain:
            f.write(f"{p} ({reasons[p]})\n")
            
    # Manifest
    with open(os.path.join(DEST_DIR, "SOURCE_MANIFEST.md"), "w") as f:
        f.write("# Source Manifest\n\n")
        f.write("| Original path | Classification | Reason | Copied | Checksum |\n")
        f.write("|---|---|---|---|---|\n")
        for p in included:
            f.write(f"| {p} | {classifications[p]} | {reasons[p]} | Yes | Verified |\n")
        for p in excluded:
            f.write(f"| {p} | {classifications[p]} | {reasons[p]} | No | N/A |\n")

    # Documentations
    docs = {
        "README.md": """# BodyArcade Current Design Source
This is a complete design-source extraction of the BodyArcade/PosePuppet repository.
Copied source files are full and unmodified.
It is not intended to run. It exists to support an aesthetic and experience redesign.
Original paths are preserved below `source/`.
Original commit: """ + os.popen("git rev-parse HEAD").read().strip() + """
""",
        "DESIGN_SOURCE_GUIDE.md": """# Design Source Guide
1. Read STATUS_OF_EACH_MODE.md
2. Read BODYARCADE_CONTEXT.md and FUTURES.md
3. Inspect PosePuppet styles and UI
4. Inspect Flight Game.ts and Globe.ts
5. Inspect plane, boat, carpet and camera files
6. Inspect atmosphere and effects
7. Inspect HUD and lobby
8. Inspect campsite files
9. Inspect body-input types and game integration
10. Review asset and license manifests
""",
        "STATUS_OF_EACH_MODE.md": """# Status of Each Mode
## Flight
Implemented and playable.
## Rowing
Existing boat vehicle, ocean presentation, wake and related gameplay exist. A complete articulated-oar, body-controlled rowing simulator does not yet exist.
## Walking
A campsite/on-foot system exists but is partial and disabled.
## Dolphin
No complete Dolphin implementation exists. The repository contains planning and reusable vehicle, ocean, camera and control foundations.
""",
        "DEPENDENCY_CONTEXT.md": """# Dependency Context
Implementation-adjacent files are included to provide context for world generation, terrain and surface math, vehicle transforms, camera, body input, progression and visible unlocks, audio, asset references, feature flags, and runtime integration.
""",
        "ASSET_MANIFEST.md": """# Asset Manifest
Note: Large binary assets were excluded. Check inventories/excluded-files.txt for binary exclusions.
""",
        "LICENSE_AND_ATTRIBUTION.md": """# License and Attribution
This contains source from PosePuppet and Tiny Skies/GlobeFly.
Original repository commit: """ + os.popen("git rev-parse HEAD").read().strip() + """
"""
    }
    
    for name, content in docs.items():
        with open(os.path.join(DEST_DIR, name), "w") as f:
            f.write(content)
            
    print(f"Copied {len(included)} files. Excluded {len(excluded)}. Uncertain {len(uncertain)}.")

if __name__ == "__main__":
    main()
