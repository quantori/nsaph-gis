from nsaph_gis import downloader


def test_links_2017():
    links, is_exact = downloader.GISDownloader._get_links(2017)

    assert links == [
        "https://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_county_500k.zip",
        "https://www2.census.gov/geo/tiger/GENZ2017/shp/cb_2017_us_zcta510_500k.zip",
    ]
    assert is_exact is True


def test_links_2022():
    links, is_exact = downloader.GISDownloader._get_links(2022)

    assert links == [
        "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_county_500k.zip",
        "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_zcta520_500k.zip",
    ]
    assert is_exact is False
