
"""
    Script: TinLayer_ArcGIS.py 
    Programmer: Luis Maldonado
    Date: March 2nd, 2026
    Purpose: Convert point CSV to feature class and reclassify the z values, select the desired features,
    and build a TIN surface using mass points and breaklines
    Course: Advanced GIS 

    Python Version: 3.12.11
    ArcGIS Pro 3.5.2 
"""

import arcpy

arcpy.CheckOutExtension("3D")
arcpy.env.overwriteOutput = True # Allows overwriting on existing files

# Working directory
work_dir = r"C:\COGS\Winter Courses\GISY6020_Advanced GIS\Ass03_ThreeD\Scripts" 
arcpy.env.workspace = work_dir

try:

    # Reclassify height values shape, -32767 to -10
    arcpy.management.CalculateField(
        in_table=r"TIN_Inputs\POINT_DATA_XYTableToPoint.shp",
        field="zcoor",
        expression="reclassify(!zcoor!)",
        expression_type="PYTHON3",
        code_block="""def reclassify(val):
    if val == -32767:
        return -10
    else:
        return val""",
        field_type="DOUBLE",
        enforce_domains="NO_ENFORCE_DOMAINS")
    print("Reclassify done!")


    # Creating empty TIN
    arcpy.CreateTin_3d(
        r"TIN\TINLayer",
        'COMPOUNDCRS["",GEOGCRS["GCS_North_American_1983_CSRS",DATUM["D_North_American_1983_CSRS",ELLIPSOID["GRS_1980",6378137.0,298.257222101]],PRIMEM["Greenwich",0.0],CS[ellipsoidal,2],AXIS["Latitude (lat)",north,ORDER[1]],AXIS["Longitude (lon)",east,ORDER[2]],ANGLEUNIT["Degree",0.0174532925199433]],VERTCRS["CGVD2013_CGG2013a_height",VDATUM["Canadian_Geodetic_Vertical_Datum_of_2013_CGG2013a",ANCHOREPOCH[2010.0]],CS[vertical,1],AXIS["Gravity-related height (H)",up,LENGTHUNIT["Meter",1.0]]]]')
    # SetTIN Parameters
    TIN_Inputs = (
        r"TIN_Inputs\POINT_DATA_XYTableToPoint.shp zcoor      <None> masspoints  false;"
        r"TIN_Inputs\Streams.shp                   <None>     <None> hardline    false;"
        r"TIN_Inputs\Roads.shp                     <None>     <None> hardline    false;"
        r"TIN_Inputs\Contours.shp                  md_vert__1 <None> hardline    false"
    )
    # Create the TIN layer within the previous empty TIN file
    arcpy.EditTin_3d(
        r"TIN\TINLayer",
        TIN_Inputs,
        "DELAUNAY"
    )
    print("TIN created")


except Exception as error:
    print(f"An error occurred:{error}")

