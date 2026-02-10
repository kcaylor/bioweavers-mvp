# Geometry Tutorial

This walkthrough builds each function in `src/geometry.py` step by step.

## `load_boundary`

**1. Function definition and docstrings**
```python
import geopandas as gpd
from pathlib import Path


def load_boundary(filepath: str | Path) -> gpd.GeoDataFrame:
    """
    Load a project boundary from GeoJSON or KML file.

    Parameters
    ----------
    filepath : str or Path
        Path to GeoJSON or KML file

    Returns
    -------
    gpd.GeoDataFrame
        GeoDataFrame with boundary geometry in WGS84 (EPSG:4326)
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    filepath = Path(filepath)
    gdf = gpd.read_file(filepath)
    return gdf
```

**3. Function implementation**
```python
    filepath = Path(filepath)

    if filepath.suffix.lower() == ".geojson":
        gdf = gpd.read_file(filepath)
    elif filepath.suffix.lower() in [".kml", ".kmz"]:
        gdf = gpd.read_file(filepath, driver="KML")
    else:
        raise ValueError(f"Unsupported file type: {filepath.suffix}")

    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    elif gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    return gdf
```

**4. Example usage**
```python
from src.geometry import load_boundary

gdf = load_boundary("data/sample_boundary.geojson")
print(gdf.crs)
```

## `create_buffer`

**1. Function definition and docstrings**
```python
def create_buffer(gdf: gpd.GeoDataFrame, distance_miles: float) -> gpd.GeoDataFrame:
    """
    Create a buffer around the boundary geometry.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        Input geometry (should be in WGS84)
    distance_miles : float
        Buffer distance in miles

    Returns
    -------
    gpd.GeoDataFrame
        Buffered geometry in WGS84 (EPSG:4326)
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    distance_m = distance_miles * 1609.34
    return gdf
```

**3. Function implementation**
```python
    distance_m = distance_miles * 1609.34
    gdf_projected = gdf.to_crs("EPSG:3310")

    gdf_buffered = gdf_projected.copy()
    gdf_buffered["geometry"] = gdf_projected.geometry.buffer(distance_m)

    gdf_buffered = gdf_buffered.to_crs("EPSG:4326")
    return gdf_buffered
```

**4. Example usage**
```python
from src.geometry import load_boundary, create_buffer

boundary = load_boundary("data/sample_boundary.geojson")
buffered = create_buffer(boundary, distance_miles=5)
```

## `get_bounding_box`

**1. Function definition and docstrings**
```python
def get_bounding_box(gdf: gpd.GeoDataFrame) -> tuple[float, float, float, float]:
    """
    Get the bounding box of a GeoDataFrame in (minx, miny, maxx, maxy) format.

    Returns coordinates in WGS84 for API queries.
    """
    raise NotImplementedError
```

**2. Stub out functional code**
```python
    bounds = gdf.total_bounds
    return tuple(bounds)
```

**3. Function implementation**
```python
    if gdf.crs != "EPSG:4326":
        gdf = gdf.to_crs("EPSG:4326")

    bounds = gdf.total_bounds
    return tuple(bounds)
```

**4. Example usage**
```python
from src.geometry import load_boundary, get_bounding_box

boundary = load_boundary("data/sample_boundary.geojson")
bbox = get_bounding_box(boundary)
print(bbox)
```
