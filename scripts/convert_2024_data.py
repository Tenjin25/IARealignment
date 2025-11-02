import csv

# Read the 2024 election summary CSV and convert to standard format
input_file = 'Data/2024electionsummary.csv'
output_file = 'Data/20241105__ia__general__president__county.csv'

# Map candidate names to party
party_map = {
    'Kamala D. Harris and Tim Walz': 'Democratic',
    'Donald J. Trump and JD Vance': 'Republican',
    'Chase Oliver and Mike ter Maat': 'Libertarian',
    'Shiva Ayyadurai and Crystal Ellis': 'Independent',
    'Claudia De la Cruz and Karina Garcia': 'Party for Socialism and Liberation',
    'William P. Stodden and Stephanie H. Cholensky': 'Independent',
    'Robert F. Kennedy Jr and Nicole Shanahan': 'Independent',
    'Write-in': 'Write-In'
}

# Read CSV and extract candidate names from row 2 (index 1)
# Data starts at row 4 (index 3)
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Row 2 has candidate names
# Row 3 has column headers (Election Day, Absentee, Total Votes)
candidate_row = rows[1]
header_row = rows[2]

# Find candidates and their Total Votes column index
candidates = []
col_indices = []

for i, cell in enumerate(candidate_row):
    cell = cell.strip()
    if cell and cell in party_map:
        # Find the "Total Votes" column for this candidate
        # Look ahead for the next few columns
        for j in range(i, min(i+5, len(header_row))):
            if 'Total Votes' in header_row[j]:
                candidates.append(cell)
                col_indices.append(j)
                break

print(f"Found {len(candidates)} candidates:")
for name in candidates:
    print(f"  - {name}")

# Create output CSV
output_rows = []
for row in rows[3:]:  # Data starts at row 4 (index 3)
    if len(row) < 2:
        continue
    
    county = row[0].strip()
    if not county or county == 'Total':
        continue
    
    # Extract votes for each candidate
    for candidate, col_idx in zip(candidates, col_indices):
        if col_idx < len(row):
            try:
                votes_str = row[col_idx].strip()
                votes = int(votes_str) if votes_str else 0
                party = party_map.get(candidate, 'Other')
                output_rows.append({
                    'office': 'President/Vice President',
                    'district': '',
                    'candidate': candidate,
                    'party': party,
                    'county': county.upper(),
                    'votes': votes
                })
            except (ValueError, IndexError):
                pass

# Write output CSV
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['office', 'district', 'candidate', 'party', 'county', 'votes'])
    writer.writeheader()
    writer.writerows(output_rows)

print(f"\nConverted data saved to: {output_file}")
print(f"Total rows: {len(output_rows)}")

# Show sample
print("\nSample rows:")
for row in output_rows[:10]:
    print(f"  {row['county']}: {row['candidate']} ({row['party']}) - {row['votes']} votes")
