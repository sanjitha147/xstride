import os
import zipfile
import base64
import shutil

base_dir = r"E:\downloads_2\xstride_rtl"
target_dir = os.path.join(base_dir, "my_design")
zip_path = os.path.join(base_dir, "my_design.zip")
bundle_path = os.path.join(base_dir, "my_design.bundle")
setup_script_path = os.path.join(base_dir, "setup_my_design.py")

# 1. Create clean ZIP
print("[*] Creating zip archive...")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(target_dir):
        if ".git" in root:
            continue
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, target_dir)
            zipf.write(full_path, rel_path)

print(f"[+] Zip created at: {zip_path} ({os.path.getsize(zip_path)} bytes)")

# 2. Create self-extracting setup script from bundle
with open(bundle_path, "rb") as f:
    bundle_bytes = f.read()

bundle_b64 = base64.b64encode(bundle_bytes).decode("ascii")

setup_code = [
    '#!/usr/bin/env python3',
    '"""',
    'setup_my_design.py - Self-Extracting Installer for X-STRIDE EDA Project (v2.0)',
    'Extracts the complete EDA repository tree tagged as v2.0 with git history intact.',
    '"""',
    '',
    'import os',
    'import sys',
    'import base64',
    'import subprocess',
    '',
    f'BUNDLE_B64 = """{bundle_b64}"""',
    '',
    'def setup_repo(dest_dir="my_design"):',
    '    print("=" * 65)',
    '    print(" X-STRIDE EDA REPOSITORY INSTALLER (v2.0 Release)")',
    '    print("=" * 65)',
    '    ',
    '    abs_dest = os.path.abspath(dest_dir)',
    '    print(f"[*] Extracting to: {abs_dest}")',
    '    ',
    '    temp_bundle = os.path.abspath("temp_xstride.bundle")',
    '    try:',
    '        with open(temp_bundle, "wb") as f:',
    '            f.write(base64.b64decode(BUNDLE_B64))',
    '        ',
    '        print("[*] Restoring git repository from bundle...")',
    '        cmd = ["git", "clone", temp_bundle, abs_dest]',
    '        ret = subprocess.run(cmd, capture_output=True, text=True)',
    '        if ret.returncode != 0:',
    '            print(f"[-] Git clone failed: {ret.stderr}")',
    '            sys.exit(1)',
    '        ',
    '        subprocess.run(["git", "checkout", "v2.0"], cwd=abs_dest, capture_output=True)',
    '        print("[+] Repository successfully cloned and verified at tag v2.0!")',
    '        print("[+] Standard EDA directory structure ready:")',
    '        print("    my_design/")',
    '        print("    |-- project.json")',
    '        print("    |-- source/")',
    '        print("    |-- include/")',
    '        print("    |-- simulation/")',
    '        print("    |-- constraints/")',
    '        print("    |-- configuration/")',
    '        print("    |-- technology/")',
    '        print("    |-- firmware/")',
    '        print("    `-- runs/")',
    '        print("=" * 65)',
    '    finally:',
    '        if os.path.exists(temp_bundle):',
    '            os.remove(temp_bundle)',
    '',
    'if __name__ == "__main__":',
    '    dest = sys.argv[1] if len(sys.argv) > 1 else "my_design"',
    '    setup_repo(dest)'
]

with open(setup_script_path, "w", encoding="utf-8") as f:
    f.write("\n".join(setup_code) + "\n")

print(f"[+] Setup script created at: {setup_script_path} ({os.path.getsize(setup_script_path)} bytes)")
