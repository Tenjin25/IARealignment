import csv
import json
import os
import glob
from datetime import datetime
from collections import defaultdict

# Competitiveness categorization system
categorization_system = {
    "competitiveness_scale": {
        "Republican": [
            {"category": "Annihilation", "range": "R+40%+", "color": "#67000d", "min": 40, "max": 100},
            {"category": "Dominant", "range": "R+30-40%", "color": "#a50f15", "min": 30, "max": 40},
            {"category": "Stronghold", "range": "R+20-30%", "color": "#cb181d", "min": 20, "max": 30},
            {"category": "Safe", "range": "R+10-20%", "color": "#ef3b2c", "min": 10, "max": 20},
            {"category": "Likely", "range": "R+5.5-10%", "color": "#fb6a4a", "min": 5.5, "max": 10},
            {"category": "Lean", "range": "R+1-5.5%", "color": "#fcae91", "min": 1, "max": 5.5},
            {"category": "Tilt", "range": "R+0.5-1%", "color": "#fee8c8", "min": 0.5, "max": 1}
        ],
        "Tossup": [
            {"category": "Tossup", "range": "±0.5%", "color": "#f7f7f7", "min": -0.5, "max": 0.5}
        ],
        "Democratic": [
            {"category": "Tilt", "range": "D+0.5-1%", "color": "#e1f5fe", "min": -1, "max": -0.5},
            {"category": "Lean", "range": "D+1-5.5%", "color": "#c6dbef", "min": -5.5, "max": -1},
            {"category": "Likely", "range": "D+5.5-10%", "color": "#9ecae1", "min": -10, "max": -5.5},
            {"category": "Safe", "range": "D+10-20%", "color": "#6baed6", "min": -20, "max": -10},
            {"category": "Stronghold", "range": "D+20-30%", "color": "#3182bd", "min": -30, "max": -20},
            {"category": "Dominant", "range": "D+30-40%", "color": "#08519c", "min": -40, "max": -30},
            {"category": "Annihilation", "range": "D+40%+", "color": "#08306b", "min": -100, "max": -40}
        ]
    }
}

def categorize_margin(margin):
    """Categorize a margin based on the competitiveness scale"""
    all_categories = (categorization_system["competitiveness_scale"]["Republican"] + 
                     categorization_system["competitiveness_scale"]["Tossup"] +
                     categorization_system["competitiveness_scale"]["Democratic"])
    
    for cat in all_categories:
        if cat["min"] <= margin < cat["max"]:
            party = "Republican" if margin > 0.5 else ("Democratic" if margin < -0.5 else "Tossup")
            code = f"{party[0]}_{'TOSSUP' if party == 'Tossup' else cat['category'].upper()}"
            if party == "Tossup":
                code = "TOSSUP"
            return {
                "category": cat["category"],
                "party": party,
                "code": code,
                "color": cat["color"]
            }
    
    # Handle edge cases
    if margin >= 40:
        cat = categorization_system["competitiveness_scale"]["Republican"][0]
        return {"category": cat["category"], "party": "Republican", "code": "R_ANNIHILATION", "color": cat["color"]}
    elif margin <= -40:
        cat = categorization_system["competitiveness_scale"]["Democratic"][-1]
        return {"category": cat["category"], "party": "Democratic", "code": "D_ANNIHILATION", "color": cat["color"]}
    
    return None

