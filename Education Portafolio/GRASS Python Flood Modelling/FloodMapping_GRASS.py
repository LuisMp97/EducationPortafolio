
"""
    Script: FloodMapping_GRASS.py 
    Programmer: Luis Maldonado
    Date: March 2nd, 2026
    Purpose: Perform a spatial analysis on a 1m resolution DEM to model potential flood extent and inundation height resulting
             from increased water levels in nearby rivers and the ocean. The input dataset is a DM covering Richmond, BC, retrieved
             from: https://lidar.gov.bc.ca/pages/download-discovery
    Course: Advanced GIS 

    Python Version: 3.12.11
    Grass GIS 8.4.1 64bit
"""

import os
import grass.script as gs

def main():
    # Before starting, set the CSR to 3157 by following this steps in Grass GUI:
    # Create new project > Select CRS from a list by EPSG or description > 3157 NAD83(CSRS)/UTM Zone 10N

    
    # Set working directory 
    os.chdir(r"C:\COGS\Winter Courses\GISY6020_Advanced GIS\Ass03_ThreeD\Scripts")
    input_dem_path = r"Flooding Inputs\DEMRichmond.tif" # DEM pathfile 
    output_dir     = r"C:\COGS\Winter Courses\GISY6020_Advanced GIS\Ass03_ThreeD\Scripts\Flooding" # outputs DIR


    # Input layer
    input_dem      = "DEMRichmond"

    # Memory created layers
    richmond_clean = "Richmond_River_Clean"
    topobathy      = "Topobathy"
    relief         = "relief_scaled"
    shaded         = "shaded_relief"


    # Import DEM
    gs.run_command(
        "r.in.gdal",
        input=input_dem_path,
        output=input_dem,
        overwrite=True)

    gs.run_command("g.region", raster=input_dem) # Area of interest set to the DEM Region
    print('DEM and Region set up done!')

    
    # Use map calculator to set values below 0 as null, then setting it as -2
    gs.run_command(
        "r.mapcalc",
        expression=f"{richmond_clean} = if({input_dem} <= 0, null(), {input_dem})",
        overwrite=True)

    print("Step 2: Creating topobathy - replacing nulls with -2...")
    gs.run_command(
        "r.mapcalc",
        expression=f"{topobathy} = if(isnull({richmond_clean}), -2, {richmond_clean})",
        overwrite=True)
    print('Map algebra done!')


    # Creating Hillshade in case that needed (Richmond is flat so it won't be displayed in the ArcGIS Scene),
    # afterwards, the it is exported
    gs.run_command(
        "r.relief",
        input=topobathy,
        output=relief,
        altitude=45,
        azimuth=320,
        zscale=1,
        scale=2,
        overwrite=True)
    
    gs.run_command(
        "r.shade",
        shade=relief,
        color=richmond_clean,
        output=shaded,
        brighten=30,
        overwrite=True)


    print("Exporting shaded relief...")
    gs.run_command(
        "r.out.gdal",
        input=shaded,
        output=os.path.join(output_dir, "shaded_relief.tif"),
        format="GTiff",
        overwrite=True
    )

    print('Hill and Shade done!')


    # Use r.lake to model the flooding bearing in mind that ocean water level may increase to 2m by 2021
    # set a list from 0 to 2 meters for looping purposes, and export the results into the output DIR
    print("Step 5: Simulating and exporting lake levels...")
    water_levels = [0, 1, 1.5, 2]

    os.makedirs(output_dir, exist_ok=True)

    for level in water_levels:

        level_str  = str(level).replace(".", "_")   # GRASS does not get along adding . to the output name file
        lake_map   = f"lake_{level_str}m"
        out_path   = os.path.join(output_dir, f"lake_{level_str}m.tif")

        # r.lake method
        gs.run_command(
            "r.lake",
            elevation=topobathy,
            water_level=level,
            lake=lake_map,
            coordinates=(496766.179087, 5443193.582967),
            overwrite=True)

        # exporting the data

        print(f"  Exporting {lake_map} → {out_path}")
        gs.run_command(
            "r.out.gdal",
            input=lake_map,
            output=out_path,
            format="GTiff",
            overwrite=True)

    print("\nEverything went smooth!")

# We run the function
if __name__ == "__main__":  
    main()
