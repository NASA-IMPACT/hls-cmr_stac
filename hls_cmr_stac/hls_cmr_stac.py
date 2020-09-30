import untangle
import datetime
import pystac
from pystac.extensions.eo import Band
from geojson import MultiPolygon
from shapely.geometry import shape


landsat_band_info = {
    'B01': {
        'band': Band.create(name="B01", common_name="coastal", center_wavelength=0.48, full_width_half_max=0.02),
        'gsd': 30.0
    },
    'B02': {
        'band': Band.create(name="B02", common_name="blue", center_wavelength=0.44, full_width_half_max=0.06),
        'gsd': 30.0
    },
    'B03': {
        'band': Band.create(name="B03", common_name="green", center_wavelength=0.56, full_width_half_max=0.06),
        'gsd': 30.0
    },
    'B04': {
        'band': Band.create(name="B04", common_name="red", center_wavelength=0.65, full_width_half_max=0.04),
        'gsd': 30.0
    },
    'B05': {
        'band': Band.create(name="B05", common_name="nir", center_wavelength=0.86, full_width_half_max=0.03),
        'gsd': 30.0
    },
    'B06': {
        'band': Band.create(name="B06", common_name="swir16", center_wavelength=1.6, full_width_half_max=0.08),
        'gsd': 30.0
    },
    'B07': {
        'band': Band.create(name="B07", common_name="swir22", center_wavelength=2.2, full_width_half_max=0.2),
        'gsd': 30.0
    },
    'B09': {
        'band': Band.create(name="B09", common_name="cirrus", center_wavelength=1.37, full_width_half_max=0.02),
        'gsd': 30.0
    },
    'B10': {
        'band': Band.create(name="B10", common_name="lwir11", center_wavelength=10.9, full_width_half_max=0.8),
        'gsd': 30.0
    },
    'B11': {
        'band': Band.create(name="B11", common_name="lwir12", center_wavelength=12.0, full_width_half_max=1.0),
        'gsd': 30.0
    }
}

sentinel_band_info = {
    'B01': {
        'band': Band.create(name="B01", common_name="coastal", center_wavelength=0.4439, full_width_half_max=0.027),
        'gsd': 30.0
    },
    'B02': {
        'band': Band.create(name="B02", common_name="blue", center_wavelength=0.4966, full_width_half_max=0.098),
        'gsd': 30.0
    },
    'B03': {
        'band': Band.create(name="B03", common_name="green", center_wavelength=0.56, full_width_half_max=0.045),
        'gsd': 30.0
    },
    'B04': {
        'band': Band.create(name="B04", common_name="red", center_wavelength=0.6645, full_width_half_max=0.038),
        'gsd': 30.0
    },
    'B05': {
        'band': Band.create(name="B05", center_wavelength=0.7039, full_width_half_max=0.019),
        'gsd': 30.0
    },
    'B06': {
        'band': Band.create(name="B06", center_wavelength=0.7402, full_width_half_max=0.018),
        'gsd': 30.0
    },
    'B07': {
        'band': Band.create(name="B07", center_wavelength=0.7825, full_width_half_max=0.028),
        'gsd': 30.0
    },
    'B08': {
        'band': Band.create(name="B08", common_name="nir", center_wavelength=0.8351, full_width_half_max=0.145),
        'gsd': 30
    },
    'B8A': {
        'band': Band.create(name="B8A", center_wavelength=0.8648, full_width_half_max=0.033),
        'gsd': 30
    },
    'B09': {
        'band': Band.create(name="B09", center_wavelength=0.945, full_width_half_max=0.026),
        'gsd': 30.0
    },
    'B10': {
        'band': Band.create(name="B10", common_name="cirrus", center_wavelength=1.3735, full_width_half_max=0.075),
        'gsd': 30
    },
    'B11': {
        'band': Band.create(name="B11", common_name="swir16", center_wavelength=1.6137, full_width_half_max=0.143),
        'gsd': 30
    },
    'B12': {
        'band': Band.create(name="B12", common_name="swir16", center_wavelength=2.22024, full_width_half_max=0.242),
        'gsd': 30
    }
}


def get_geometry(granule):
    multipolygon = []
    for poly in granule.Spatial.HorizontalSpatialDomain.Geometry.GPolygon:
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


def process_common_metadata(item, granule):
    start_datetime_str = granule.Temporal.RangeDateTime.BeginningDateTime.cdata
    item_start_datetime = datetime.datetime.strptime(start_datetime_str,
                                                     '%Y-%m-%dT%H:%M:%S.%fZ')
    end_datetime_str = granule.Temporal.RangeDateTime.EndingDateTime.cdata
    item_end_datetime = datetime.datetime.strptime(end_datetime_str,
                                                   '%Y-%m-%dT%H:%M:%S.%fZ')
    item.common_metadata.start_datetime = item_start_datetime
    item.common_metadata.end_datetime = item_end_datetime
    item.common_metadata.platform = granule.Platforms.Platform \
        .ShortName.cdata.lower()
    instrument = granule.Platforms.Platform.Instruments.Instrument \
        .ShortName.cdata.lower()
    if " " in instrument:
        item_instrument = instrument.split()[1]
    else:
        item_instrument = instrument
    item.common_metadata.instruments = [item_instrument]


def process_eo(item, granule):
    item.ext.enable('eo')
    for attribute in granule.AdditionalAttributes.AdditionalAttribute:
        if attribute.Name == "CLOUD_COVERAGE":
            item.ext.eo.cloud_cover = float(attribute.Values.Value.cdata)


def add_bands(item, granule):
    item_id = granule.GranuleUR.cdata
    product = item_id.split(".")[1]
    if product == "S30":
        band_info = sentinel_band_info
    if product == "L30":
        band_info = landsat_band_info

    for band_id, band_info in band_info.items():
        band_url = "./{}.{}.TIF".format(item_id, band_id)
        asset = pystac.Asset(href=band_url, media_type=pystac.MediaType.COG)
        bands = [band_info['band']]
        item.ext.eo.set_bands(bands, asset)
        item.add_asset(band_id, asset)


def main():
    cmr = untangle.parse("../tests/data/HLS.S30.T01LAH.2020097T222759.v1.5.xml")
    granule = cmr.Granule
    item_id = granule.GranuleUR.cdata
    datetime_str = granule.Temporal.RangeDateTime.BeginningDateTime.cdata
    item_datetime = datetime.datetime.strptime(datetime_str,
                                               '%Y-%m-%dT%H:%M:%S.%fZ')

    item_geometry = get_geometry(granule)
    multi = shape(item_geometry)
    item_bbox = list(multi.bounds)
    item = pystac.Item(id=item_id,
                       datetime=item_datetime,
                       geometry=item_geometry,
                       bbox=item_bbox,
                       properties={})

    process_common_metadata(item, granule)
    process_eo(item, granule)
    add_bands(item, granule)
    item.validate()


main()
