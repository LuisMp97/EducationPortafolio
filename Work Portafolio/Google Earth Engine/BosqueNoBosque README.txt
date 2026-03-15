Forest Cover Change Detection in Caquetá, Colombia
Using Google Earth Engine (GEE)

Overview
This project performs a binary forest/non-forest classification for the years 2022 and 2023 in the Caquetá region, and detects deforestation by comparing both classifications. It combines Sentinel-2 optical imagery, Sentinel-1 SAR radar, and SRTM elevation data.

Input Data
DatasetDescriptionCOPERNICUS/S2_SRSentinel-2 Surface ReflectanceCOPERNICUS/S2_CLOUD_PROBABILITYS2 Cloudless cloud probabilityCOPERNICUS/S1_GRDSentinel-1 SAR (VV, VH polarizations)USGS/SRTMGL1_003SRTM Digital Elevation ModelBosque / No_BosqueTraining samples for 2022Bosque_2023 / No_Bosque_2023Training samples for 2023AOIArea of Interest — Caquetá department


Feature Bands Used for Classification
BandSourceDescriptionB2, B3, B4, B5, B8, B9, B11Sentinel-2Optical reflectance bandsEVISentinel-2Enhanced Vegetation IndexNDWISentinel-2Normalized Difference Water IndexSBI, GVI, WETSentinel-2Tasseled Cap Brightness, Greenness, WetnessElevacionSRTMElevation (resampled to 10m)PendienteSRTMSlope (resampled to 10m)VV, VH, ratioSentinel-1 SARRadar backscatter (linear intensity)

Outputs
OutputFormatDescriptionImagen_Final_2022GEE AssetFull feature image for 2022Imagen_Final_2023GEE AssetFull feature image for 2023Def_CaquetaGEE AssetDifference raster (deforestation mask)PastizalesGeoJSON (Drive)Vectorized deforestation polygons

Classification Logic

Training/validation split: 80% / 20% (random column)
Classifier: Random Forest with 100 trees (smileRandomForest)
Class values: 1 = Forest, 2 = Non-Forest
Deforestation pixels are identified where classificacion_1 - classificacion_2 = -2 (Forest in 2022 → Non-Forest in 2023)


Requirements

Google Earth Engine account with access to:

users/luismaldonado/ assets
projects/ee-luismaldonado123/assets/ assets


Training samples for both 2022 and 2023 must be uploaded to GEE before running


Notes

SAR data is filtered to DESCENDING orbit, IW mode, 10m resolution
SAR time window used: January to June of each year
Cloud filtering threshold: 60% maximum cloud cover per scene
All bands resampled to a common 10m spatial resolution