import os
import zipfile
from typing import List, Tuple
from urllib import request


class GISDownloader:
    """
    Geographic Downloader downloads shape files for given dates
    from https://www.census.gov/
    """
    COUNTY_TEMPLATE = 'https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_us_county_500k.zip'
    ZIP_TEMPLATE = 'https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_us_zcta510_500k.zip'

    @classmethod
    def download_shapes(cls, year: int, output_dir: str = None, strict: bool = False):
        if output_dir is None:
            output_dir = '.'

        shape_file_links, is_exact = cls._get_links(year)
        if strict and not is_exact:
            raise ValueError(f'There is no census data for year { year }.')

        for link in [shape_file_links[1]]:
            shape_file = link.rsplit('/', 1)[1]
            dest = os.path.join(output_dir, shape_file)
            request.urlretrieve(link, dest)

            with zipfile.ZipFile(dest, 'r') as zip_ref:
                zip_ref.extractall(output_dir)

    @classmethod
    def _get_links(cls, year: int) -> Tuple[List[str], bool]:
        """
            Method returns links to zip and county shape files for nearest existing year data
        """
        if year > 2020:
            return cls._get_links(2020)[0], False

        if year in (2012, 2011) or year < 2010:
            return cls._get_links(2010)[0], False

        if year == 2010:
            return [
                'https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_us_050_00_500k.zip',
                'https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_us_860_00_500k.zip',
            ], True

        if year == 2013:
            return [
                'https://www2.census.gov/geo/tiger/GENZ2013/cb_2013_us_county_500k.zip',
                'https://www2.census.gov/geo/tiger/GENZ2013/cb_2013_us_zcta510_500k.zip',
            ], True

        if 2014 <= year <= 2019:
            return [
                cls.COUNTY_TEMPLATE.format(year=year),
                cls.ZIP_TEMPLATE.format(year=year),
            ], True

        if year == 2020:
            return [
                cls.COUNTY_TEMPLATE.format(year=year),
                'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_zcta520_500k.zip',
            ], True
