from enum import Enum


class RasterizationStrategy(Enum):
    """
    Rasterization Strategy, see details at
    https://pythonhosted.org/rasterstats/manual.html#rasterization-strategy
    """

    # The default strategy is to include all pixels along the line render path
    # (for lines), or cells where the center point is within the polygon
    # (for polygons).
    default = 'default'

    # Alternate, all_touched strategy, rasterizes the geometry
    # by including all pixels that it touches.
    all_touched = 'all_touched'

    # Calculate statistics using both default and all_touched strategy and
    # combine results, e.g. using arithmetic means
    combined = 'combined'

    # Equivalent of "default" startegy with factor = 5
    downscale = 'downscale'


class Geography(Enum):
    """Type of geography"""
    zip = 'zip'
    county = 'county'
    custom = 'custom'
