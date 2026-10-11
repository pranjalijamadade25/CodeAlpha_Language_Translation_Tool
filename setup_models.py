
import argostranslate.package

print("Updating the translation model list...")

argostranslate.package.update_package_index()
packages = argostranslate.package.get_available_packages()

# Find models that translate to or from English
selected = {}

for package in packages:
    if package.from_code == "en" or package.to_code == "en":
        key = (package.from_code, package.to_code)

        # Keep one model for each language pair
        if key not in selected:
            selected[key] = package

print("Models found:", len(selected))
print("Downloads may take a long time and use several GB of data.")

failed = []

for i, (pair, package) in enumerate(selected.items(), start=1):
    source, target = pair
    print(f"\n[{i}/{len(selected)}] Installing {source} -> {target}")

    try:
        model_path = package.download()
        argostranslate.package.install_from_path(model_path)
        print("Installed successfully.")
    except Exception as error:
        failed.append(f"{source} -> {target}: {error}")
        print("Installation failed:", error)

print("\nInstallation process finished.")

if failed:
    print("\nFailed models:")
    for item in failed:
        print("-", item)
else:
    print("All selected models installed successfully.")