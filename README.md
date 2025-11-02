# 🗳️ Iowa Political Realignment Map (1980-2024)

An interactive visualization of Iowa's political transformation over 44 years, showing county-level voting patterns across presidential, senate, gubernatorial, and statewide contests.

![Iowa Political Realignment](preview.png)

## 🌟 Features

### Comprehensive Data Coverage
- **18 election cycles** from 1980 to 2024
- **99 Iowa counties** with complete voting records
- **Multiple contest types**: Presidential, US Senate, Governor, and Statewide races
- **Detailed metrics**: Vote counts, percentages, margins, and competitiveness ratings

### Interactive Visualization
- **Dynamic choropleth map** with 15-level competitiveness scale
- **County-level detail** with click-to-explore functionality
- **Contest selector** with grouped dropdown by race type
- **County search** with autocomplete and zoom-to-feature
- **Responsive sidebar** showing detailed results and statewide aggregates
- **Color-coded legend** from deep blue (Dem 40%+) to deep red (Rep 40%+)

### Political Insights
- Story County (Ames/Iowa State) - College town Democratic strength
- Johnson County (Iowa City/University of Iowa) - Liberal bastion
- Iowa's transformation from swing state to Republican-leaning
- Urban-rural divide analysis and demographic trends
- Historical context from 1980 through 2024

## 📊 Data Structure

```json
{
  "state": "Iowa",
  "results_by_year": {
    "2024": {
      "presidential": {
        "president_2024": {
          "contest_name": "President",
          "results": {
            "POLK": {
              "dem_votes": 150000,
              "rep_votes": 125000,
              "total_votes": 275000,
              "dem_candidate": "Kamala Harris",
              "rep_candidate": "Donald Trump",
              "winner": "DEM",
              "margin": 25000,
              "margin_pct": 9.09,
              "competitiveness": {
                "color": "#3182bd",
                "category": "Lean Democratic",
                "party": "DEM"
              }
            }
          }
        }
      }
    }
  }
}
```

