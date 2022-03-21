from constants import RasterizationStrategy, Geography


class ComputeShapesTask:
    """
    Class describes a compute task to aggregate data over geography shapes

    The data is expected in
    .. _Unidata netCDF (Version 4) format: https://www.unidata.ucar.edu/software/netcdf/
    """

    def __init__(
            self, year: int, variable: GridmetVariable, infile: str,
            outfile: str, strategy: RasterizationStrategy, shapefile: str,
            geography: Geography, date_filter=None
    ) -> None:
        """
        :param date_filter:
        :param year: year
        :param variable: Gridemt band (variable)
        :param infile: File with source data in  NCDF4 format
        :param outfile: Resulting CSV file
        :param strategy: Rasterization strategy to use
        :param shapefile: Shapefile for used collection of geographies
        :param geography: Type of geography, e.g. zip code or county
        """

        super().__init__(year, variable, infile, outfile, date_filter)


        if strategy == RasterizationStrategy.downscale:
            self.strategy = RasterizationStrategy.default
            self.factor = 5
        else:
            self.strategy = strategy
        self.shapefile = shapefile
        self.geography = geography

    def to_date(self, day) -> datetime.date:
        origin = date(1900, 1, 1)
        return self.origin + timedelta(days=day)

    def compute_one_day(self, writer: Collector, day, layer):
        dt = self.to_date(day)
        if self.factor > 1:
            layer = disaggregate(layer, self.factor)
        logging.info("{}:{}:{}".format(
            self.geography.value,self.band.value,str(dt))
        )
        l = None
        stats1 = []
        stats2 = []
        if self.strategy in [RasterizationStrategy.default,
                             RasterizationStrategy.combined]:
            stats1 = zonal_stats(self.shapefile, layer, stats="mean",
                                 affine=self.affine, geojson_out=True,
                                 all_touched=False, nodata=NO_DATA)
            l = len(stats1)
        if self.strategy in [RasterizationStrategy.all_touched,
                             RasterizationStrategy.combined]:
            stats2 = zonal_stats(self.shapefile, layer, stats="mean",
                                 affine=self.affine, geojson_out=True,
                                 all_touched=True, nodata=NO_DATA)
            l = len(stats2)

        for i in range(0, l):
            record = stats1[0] if stats1 else stats2[0]
            key = self.determine_key(record)

            if self.strategy == RasterizationStrategy.combined:
                mean, prop = self.combine(key, stats1[i], stats2[i])
            elif self.strategy == RasterizationStrategy.default:
                mean = stats1[i]['properties']['mean']
                prop = stats1[i]['properties'][key]
            else:
                mean = stats2[i]['properties']['mean']
                prop = stats2[i]['properties'][key]
            writer.writerow([mean, dt.strftime("%Y-%m-%d"), prop])
        return

    def get_key(self):
        return self.geography.value.upper()

    @staticmethod
    def determine_key(record) -> str:
        if "ZIP" in record['properties']:
            return "ZIP"
        elif "ZCTA5CE10" in record['properties']:
            return "ZCTA5CE10"
        else:
            raise ValueError("Unknown shape format, no ZIP neither ZCTA5CE10")

    @staticmethod
    def combine(key, r1, r2):
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
        return mean, prop
