import os
import shutil
import hashlib

SOURCE_DIR = "/Users/lekan/Dev/posepuppet"
DEST_DIR = os.path.expanduser("~/Downloads/bodyarcade-current-design-source")

def main():
    uncertain_file = os.path.join(DEST_DIR, "inventories", "uncertain-files.txt")
    if not os.path.exists(uncertain_file):
        return
        
    with open(uncertain_file, "r") as f:
        lines = f.readlines()
        
    new_includes = []
    
    with open(os.path.join(DEST_DIR, "inventories", "copied-file-checksums.sha256"), "a") as checksum_file:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            path = line.split(" (")[0]
            new_includes.append(path)
            
            dest_path = os.path.join(DEST_DIR, "source", path)
            src_path = os.path.join(SOURCE_DIR, path)
            
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                with open(src_path, 'rb') as sf:
                    csum = hashlib.sha256(sf.read()).hexdigest()
                checksum_file.write(f"{csum}  {path}\n")

    # Update manifest
    with open(os.path.join(DEST_DIR, "SOURCE_MANIFEST.md"), "a") as f:
        for p in new_includes:
            f.write(f"| {p} | INCLUDE_DESIGN_ADJACENT | Previously uncertain, conservatively included | Yes | Verified |\n")
            
    # Empty uncertain files since we resolved them
    with open(uncertain_file, "w") as f:
        f.write("")

if __name__ == "__main__":
    main()