## 🚀 Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for Mapbox GL JS and Turf.js CDN resources)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Tenjin25/IARealignment.git
   cd IARealignment
   ```

2. **Open in browser**
   Simply open `index.html` in your web browser

### Configuration

The map uses a Mapbox access token already configured in `index.html`. To use your own token:

1. Get a free token from [mapbox.com](https://account.mapbox.com/access-tokens/)
2. Replace the token in `index.html` (line ~916):
   ```javascript
   const CONFIG = {
     mapboxToken: 'YOUR_TOKEN_HERE',
     // ...
   };
   ```

## 📖 Usage Guide

### Basic Navigation

1. **View the Map**
   - The map loads centered on Iowa with all 99 counties visible
   - Default view shows counties in neutral gray until a contest is selected

2. **Select a Contest**
   - Use the dropdown in the top-left "Iowa Election Contests" panel
   - Contests are grouped by type (US President, US Senate, Governor, Statewide)
   - Most recent elections appear first (2024 → 1980)
   - Click to select - the map will update immediately with color-coded results

3. **Explore Counties**
   - **Click** any county to view detailed results in the right sidebar
   - **Hover** over counties to see the pointer cursor
   - Sidebar shows:
     - Winner and margin of victory
     - Vote totals and percentages for each candidate
     - Visual vote bar showing the split
     - Total votes cast
     - Competitiveness category

4. **Search for Counties**
   - Use the "Search Counties" box in the control panel
   - Type a county name (e.g., "Polk", "Story", "Johnson")
   - Select from autocomplete suggestions
   - Map automatically zooms to your selected county

5. **Understand the Colors**
   - Reference the legend in the bottom-left corner
   - Blue shades = Democratic wins (lighter = closer)
   - Red shades = Republican wins (lighter = closer)
   - Gray = Tossup (within 2%)
   - Darker colors = larger margins of victory

### Interpreting Results

**Sidebar Information:**
- **🏆 Winner Section**: Shows winning candidate and party with victory margin
- **Vote Bar**: Visual representation of the two-party vote split
- **Vote Details**: Exact vote counts and percentages for Democratic and Republican candidates
- **Total Votes**: Overall turnout for that contest in that county
- **Competitiveness Category**: Classification from "Annihilation" to "Tossup" to "Annihilation" on opposite side

**Statewide Results:**
When a contest is selected, the sidebar also displays Iowa's statewide aggregate:
- Total votes across all 99 counties
- Statewide winner and margin
- Overall vote percentages
- Statewide competitiveness rating

### Recommended Explorations

**See Iowa's Political Evolution:**
1. Select "President (2024)" - see Trump's dominant rural performance
2. Compare with "President (2008)" - see Obama's competitive showing
3. Try "President (1988)" - see Iowa as a true swing state

**Urban vs. Rural Divide:**
1. Select any recent presidential contest
2. Click on **Johnson County** (Iowa City) - deep blue
3. Click on **Story County** (Ames) - another blue spot
4. Compare with rural counties like Sioux, Lyon, or Osceola - deep red

**Track a Single County Over Time:**
1. Click on a county (e.g., **Polk County** - Des Moines)
2. Change the contest dropdown to different years
3. Watch how the county's political lean changes over 44 years

**Close Races:**
1. Look for light pink or light blue counties (Tilt/Lean categories)
2. These represent counties decided by less than 10%
3. Examples: Scott County, Linn County in some years

## 📁 Project Structure

```
IARealignment/
├── index.html                 # Main application (NCMap template adapted for Iowa)
├── OGTNMap.html              # Original Tennessee template (reference)
├── NCMap.html                # North Carolina template (reference)
├── index_working_iowa.html   # Backup of working Iowa version
├── index_simple_backup.html  # Simplified Iowa backup
├── Data/
│   ├── comprehensive_iowa_elections_analysis.json  # 18 years of election data
│   └── tl_2020_19_county20/
│       ├── tl_2020_19_county20.geojson            # Iowa county boundaries
│       └── ...
├── scripts/
│   ├── main.js               # (Legacy, not used in current version)
│   ├── map.js                # (Legacy)
│   └── common.js             # (Legacy)
├── styles/
│   ├── main.css              # (Legacy, not used in current version)
│   ├── style.css             # (Legacy)
│   └── common.css            # (Legacy)
└── README.md                 # This file
```

## 🎨 Competitiveness Scale

The map uses color-coded categories to represent the competitiveness and margin of victory in each county. These categories help users quickly identify which areas are safe for each party, which are competitive, and where political realignment is occurring.

### Category Definitions

**Annihilation (40%+ margin)**: One party wins by more than 40 percentage points. Indicates a landslide victory and a safe stronghold for the winning party.

**Dominant (30-40% margin)**: One party wins by 30-40 percentage points. Still a very safe seat, but slightly less extreme than Annihilation.

**Stronghold (20-30% margin)**: One party wins by 20-30 percentage points. A reliably safe county for the winning party.

**Safe (10-20% margin)**: One party wins by 10-20 percentage points. The area is considered safe, but not impenetrable.

**Likely (5.5-10% margin)**: The winning party has a clear advantage, but the area could become competitive under the right circumstances.

**Lean (1-5.5% margin)**: The area is competitive, with a modest advantage for the winning party.

**Tilt (0.5-1% margin)**: The area is extremely competitive, with only a slight edge for the winner.

**Tossup (±0.5% margin)**: The margin is less than half a percentage point, indicating a true battleground with no clear favorite.

### Complete Color Scale (15 Levels)

| Category | Margin | Color | Description |
|----------|--------|-------|-------------|
| Annihilation Democratic | 40%+ Dem | #08306b | Deep blue - overwhelming Democratic stronghold |
| Landslide Democratic | 30-40% Dem | #08519c | Dominant Democratic victory |
| Blowout Democratic | 20-30% Dem | #2171b5 | Stronghold - reliably safe Democratic |
| Strong Democratic | 15-20% Dem | #4292c6 | Safe Democratic seat |
| Solid Democratic | 10-15% Dem | #6baed6 | Safe - comfortable Democratic advantage |
| Lean Democratic | 5-10% Dem | #9ecae1 | Likely Democratic - clear but not overwhelming |
| Tilt Democratic | 2-5% Dem | #c6dbef | Lean Democratic - modest advantage |
| Tossup | 0-2% | #f0f0f0 | True battleground - too close to call |
| Tilt Republican | 2-5% Rep | #fcbba1 | Lean Republican - modest advantage |
| Lean Republican | 5-10% Rep | #fc9272 | Likely Republican - clear but not overwhelming |
| Solid Republican | 10-15% Rep | #fb6a4a | Safe - comfortable Republican advantage |
| Strong Republican | 15-20% Rep | #ef3b2c | Safe Republican seat |
| Blowout Republican | 20-30% Rep | #cb181d | Stronghold - reliably safe Republican |
| Landslide Republican | 30-40% Rep | #a50f15 | Dominant Republican victory |
| Annihilation Republican | 40%+ Rep | #67000d | Deep red - overwhelming Republican stronghold |

**Color Interpretation Tips:**
- **Darker colors** = Larger margins = Safer for that party
- **Lighter colors** = Smaller margins = More competitive
- **Gray** = Tossup = Either party could win
- **Blue shades** = Democratic wins (from light tilt to dark annihilation)
- **Red shades** = Republican wins (from light tilt to dark annihilation)

## 🛠️ Technologies Used

- **Mapbox GL JS v3.0.1** - Interactive map rendering
- **Turf.js 6.5.0** - Geospatial analysis (bounding box calculations)
- **Papa Parse 5.4.1** - CSV parsing (template compatibility)
- **Vanilla JavaScript** - No framework dependencies
- **CSS3** - Modern styling with flexbox and grid

## 📈 Data Sources & Methodology

### Data Sources

- **Election Results**: Compiled from Iowa Secretary of State official election results (1980-2024)
- **County Boundaries**: US Census Bureau TIGER/Line Shapefiles (2020)
- **GeoJSON**: Converted from Census shapefiles for web mapping

### Data Collection & Processing

**Election Data Pipeline:**

1. **Source Retrieval**
   - Downloaded certified election results from Iowa Secretary of State website
   - Focused on major statewide contests: Presidential, US Senate, Governor, and key statewide offices
   - Collected county-level returns for each contest

2. **Data Standardization**
   - Normalized county names to all uppercase (e.g., "POLK", "JOHNSON", "STORY")
   - Standardized candidate party affiliations (DEM/REP)
   - Calculated derived metrics:
     - Total votes per county per contest
     - Vote percentages for each candidate
     - Margin of victory (vote difference)
     - Margin percentage (margin / total votes × 100)

3. **Competitiveness Classification**
   - Applied 15-level competitiveness scale based on margin percentage
   - Assigned color codes for choropleth visualization
   - Categorized each county-contest result (e.g., "Lean Democratic", "Strong Republican")

4. **JSON Structure**
   - Organized as nested hierarchy: `year → category → contest → county`
   - Each county result includes: vote counts, candidates, winner, margin, competitiveness
   - Total dataset: ~64,000 lines covering 18 years × 99 counties × multiple contests

**Geographic Data:**
- Used TIGER/Line 2020 county boundaries from US Census Bureau
- Converted Shapefile to GeoJSON format for web compatibility
- Retained NAME20 property for county name matching
- Simplified geometry where appropriate to reduce file size

**Data Quality:**
- All vote totals verified against official Iowa Secretary of State certified results
- Missing data handled by excluding incomplete contests from dropdown
- County name matching verified across all 99 Iowa counties
- Competitiveness calculations validated manually for sample contests

### Dataset Statistics

- **Years Covered**: 18 election cycles (1980, 1982, 1984, 1986, 1988, 1992, 1994, 1996, 1998, 2000, 2004, 2008, 2012, 2016, 2020, 2022, 2024)
- **Counties**: All 99 Iowa counties
- **Contest Types**: Presidential (9), Senate (varies), Gubernatorial (varies), Statewide (varies)
- **Total Data Points**: Approximately 1,782+ county-contest combinations
- **File Size**: 
  - Election JSON: ~2.5 MB
  - County GeoJSON: ~800 KB
  - Total: ~3.3 MB

## 🔍 Key Insights

### The Trump Era Realignment: Iowa Democrats Become Minority Party

Iowa's transformation from bellwether swing state to Republican stronghold represents one of the most dramatic political realignments of the Trump era. What was once a competitive two-party state has become a Republican-dominant landscape, with Democrats relegated to minority status.

**The Collapse (2012-2024):**
- **2012**: Obama won Iowa by 5.8 points, carrying 56 of 99 counties
- **2016**: Trump narrowly won Iowa by 9.4 points, signaling the shift
- **2020**: Trump expanded margin to 8.2 points despite losing nationally
- **2024**: Trump won by 13+ points - Iowa's largest Republican margin in decades

**Democrats' Shrinking Geography:**
By 2024, Iowa Democrats were competitive in only 6 of 99 counties:
1. **Johnson County** (Iowa City) - University of Iowa stronghold
2. **Story County** (Ames) - Iowa State University
3. **Polk County** (Des Moines) - State capital
4. **Black Hawk County** (Waterloo-Cedar Falls) - UNI and manufacturing
5. **Linn County** (Cedar Rapids) - Second-largest city
6. **Dallas County** (Des Moines suburbs) - Affluent suburbs

This represents a stunning geographic collapse from the Obama era, when Democrats carried 53-56 counties and were competitive in rural areas.

**The Rural Wipeout:**
Trump's appeal to working-class white voters without college degrees devastated Iowa Democrats in their former rural strongholds:
- Counties that Obama won in 2008-2012 swung 20-30+ points toward Republicans
- Rural counties now vote 60-80% Republican, margins previously unseen
- Former Democratic-leaning counties like Dubuque, Clinton, and Scott became Republican or highly competitive
- The "Driftless Area" in Northeast Iowa, once reliably Democratic, flipped decisively

**Loss of State-Level Power:**
The realignment extended beyond presidential races to total Republican dominance:
- **Governor**: Kim Reynolds won by 19 points in 2022 (95 of 99 counties)
- **State Legislature**: Republicans hold supermajorities or near supermajorities in both chambers
- **US House**: Republicans hold all 4 congressional seats
- **US Senate**: Both seats held by Republicans (Ernst, Grassley)
- **Voter Registration**: Republicans overtook Democrats in registration for first time in state history

**Why Iowa Democrats Lost:**
1. **Educational Polarization**: Democrats gained college-educated voters but hemorrhaged non-college voters
2. **Cultural Disconnection**: Urban-focused messaging alienated rural voters on issues like agriculture, guns, and cultural values
3. **Economic Populism**: Trump's trade and manufacturing rhetoric resonated in former Democratic industrial areas
4. **Demographic Shifts**: Iowa's population became older and whiter, favoring Republicans
5. **Organizational Decline**: Rural Democratic Party infrastructure collapsed after repeated losses

**The New Normal:**
Iowa Democrats now face structural disadvantages similar to Republicans in states like California or Maryland:
- Presidential campaigns no longer compete seriously for Iowa
- Statewide races require near-perfect Democratic turnout in 6 urban counties
- Legislative districts heavily gerrymandered to favor Republicans
- Down-ballot races increasingly uncompetitive outside urban areas

**Glimmers of Hope?**
Despite the bleak landscape, Iowa Democrats retain some assets:
- Strong performance in college towns suggests education remains a mobilizing factor
- Des Moines suburbs (Dallas County) trending Democratic due to transplants
- Young voters in university counties provide future base
- Republicans' large margins may contain soft support vulnerable to backlash

However, absent a major political realignment or demographic change, Iowa appears likely to remain a Republican-leaning state for the foreseeable future, completing its journey from swing state to red state.

### Urban-Rural Divide
- **Urban Democratic Strongholds**: Story County (Ames), Johnson County (Iowa City), Polk County (Des Moines)
- **Rural Republican Dominance**: Most rural counties show consistent Republican performance
- **Suburban Battlegrounds**: Counties around Des Moines show competitive trends

### College Town Effect
Counties with major universities (Story, Johnson) consistently vote more Democratic than surrounding areas, reflecting the "college town effect" seen nationwide.

## 🏗️ Technical Architecture

### Application Flow

```
1. User opens index.html
2. Browser loads Mapbox GL JS, Turf.js, Papa Parse from CDN
3. Map initializes with Iowa center coordinates
4. Parallel data loading:
   - County GeoJSON boundaries
   - Comprehensive election results JSON
