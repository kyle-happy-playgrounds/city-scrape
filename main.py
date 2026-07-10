import os
import subprocess
import glob
import importlib
import json
import shutil

def run_scrapers():
    output_dir = "public_data"
    os.makedirs(output_dir, exist_ok=True)
    
    master_data = [] 

    for file_path in glob.glob("scrapers/*.py"):
        filename = os.path.basename(file_path)
        
        if filename.startswith("__") or filename == "custom_city.py":
            continue

        module_name = filename.replace(".py", "")
        output_folder = f"{output_dir}/{module_name}"
        final_file = f"{output_dir}/{module_name}.json"
        
        module = importlib.import_module(f"scrapers.{module_name}")
        class_name = module.get_scraper().__class__.__name__

        print(f"Running scraper: {module_name}...")
        
        cmd = [
            "pipenv", "run", "spatula", "scrape", 
            f"scrapers.{module_name}.{class_name}", 
            "-o", output_folder
        ]
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            combined_data = []
            for uuid_file in glob.glob(f"{output_folder}/*.json"):
                with open(uuid_file, "r") as f:
                    combined_data.append(json.load(f))
            
            with open(final_file, "w") as f:
                json.dump(combined_data, f, indent=2)
                
            shutil.rmtree(output_folder)
            
            # --- ADD THIS: Add this city's data to the master list ---
            master_data.extend(combined_data)
            
            print(f"Success! Merged {len(combined_data)} documents into {final_file}\n")
        else:
            print(f"❌ Failed to run {module_name}\n")

    # --- ADD THIS: Write the master file at the very end ---
    master_file = f"{output_dir}/all_data.json"
    with open(master_file, "w") as f:
        json.dump(master_data, f, indent=2)

    # Copy the HTML frontend into the public folder
    shutil.copy("index.html", f"{output_dir}/index.html")
    print(f"Created master dataset with {len(master_data)} total documents at {master_file}!")

if __name__ == "__main__":
    run_scrapers()