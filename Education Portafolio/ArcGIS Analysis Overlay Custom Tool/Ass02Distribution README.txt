Customer Distribution Analysis Tool
ArcPy Geoprocessing Script
Overview
Custom ArcGIS geoprocessing tool that selects customers within a user-defined distance from a store and calculates what percentage of the total customer base they represent. Results are saved to a table in the geodatabase.
Inputs
ParameterDescriptioncustomer_layerCustomer feature classuser_valueDistance threshold (kilometers)
Output
A table called CustomerSelected with two fields: Distance (km) and Percent (% of total customers).
Requirements

ArcGIS Pro + arcpy
StoresCustomers.gdb with a Stores feature dataset
Update the workspace path before running

Author
Luis Maldonado — Geoprocessing and Modelling, February 2026