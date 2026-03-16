/*
Note:  
This is not the company’s final product. 
For data privacy reasons, and with permission from my previous employer, I have uploaded an early version of the code.
*/


// Vector Data
var Bosque = ee.FeatureCollection("users/luismaldonado/Bosque_2022_Caqueta");
var No_Bosque = ee.FeatureCollection("users/luismaldonado/No_Bosque_2022_Caqueta");
var Poligono_Leaf = ee.FeatureCollection("projects/ee-luismaldonado123/assets/Poligonos_Leaf");
var AOI = ee.FeatureCollection("projects/ee-luismaldonado123/assets/Caqueta");

// Imagery Datasets
var Sentinel_Radar = ee.ImageCollection("COPERNICUS/S1_GRD"); 
var SRTM = ee.Image("USGS/SRTMGL1_003");


// Cloud-Free Time Series Sentinel-2
var START_DATE = '2022-01-01'
var END_DATE = '2022-12-31'
var CLOUD_FILTER = 60
var CLD_PRB_THRESH = 30
var NIR_DRK_THRESH = 0.15
var CLD_PRJ_DIST = 1
var BUFFER = 50

function get_s2_sr_cld_col(AOI, start_date, end_date) {
    var s2_sr_col_1 = (ee.ImageCollection('COPERNICUS/S2_SR')  // Harmonized Sentinel-2 Dataset
        .filterBounds(AOI)
        .filterDate(start_date, end_date)
        .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE', CLOUD_FILTER)))

    var s2_cloudless_col_1 = (ee.ImageCollection('COPERNICUS/S2_CLOUD_PROBABILITY')
        .filterBounds(AOI)
        .filterDate(start_date, end_date))

    return ee.ImageCollection(ee.Join.saveFirst('s2cloudless').apply({
        'primary': s2_sr_col_1,
        'secondary': s2_cloudless_col_1,
        'condition': ee.Filter.equals({
            'leftField': 'system:index',
            'rightField': 'system:index'
        })
    }))
}

function add_cloud_bands(img) {
    var cld_prb = ee.Image(img.get('s2cloudless')).select('probability')
    var is_cloud = cld_prb.gt(CLD_PRB_THRESH).rename('clouds')
    return img.addBands(ee.Image([cld_prb, is_cloud]))
}

function add_shadow_bands(img) {
    var not_water = img.select('SCL').neq(6)
    var SR_BAND_SCALE = 1e4
    var dark_pixels = img.select('B8').lt(NIR_DRK_THRESH*SR_BAND_SCALE).multiply(not_water).rename('dark_pixels')
    var shadow_azimuth = ee.Number(90).subtract(ee.Number(img.get('MEAN_SOLAR_AZIMUTH_ANGLE')));
    var cld_proj = (img.select('clouds').directionalDistanceTransform(shadow_azimuth, CLD_PRJ_DIST*10)
        .reproject({'crs': img.select(0).projection(), 'scale': 10}) // Scale affects total memory used 
        .select('distance')
        .mask()
        .rename('cloud_transform'))
    var shadows = cld_proj.multiply(dark_pixels).rename('shadows')
    return img.addBands(ee.Image([dark_pixels, cld_proj, shadows]))
}

function add_cld_shdw_mask(img) {
    var img_cloud = add_cloud_bands(img)
    var img_cloud_shadow = add_shadow_bands(img_cloud)
    var is_cld_shdw = img_cloud_shadow.select('clouds').add(img_cloud_shadow.select('shadows')).gt(0)
    is_cld_shdw = (is_cld_shdw.focal_min(2).focal_max(BUFFER*2/20)
        .reproject({'crs': img.select([0]).projection(), 'scale': 20})
        .rename('cloudmask'))
    return img_cloud_shadow.addBands(is_cld_shdw)
}

function apply_cld_shdw_mask(img) {
    var not_cld_shdw = img.select('cloudmask').not()
    return img.select('B.*').updateMask(not_cld_shdw)
}

var s2_sr_cld_col = get_s2_sr_cld_col(AOI, START_DATE, END_DATE)
var s2_sr_median = (s2_sr_cld_col.map(add_cld_shdw_mask)
                             .map(apply_cld_shdw_mask)
                             .median())

function interpolate_band(band) {
  return band.resample('bilinear').reproject(band.projection().atScale(10));
}

// Cloud-Free image cut into AOI

var cortado = s2_sr_median.addBands(interpolate_band(s2_sr_median.select('B5')))
                          .addBands(interpolate_band(s2_sr_median.select('B9')))
                          .addBands(interpolate_band(s2_sr_median.select('B11')))
                          .clip(AOI)
// Required Indices

var evi = cortado.expression('2.5 * ((NIR - Red) / (NIR + 6 * Red - 7.5 * Blue + 1))',{
          'NIR': cortado.select('B8'),
          'Red': cortado.select('B4'),
          'Blue':cortado.select('B2'),
})

var ndwi = cortado.expression('(Green - NIR)/(Green + NIR)',{
          'NIR': cortado.select('B8'),
          'Green': cortado.select('B3')
});

var tcb= cortado.expression('(0.3510*Blue)+ (0.3813*Green)+ (0.3437*Red)+ (0.7196*NIR)+ (0.2396*SWIR) + (0.1949*SWIR2)',{
          'Blue':cortado.select('B2'),
          'Green':cortado.select('B3'),
          'Red': cortado.select('B4'),
          'NIR': cortado.select('B8'),
          'SWIR': cortado.select('B11'),
          'SWIR2': cortado.select('B12')
});

var tcg= cortado.expression('(-0.3599* Blue) + (-0.3533*Green)+(-0.4734*Red) + (0.6633*NIR) +(0.0087*SWIR) + (-0.2856*SWIR2)',{
          'Blue':cortado.select('B2'),
          'Green':cortado.select('B3'),
          'Red': cortado.select('B4'),
          'NIR': cortado.select('B8'),
          'SWIR': cortado.select('B11'),
          'SWIR2': cortado.select('B12')
});

var tcw= cortado.expression('((0.2578*Blue) + (0.2305*Green) +(0.0883*Red) + (0.1071*NIR) +(-0.7611*SWIR) + (-0.5308*SWIR2))',{
          'Blue':cortado.select('B2'),
          'Green':cortado.select('B3'),
          'Red': cortado.select('B4'),
          'NIR': cortado.select('B8'),
          'SWIR': cortado.select('B11'),
          'SWIR2': cortado.select('B12')
});

// Slope and Elev using SRTM10m

var SRTM_10m = SRTM.resample('bilinear').reproject(SRTM.projection().atScale(10));

print(SRTM_10m)
var Elev = SRTM_10m.select('elevation')
var Slope = ee.Terrain.slope(SRTM_10m.select('elevation'))


// Using Sentinel-1 Band C (Descending as the images are from Colombia)

var Sentinel_SAR= Sentinel_Radar.filterBounds(AOI)
           .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
           .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
           .filter(ee.Filter.eq('instrumentMode', 'IW'))
           .filter(ee.Filter.eq('resolution_meters', 10))
           .filter(ee.Filter.eq('resolution', 'H'))                 
           .filterDate('2022-01-01', '2022-06-20')
           .filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))
    
