# GeoTag Detection

GeoTag Detection is a NovaVision component designed to convert pixel-based object detections into real-world geographic coordinates (Latitude & Longitude) using camera telemetry data.

## Features
* **Flat-Earth Projection:** Calculates precise geographic coordinates using camera altitude, FOV, and heading.
* **Tensor Support:** Dynamically handles both 3D image arrays and 4D video tensors without shape mismatch errors.
* **Fault Tolerance:** Robust exception handling for empty prediction streams and missing telemetry.
* **Standardized Output:** Generates ready-to-use `GeoJSON` FeatureCollections for immediate map visualization.

## Configuration Parameters
* `latitude`: GPS latitude of the camera ([-90.0, 90.0]).
* `longitude`: GPS longitude of the camera ([-180.0, 180.0]).
* `altitude`: Camera altitude above ground level in meters (> 0.0).
* `horizontal_fov`: Horizontal field of view of the sensor in degrees (e.g., 73.7).
* `heading`: Compass bearing in degrees (0-360).

## Quick Start (Sample Payload)
```json
{
  "inputImage": { "type": "Image", "encoding": "base64", "value": "..." },
  "predictions": [
    { "class": "vehicle", "confidence": 0.85, "x": 960, "y": 540, "width": 100, "height": 50 }
  ],
  "configs": {
    "latitude": 40.123456,
    "longitude": 29.654321,
    "altitude": 50.0,
    "horizontal_fov": 73.7,
    "heading": 90.0
  }
}
Outputs
geo_detections: A raw list of enriched detection objects with real-world coordinates.

geojson: A standard GeoJSON FeatureCollection optimized for GIS and map interfaces.
