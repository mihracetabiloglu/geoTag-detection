from sdks.novavision.src.helper.package import PackageHelper
from components.GeoTagDetection.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    GeoTagDetectionExecutor,
    GeoTagDetectionResponse,
    GeoTagDetectionOutputs,
    OutputGeoDetections,
    OutputGeojson,
)


def build_response(context):
    output_geo_detections = OutputGeoDetections(value=context.geo_detections)
    output_geojson = OutputGeojson(value=context.geojson)
    outputs = GeoTagDetectionOutputs(
        geo_detections=output_geo_detections,
        geojson=output_geojson,
    )

    geoTagDetectionResponse = GeoTagDetectionResponse(outputs=outputs)
    geoTagDetectionExecutor = GeoTagDetectionExecutor(value=geoTagDetectionResponse)
    executor = ConfigExecutor(value=geoTagDetectionExecutor)
    package_configs = PackageConfigs(executor=executor)

    package = PackageHelper(packageModel=PackageModel, packageConfigs=package_configs)
    packageModel = package.build_model(context)
    return packageModel