print(Sentinel_SAR)
var Sentinel_SAR_conversion= function(image) {
  var Intensidad_Lineal_VV = ee.Image(10).pow(image.select('VV').divide(10)).rename('Intensidad_VV');
  var Intensidad_Lineal_VH = ee.Image(10).pow(image.select('VH').divide(10)).rename('Intensidad_VH');
  var VV_VH_Ratio = image.select('VV').divide(image.select('VH')).rename('VV/VH Ratio');
  return image.addBands(Intensidad_Lineal_VV).addBands(Intensidad_Lineal_VH).addBands(VV_VH_Ratio);
};

var Sentinel_Intensidad= Sentinel_SAR.map(Sentinel_SAR_conversion).median()
print(Sentinel_Intensidad)

// Combine all the indices into one band

var imagen_final = cortado
                          .addBands(evi.rename('EVI'))
                          .addBands(ndwi.rename('NDWI'))
                          .addBands(tcb.rename('SBI'))
                          .addBands(tcg.rename('GVI'))
                          .addBands(tcw.rename('WET'))
                          .addBands(Elev.rename('Elevacion'))
                          .addBands(Slope.rename('Pendiente'))
                          .addBands(Sentinel_Intensidad.select('Intensidad_VV').rename('VV'))
                          .addBands(Sentinel_Intensidad.select('Intensidad_VH').rename('VH'))
                          .addBands(Sentinel_Intensidad.select('VV/VH Ratio').rename('ratio'))
                       ;

print(imagen_final) 
var bands = ['B2', 'B3', 'B4', 'B5', 'B8', 'B9', 'B11',
 'EVI', 'NDWI','SBI','GVI','WET',
'Elevacion', 'Pendiente', 'VV', 'VH', 'ratio' ]


// Training points 

var samples = Bosque.merge(No_Bosque)
print(samples.size())

var total_samples= imagen_final.select(bands).sampleRegions({
  collection: samples,
  properties: ['name','id'],
  scale: 10
})

total_samples= total_samples.randomColumn() 

var trainingSample = total_samples.filter('random <= 0.8');
var validationSample = total_samples.filter('random > 0.8');

print(total_samples.size())

// Classifier trained

var clasificador = ee.Classifier.smileRandomForest(100)
  .train({
  features: trainingSample,
  classProperty: 'id',
  inputProperties: bands})

// Applied classifier into the final indice image 

var classificacion_1 = imagen_final.select(bands).classify(clasificador)

var classVis = {
  min: 1,
  max: 2,
  palette: ['00B200 ' ,'#ff0400']
};

Map.centerObject(AOI)

print(classificacion_1)

var styling = {color: 'black', fillColor: '00000000'};

print(imagen_final)

// Export it into Google Drive 

Export.image.toAsset({ image: imagen_final,
description: 'Imagen_Final_2023',
scale: 10, 
region: AOI,
maxPixels: 1e11,
});