def infer_party_from_candidate(candidate_name, year=None):
    """Infer party affiliation from candidate name based on known candidates"""
    candidate_lower = candidate_name.lower()
    
    # Presidential candidates (use full names to avoid false matches)
    presidential_dems = [
        'joseph r. biden', 'joe biden', 'biden',
        'barack obama', 'obama',
        'hillary clinton', 'bill clinton', 'clinton',
        'al gore', 'gore',
        'john kerry', 'kerry',
        'michael dukakis', 'dukakis',
        'walter mondale', 'mondale',
        'jimmy carter', 'carter',
        'kamala harris', 'kamala d. harris'
    ]
    presidential_reps = [
        'donald trump', 'donald j. trump', 'trump',
        'john mccain', 'mccain',
        'mitt romney', 'romney',
        'george bush', 'george w. bush', 'bush',
        'bob dole', 'dole',
        'ronald reagan', 'reagan',
        'michael pence', 'michael r. pence', 'pence'
    ]
    
    # Iowa-specific candidates (use more specific names)
    iowa_dems = [
        'chet culver', 'culver/judge',
        'patty judge', 'judge/hart',
        'tom harkin', 'harkin',
        'bruce braley', 'braley',
        'fred hubbell', 'hubbell',
        'rita hart', 'rita r. hart',
        'abby finkenauer', 'finkenauer',
        'theresa greenfield', 'greenfield',
        'michael franken', 'mike franken',
        'michael a. mauro', 'michael mauro',
        'roxanne conlin', 'conlin',
        'deidre dejear', 'dejear',
        # Statewide officials
        'tom miller',  # Attorney General
        'michael l. fitzgerald', 'michael fitzgerald',  # Treasurer
        'francis thicke',  # Agriculture
        'tim gannon',  # Agriculture
        'rob sand',  # Auditor
        'jonathan neiderbach', 'jon murphy'  # Auditor
    ]
    iowa_reps = [
        'terry branstad', 'terry e. branstad', 'branstad/reynolds',
        'kim reynolds', 'reynolds/gregg',
        'chuck grassley', 'grassley',
        'joni ernst', 'ernst',
        'steve king', 'king (r-', # More specific for Rep Steve King
        'mariannette miller-meeks', 'miller-meeks',
        'ashley hinson', 'hinson',
        'matt schultz', 'schultz',
        'paul pate', 'paul d. pate', 'pate',
        # Statewide officials
        'brenna findley',  # Attorney General 2010
        'adam gregg',  # Attorney General 2018 (also Lt. Governor)
        'david a. vaudt', 'david vaudt',  # Auditor
        'mary mosiman',  # Auditor
        'bill northey',  # Agriculture
        'mike naig',  # Agriculture
        'david d. jamison', 'david jamison',  # Treasurer
        'jeremy davis', 'jeremy n. davis',  # Treasurer
        'sam clovis'  # Treasurer
    ]
    
    # Check presidential candidates first (more specific matches)
    for dem_name in presidential_dems:
        if dem_name in candidate_lower:
            return 'DEM'
    
    for rep_name in presidential_reps:
        if rep_name in candidate_lower:
            return 'REP'
    
    # Then check Iowa candidates
    for dem_name in iowa_dems:
        if dem_name in candidate_lower:
            return 'DEM'
    
    for rep_name in iowa_reps:
        if rep_name in candidate_lower:
            return 'REP'
    
    return None

