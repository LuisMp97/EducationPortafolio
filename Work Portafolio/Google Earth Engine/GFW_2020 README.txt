Farm-Level Forest Loss Analysis using Hansen Global Forest Change
Using Google Earth Engine (GEE)
Overview
This script analyzes forest cover loss between 2020 and 2022 at the individual farm level using the Hansen Global Forest Change dataset. It calculates the area and pixel count of forest loss within each farm polygon from the Racafé portfolio, and exports the results as a table.

Input Data
DatasetDescriptionUMD/hansen/global_forest_change_2022_v1_10Hansen Global Forest Change v1.10Racafe_PoligonosFarm polygons (FeatureCollection)

Output Fields per Farm
FieldDescriptionforest_loss_areaSum of lossyear values within the farm (proxy for loss area)forest_loss_pixel_countNumber of pixels with forest loss since 2020

Map Layers
LayerDescriptionFincasFarm polygons styled with black outlineTree Loss 2020-2022Forest loss pixels colored from yellow (2020) to red (2022)

Outputs
OutputFormatDescriptionfarmsWithLossDataAndPixelCountGoogle Drive TableFarm polygons enriched with forest loss statistics

Key Parameters
ParameterValueDescriptionlossyear min20Filters from year 2020 onwardlossyear max22Up to year 2022Scale30mNative Hansen dataset resolution

Requirements

Google Earth Engine account with access to:

projects/ee-luismaldonado123/assets/Racafe_Poligonos


The Hansen dataset is publicly available in GEE


Notes

The lossyear band encodes years as two-digit numbers (e.g., 20 = 2020, 22 = 2022)
Loss area is approximated by summing lossyear pixel values, not by direct area calculation in m². For precise area in hectares, consider using ee.Image.pixelArea() combined with the loss mask
The script includes a filter example by farm owner name (Nombre_Pro) that can be adapted to inspect individual farms
Scale can be adjusted depending on the required precision vs. computation time