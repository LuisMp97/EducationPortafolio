Field Crops & Ferry Ridership — Oracle Database Pipeline
Python ETL Scripts — Assignment 01
Overview
Two Python scripts that load and normalize datasets into an Oracle database. The first loads ferry ridership data into a single table. The second normalizes a Statistics Canada field crops dataset to Third Normal Form (3NF) and runs an analysis query.

Scripts
1. load_data_to_oracle.py
Loads ferry ridership data from a CSV file into a new Oracle table.
StepDescriptionReadParses ferry-ridership.csvCreateCreates ferry_ridership tableInsertBulk inserts all rows via executemanyCommitCommits transaction
Table created: ferry_ridership
ColumnTypeDescriptionrouteidINTRoute identifierroutenameVARCHAR2(50)Route nameridership_dateDATEDate of ridership recordridershipINTPassenger count

2. normalization_to_oracle.py
Normalizes the field_crops_hay table from flat structure to 3NF and runs a PEI Potatoes analysis query.
Normalization steps:
StepAction1NFAdds primary key (ccs_uid, crop_uid) to field_crops_hay2NFExtracts ccs and crops tables, removes partial dependencies3NFExtracts province table from ccs, removes transitive dependency
Analysis query: Total potato crop area in Prince Edward Island, grouped by province and crop name.

Requirements

Python 3.x
oracledb library (pip install oracledb)
Oracle Client installed and accessible
ORACLE_PASSWORD set as an environment variable
Oracle DSN: gisy6021_high, User: USER1
ferry-ridership.csv and field_crops_hay table must exist before running


Usage
bash# Set password
export ORACLE_PASSWORD=your_password

# Load ferry data
python load_data_to_oracle.py

# Normalize crops and run analysis
python normalization_to_oracle.py

Author
Luis Maldonado — Spatial Databases, March 2026