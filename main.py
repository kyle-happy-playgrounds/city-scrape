import os
import subprocess
import glob
import importlib

def run_scrapers():
    output_dir = "public_data"
    os.makedirs(output_dir, exist_ok=True)

    scraper_files = glob.glob("scrapers/*.py")

    for file_path in scraper_files:
        filename = os.path.basename(file_path)
        
        if filename.startswith("__") or filename == "custom_city.py":
            continue

        module_name = filename.replace(".py", "")
        

        module = importlib.import_module(f"scrapers.{module_name}")
        class_name =  module.get_scraper().__class__.__name__

        output_folder = f"{output_dir}/{module_name}"
        
        print(f"🚀 Running scraper: {module_name} (Class: {class_name})...")
        
        cmd = [
            "pipenv", "run", "spatula", "scrape", 
            f"scrapers.{module_name}.{class_name}", 
            "-o", output_folder
        ]
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print(f"Success! Saved to {output_folder}\n")
        else:
            print(f"Failed to run {module_name}\n")

if __name__ == "__main__":
    run_scrapers()