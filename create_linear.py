#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Linear Camera Profile Generator
Creates a camera-specific linear DCP profile required for applying 3D LUTs in Camera Raw.
Licensed under the MIT License.
"""

import os
import sys
import platform
import shutil
import subprocess
import re
import tempfile
from pathlib import Path

def get_adobe_paths():
    system = platform.system()
    if system == "Windows":
        base_search = Path(os.environ.get("ProgramData", "C:\\ProgramData")) / "Adobe" / "CameraRaw" / "CameraProfiles" / "Adobe Standard"
        user_profiles_dir = Path(os.environ.get("APPDATA", "")) / "Adobe" / "CameraRaw" / "CameraProfiles"
    elif system == "Darwin":
        base_search = Path("/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Adobe Standard")
        user_profiles_dir = Path.home() / "Library" / "Application Support" / "Adobe" / "CameraRaw" / "CameraProfiles"
    else:
        base_search = Path.cwd()
        user_profiles_dir = Path.cwd() / "installed_profiles"
    return base_search, user_profiles_dir

def find_dcptool():
    candidates = ["dcptool.exe", "dcpTools.exe", "dcptool", "dcpTool"]
    for name in candidates:
        local_path = Path.cwd() / name
        if local_path.is_file():
            return str(local_path.resolve())
    for name in candidates:
        system_path = shutil.which(name)
        if system_path:
            return system_path
    return None

def search_camera_profile(query, search_dir):
    candidates = []
    if search_dir.is_dir():
        candidates.extend(list(search_dir.glob("*.dcp")))
    candidates.extend(list(Path.cwd().glob("*.dcp")))
    
    unique_candidates = list({p.resolve(): p for p in candidates}.values())
    query_lower = query.lower()
    matches = [
        p for p in unique_candidates
        if query_lower in p.name.lower()
        and (p.stem.lower() == "adobe standard" or p.stem.lower().endswith(" adobe standard"))
    ]
    return sorted(matches, key=lambda x: x.name)

def ask_yes_no(prompt_text, default=True):
    hint = "[Y/n]" if default else "[y/N]"
    user_input = input(f"{prompt_text} {hint}: ").strip().lower()
    if not user_input:
        return default
    return user_input in ["y", "yes", "j", "ja"]

def select_profile_interactive(adobe_search_dir):
    while True:
        camera_query = input("\nEnter camera model (e.g., 'd5300' or 'Nikon D5300') [or 'q' to quit]: ").strip()
        if not camera_query or camera_query.lower() in ["q", "quit", "exit"]:
            sys.exit("Aborted by user.")

        matches = search_camera_profile(camera_query, adobe_search_dir)
        if not matches:
            print(f"No profile matching '{camera_query}' found.")
            if ask_yes_no("Do you want to search again?", default=True):
                continue
            sys.exit("Aborted by user.")

        print(f"\nFound profile(s) matching '{camera_query}':")
        for idx, match in enumerate(matches, 1):
            print(f"  [{idx}] {match.name} ({match.parent})")
        print("  [s] Search again")
        print("  [q] Quit")

        while True:
            choice = input(f"\nSelect an option (1-{len(matches)}, 's', 'q'): ").strip().lower()
            if choice in ["q", "quit", "exit"]:
                sys.exit("Aborted by user.")
            if choice in ["s", "search"]:
                break
            try:
                idx = int(choice)
                if 1 <= idx <= len(matches):
                    return matches[idx - 1]
            except ValueError:
                pass
            print(f"Invalid input. Please enter 1-{len(matches)}, 's' to search again, or 'q' to quit.")

def set_xml_tag(xml_text, tag, value):
    pattern = rf"<{tag}>.*?</{tag}>"
    if re.search(pattern, xml_text):
        return re.sub(pattern, f"<{tag}>{value}</{tag}>", xml_text)
    match = re.search(r"</\w+>\s*$", xml_text)
    if match:
        idx = match.start()
        return xml_text[:idx] + f"  <{tag}>{value}</{tag}>\n" + xml_text[idx:]
    return xml_text + f"\n<{tag}>{value}</{tag}>"

def main():
    print("=== Linear Camera Profile Generator ===")
    
    dcptool_bin = find_dcptool()
    if not dcptool_bin:
        sys.exit("Error: 'dcpTool' binary not found in working directory or system PATH.")

    adobe_search_dir, user_profiles_dir = get_adobe_paths()
    selected_dcp = select_profile_interactive(adobe_search_dir)

    camera_name = selected_dcp.stem.replace(" Adobe Standard", "").strip()
    profile_display_name = "Adobe Standard Linear"

    out_dir = Path.cwd() / "output" / f"{camera_name} Linear"
    out_dir.mkdir(parents=True, exist_ok=True)
    target_dcp = out_dir / f"{camera_name} Linear.dcp"

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        temp_base_dcp = temp_dir / selected_dcp.name
        temp_base_xml = temp_dir / f"{selected_dcp.stem}.xml"
        shutil.copy2(selected_dcp, temp_base_dcp)

        print(f"\nDecompiling '{selected_dcp.name}'...")
        res = subprocess.run([dcptool_bin, "-d", str(temp_base_dcp), str(temp_base_xml)], capture_output=True, text=True)
        if res.returncode != 0 or not temp_base_xml.is_file():
            err_msg = (res.stderr or res.stdout).strip()
            sys.exit(f"dcpTool decompile failed: {err_msg if err_msg else 'Unknown error'}")

        with open(temp_base_xml, "r", encoding="utf-8", errors="ignore") as f:
            xml_content = f.read()

        # 1. Remove LookTable
        xml_content = re.sub(r"<LookTable[\s\S]*?</LookTable>", "", xml_content)

        # 2. Set ToneCurve to strictly linear (0 to 1 diagonal)
        linear_curve = (
            '  <ToneCurve Size="2">\n'
            '    <Element N="0" h="0.000000" v="0.000000"/>\n'
            '    <Element N="1" h="1.000000" v="1.000000"/>\n'
            '  </ToneCurve>'
        )
        if re.search(r"<ToneCurve[\s\S]*?</ToneCurve>", xml_content):
            xml_content = re.sub(r"<ToneCurve[\s\S]*?</ToneCurve>", linear_curve, xml_content, count=1)
        else:
            match = re.search(r"</\w+>\s*$", xml_content)
            idx = match.start()
            xml_content = xml_content[:idx] + linear_curve + "\n" + xml_content[idx:]

        # 3. Set ProfileName
        xml_content = set_xml_tag(xml_content, "ProfileName", profile_display_name)
        
        # 4. Set DefaultBlackRender
        xml_content = set_xml_tag(xml_content, "DefaultBlackRender", "1")

        target_xml = temp_dir / f"{camera_name} Linear.xml"
        with open(target_xml, "w", encoding="utf-8") as f:
            f.write(xml_content)

        print(f"Compiling '{target_dcp.name}'...")
        compile_res = subprocess.run([dcptool_bin, "-c", str(target_xml), str(target_dcp)], capture_output=True, text=True)

        if compile_res.returncode != 0 or not target_dcp.is_file():
            err_msg = (compile_res.stderr or compile_res.stdout).strip()
            sys.exit(f"Compilation failed: {err_msg if err_msg else 'Unknown error'}")

    print(f"[OK] Linear profile created at:\n{target_dcp}")

    # Installation
    print("\n--- Deployment ---")
    if ask_yes_no("Install linear profile directly into CameraRaw?", default=True):
        target_install_dir = user_profiles_dir / "Linear Profiles"
        target_install_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target_dcp, target_install_dir / target_dcp.name)
        print(f"\nSuccessfully copied to:\n{target_install_dir / target_dcp.name}")
        print("\nRestart Photoshop / Camera Raw to use this profile as your base for 3D LUTs.")
    else:
        print(f"\nManual installation: Copy '{target_dcp.name}' to:\n{user_profiles_dir}")

if __name__ == "__main__":
    main()
