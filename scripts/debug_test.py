import csv

csv_path = "Data/20021105__ia__general__county.csv"

count = 0
senate_count = 0

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        count += 1
        if row['office'] == 'U.S. Senate':
            senate_count += 1
            if senate_count <= 3:
                print(f"Row {count}: Office={row['office']}, County={row.get('county') or row.get('jurisdiction')}, Candidate={row['candidate']}, Party={row['party']}")

print(f"\nTotal rows: {count}")
print(f"U.S. Senate rows: {senate_count}")
