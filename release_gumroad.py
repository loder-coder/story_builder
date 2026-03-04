import os
import subprocess
import shutil
import zipfile
import glob
import sys

def run(cmd, cwd=None):
    print(f"Running: {cmd} in {cwd or '.'}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def main():
    # 1. Cleanup
    dirs_to_clean = ["dist", "pro/dist", "gumroad", "build", "pro/build", "story_builder.egg-info", "pro/story_builder_pro.egg-info"]
    for d in dirs_to_clean:
        if os.path.exists(d):
            print(f"Cleaning {d}...")
            shutil.rmtree(d, ignore_errors=True)

    # 2. Build Lite
    print("\n--- Building Lite Wheel ---")
    run(f"{sys.executable} -m build --wheel")

    # 3. Build Pro
    print("\n--- Building Pro Wheel ---")
    run(f"{sys.executable} -m build --wheel", cwd="pro")

    # 4. Prepare Gumroad Package
    print("\n--- Packaging for Gumroad ---")
    os.makedirs("gumroad", exist_ok=True)
    
    zip_path = "gumroad/story_builder_pro_package.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add Lite Wheel
        lite_wheels = glob.glob("dist/*.whl")
        if not lite_wheels:
            print("Error: Lite wheel not found!")
            sys.exit(1)
        zipf.write(lite_wheels[0], os.path.basename(lite_wheels[0]))

        # Add Pro Wheel
        pro_wheels = glob.glob("pro/dist/*.whl")
        if not pro_wheels:
            print("Error: Pro wheel not found!")
            sys.exit(1)
        zipf.write(pro_wheels[0], os.path.basename(pro_wheels[0]))

        # Add Docs & Meta
        files_to_include = [
            ("pro/README_PRO.md", "README_PRO.md"),
            ("pro/LICENSE_PRO.txt", "LICENSE_PRO.txt"),
            ("CHANGELOG.md", "CHANGELOG.md"),
        ]
        for src, dst in files_to_include:
            if os.path.exists(src):
                zipf.write(src, dst)

        # Add Examples
        examples_to_include = [
            ("pro/examples/ai_generate_demo.py", "examples/ai_generate_demo.py"),
            ("examples/minimal_story.json", "examples/minimal_story.json")
        ]
        for src, dst in examples_to_include:
            if os.path.exists(src):
                zipf.write(src, dst)

    print(f"\n[SUCCESS] Package created: {zip_path}")

    # 5. Print Instructions
    lite_wheel = os.path.basename(glob.glob("dist/*.whl")[0])
    pro_wheel = os.path.basename(pro_wheels[0])

    print("\n" + "="*50)
    print("GUMROAD CUSTOMER INSTRUCTIONS")
    print("="*50)
    print("Thank you for purchasing Story Builder Pro!")
    print("\nTo install and get started:")
    print(f"1. Install the core Lite engine first (if not already installed):")
    print(f"   pip install {lite_wheel}")
    print(f"\n2. Install the Pro package from the zip:")
    print(f"   pip install {pro_wheel}")
    print("\n3. Set your API Key:")
    print("   export OPENROUTER_API_KEY=your_key")
    print("\n4. Run the demo:")
    print("   python examples/ai_generate_demo.py")
    print("="*50)

if __name__ == "__main__":
    main()
