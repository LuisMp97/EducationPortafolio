"""
Program: ass01_normalization.py
Made by: Luis Maldonado
Date:    03/03/2026
Purpose: Normalize crop and hay dataset from Statistics Canada using OracleDB
"""

import oracledb
import os

oracle_password = os.environ["ORACLE_PASSWORD"]

oracledb.init_oracle_client()

with oracledb.connect(user="USER1",
                      password=oracle_password,
                      dsn="gisy6021_high") as con:
    with con.cursor() as cursor:

        # -----------------------------------------------------------------
        # 1. Normalization: First Form
        # -----------------------------------------------------------------

        print("1NF Process")
        cursor.execute("""
            ALTER TABLE user1.field_crops_hay
            ADD CONSTRAINT field_crops_hay_pk
            PRIMARY KEY (ccs_uid, crop_uid)
            """)

        # -----------------------------------------------------------------
        # 2. Normalization: Second Form — Partial Dependencies
        # -----------------------------------------------------------------

        print("2NF Process")
        cursor.execute("""
            CREATE TABLE user1.ccs AS
            SELECT DISTINCT ccs_uid, ccs_name, province_uid, province_name
            FROM user1.field_crops_hay
            """)
        cursor.execute("""
            ALTER TABLE user1.ccs
            ADD CONSTRAINT ccs_pk PRIMARY KEY (ccs_uid)
            """)
        cursor.execute("""
            ALTER TABLE user1.field_crops_hay
            ADD CONSTRAINT field_crops_hay_ccs_fk
            FOREIGN KEY (ccs_uid) REFERENCES user1.ccs(ccs_uid)
            """)
        cursor.execute("""
            ALTER TABLE user1.field_crops_hay
            DROP (ccs_name, province_uid, province_name)
            """)

        cursor.execute("""
            CREATE TABLE user1.crops AS
            SELECT DISTINCT crop_uid, crop_name
            FROM user1.field_crops_hay
            """)
        cursor.execute("""
            ALTER TABLE user1.crops
            ADD CONSTRAINT crops_pk PRIMARY KEY (crop_uid)
            """)
        cursor.execute("""
            ALTER TABLE user1.field_crops_hay
            ADD CONSTRAINT field_crops_hay_crops_fk
            FOREIGN KEY (crop_uid) REFERENCES user1.crops(crop_uid)
            """)
        cursor.execute("""
            ALTER TABLE user1.field_crops_hay
            DROP COLUMN crop_name
            """)

        # -----------------------------------------------------------------
        # 3. Normalization: Third Form — Transitive Dependencies
        # -----------------------------------------------------------------

        print("3NF Process")
        cursor.execute("""
            CREATE TABLE user1.province AS
            SELECT DISTINCT province_uid, province_name
            FROM user1.ccs
            """)
        cursor.execute("""
            ALTER TABLE user1.province
            ADD CONSTRAINT province_pk PRIMARY KEY (province_uid)
            """)
        cursor.execute("""
            ALTER TABLE user1.ccs
            ADD CONSTRAINT ccs_provinces_fk
            FOREIGN KEY (province_uid) REFERENCES user1.province(province_uid)
            """)
        cursor.execute("""
            ALTER TABLE user1.ccs
            DROP COLUMN province_name
            """)

        con.commit()
        print("Normalization completed")

        # -----------------------------------------------------------------
        # 4. Analysis Query — PEI Potatoes total area
        # -----------------------------------------------------------------

        print("\nPrince Edward Island Potatoes Analysis\n")
        cursor.execute("""
            SELECT
                pro.province_name   AS "Province",
                cp.crop_name        AS "Crop",
                SUM(fch.crop_area_ha) AS "Total Area (ha)"
            FROM user1.ccs cc
            JOIN user1.field_crops_hay fch ON cc.ccs_uid     = fch.ccs_uid
            JOIN user1.province pro        ON cc.province_uid = pro.province_uid
            JOIN user1.crops cp            ON fch.crop_uid    = cp.crop_uid
            WHERE
                pro.province_name = 'Prince Edward Island'
                AND cp.crop_name LIKE 'Potatoes'
            GROUP BY pro.province_name, cp.crop_name
            """)

        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

   
