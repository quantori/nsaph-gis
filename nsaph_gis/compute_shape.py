from dataclasses import dataclass
from typing import Iterable, Optional

import rasterio
from rasterstats import zonal_stats

from .constants import RasterizationStrategy

NO_DATA = -999  # I do not know what it is, but not setting it causes a warning


@dataclass
class Record:
    mean: Optional[float]
    prop: str


class StatsCounter:
    @classmethod
    def process(
        cls,
        strategy: RasterizationStrategy,
        shapefile: str,
        affine: rasterio.Affine,
        layer: Iterable
    ) -> Iterable[Record]:
        all_touched_strategies = [
            RasterizationStrategy.default,
            RasterizationStrategy.combined,
            RasterizationStrategy.downscale,
        ]
        non_all_touched_strategies = [
            RasterizationStrategy.all_touched,
            RasterizationStrategy.combined,
        ]

        stats = []
        if strategy in all_touched_strategies:
            stats.append(
                zonal_stats(
                    shapefile,
                    layer,
                    stats="mean",
                    affine=affine,
                    geojson_out=True,
                    all_touched=False,
                    nodata=NO_DATA,
                )
            )
        if strategy in non_all_touched_strategies:
            stats.append(
                zonal_stats(
                    shapefile,
                    layer,
                    stats="mean",
                    affine=affine,
                    geojson_out=True,
                    all_touched=True,
                    nodata=NO_DATA,
                )
            )

        if not len(stats[0]):
            return

        row = stats[0][0]
        key = cls._determine_key(row)

        for i in range(len(stats[0])):
            if len(stats) == 2:
                # Combined strategy
                mean, prop = cls._combine(key, stats[0][i], stats[1][i])

            else:
                mean = stats[0][i]['properties']['mean']
                prop = stats[0][i]['properties'][key]

            yield Record(mean=mean, prop=prop)

    @staticmethod
    def _determine_key(row) -> str:
        if "ZIP" in row['properties']:
            return "ZIP"
        elif "ZCTA5CE10" in row['properties']:
            return "ZCTA5CE10"
        else:
            raise ValueError("Unknown shape format, no ZIP neither ZCTA5CE10")

    @staticmethod
    def _combine(key, r1, r2) -> Record:
        prop = r1['properties'][key]
        assert prop == r2['properties'][key]

        m1 = r1['properties']['mean']
        m2 = r2['properties']['mean']
        if m1 and m2:
            mean = (m1 + m2) / 2
        elif m2:
            mean = m2
        elif m1:
            raise AssertionError("m1 && !m2")
        else:
            mean = None
        return Record(mean=mean, prop=prop)
