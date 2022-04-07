from nsaph_gis import downloader


def test_county_url_2017():
    url, is_exact = downloader.GISDownloader._get_county_url(2017)

    assert url == "https://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_county_500k.zip"
    assert is_exact is True


def test_zip_url_2017():
    url, is_exact = downloader.GISDownloader._get_zip_url(2017)

    assert url == "https://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_zcta510_500k.zip"
    assert is_exact is True


def test_county_url_2022():
    url, is_exact = downloader.GISDownloader._get_county_url(2022)

    assert url == "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_500k.zip"
    assert is_exact is False


def test_zip_url_2022():
    url, is_exact = downloader.GISDownloader._get_zip_url(2022)

    assert url == "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_zcta520_500k.zip"
    assert is_exact is False
