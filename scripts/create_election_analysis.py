import csv
import json
from datetime import datetime
from collections import defaultdict

# Path to your CSV file
csv_path = "Data/20221108__ia__general__precinct.csv"
# Output JSON path
json_path = "Data/20221108__ia__general__precinct_analysis.json"

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
            return {
                "category": cat["category"],
                "range": cat["range"],
                "color": cat["color"],
                "margin": margin
            }
    
    # Handle edge case for exactly max value
    if margin >= 40:
        cat = categorization_system["competitiveness_scale"]["Republican"][0]
        return {"category": cat["category"], "range": cat["range"], "color": cat["color"], "margin": margin}
    elif margin <= -40:
        cat = categorization_system["competitiveness_scale"]["Democratic"][-1]
        return {"category": cat["category"], "range": cat["range"], "color": cat["color"], "margin": margin}
    
    return None

# Read CSV and organize data
precincts = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
offices = set()
counties = set()

with open(csv_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        county = row['county']
        precinct = row['precinct']
        office = row['office']
        district = row['district'] if row['district'] else None
        candidate = row['candidate']
        party = row['party']
        votes = int(row['votes']) if row['votes'] else 0
        
        counties.add(county)
        offices.add(office)
        
        # Create unique key for office/district combination
        office_key = f"{office}" + (f" District {district}" if district else "")
        
        if office_key not in precincts[county][precinct]:
            precincts[county][precinct][office_key] = {
                "office": office,
                "district": district,
                "candidates": [],
                "total_votes": 0,
                "dem_votes": 0,
                "rep_votes": 0
            }
        
        precincts[county][precinct][office_key]["candidates"].append({
            "name": candidate,
            "party": party,
            "votes": votes
        })
        precincts[county][precinct][office_key]["total_votes"] += votes
        
        if party == "DEM":
            precincts[county][precinct][office_key]["dem_votes"] += votes
        elif party == "REP":
            precincts[county][precinct][office_key]["rep_votes"] += votes

# Process and categorize each precinct
processed_precincts = []

for county in precincts:
    for precinct in precincts[county]:
        precinct_data = {
            "county": county,
            "precinct": precinct,
            "races": []
        }
        
        for office_key in precincts[county][precinct]:
            race = precincts[county][precinct][office_key]
            
            # Calculate margins and categorization
            if race["total_votes"] > 0:
                dem_pct = (race["dem_votes"] / race["total_votes"]) * 100
                rep_pct = (race["rep_votes"] / race["total_votes"]) * 100
                margin = rep_pct - dem_pct  # Positive = Republican lead
                
                categorization = categorize_margin(margin)
                
                race_data = {
                    "office": race["office"],
                    "district": race["district"],
                    "total_votes": race["total_votes"],
                    "results": {
                        "democratic": {
                            "votes": race["dem_votes"],
                            "percentage": round(dem_pct, 2)
                        },
                        "republican": {
                            "votes": race["rep_votes"],
                            "percentage": round(rep_pct, 2)
                        },
                        "margin": {
                            "value": round(margin, 2),
                            "winner": "Republican" if margin > 0 else ("Democratic" if margin < 0 else "Tie")
                        }
                    },
                    "competitiveness": categorization,
                    "candidates": race["candidates"]
                }
                
                precinct_data["races"].append(race_data)
        
        processed_precincts.append(precinct_data)

# Create final JSON structure
output_data = {
    "election_date": "2022-11-08",
    "state": "Iowa",
    "election_type": "General Election",
    "processed_date": "2025-01-07",
    "categorization_system": categorization_system,
    "summary": {
        "total_precincts": len(processed_precincts),
        "total_counties": len(counties),
        "offices": sorted(list(offices))
    },
    "precincts": processed_precincts
}

# Write to JSON file
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=2)

print(f"Comprehensive election JSON created")
print(f"Total precincts: {len(processed_precincts)}")
print(f"Total counties: {len(counties)}")
print(f"Offices: {', '.join(sorted(list(offices)))}")
print(f"Saved to: {json_path}")
