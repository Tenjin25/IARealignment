// Replace with your Mapbox access token
mapboxgl.accessToken = 'pk.eyJ1Ijoic2hhbWFyZGF2aXMiLCJhIjoiY21kcW8yeDB2MDhvbTJzb29qeGp1aDZmZCJ9.Zw_i6U-dL7_bEKRHTUh7yg';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-93.581543, 41.878003], // Iowa center
    zoom: 6
});

// UI logic wiring for sidebar, controls, legend
function toggleMainControls() {
    const controls = document.getElementById('main-controls');
    const btn = document.getElementById('controls-minimize-btn');
    controls.classList.toggle('minimized');
    btn.textContent = controls.classList.contains('minimized') ? '+' : '−';
}
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const btn = document.getElementById('sidebar-minimize-btn');
    sidebar.classList.toggle('minimized');
    btn.textContent = sidebar.classList.contains('minimized') ? '+' : '−';
}
function toggleLegend() {
    const legend = document.getElementById('legend');
    const btn = document.getElementById('legend-minimize-btn');
    legend.classList.toggle('minimized');
    btn.textContent = legend.classList.contains('minimized') ? '+' : '−';
}
function setMode(mode) {
    document.getElementById('county-mode').classList.toggle('active', mode === 'county');
    document.getElementById('precinct-mode').classList.toggle('active', mode === 'precinct');
    // Add logic to switch map layers if needed
}
function applyCategories() {
    // Placeholder: Add logic to color counties by election results
    alert('Apply categories logic goes here');
}
function resetView() {
    map.flyTo({center: [-93.581543, 41.878003], zoom: 6});
}
function toggleLabels() {
    // Placeholder: Add logic to toggle county labels
    alert('Toggle county labels logic goes here');
}
function togglePrecinctsLayer() {
    // Placeholder: Add logic to toggle precincts layer
    alert('Toggle precincts layer logic goes here');
}
function showSwingCounties() {
    // Placeholder: Add logic to analyze swing counties
    alert('Swing counties analysis logic goes here');
}
function showSwingArrows() {
    // Placeholder: Add logic to show swing arrows
    alert('Show swing arrows logic goes here');
}
function hideSwingArrows() {
    // Placeholder: Add logic to hide swing arrows
    alert('Hide swing arrows logic goes here');
}
// Sidebar county search
const countySearch = document.getElementById('county-search');
if (countySearch) {
    countySearch.addEventListener('input', function() {
        // Placeholder: Add logic to zoom to county by name
        alert('County search logic goes here');
    });
}
// Example: Show sidebar when a county is clicked (Mapbox event)
map.on('click', function(e) {
    // Placeholder: Add logic to show county details in sidebar
    document.getElementById('sidebar').classList.remove('minimized');
});
// Add more wiring as needed for Iowa election data and interactivity
