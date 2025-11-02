import csv
import json
from collections import defaultdict

def categorize_margin(margin_pct):
    """
    Categorize the competitiveness based on margin percentage.
    Returns a dictionary with category, party, code, and color.
    """
    abs_margin = abs(margin_pct)
    
    if abs_margin < 0.5:
        return {
            "category": "Tossup",
            "party": "None",
            "code": "TOSSUP",
            "color": "#f7f7f7"
        }
    
    # Determine party
    party = "Republican" if margin_pct > 0 else "Democratic"
    party_code = "R" if margin_pct > 0 else "D"
    
    # Determine category based on margin
    if abs_margin >= 40:
        category = "Annihilation"
        color = "#67000d" if party == "Republican" else "#08306b"
    elif abs_margin >= 30:
        category = "Dominant"
        color = "#a50f15" if party == "Republican" else "#08519c"
    elif abs_margin >= 20:
        category = "Stronghold"
        color = "#cb181d" if party == "Republican" else "#2171b5"
    elif abs_margin >= 10:
        category = "Safe"
        color = "#ef3b2c" if party == "Republican" else "#4292c6"
    elif abs_margin >= 5.5:
        category = "Likely"
        color = "#fb6a4a" if party == "Republican" else "#6baed6"
    elif abs_margin >= 1:
        category = "Lean"
        color = "#fc9272" if party == "Republican" else "#9ecae1"
    else:  # 0.5 to 1
        category = "Tilt"
        color = "#fcbba1" if party == "Republican" else "#c6dbef"
    
    return {
        "category": category,
        "party": party,
        "code": f"{party_code}_{category.upper()}",
        "color": color
    }

def parse_2024_csv(csv_path):
    """
    Parse the 2024 wide-format CSV and return county-level results.
    """
    results = {}
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Skip the first 3 header rows and get to data
    data_lines = lines[3:]
    
    for line in data_lines:
        parts = line.strip().split(',')
        
        # Skip empty lines
        if not parts or not parts[0].strip():
            continue
        
        county = parts[0].strip()
        
        # Skip the "Total:" row
        if county.lower() == "total:" or county.lower() == "total":
            continue
        
        try:
            # Extract Total Votes for each candidate
            # Column positions based on the CSV structure:
            # 0: Precinct, 1: Registered Voters
            # 2-4: Harris (Election Day, Absentee, Total)
            # 5-7: Trump (Election Day, Absentee, Total)
            # 8-10: Oliver (Election Day, Absentee, Total)
            # 11-13: Ayyadurai (Election Day, Absentee, Total)
            # 14-16: De la Cruz (Election Day, Absentee, Total)
            # 17-19: Stodden (Election Day, Absentee, Total)
            # 20-22: Kennedy (Election Day, Absentee, Total)
            # 23-25: Write-in (Election Day, Absentee, Total)
            
            harris_votes = int(parts[4].strip()) if parts[4].strip() else 0
            trump_votes = int(parts[7].strip()) if parts[7].strip() else 0
            oliver_votes = int(parts[10].strip()) if parts[10].strip() else 0
            ayyadurai_votes = int(parts[13].strip()) if parts[13].strip() else 0
            delacruz_votes = int(parts[16].strip()) if parts[16].strip() else 0
            stodden_votes = int(parts[19].strip()) if parts[19].strip() else 0
            kennedy_votes = int(parts[22].strip()) if parts[22].strip() else 0
            writein_votes = int(parts[25].strip()) if parts[25].strip() else 0
            
            # Calculate totals
            dem_votes = harris_votes
            rep_votes = trump_votes
            other_votes = oliver_votes + ayyadurai_votes + delacruz_votes + stodden_votes + kennedy_votes + writein_votes
            total_votes = dem_votes + rep_votes + other_votes
            two_party_total = dem_votes + rep_votes
            
            # Calculate margin (positive = Republican, negative = Democratic)
            margin = rep_votes - dem_votes
            margin_pct = (margin / two_party_total * 100) if two_party_total > 0 else 0
            
            # Determine winner
            winner = "REP" if rep_votes > dem_votes else "DEM"
            
            # Get competitiveness
            competitiveness = categorize_margin(margin_pct)
            
            # Store result
            results[county.upper()] = {
                "county": county.upper(),
                "contest": "PRESIDENT",
                "year": "2024",
                "dem_candidate": "Kamala D. Harris/Tim Walz",
                "rep_candidate": "Donald J. Trump/JD Vance",
                "dem_votes": dem_votes,
                "rep_votes": rep_votes,
                "other_votes": other_votes,
                "total_votes": total_votes,
                "two_party_total": two_party_total,
                "margin": margin,
                "margin_pct": round(margin_pct, 2),
                "winner": winner,
                "competitiveness": competitiveness,
                "all_parties": {
                    "DEM": harris_votes,
                    "REP": trump_votes,
                    "LIB": oliver_votes,
                    "OTHER": ayyadurai_votes + delacruz_votes + stodden_votes + kennedy_votes + writein_votes
                }
            }
            
        except (IndexError, ValueError) as e:
            print(f"[SKIP] Error parsing county {county}: {e}")
            continue
    
    return results

def add_2024_to_comprehensive_json(json_path, results_2024):
    """
    Add 2024 results to the comprehensive JSON file.
    """
    # Load existing JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add 2024 to results_by_year
    if "2024" not in data["results_by_year"]:
        data["results_by_year"]["2024"] = {}
    
    if "presidential" not in data["results_by_year"]["2024"]:
        data["results_by_year"]["2024"]["presidential"] = {}
    
    # Add the contest
    data["results_by_year"]["2024"]["presidential"]["president_2024"] = {
        "contest_name": "PRESIDENT",
        "results": results_2024
    }
    
    # Save back to file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    
    return len(results_2024)

if __name__ == "__main__":
    csv_path = r"c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\IARealignment\Data\2024electionsummary.csv"
    json_path = r"c:\Users\Shama\OneDrive\Documents\Course_Materials\CPT-236\Side_Projects\IARealignment\Data\comprehensive_iowa_elections_analysis.json"
    
    print("Parsing 2024 election data...")
    results_2024 = parse_2024_csv(csv_path)
    
    print(f"Parsed {len(results_2024)} counties from 2024 data")
    
    print("Adding 2024 data to comprehensive JSON...")
    count = add_2024_to_comprehensive_json(json_path, results_2024)
    
    print(f"\n[OK] Successfully added 2024 presidential data")
    print(f"     Counties processed: {count}")
    print(f"     File: {json_path}")