def process_csv_file(csv_path):
    """Process a single CSV file and return aggregated county data"""
    # Define offices we're interested in - including variations
    target_offices = {
        "President",
        "President/Vice President",
        "U.S. Senate",
        "US Senate",
        "U.S. Senator",
        "Governor",
        "Secretary of State",
        "Auditor of State",
        "State Auditor",
        "Treasurer of State",
        "State Treasurer",
        "Secretary of Agriculture",
        "Attorney General"
    }
    
    # Normalize office names to standard format
    def normalize_office(office):
        if "President" in office:
            return "President"
        if "Senate" in office or "Senator" in office:
            return "U.S. Senate"
        # Only match state-level offices, not county offices
        if "Auditor of State" in office or "State Auditor" in office:
            return "Auditor of State"
        if "Treasurer of State" in office or "State Treasurer" in office:
            return "Treasurer of State"
        return office
    
    counties = defaultdict(lambda: defaultdict(dict))
    offices = set()
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            
            # Check if this is a valid election file
            if 'county' not in csv_reader.fieldnames and 'jurisdiction' not in csv_reader.fieldnames:
                return None
            
            for row in csv_reader:
                # Check if this is county-level data
                reporting_level = row.get('reporting_level', 'county')
                if reporting_level and reporting_level != 'county':
                    continue
                
                # Handle both 'county' and 'jurisdiction' column names
                county = row.get('county', '') or row.get('jurisdiction', '')
                county = county.strip().upper()  # Normalize county names to uppercase
                if not county:
                    continue
                    
                office = row.get('office', 'Unknown')
                
                # Normalize the office name first
                normalized_office = normalize_office(office)
                
                # Skip if not in target offices (check both original and normalized)
                if office not in target_offices and normalized_office not in target_offices:
                    continue
                    
                district = row.get('district', None)
                if district:
                    district = district.strip()
                candidate = row.get('candidate', '').strip()
                
                # Skip non-candidate rows
                if not candidate or candidate in ['Totals', 'Total', 'Write-In Votes', 'Write-in', 
                                                   'Over Votes', 'Under Votes', 'Undervotes', 'Overvotes']:
                    continue
                
                party = row.get('party', '').strip()
                
                # If party is empty, try to infer from candidate name
                if not party or party == '':
                    # Extract year from filename
                    year_match = os.path.basename(csv_path)[:4]
                    party = infer_party_from_candidate(candidate, year_match)
                
                # Normalize party names (case-insensitive)
                if party:
                    party_lower = party.lower()
                    if 'democrat' in party_lower or party == 'DEM' or party_lower == 'dem':
                        party = 'DEM'
                    elif 'republican' in party_lower or party == 'REP' or party_lower == 'rep':
                        party = 'REP'
                    elif 'libertarian' in party_lower:
                        party = 'LIB'
                    elif 'green' in party_lower:
                        party = 'GRN'
                    elif party not in ['', 'Nominated by Petition', 'Nominated By Petition']:
                        party = 'OTH'
                
                # Handle both integer and floating-point vote values
                try:
                    vote_str = row.get('votes', '0').strip()
                    votes = int(float(vote_str)) if vote_str else 0
                except (ValueError, AttributeError):
                    votes = 0
                
                offices.add(normalized_office)
                
                # Create unique key for office/district combination using normalized name
                office_key = f"{normalized_office}" + (f" District {district}" if district else "")
                
                if office_key not in counties[county]:
                    counties[county][office_key] = {
                        "office": normalized_office,
                        "district": district,
                        "candidates": defaultdict(lambda: {"votes": 0, "party": None}),
                        "total_votes": 0,
                        "dem_votes": 0,
                        "rep_votes": 0
                    }
                
                # Aggregate votes by candidate
                counties[county][office_key]["candidates"][candidate]["votes"] += votes
                counties[county][office_key]["candidates"][candidate]["party"] = party
                counties[county][office_key]["total_votes"] += votes
                
                if party == "DEM":
                    counties[county][office_key]["dem_votes"] += votes
                elif party == "REP":
                    counties[county][office_key]["rep_votes"] += votes
    
    except Exception as e:
        print(f"  Error: {e}")
        return None
    
    if not dict(counties):
        return None
    
    # Process and categorize each county - organize by county name as key
    processed_counties = {}
    
    for county in sorted(counties.keys()):
        for office_key in counties[county]:
            race = counties[county][office_key]
            
            # Calculate margins and categorization
            if race["total_votes"] > 0:
                dem_pct = (race["dem_votes"] / race["total_votes"]) * 100
                rep_pct = (race["rep_votes"] / race["total_votes"]) * 100
                two_party_total = race["dem_votes"] + race["rep_votes"]
                two_party_pct = (two_party_total / race["total_votes"]) * 100 if race["total_votes"] > 0 else 0
                margin = race["rep_votes"] - race["dem_votes"]  # Raw vote margin
                margin_pct = ((race["rep_votes"] - race["dem_votes"]) / two_party_total * 100) if two_party_total > 0 else 0
                
                categorization = categorize_margin(margin_pct)
                
                # Get candidate names
                dem_candidate = ""
                rep_candidate = ""
                all_parties = {}
                
                for name, data in race["candidates"].items():
                    party = data["party"]
                    votes = data["votes"]
                    all_parties[party if party else "OTHER"] = votes
                    
                    if party == "DEM" or party == "Democratic":
                        dem_candidate = name
                    elif party == "REP" or party == "Republican":
                        rep_candidate = name
                
                other_votes = race["total_votes"] - two_party_total
                winner = "REP" if margin > 0 else ("DEM" if margin < 0 else "TIE")
                
                # Create contest key (county name + office to allow multiple offices per county)
                contest_key = f"{county}_{race['office']}"
                
                if contest_key not in processed_counties:
                    processed_counties[contest_key] = {
                        "county": county,
                        "contest": race["office"],
                        "dem_candidate": dem_candidate,
                        "rep_candidate": rep_candidate,
                        "dem_votes": race["dem_votes"],
                        "rep_votes": race["rep_votes"],
                        "other_votes": other_votes,
                        "total_votes": race["total_votes"],
                        "two_party_total": two_party_total,
                        "margin": margin,
                        "margin_pct": round(margin_pct, 2),
                        "winner": winner,
                        "competitiveness": categorization,
                        "all_parties": all_parties
                    }
                    
                    if race["district"]:
                        processed_counties[contest_key]["district"] = race["district"]
    
    return {
        "results": processed_counties,
        "offices": sorted(list(offices))
    }

