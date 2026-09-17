#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""
Fujifilm DCP Camera Profile Generator
Compiles native DCP profiles directly for Adobe Lightroom & Camera Raw.
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
    """Detect default Adobe CameraRaw profile paths across operating systems."""
    system = platform.system()
    if system == "Windows":
        base_search = Path(os.environ.get("ProgramData", "C:\\ProgramData")) / "Adobe" / "CameraRaw" / "CameraProfiles" / "Adobe Standard"
        user_profiles = Path(os.environ.get("APPDATA", "")) / "Adobe" / "CameraRaw" / "CameraProfiles"
    elif system == "Darwin":  # macOS
        base_search = Path("/Library/Application Support/Adobe/CameraRaw/CameraProfiles/Adobe Standard")
        user_profiles = Path.home() / "Library" / "Application Support" / "Adobe" / "CameraRaw" / "CameraProfiles"
    else:
        base_search = Path.cwd()
        user_profiles = Path.cwd() / "installed_profiles"
    return base_search, user_profiles

def find_dcptool():
    """Locate the dcpTool binary in the current working directory or system PATH."""
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
    """Search for matching DCP profiles in Adobe Standard directory and current working directory."""
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
    """Prompt user for a yes/no decision with default support."""
    hint = "[Y/n]" if default else "[y/N]"
    user_input = input(f"{prompt_text} {hint}: ").strip().lower()
    if not user_input:
        return default
    return user_input in ["y", "yes"]

def select_profile_interactive(adobe_search_dir):
    """Interactive loop to query, select, re-search, or abort base profile selection."""
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
    """Update an existing XML tag or insert it before the closing root tag."""
    pattern = rf"<{tag}>.*?</{tag}>"
    if re.search(pattern, xml_text):
        return re.sub(pattern, f"<{tag}>{value}</{tag}>", xml_text)
    match = re.search(r"</\w+>\s*$", xml_text)
    if match:
        idx = match.start()
        return xml_text[:idx] + f"  <{tag}>{value}</{tag}>\n" + xml_text[idx:]
    return xml_text + f"\n<{tag}>{value}</{tag}>"

def clean_look_name(stem_name):
    """Format the file stem cleanly and strip duplicate fuji prefixes."""
    name = stem_name.replace("_", " ").strip()
    name = re.sub(r"(?i)^fuji(film)?\s*", "", name)
    return name.title()

def main():
    print("=== Fujifilm Camera Profile Generator ===")
    
    dcptool_bin = find_dcptool()
    if not dcptool_bin:
        sys.exit("Error: 'dcpTool' binary not found in working directory or system PATH.")

    tables_dir = Path.cwd() / "xml tables"
    if not tables_dir.is_dir():
        sys.exit(f"Error: Directory '{tables_dir.name}' not found in current working directory.")

    txt_files = sorted(list(tables_dir.glob("*.txt")), key=lambda x: x.name)
    if not txt_files:
        sys.exit(f"Error: No .txt files found in '{tables_dir.name}' directory.")

    adobe_search_dir, user_profiles_dir = get_adobe_paths()
    selected_dcp = select_profile_interactive(adobe_search_dir)

    camera_name = selected_dcp.stem.replace(" Adobe Standard", "").strip()

    out_dir = Path.cwd() / "output" / f"Fujifilm Simulations {camera_name}"
    out_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)
        temp_base_dcp = temp_dir / selected_dcp.name
        temp_base_xml = temp_dir / f"{selected_dcp.stem}.xml"
        shutil.copy2(selected_dcp, temp_base_dcp)

        print(f"\nDecompiling base profile '{selected_dcp.name}'...")
        res = subprocess.run([dcptool_bin, "-d", str(temp_base_dcp), str(temp_base_xml)], capture_output=True, text=True)
        if res.returncode != 0 or not temp_base_xml.is_file():
            err_msg = (res.stderr or res.stdout).strip()
            sys.exit(f"dcpTool decompile failed: {err_msg if err_msg else 'Unknown error'}")

        with open(temp_base_xml, "r", encoding="utf-8", errors="ignore") as f:
            base_xml_content = f.read()

        cleaned_base_xml = re.sub(r"<LookTable[\s\S]*?</LookTable>", "", base_xml_content)

        successful_dcps = []
        failed_dcps = []

        print(f"\nBuilding profiles for {camera_name}:")
        for txt_file in txt_files:
            look_name = clean_look_name(txt_file.stem)
            
            # In Lightroom UI: "Fuji <Name>" (e.g. "Fuji Astia", "Fuji Classic Chrome")
            display_name = f"Fuji {look_name}"
            
            # Descriptive filename on disk
            target_dcp = out_dir / f"{camera_name} - {look_name}.dcp"

            with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
                replacement_snippet = f.read().strip()

            if re.search(r"<ToneCurve[\s\S]*?</ToneCurve>", cleaned_base_xml):
                modified_xml = re.sub(r"<ToneCurve[\s\S]*?</ToneCurve>", replacement_snippet, cleaned_base_xml, count=1)
            else:
                match = re.search(r"</\w+>\s*$", cleaned_base_xml)
                idx = match.start()
                modified_xml = cleaned_base_xml[:idx] + replacement_snippet + "\n" + cleaned_base_xml[idx:]

            # Apply required metadata tags
            modified_xml = set_xml_tag(modified_xml, "DefaultBlackRender", "1")
            modified_xml = set_xml_tag(modified_xml, "ProfileLookTableEncoding", "1")
            modified_xml = set_xml_tag(modified_xml, "ProfileName", display_name)

            target_xml = temp_dir / f"{look_name}.xml"
            with open(target_xml, "w", encoding="utf-8") as f:
                f.write(modified_xml)

            compile_res = subprocess.run([dcptool_bin, "-c", str(target_xml), str(target_dcp)], capture_output=True, text=True)
            if compile_res.returncode == 0 and target_dcp.is_file():
                print(f"  [OK] '{display_name}' -> {target_dcp.name}")
                successful_dcps.append(target_dcp)
            else:
                err_msg = (compile_res.stderr or compile_res.stdout).strip()
                print(f"  [FAILED] {target_dcp.name}: {err_msg if err_msg else 'Unknown error'}")
                failed_dcps.append((display_name, err_msg))

    if not successful_dcps:
        sys.exit("\nError: No profiles could be compiled. Aborting.")

    if failed_dcps:
        print(f"\nBuild finished with {len(failed_dcps)} failure(s). {len(successful_dcps)} profile(s) saved to: {out_dir}")
    else:
        print(f"\nBuild complete. All profiles saved to: {out_dir}")

    # Installation Prompt
    print("\n--- Deployment ---")
    if ask_yes_no("Do you want to install these profiles directly to Lightroom/CameraRaw?", default=True):
        target_install_dir = user_profiles_dir / f"Fujifilm Simulations {camera_name}"
        target_install_dir.mkdir(parents=True, exist_ok=True)
        for dcp in successful_dcps:
            shutil.copy2(dcp, target_install_dir / dcp.name)

        print(f"\nSuccessfully installed {len(successful_dcps)} profile(s) to:\n{target_install_dir}")
        print("\nRestart Lightroom Classic to load the profiles.")
    else:
        print(f"\nManual installation: Copy the folder '{out_dir.name}' to:\n{user_profiles_dir}")

if __name__ == "__main__":
    main()
