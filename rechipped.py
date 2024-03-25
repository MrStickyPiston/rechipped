import os
import json
import shutil


# Function to read JSON files and extract values
def extract_values_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        if 'values' in data:
            return data['values']
        else:
            return None


# Function to write data to the output file
def write_to_output(values, output_file):
    with open(output_file, 'w') as file:
        json.dump({
            "type": "rechiseled:chiseling",
            "overwrite": False,
            "entries": [{"item": value} for value in values]
        }, file, indent=2)


# Directory paths
lib = './lib'
datapack_base = lib + '/datapack'
item_dir = lib + '/chipped/data/chipped/tags/items'

dist = './dist'
output_file = dist + '/rechipped'
output_dir = dist + '/rechipped/data/rechipped/chiseling_recipes'
pack_mcmeta_file = dist + '/rechipped/pack.mcmeta'

# Ensure output directory exists
try:
    shutil.rmtree(output_file)
except OSError:
    pass

shutil.copytree(datapack_base, output_file)

os.makedirs(output_dir, exist_ok=True)

# Iterate through files in input directory
for filename in os.listdir(item_dir):
    if filename.endswith('.json'):
        input_file_path = os.path.join(item_dir, filename)
        output_file_path = os.path.join(output_dir, filename)

        # Extract values from JSON file
        values = extract_values_from_json(input_file_path)
        if values:
            write_to_output(values, output_file_path)
            print(f"Data written to {output_file_path}")
        else:
            print(f"No 'values' found in {input_file_path}. Skipping.")

# Write pack.mcmeta file
pack_mcmeta_content = {
    "pack": {
        "pack_format": 9,
        "description": "Chipped recipes in rechiseled"
    }
}

with open(pack_mcmeta_file, 'w') as mcmeta:
    json.dump(pack_mcmeta_content, mcmeta, indent=2)

print(f"pack.mcmeta file written to {pack_mcmeta_file}")

shutil.make_archive(output_file, 'zip', output_file)
