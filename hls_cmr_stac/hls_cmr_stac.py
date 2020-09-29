import untangle
import datetime
from pystac import Item
from geojson import MultiPolygon
from shapely.geometry import shape


def get_geometry(cmr):
    multipolygon = []
    for poly in cmr.Granule.Spatial.HorizontalSpatialDomain.Geometry.GPolygon:
        ring = []
        for point in poly.Boundary.Point:
            geojson_point = [
                float(point.PointLongitude.cdata),
                float(point.PointLatitude.cdata),
            ]
            ring.append(geojson_point)

        closing_point = [
            float(poly.Boundary.Point[0].PointLongitude.cdata),
            float(poly.Boundary.Point[0].PointLatitude.cdata),
        ]
        ring.append(closing_point)
        ringtuple = (ring, )
        multipolygon.append(ringtuple)
    geometry = MultiPolygon(multipolygon)
    return geometry


def main():
    cmr = untangle.parse("../tests/data/HLS.S30.T01LAH.2020097T222759.v1.5.xml")
    item_id = cmr.Granule.GranuleUR.cdata
    datetime_str = cmr.Granule.Temporal.RangeDateTime.BeginningDateTime.cdata
    item_datetime = datetime.datetime.strptime(datetime_str,
                                               '%Y-%m-%dT%H:%M:%S.%fZ')

    item_geometry = get_geometry(cmr)
    multi = shape(item_geometry)
    item_bbox = list(multi.bounds)
    item = Item(id=item_id,
                datetime=item_datetime,
                geometry=item_geometry,
                bbox=item_bbox,
                properties={})

    item.validate()

main()
