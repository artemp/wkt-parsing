from shapely.wkt import loads
from shapely.wkb import dumps
from osgeo import ogr
from osgeo import gdal
import mapnik

import time

wkt ="Polygon((-69.876092 12.427201,-69.887383 12.417538,-69.908054 12.417641,-69.92981 12.425806,-69.944356 12.440224,-69.923893 12.440224,-69.923893 12.447045,-69.957766 12.463013,-70.026884 12.522751,-70.04727 12.531019,-70.057399 12.536962,-70.061636 12.546677,-70.059621 12.556806,-70.050293 12.573911,-70.048045 12.583626,-70.051895 12.599801,-70.05882 12.614063,-70.060344 12.625225,-70.048045 12.631995,-70.006368 12.585383,-69.996188 12.577373,-69.935649 12.531639,-69.923893 12.51903,-69.91503 12.496861,-69.879425 12.453401,-69.876092 12.427201))"

import sys

if __name__ == "__main__":

    if len(sys.argv) < 2 :
        print>>sys.stderr,"Usage:",sys.argv[0],"<wkt> [<num_runs>]"
        sys.exit(1)

    if len(sys.argv) == 3:
        num_runs = int(sys.argv[2])
    else:
        num_runs = 1000

    for k in range(2):
        print "GDAL/OGR ...."
        ogr.UseExceptions()
        gdal.ErrorReset()
        start = time.clock()
        for i in range(num_runs):
            geometry = ogr.CreateGeometryFromWkt(sys.argv[1])
            wkb = geometry.ExportToWkb()
            geometry.Destroy()
        elapsed = (time.clock() - start)
        print>>sys.stderr,"elapsed=",elapsed

        print "Shapely ...."
        start = time.clock()
        for i in range(num_runs):
            geometry = loads(sys.argv[1])
            wkb = dumps(geometry)

        elapsed = (time.clock() - start)
        print>>sys.stderr,"elapsed=",elapsed

        print "Mapnik ...."
        start = time.clock()
        reader = mapnik.WKTReader()
        for i in range(num_runs):
            #geometry = mapnik.Path.from_wkt(sys.argv[1])
            geometry = reader.read(sys.argv[1])
            wkb = geometry.to_wkb(mapnik.wkbByteOrder.XDR)

        elapsed = (time.clock() - start)
        print>>sys.stderr,"elapsed=",elapsed
