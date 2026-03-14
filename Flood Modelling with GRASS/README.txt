README

Content

1. Python Script
    - FloodMapping_GRASS.py: Python script for GRASS GIS 8.4.1 (Python 3.12.11). Implements flood modeling options using a high-resolution    DEM.

    -TinLayer_ArcGIS.py: Python script for ArcGIS Pro 3.5. Generates a TIN (Triangulated Irregular Network) layer from input data.

2. Folders
    - Flooding: Contains the output results of the flood simulation model.
    - Flooding_Inputs: Input datasets for the flooding workflow (DEM raster), used by the corresponding Python script.

    - TIN: Output files generated from the TIN modeling process.
    - TIN_Inputs: Input datasets for TIN generation, used by the corresponding Python script.

3. Notes

    - DEM resolution: 1 m, covering Richmond, BC.
    - Scripts are designed for reproducibility and can be adapted to similar flood modeling projects.
    - Ensure that the correct GIS environments (GRASS GIS 8.4.1 and ArcGIS Pro 3.5) are installed before running the script