import csv
import json

# Path to your CSV file
csv_path = "Data/20221108__ia__general__precinct.csv"
# Output JSON path
json_path = "Data/20221108__ia__general__precinct.json"

# Read CSV and convert to JSON
data = []
with open(csv_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data.append(row)

# Write to JSON file
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=2)

print(f"JSON file created with {len(data)} records")
print(f"Saved to: {json_path}")
