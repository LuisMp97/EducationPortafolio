"""
   Geoprocess: Assignment02 Distribution Analysis Script 
   Programmer: Luis Maldonado
   Date: February 11th, 2026
   Purpose: Performs spatial analysis to determine customer distribution patterns
            by selecting customers within a user-defined distance threshold and
            calculating the percentage of total customers within that range.
   Course: Geoprocessing and Modelling
"""
import arcpy
# Allows software to overwrite existing files 
arcpy.env.overwriteOutput= True
# Create DIR, ****change the URI to match the geodatabase**** that contains the Store and Customer FeatureClasses
workspace = r'C:\COGS\Winter Courses\GIS6060_Geoprocessing and Modelling\Assignments\Ass02_Buffer\Deliverables\StoresCustomers.gdb'
arcpy.env.workspace = workspace
arcpy.AddMessage('Workspace and env configured')
try:
    
    # Parameter retrieved from the geoprocessing tool
    customer_layer = arcpy.GetParameterAsText(0)
    arcpy.AddMessage(f'customer path is: {customer_layer}')
    user_value = arcpy.GetParameterAsText(1)
    interval_range = user_value + ' Kilometers'
    # Create a feature layer for geoprocessing purposes (It seems that FeatureClass is mainly to store data)
    feature_layer_customer = "FeatureLayerCustomer"
    arcpy.MakeFeatureLayer_management(customer_layer, feature_layer_customer)
    # Get store name by getting the name of the customer layer
    store_name = arcpy.GetParameterAsText(0).split('\\')[-1] # Retrieves the layer name
    store_layer = r'Stores\Store_' + store_name # Relative path since workspace is set
    arcpy.AddMessage(f'store path is: {store_layer}')
    # Select the total feature within customer layer selected, converted to int as it returns a non-numeric value
    total_count = int(arcpy.GetCount_management(customer_layer)[0]) # Index 0 contains the number of features 
    arcpy.AddMessage(f'The total numbers of features is: {total_count}')
    # SelectLayerByLocation tool
    arcpy.management.SelectLayerByLocation(
        in_layer=feature_layer_customer,   # use layer instead of feature class
        overlap_type="WITHIN_A_DISTANCE",
        select_features=store_layer,       # Store Layer
        search_distance=interval_range,    # Range 
        selection_type="NEW_SELECTION",
        invert_spatial_relationship="NOT_INVERT"
    )
    # Count the number of features previously selected
    features_selected = int(arcpy.GetCount_management(feature_layer_customer)[0])  
    arcpy.AddMessage(f'The numbers of features within {interval_range} are: {features_selected}')
    # Make calculation of percentage
    customer_percentage = features_selected/total_count * 100
    arcpy.AddMessage(f'percentage is {customer_percentage}')
    
    # Create table
    arcpy.CreateTable_management(workspace, 'CustomerSelected')
    # Add the fields
    arcpy.AddField_management('CustomerSelected', 'Distance', 'Short')
    arcpy.AddField_management('CustomerSelected', 'Percent', 'Float')
    arcpy.AddMessage(f'Tables and fields created')
    # Cursor created and row added
    cursor = arcpy.da.InsertCursor('CustomerSelected', ['Distance', 'Percent'])
    cursor.insertRow([int(user_value), customer_percentage])
    arcpy.AddMessage(f'Row added')
    del cursor # Drop cursor
      
except:
    print('Something went wrong! Try again')
