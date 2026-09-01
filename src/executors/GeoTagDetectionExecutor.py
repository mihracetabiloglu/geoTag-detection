import os
import cv2
import sys
import math

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.GeoTagDetection.src.utils.response import build_response
from components.GeoTagDetection.src.models.PackageModel import PackageModel


class GeoTagDetectionExecutor(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))

        self.latitude = self.request.get_param("latitude")
        self.longitude = self.request.get_param("longitude")
        self.altitude = self.request.get_param("altitude")
        self.horizontal_fov = self.request.get_param("horizontal_fov")
        self.heading = self.request.get_param("heading")

        self.image = self.request.get_param("inputImage")
        self.predictions = self.request.get_param("predictions")

        # plain instance attributes, filled in by compute_geotags() and
        # read directly by build_response() (context.geo_detections /
        # context.geojson) — mirrors CountPixelExecutor.matching_pixels_count
        self.geo_detections = []
        self.geojson = {"type": "FeatureCollection", "features": []}

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def compute_geotags(self, img_shape, predictions):
        img_h, img_w = img_shape[:2]

        if self.altitude <= 0:
            return [], {"type": "FeatureCollection", "features": []}

        hfov_rad = math.radians(self.horizontal_fov)
        ground_width = 2.0 * self.altitude * math.tan(hfov_rad / 2.0)

        aspect_ratio = img_h / img_w if img_w > 0 else 1.0
        ground_height = ground_width * aspect_ratio

        m_per_pixel_x = ground_width / img_w if img_w > 0 else 0
        m_per_pixel_y = ground_height / img_h if img_h > 0 else 0

        cx = img_w / 2.0
        cy = img_h / 2.0

        heading_rad = math.radians(self.heading)
        cos_h = math.cos(heading_rad)
        sin_h = math.sin(heading_rad)

        lat_rad = math.radians(self.latitude)
        meters_per_deg_lat = 111132.0
        meters_per_deg_lon = 111132.0 * math.cos(lat_rad)

        geo_detections = []
        features = []

        if predictions is None or len(predictions) == 0:
            return geo_detections, {"type": "FeatureCollection", "features": features}

        for pred in predictions:
            pred_x = pred.get("x", 0.0)
            pred_y = pred.get("y", 0.0)
            conf = pred.get("confidence", 0.0)
            class_name = pred.get("class", "object")

            dx_px = pred_x - cx
            dy_px = cy - pred_y

            dx_m = dx_px * m_per_pixel_x
            dy_m = dy_px * m_per_pixel_y

            east_offset = dx_m * cos_h - dy_m * sin_h
            north_offset = dx_m * sin_h + dy_m * cos_h

            d_lat = north_offset / meters_per_deg_lat
            d_lon = east_offset / meters_per_deg_lon if meters_per_deg_lon != 0 else 0.0

            det_lat = self.latitude + d_lat
            det_lon = self.longitude + d_lon

            detection_record = {
                "class": class_name,
                "confidence": conf,
                "latitude": det_lat,
                "longitude": det_lon,
                "altitude": 0.0,
                "bounding_box": {
                    "x": pred_x,
                    "y": pred_y,
                    "width": pred.get("width", 0),
                    "height": pred.get("height", 0)
                }
            }
            geo_detections.append(detection_record)

            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [det_lon, det_lat]
                },
                "properties": {
                    "class": class_name,
                    "confidence": conf,
                    "altitude": self.altitude
                }
            }
            features.append(feature)

        geojson_output = {
            "type": "FeatureCollection",
            "features": features
        }

        return geo_detections, geojson_output

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)

        shape = img.value.shape
      
        if len(shape) == 4:
            img_h, img_w = shape[1], shape[2]
       
        else:
            img_h, img_w = shape[0], shape[1]

        self.geo_detections, self.geojson = self.compute_geotags((img_h, img_w), self.predictions)

        packageModel = build_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()