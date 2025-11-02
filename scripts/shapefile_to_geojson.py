import geopandas as gpd

# Path to your shapefile
shapefile_path = "Data/tl_2020_19_county20/tl_2020_19_county20.shp"
# Output GeoJSON path
geojson_path = "Data/tl_2020_19_county20/tl_2020_19_county20.geojson"

# Read the shapefile
gdf = gpd.read_file(shapefile_path)

# Write to GeoJSON
gdf.to_file(geojson_path, driver="GeoJSON")

print(f"GeoJSON saved to {geojson_path}")