# Find all CSV files in Data directory
data_dir = "Data"
csv_files = []

# Get CSV files from root Data directory
csv_files.extend(glob.glob(os.path.join(data_dir, "*__ia__general__*.csv")))

# Get CSV files from subdirectories
for subdir in ["2012", "2018", "2020", "2022"]:
    subdir_path = os.path.join(data_dir, subdir)
    if os.path.exists(subdir_path):
        # Get the consolidated county or precinct files
        csv_files.extend(glob.glob(os.path.join(subdir_path, "*__ia__general__county.csv")))
        csv_files.extend(glob.glob(os.path.join(subdir_path, "*__ia__general__precinct.csv")))
        # Also get per-county precinct files (format: *__ia__general__[countyname]__precinct.csv)
        csv_files.extend(glob.glob(os.path.join(subdir_path, "*__ia__general__*__precinct.csv")))

# Sort files by date
csv_files.sort()

print(f"Found {len(csv_files)} CSV files to process")

# Process all files and create a comprehensive JSON organized by year
results_by_year = defaultdict(lambda: defaultdict(dict))

def get_contest_category(office):
    """Categorize office into contest type"""
    if office == "President":
        return "presidential"
    elif office == "U.S. Senate":
        return "senate"
    elif office == "Governor":
        return "gubernatorial"
    else:
        return "statewide"

for csv_file in csv_files:
    filename = os.path.basename(csv_file)
    print(f"Processing: {filename}")
    
    # Extract date from filename (YYYYMMDD format)
    date_str = filename[:8]
    try:
        election_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
        year = date_str[:4]
    except:
        election_date = "Unknown"
        year = "Unknown"
    
    result = process_csv_file(csv_file)
    
    if result:
        # Organize results by office/contest
        for office in result["offices"]:
            contest_category = get_contest_category(office)
            
            # Create contest key
            contest_key = office.lower().replace(" ", "_").replace(".", "") + "_" + year
            contest_name = office.upper()
            
            # Filter results for this office only
            office_results = {}
            for county_key, county_data in result["results"].items():
                if county_data["contest"] == office:
                    county_data["year"] = year
                    # Use just the county name as the key in the final output
                    county_name = county_data["county"]
                    office_results[county_name] = county_data
            
            if office_results:
                if contest_key not in results_by_year[year][contest_category]:
                    results_by_year[year][contest_category][contest_key] = {
                        "contest_name": contest_name,
                        "results": office_results
                    }
        
        print(f"  [OK] Processed {len(result['results'])} counties, {len(result['offices'])} offices")
    else:
        print(f"  [SKIP] Skipped (no valid data)")

# Create final comprehensive JSON
output_data = {
    "state": "Iowa",
    "election_type": "General Elections",
    "processed_date": datetime.now().strftime("%Y-%m-%d"),
    "categorization_system": categorization_system,
    "summary": {
        "total_years": len(results_by_year),
        "years": sorted(results_by_year.keys())
    },
    "results_by_year": dict(results_by_year)
}

# Write to JSON file
output_path = "Data/comprehensive_iowa_elections_analysis.json"
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=2)

print(f"\n{'='*60}")
print(f"Comprehensive election analysis complete!")
print(f"Total years processed: {len(results_by_year)}")
print(f"Years: {', '.join(sorted(results_by_year.keys()))}")
print(f"Saved to: {output_path}")
print(f"{'='*60}")
