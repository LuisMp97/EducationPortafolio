Transit Route Data Extraction & Classification Workspace
FME Workspace — Assignment 03
Overview
Two-workspace FME solution that performs spatial analysis on Nova Scotia land cover data for a selected location. It determines site extents, buffers site geometries, overlays spatial datasets, and produces a vector output and a summary statistics Excel table.

Inputs
DatasetFormatCRSSourceSitesESRI ArcGIS Feature ServiceEPSG:26920 → relabelled to EPSG:2961COGS ArcGIS OnlineCountiesESRI ArcGIS Feature ServiceEPSG:2961AGOL group: WKID_Transformation_GISY5040SoilsESRI ArcGIS Feature ServiceEPSG:2961AGOL group: WKID_Transformation_GISY5040ForestESRI ArcGIS Feature ServiceEPSG:2961COGS ArcGIS Online

Outputs
Vector Dataset (GeoPackage or ESRI Geodatabase)
FieldSourcedescriptionSites — DescriptioncountyNSCounties — COUNTYsoil_stoninessNSSoilsPg — STONINESSsoil_nameNSSoilsPg — SOILNAMEforest_heightNSForest_Pg — HEIGHTforest_species_1NSForest_Pg — SP1areaCalculated (hectares)
Summary Table (Microsoft Excel)
ColumnDescriptiondescriptionSite descriptionsoil_nameSoil nameforest_species_1Primary forest speciesforest_height_meanMean forest height (grouped)area_totalTotal area per group (hectares)
Grouped by: description, soil_name, forest_species_1

Key Notes

Only one location (3 sites) needs to be processed
Use a spatial extent filter on the Forest reader to avoid loading the full dataset
The CoordinateSystemSetter only relabels the CRS — it does not reproject
Apply GeometryValidator (Spatial Standard Compliance, OGC SFA 1.2.0) before AreaOnAreaOverlayer
All workspaces should include comments and bookmarks for clarity


Requirements

FME 2025.2 or later
Access to COGS ArcGIS Online instance
Additional FME package may be required for the ArcGIS Feature Service reader

Author
Luis Maldonado — ETL Fundamentals, 2026