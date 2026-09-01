from sdks.novavision.src.helper.package import PackageHelper
from components.GeoTagDetection.src.models.PackageModel import (
    PackageModel,
    OutputGeoDetections,
    OutputGeojson,
    GeoTagDetectionOutputs,
    GeoTagDetectionResponse,
    PackageConfigs
)


def build_response(context):
    output_geo_detection = OutputGeoDetections(value = context.geo_detections)
    output_geojson = OutputGeojson(value = context.geojson)
    outputs = GeoTagDetectionOutputs(geo_detections = output_geo_detection, geojson = output_geojson)
    geoTagDetectionResponse = GeoTagDetectionResponse(outputs=outputs)
    geoTagDetectionExecutor =geoTagDetectionExecutor(value=geoTagDetectionResponse)
    packageConfigs = PackageConfigs(executor=geoTagDetectionExecutor)
    package = PackageHelper(packageModel=PackageModel, geoTagDetectionResponse=geoTagDetectionResponse)
    packageModel = package.build_model(context)
    return packageModel