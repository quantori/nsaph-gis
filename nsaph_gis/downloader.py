import os
import zipfile
from typing import Tuple
from urllib import request

from tqdm import tqdm


class GISDownloader:
    """
    Geographic Downloader downloads shape files for given dates
    from https://www.census.gov/
    """
    COUNTY_TEMPLATE = 'https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_us_county_500k.zip'
    ZIP_TEMPLATE = 'https://www2.census.gov/geo/tiger/GENZ{year}/shp/cb_{year}_us_zcta510_500k.zip'

    @classmethod
    def download_shapes(cls, year: int, output_dir: str = None, strict: bool = False) -> None:
        cls.download_zip(year, output_dir, strict)
        cls.download_county(year, output_dir, strict)

    @classmethod
    def download_zip(cls, year: int, output_dir: str = None, strict: bool = False) -> None:
        zip_url, is_exact = cls._get_zip_url(year)
        if strict and not is_exact:
            raise ValueError(f'There is no census data for year { year }.')

        cls._download_shape(zip_url, output_dir)

    @classmethod
    def download_county(cls, year: int, output_dir: str = None, strict: bool = False) -> None:
        county_url, is_exact = cls._get_county_url(year)
        if strict and not is_exact:
            raise ValueError(f'There is no census data for year { year }.')

        cls._download_shape(county_url, output_dir)

    @classmethod
    def _download_shape(cls, url: str, output_dir: str = None) -> None:
        if output_dir is None:
            output_dir = '.'

        shape_file = url.rsplit('/', 1)[1]
        dest = os.path.join(output_dir, shape_file)

        if not os.path.exists(dest):
            https_proxy = os.environ.get('HTTPS_PROXY')
            if https_proxy:
                proxy = request.ProxyHandler({'http': https_proxy, 'https': https_proxy})
                opener = request.build_opener(proxy)
                request.install_opener(opener)

            with tqdm() as bar:
                def report(blocknum, bs, size):
                    bar.total = size
                    bar.update(bs)
                request.urlretrieve(url, dest, reporthook=report)

        with zipfile.ZipFile(dest, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

    @classmethod
    def _get_county_url(cls, year: int) -> Tuple[str, bool]:
        """
            Method returns url to county shape file for nearest existing year data
        """
        if year > 2020:
            return cls._get_county_url(2020)[0], False

        if year in (2012, 2011) or year < 2010:
            return cls._get_county_url(2010)[0], False

        if year == 2010:
            return 'https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_us_050_00_500k.zip', True

        if year == 2013:
            return 'https://www2.census.gov/geo/tiger/GENZ2013/cb_2013_us_county_500k.zip', True

        if 2014 <= year <= 2020:
            return cls.COUNTY_TEMPLATE.format(year=year), True

    @classmethod
    def _get_zip_url(cls, year: int) -> Tuple[str, bool]:
        """
            Method returns url to zip shape file for nearest existing year data
        """
        if year > 2020:
            return cls._get_zip_url(2020)[0], False

        if year in (2012, 2011) or year < 2010:
            return cls._get_zip_url(2010)[0], False

        if year == 2010:
            return 'https://www2.census.gov/geo/tiger/GENZ2010/gz_2010_us_860_00_500k.zip', True

        if year == 2013:
            return 'https://www2.census.gov/geo/tiger/GENZ2013/cb_2013_us_zcta510_500k.zip', True

        if 2014 <= year <= 2019:
            return cls.ZIP_TEMPLATE.format(year=year), True

        if year == 2020:
            return 'https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_zcta520_500k.zip', True
