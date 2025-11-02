import csv
import json
from datetime import datetime
from collections import defaultdict

# Path to your CSV file
csv_path = "Data/20221108__ia__general__precinct.csv"
# Output JSON path
json_path = "Data/20221108__ia__general__county_analysis.json"

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

# Read CSV and organize data by county
counties = defaultdict(lambda: defaultdict(dict))
offices = set()
all_counties = set()

with open(csv_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        county = row['county']
        office = row['office']
        district = row['district'] if row['district'] else None
        candidate = row['candidate']
        party = row['party']
        votes = int(row['votes']) if row['votes'] else 0
        
        all_counties.add(county)
        offices.add(office)
        
        # Create unique key for office/district combination
        office_key = f"{office}" + (f" District {district}" if district else "")
        
        if office_key not in counties[county]:
            counties[county][office_key] = {
                "office": office,
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

# Process and categorize each county
processed_counties = []

for county in sorted(counties.keys()):
    county_data = {
        "county": county,
        "races": []
    }
    
    for office_key in counties[county]:
        race = counties[county][office_key]
        
        # Calculate margins and categorization
        if race["total_votes"] > 0:
            dem_pct = (race["dem_votes"] / race["total_votes"]) * 100
            rep_pct = (race["rep_votes"] / race["total_votes"]) * 100
            margin = rep_pct - dem_pct  # Positive = Republican lead
            
            categorization = categorize_margin(margin)
            
            # Convert candidates dict to list
            candidates_list = [
                {
                    "name": name,
                    "party": data["party"],
                    "votes": data["votes"],
                    "percentage": round((data["votes"] / race["total_votes"]) * 100, 2)
                }
                for name, data in race["candidates"].items()
            ]
            # Sort by votes descending
            candidates_list.sort(key=lambda x: x["votes"], reverse=True)
            
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
                "candidates": candidates_list
            }
            
            county_data["races"].append(race_data)
    
    processed_counties.append(county_data)

# Create final JSON structure
output_data = {
    "election_date": "2022-11-08",
    "state": "Iowa",
    "election_type": "General Election",
    "processed_date": "2025-01-07",
    "aggregation_level": "county",
    "categorization_system": categorization_system,
    "summary": {
        "total_counties": len(processed_counties),
        "offices": sorted(list(offices))
    },
    "counties": processed_counties
}

# Write to JSON file
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, indent=2)

print(f"County-aggregated election JSON created")
print(f"Total counties: {len(processed_counties)}")
print(f"Offices: {', '.join(sorted(list(offices)))}")
print(f"Saved to: {json_path}")
