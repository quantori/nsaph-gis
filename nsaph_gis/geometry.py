#  Copyright (c) 2021. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import itertools
from typing import Optional

from numpy.ma import masked
from rasterstats import point


class PointInRaster:
    COMPLETELY_MASKED = 1
    PARTIALLY_MASKED = 2

    def __init__(self, raster, affine, x, y):
        self.window, unitxy = point.point_window_unitxy(x, y, affine)
        self.x, self.y = unitxy
        self.masked = 0

        m = 0
        array = raster.read(window=self.window, masked=True).array
        for i, j in itertools.product([0,1], [0,1]):
            r = self.window[0][0] + i
            c = self.window[1][0] + j
            if array[i, j] is masked:
                m += 1
            elif raster.array[r, c] is masked:
                m += 1
            else:
                self.r, self.c = r, c

        if m == 4:
            self.masked = self.COMPLETELY_MASKED
        elif m > 0:
            self.masked = self.PARTIALLY_MASKED

    def is_masked(self):
        return self.masked == self.COMPLETELY_MASKED

    def array(self, raster):
        return raster.array[
            self.window[0][0]:self.window[0][1],
            self.window[1][0]:self.window[1][1],
        ]

    def bilinear(self, raster) -> Optional[float]:
        if self.masked == self.COMPLETELY_MASKED:
            return None

        if self.masked == self.PARTIALLY_MASKED:
            return raster.array[self.r, self.c]

        array = self.array(raster)

        x, y = self.x, self.y
        ulv, urv, llv, lrv = array[0,0], array[0,1], array[1,0], array[1,1]
        return (
            (llv * (1 - x) * (1 - y)) +
            (lrv * x * (1 - y)) +
            (ulv * (1 - x) * y) +
            (urv * x * y)
        )
