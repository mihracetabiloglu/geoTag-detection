from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image, None] = None
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        if isinstance(val, Image):
            return "object"
        elif isinstance(val, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class InputPredictions(Input):
    """
    Detection predictions coming from an upstream detection component
    (e.g. bounding boxes with x, y, width, height, confidence, class).
    NOTE: if the SDK already exposes a typed Prediction/Detection model
    (e.g. sdks.novavision.src.media.prediction.Prediction), swap the
    `List[dict]` below for `List[Prediction]` to get proper validation.
    """
    name: Literal["predictions"] = "predictions"
    value: List[dict] = []
    type: Literal["list"] = "list"

    class Config:
        title = "Predictions"


class OutputGeoDetections(Output):
    name: Literal["geo_detections"] = "geo_detections"
    value: List[dict] = []
    type: Literal["list"] = "list"

    class Config:
        title = "Geo Detections"


class OutputGeojson(Output):
    name: Literal["geojson"] = "geojson"
    value: dict = {}
    type: Literal["object"] = "object"

    class Config:
        title = "GeoJSON"


class Latitude(Config):
    """
    GPS latitude of the camera position in decimal degrees.
    Positive values are North, negative are South.
    """
    name: Literal["latitude"] = "latitude"
    value: float = Field(ge=-90.0, le=90.0, default=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-90, 90]"] = "[-90, 90]"

    class Config:
        title = "Latitude"


class Longitude(Config):
    """
    GPS longitude of the camera position in decimal degrees.
    Positive values are East, negative are West.
    """
    name: Literal["longitude"] = "longitude"
    value: float = Field(ge=-180.0, le=180.0, default=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-180, 180]"] = "[-180, 180]"

    class Config:
        title = "Longitude"


class Altitude(Config):
    """
    Camera altitude above ground level in meters. For drones, this is
    the relative altitude reported by the flight controller.
    """
    name: Literal["altitude"] = "altitude"
    value: float = Field(gt=0.0, default=50.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["> 0"] = "> 0"

    class Config:
        title = "Altitude"


class HorizontalFov(Config):
    """
    Horizontal field of view of the camera in degrees. Default 73.7
    covers most DJI consumer drones (Mini, Air, Mavic series).
    """
    name: Literal["horizontal_fov"] = "horizontal_fov"
    value: float = Field(gt=0.0, lt=180.0, default=73.7)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["(0, 180)"] = "(0, 180)"

    class Config:
        title = "Horizontal FOV"


class Heading(Config):
    """
    Compass bearing that the top of the image points toward, in degrees
    clockwise from true north. 0 means image-up is North.
    """
    name: Literal["heading"] = "heading"
    value: float = Field(ge=0.0, le=360.0, default=0.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[0, 360]"] = "[0, 360]"

    class Config:
        title = "Heading"


class GeoTagDetectionInputs(Inputs):
    inputImage: InputImage
    predictions: InputPredictions


class TaskConfigs(Configs):
    latitude: Latitude
    longitude: Longitude
    altitude: Altitude
    horizontal_fov: HorizontalFov
    heading: Heading


class GeoTagDetectionOutputs(Outputs):
    geo_detections: OutputGeoDetections
    geojson: OutputGeojson


class GeoTagDetectionRequest(Request):
    inputs: Optional[GeoTagDetectionInputs]
    configs: TaskConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class GeoTagDetectionResponse(Response):
    outputs: GeoTagDetectionOutputs


class GeoTagDetectionExecutor(Config):
    name: Literal["GeoTagDetectionExecutor"] = "GeoTagDetectionExecutor"
    value: Union[GeoTagDetectionRequest, GeoTagDetectionResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "GeoTag Detection"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[GeoTagDetectionExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["GeoTagDetection"] = "GeoTagDetection"