#%%
from pathlib import Path
import geopandas as gpd
import numpy as np
from shapely.geometry import box

#%%
# Create a function to load the boundary file and return a GeoDataFrame.
def load_boundary(file_path: str | Path) -> gpd.GeoDataFrame:
    '''
    Refactor the 'Quads' column in a CNPS CSV file to extract quad IDs as a list of integers.

    Parameters
    ----------
    file_path : str | Path
        Path to the boundary file (GeoJSON or KMZ)

    Returns 
    ----------
    gdf.GeoDataFrame
        GeoDataFrame with the boundary geometry loaded from the file.

    Notes
    ----------
    Returns a GeoDataFrame with the boundary geometry loaded from the file. 
    Sets the CRS to WGS84 (EPSG:4326) if it is not already set.
    The function currently supports GeoJSON and Shapefile formats. 
    KMZ support may be added in the future.
    '''

    
    # TODO: Add documentation
    # Handle different file formats
    # For now, we will assume that the file is a GeoJSON or Shapefile
    # Add kmz support in the future
    file_path = Path(file_path)    
    gdf = gpd.read_file(file_path)
    # Set the CRS to WGS84 (EPSG:4326) if it is not already set
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
    return gdf

#%%

# Create a function to create a buffer around the boundary and return a new GeoDataFrame with the buffered geometry.
def create_buffer(gdf: gpd.GeoDataFrame, distance: float) -> gpd.GeoDataFrame:
    '''
    Create a buffer around the geometries in the GeoDataFrame and return a new GeoDataFrame with the buffered geometry.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with the boundary geometry loaded from the file.
    distance : float
        Distance in meters to buffer around the boundary.

    Returns 
    ----------
    gpd.GeoDataFrame
        GeoDataFrame with the buffered geometry.

    Notes
    ----------
    Returns a GeoDataFrame with the buffered geometry. 
    The original GeoDataFrame is not modified.
    '''

    # TODO: Add documentation
    # Distance should be in meters to match the 
    # CRS we will use for buffering (California Albers)
    # Create a buffer around the geometries in the GeoDataFrame
    # create a copy of the GeoDataFrame to avoid modifying the original
    gdf_buffered = gdf.copy()
    # Set the CRS to the California Albers (EPSG:3310) 
    # for accurate distance measurements
    gdf_buffered = gdf_buffered.to_crs(epsg=3310)
    gdf_buffered['geometry'] = gdf_buffered.geometry.buffer(distance)
    # Return the buffered GeoDataFrame in the original CRS
    gdf_buffered = gdf_buffered.to_crs(epsg=4326)
    return gdf_buffered

#%%

# Create a function of get a bounding box from a GeoDataFrame.
def get_bounding_box(gdf: gpd.GeoDataFrame) -> np.ndarray:
    '''
    Get the bounding box of the geometries in a GeoDataFrame.

    Parameters
    ----------
    gdf : gpd.GeoDataFrame
        GeoDataFrame with the boundary geometry loaded from the file

    Returns 
    ----------
    np.ndarray
        Array with the bounding box coordinates [minx, miny, maxx, maxy]

    Notes
    ----------
    Returns an array with the bounding box coordinates [minx, miny, maxx, maxy] of the geometries in the GeoDataFrame.
    '''

    # TODO: Add documentation
    # Get the bounding box of the geometries in the GeoDataFrame
    # The bounding box is returned as a list of [minx, miny, maxx, maxy]
    bounds = gdf.total_bounds
    return bounds

#%%

def load_all_quads(filepath: str | Path) -> gpd.GeoDataFrame:
    """
    Docstring for load_quads
    
    :param filepath: Description
    :type filepath: str | Path
    :return: Description
    :rtype: GeoDataFrame

    TODO: Docstrings
    
    """
    filepath = Path(filepath)
    gdf = gpd.read_file(filepath)
    return gdf
#%%

def _cell_map_code(id):
    """
    Docstring for _cell_map_code
    
    :param id: Description

    """
    lead, tail = str(id).split('-')
    pos = ['','A','B','C','D','E','F','G','H']
    my_num = pos.index(tail[0])
    cell_map_code = str(lead) + str(my_num) + str(tail[1])
    return int(cell_map_code)


def get_quads(boundary, all_quads):
    """
    Docstring for get_quads
    
    :param bounds: Description

    TODO: Docstrings
    TODO: Annotations for function arguments and return
    TODO: Ensure CRS consistency before intersect command

    """
    minx, miny, maxx, maxy = boundary.total_bounds
    bbox = box(minx, miny, maxx, maxy)
    quads = all_quads[all_quads.intersects(bbox)].copy()
    # This next line should work, but might not.
    cell_map_codes = [_cell_map_code(id) for id in set(quads['CELL_MAPCODE'])]
    return set(cell_map_codes)

# %%

def get_species(cnps_df, quad_ids):
    """
    Docstring for species_in_quads
    
    :param species: Description
    :param quads: Description
    # THis is the command to filter the CNPS data on the set of quads we find
    #    Is assume the CNPS list of quads is in the column called 'QUAD_IDS' and the 
    # CNPS data is a dataframe called... df!
    # Also, quad_ids is a set of IDs!

    """
    cnps_species = cnps_df[cnps_df['split_quad'].apply(lambda x: bool(quad_ids.intersection(x)))].copy()
    return cnps_species




# %%