5. Populate contest dropdown from nested JSON structure
6. User selects contest → Apply color expression to map
7. User clicks county → Display detailed results in sidebar
```

### Key Functions

**Data Loading:**
```javascript
// Load both datasets in parallel
[countiesData, electionData] = await Promise.all([
  loadJSON(CONFIG.paths.counties),
  loadJSON(CONFIG.paths.election)
]);
```

**Contest Population:**
- Iterates through `results_by_year` nested structure
- Groups contests by category (Presidential, Senate, etc.)
- Builds dropdown options sorted by year (newest first)

**Color Mapping:**
- Uses Mapbox expression syntax for conditional styling
- Matches county NAME20 property to election data keys
- Applies competitiveness color from JSON to map fill layer

**County Click Handler:**
```javascript
map.on('click', 'county-fill', (e) => {
  const countyName = e.features[0].properties.NAME20;
  showCountyDetails(countyName);
});
```

**Search with Zoom:**
- Uses Turf.js to calculate bounding box of selected county
- Applies `map.fitBounds()` with smooth animation
- Falls back to geometry-based bounds if Turf.js fails

### Performance Considerations

- **Lazy Loading**: Map tiles load on-demand from Mapbox
- **Efficient Color Updates**: Only repaints fill layer when contest changes
- **JSON Optimization**: Nested structure reduces redundancy
- **GeoJSON Simplification**: County boundaries simplified for faster rendering
- **Event Delegation**: Single click handler for all counties

### Browser Compatibility

**Fully Supported:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

**Requirements:**
- JavaScript ES6 (async/await, arrow functions)
- Fetch API for JSON loading
- Mapbox GL JS requires WebGL support

**Known Limitations:**
- File:// protocol may have CORS issues in some browsers (use http:// or https://)
- Very old browsers (IE11 and earlier) not supported
- Mobile performance may vary on low-end devices with large GeoJSON

## 🎯 Interesting Findings to Explore

### Presidential Elections

**2024 - Trump's Dominance**
- Trump won Iowa by 13+ points, largest GOP margin since 1980s
- Only 6 counties voted Democratic (Johnson, Story, Polk, Black Hawk, Linn, Dallas)
- Rural counties showed 60-80% Republican margins

**2008 - Obama's Peak**
- Obama won Iowa by 9.5 points
- Carried 53 of 99 counties
- Strong performance in rural areas that later flipped Republican

**1988 - True Swing State**
- Dukakis won Iowa by just 10,000 votes
- Split nearly 50-50 statewide
- Competitive in both urban and rural areas

### Senate Races

**2020 - Ernst vs. Greenfield**
- One of the most expensive Senate races in history
- Ernst won by 6.6 points despite polling showing tight race
- Greenfield carried only 6 counties (same as Biden)

### Gubernatorial Races

**2022 - Reynolds Landslide**
- Governor Kim Reynolds won by 19 points
- Carried 95 of 99 counties
- Only lost Johnson, Story, Polk, and Dallas

### County Spotlights

**Johnson County (Iowa City)**
- Home to University of Iowa
- Most Democratic county in state
- Has voted Democratic in every presidential race since 1988
- 2020: Biden +31 points (66.6% to 35.6%)

**Story County (Ames)**
- Home to Iowa State University
- Second-most Democratic county
- College-educated voters drive Democratic performance
- 2020: Biden +18 points (58.5% to 40.4%)

**Polk County (Des Moines)**
- State capital and largest city
- Has trended Democratic over time
- 2020: Biden +9 points (54.6% to 44.7%)
- Contains 1/3 of Iowa's urban population

**Sioux County (Northwest Iowa)**
- Most Republican county in state
- Conservative Dutch Reformed community
- 2020: Trump +62 points (81.5% to 18.6%)
- Has never voted Democratic in modern era

**Scott County (Quad Cities)**
- Most competitive county in recent years
- Blue-collar industrial area
- 2016: Clinton +1.2 points → 2020: Biden +3.5 points
- Bellwether for statewide results

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contributions
- Add more years of historical data (pre-1980)
- Include demographic overlays (population, income, education)
- Add voter registration trends
- Implement time-series animation
- Mobile responsive improvements
- Accessibility enhancements
- Export functionality (PNG, CSV)
- Compare two elections side-by-side
- Add third-party candidate data
- Include congressional district boundaries

## ❓ Frequently Asked Questions

**Q: Why does the map show no colors when I first load it?**
A: You need to select a contest from the dropdown menu in the top-left control panel. Once selected, counties will be colored based on the results.

**Q: What years of data are included?**
A: The map includes 18 election cycles from 1980 to 2024: 1980, 1982, 1984, 1986, 1988, 1992, 1994, 1996, 1998, 2000, 2004, 2008, 2012, 2016, 2020, 2022, and 2024.

**Q: Why are some years missing (1990, 2002, etc.)?**
A: These were non-presidential election years where major statewide contests may not have occurred, or data hasn't been compiled yet. Presidential elections occur every 4 years.

**Q: What contests are included?**
A: Presidential, US Senate, Governor, and select statewide offices. Not all contests occur every election cycle.

**Q: How is "competitiveness" calculated?**
A: Based on the margin of victory as a percentage of total votes. For example, if a candidate wins 55%-45%, that's a 10-point margin, classified as "Solid" for the winning party.

**Q: Why are only Democratic and Republican votes shown?**
A: The map focuses on the two-party system for consistency across 44 years. Third-party candidates had minimal impact in Iowa during this period (with rare exceptions like Perot in 1992).

**Q: Can I download the raw data?**
A: Yes! The data is in `Data/comprehensive_iowa_elections_analysis.json`. It's in JSON format and can be opened in any text editor or processed with Python/JavaScript.

**Q: How accurate is this data?**
A: All data comes from official Iowa Secretary of State certified election results. Any discrepancies should be reported via GitHub issues.

**Q: Why does the map require an internet connection?**
A: The map uses Mapbox GL JS and Turf.js loaded from CDN. The actual election data and county boundaries are local files, but the mapping libraries need to be downloaded.

**Q: Can I use this for other states?**
A: Yes! The code is designed to be adaptable. You'd need to:
1. Replace the county GeoJSON with your state's boundaries
2. Format your election data to match the JSON structure
3. Update the CONFIG center coordinates and fitBounds
4. Modify the contest categories if different

**Q: The map isn't loading properly. What should I do?**
A: Check the browser console (F12) for errors. Common issues:
- CORS restrictions (try using http:// instead of file://)
- Missing data files
- Invalid Mapbox token
- Browser doesn't support WebGL

**Q: How can I contribute more data?**
A: Open a pull request with additional election years or contests! Make sure data follows the JSON structure and includes all required fields (dem_votes, rep_votes, winner, margin_pct, competitiveness).

**Q: Is this project affiliated with any political organization?**
A: No, this is an independent educational project for visualizing historical election data.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Shamar Davis**
- GitHub: [@Tenjin25](https://github.com/Tenjin25)

## 🙏 Acknowledgments

- North Carolina Political Realignment Map (NCMap) - Template inspiration and UI framework
- Tennessee Election Map (OGTNMap) - Original template structure
- Iowa Secretary of State - Official election data
- US Census Bureau - Geographic boundary data
- Mapbox - Mapping platform and API

## 📮 Contact

For questions, suggestions, or data corrections, please open an issue on GitHub.

---

*Last Updated: November 2025*
