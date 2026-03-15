// Vector Datasets
var table = ee.FeatureCollection("projects/ee-luismaldonado123/assets/Racafe_Poligonos"),
    geometry = /* color: #d63000 */ee.Geometry.MultiPoint();

// Hansen Global Forest Change
var dataset = ee.Image('UMD/hansen/global_forest_change_2022_v1_10')

// Crea uina mascara para los años siguientes al 2020
var mask = dataset.select('lossyear').gte(20);

// Aplica la mascara al Dataset
var filteredDataset = dataset.updateMask(mask);

var treeLossVisParam = {
  bands: ['lossyear'],
  min: 20, // start from the year 2020
  max: 22, // adjust if new data is available
  palette: ['yellow', 'red']
};

var styling = {color: 'black', fillColor: '00000000'};

Map.addLayer(table.style(styling), {}, "Fincas");
Map.addLayer(filteredDataset, treeLossVisParam, 'Tree Loss 2020-2022');

// Modificación de la función para calcular pérdida de bosque y contar píxeles
function calculateForestLossAndCountPixels(farm) {
  // Máscara de dataset con pérdida de bosque desde 2020 dentro del límite del predio
  var lossWithinFarm = filteredDataset.updateMask(mask).clip(farm.geometry());

  // Calcula el área de pérdida de bosque
  var lossArea = lossWithinFarm.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: farm.geometry(),
    scale: 30 // Ajusta la escala según sea necesario
  });

  // Cuenta los píxeles de pérdida de bosque
  var pixelCount = lossWithinFarm.reduceRegion({
    reducer: ee.Reducer.count(),
    geometry: farm.geometry(),
    scale: 30 // Ajusta la escala según sea necesario
  });

  // Agrega el área de pérdida de bosque y el conteo de píxeles como propiedades del predio
  return farm.set({
    'forest_loss_area': lossArea.get('lossyear'),
    'forest_loss_pixel_count': pixelCount.get('lossyear')
  });
}

// Aplica la función modificada a cada predio
var farmsWithLossDataAndPixelCount = table.map(calculateForestLossAndCountPixels);

// Opcionalmente, puedes imprimir los resultados en la consola o exportarlos
print(farmsWithLossDataAndPixelCount);

// Exporta los resultados si es necesario
Export.table.toDrive({
  collection: farmsWithLossDataAndPixelCount
});

// Fincas filtradas por Nombre
var fincasFiltradasPorTipo = table.filter(ee.Filter.eq('Nombre_Pro', "Gerardo Ardila Pinto"));
Map.centerObject(fincasFiltradasPorTipo);