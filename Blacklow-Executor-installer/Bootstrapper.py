import os
import ctypes
import requests
import zipfile
import io
import shutil
import subprocess
import sys
import traceback

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_desktop_path():
    return os.path.join(os.environ['USERPROFILE'], 'Desktop')

def pause():
    input("\nPress Enter to exit...")

def download_and_extract_release(destination_folder):
    zip_url = "https://github.com/BlacklowTechnologies/Source-Code/archive/refs/heads/main.zip"

    print("\n🔄 Downloading the GitHub repository zip file...")
    response = requests.get(zip_url)
    response.raise_for_status()

    print("✅ Zip file downloaded successfully.")
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        release_folder = "Source-Code-main/Blacklow-Executor-Source-code/Executor-Source-code/Blacklow-Executor by Blacklow Technologies/bin/Release"
        members = [f for f in z.namelist() if f.startswith(release_folder)]

        print(f"\n📁 Extracting contents from Release folder to: {destination_folder}")
        extracted_files = 0
        for member in members:
            filename = os.path.relpath(member, release_folder)
            if filename == "." or member.endswith("/"):
                continue  # skip folders and root

            target_path = os.path.join(destination_folder, filename)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            with z.open(member) as source, open(target_path, "wb") as target:
                shutil.copyfileobj(source, target)
                extracted_files += 1
                print(f"   → Extracted: {filename}")

        print(f"\n✅ Finished extracting {extracted_files} files.")

def run_exe_as_admin(path_to_exe):
    print(f"\n🚀 Launching the executable as administrator: {path_to_exe}")
    ctypes.windll.shell32.ShellExecuteW(None, "runas", path_to_exe, None, None, 1)

if __name__ == '__main__':
    try:
        if not is_admin():
            print("🔐 Re-launching the script with administrator privileges...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            sys.exit()

        print("✅ Script is running with administrator rights.")

        # Define folder
        desktop_path = get_desktop_path()
        executor_folder = os.path.join(desktop_path, "Blacklow-Executor")

        print(f"\n📦 Creating folder on Desktop: {executor_folder}")
        os.makedirs(executor_folder, exist_ok=True)

        # Download and extract content
        download_and_extract_release(executor_folder)

        # Run the correct .exe with the proper name
        exe_name = "Blacklow Executor.exe"
        exe_path = os.path.join(executor_folder, exe_name)
        if os.path.exists(exe_path):
            run_exe_as_admin(exe_path)
        else:
            print(f"\n❌ ERROR: '{exe_name}' was not found in the folder.\n")

    except Exception as e:
        print("\n🔥 An error occurred:\n")
        traceback.print_exc()

    pause()
