Transit Route Data Extraction & Classification Workspace
FME Workspace — Assignment 02
Overview
This FME workspace joins transit bus route geometries with automated passenger count data, filters records by date and time, classifies routes by ridership level, and exports the enriched result as a GeoJSON file.

Inputs
InputFormatDescriptionTransit_Bus_Routes.shpShapefileBus route geometries with route attributesTransit_Automated_Passenger_Counts.csvCSVRidership data including date, hour, and total counts

Output
OutputFormatDescriptionRouteJan23_1pm_Classified.jsonGeoJSONFiltered and classified bus routes with ridership data
Output Fields
FieldDescriptionRoute_NumberBus route identifierRoute_Name / Route_TitleRoute nameRidership_TotalTotal passenger countRoute_HourHour of serviceRoute_DateDate of serviceRidership_ClassificationClassified ridership level

Requirements

FME 2025.2 or later
Input files must be in the same directory as the workspace or paths updated accordingly

Author
Luis Maldonado — ETL Fundamentals, February 2026