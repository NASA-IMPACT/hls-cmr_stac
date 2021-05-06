"""
Generate STAC items for HLS products

Usage: cmr_to_stac_item [OPTIONS] CMRXML OUTPUTFILE ENDPOINT VERSION


Example:
$ cmr_to_stac_item ./HLS.S30.T01LAH.2020097T222759.v1.5 ./stac_item.json data.lpdaac.earthdatacloud.nasa.gov 020

"""
import untangle
import datetime
import json
import pystac
import click
from pystac.extensions.eo import Band
from geojson import MultiPolygon
from shapely.geometry import shape


landsat_band_info = {
    "B01": {
        "band": Band.create(name="B01", common_name="coastal", center_wavelength=0.48, full_width_half_max=0.02),
        "gsd": 30.0
    },
    "B02": {
        "band": Band.create(name="B02", common_name="blue", center_wavelength=0.44, full_width_half_max=0.06),
        "gsd": 30.0
    },
    "B03": {
        "band": Band.create(name="B03", common_name="green", center_wavelength=0.56, full_width_half_max=0.06),
        "gsd": 30.0
    },
    "B04": {
        "band": Band.create(name="B04", common_name="red", center_wavelength=0.65, full_width_half_max=0.04),
        "gsd": 30.0
    },
    "B05": {
        "band": Band.create(name="B05", common_name="nir", center_wavelength=0.86, full_width_half_max=0.03),
        "gsd": 30.0
    },
    "B06": {
        "band": Band.create(name="B06", common_name="swir16", center_wavelength=1.6, full_width_half_max=0.08),
        "gsd": 30.0
    },
    "B07": {
        "band": Band.create(name="B07", common_name="swir22", center_wavelength=2.2, full_width_half_max=0.2),
        "gsd": 30.0
    },
    "B09": {
        "band": Band.create(name="B09", common_name="cirrus", center_wavelength=1.37, full_width_half_max=0.02),
        "gsd": 30.0
    },
    "B10": {
        "band": Band.create(name="B10", common_name="lwir11", center_wavelength=10.9, full_width_half_max=0.8),
        "gsd": 30.0
    },
    "B11": {
        "band": Band.create(name="B11", common_name="lwir12", center_wavelength=12.0, full_width_half_max=1.0),
        "gsd": 30.0
    },
    "Fmask": {
        "band": Band.create(name="Fmask"),
        "gsd": 30.0
    },
    "SZA": {
        "band": Band.create(name="SZA"),
        "gsd": 30.0
    },
    "SAA": {
        "band": Band.create(name="SAA"),
        "gsd": 30.0
    },
    "VZA": {
        "band": Band.create(name="VZA"),
        "gsd": 30.0
    },
    "VAA": {
        "band": Band.create(name="VAA"),
        "gsd": 30.0
    }
}

sentinel_band_info = {
    "B01": {
        "band": Band.create(name="B01", common_name="coastal", center_wavelength=0.4439, full_width_half_max=0.027),
        "gsd": 30.0
    },
    "B02": {
        "band": Band.create(name="B02", common_name="blue", center_wavelength=0.4966, full_width_half_max=0.098),
        "gsd": 30.0
    },
    "B03": {
        "band": Band.create(name="B03", common_name="green", center_wavelength=0.56, full_width_half_max=0.045),
        "gsd": 30.0
    },
    "B04": {
        "band": Band.create(name="B04", common_name="red", center_wavelength=0.6645, full_width_half_max=0.038),
        "gsd": 30.0
    },
    "B05": {
        "band": Band.create(name="B05", center_wavelength=0.7039, full_width_half_max=0.019),
        "gsd": 30.0
    },
    "B06": {
        "band": Band.create(name="B06", center_wavelength=0.7402, full_width_half_max=0.018),
        "gsd": 30.0
    },
    "B07": {
        "band": Band.create(name="B07", center_wavelength=0.7825, full_width_half_max=0.028),
        "gsd": 30.0
    },
    "B08": {
        "band": Band.create(name="B08", common_name="nir", center_wavelength=0.8351, full_width_half_max=0.145),
        "gsd": 30
    },
    "B8A": {
        "band": Band.create(name="B8A", center_wavelength=0.8648, full_width_half_max=0.033),
        "gsd": 30
    },
    "B09": {
        "band": Band.create(name="B09", center_wavelength=0.945, full_width_half_max=0.026),
        "gsd": 30.0
    },
    "B10": {
        "band": Band.create(name="B10", common_name="cirrus", center_wavelength=1.3735, full_width_half_max=0.075),
        "gsd": 30
    },
    "B11": {
        "band": Band.create(name="B11", common_name="swir16", center_wavelength=1.6137, full_width_half_max=0.143),
        "gsd": 30
    },
    "B12": {
        "band": Band.create(name="B12", common_name="swir22", center_wavelength=2.22024, full_width_half_max=0.242),
        "gsd": 30
    },
    "Fmask": {
        "band": Band.create(name="Fmask"),
        "gsd": 30.0
    },
    "SZA": {
        "band": Band.create(name="SZA"),
        "gsd": 30.0
    },
    "SAA": {
        "band": Band.create(name="SAA"),
        "gsd": 30.0
    },
    "VZA": {
        "band": Band.create(name="VZA"),
        "gsd": 30.0
    },
    "VAA": {
        "band": Band.create(name="VAA"),
        "gsd": 30.0
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
                                                     "%Y-%m-%dT%H:%M:%S.%fZ")
    end_datetime_str = granule.Temporal.RangeDateTime.EndingDateTime.cdata
    item_end_datetime = datetime.datetime.strptime(end_datetime_str,
                                                   "%Y-%m-%dT%H:%M:%S.%fZ")
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
    item.ext.enable("eo")
    for attribute in granule.AdditionalAttributes.AdditionalAttribute:
        if attribute.Name == "CLOUD_COVERAGE":
            item.ext.eo.cloud_cover = float(attribute.Values.Value.cdata)


def add_assets(item, granule, endpoint, version):
    item_id = granule.GranuleUR.cdata
    product = item_id.split(".")[1]
    if product == "S30":
        band_info = sentinel_band_info
        url = f"https://{endpoint}/lp-prod-protected/HLSS30.{version}/"
        public_url = f"https://{endpoint}/lp-prod-public/HLSS30.{version}/"

    if product == "L30":
        band_info = landsat_band_info
        url = f"https://{endpoint}/lp-prod-protected/HLSL30.{version}/"
        public_url = f"https://{endpoint}/lp-prod-public/HLSL30.{version}/"

    url_template = url + "{}.{}.tif"

    for band_id, band_info in band_info.items():
        band_url = url_template.format(item_id, band_id)
        asset = pystac.Asset(
            href=band_url,
            media_type=pystac.MediaType.COG,
            roles=["data"]
        )
        bands = [band_info["band"]]
        item.ext.eo.set_bands(bands, asset)
        item.add_asset(band_id, asset)

    thumbnail_url = f"{public_url}{item_id}.jpg"
    thumbnail_asset = pystac.Asset(
        href=thumbnail_url,
        media_type=pystac.MediaType.JPEG,
        roles=["thumbnail"]
    )
    item.add_asset("thumbnail", thumbnail_asset)
    item.set_self_href(f"{public_url}{item_id}_stac.json")


def process_projection(item, granule):
    item.ext.enable("projection")
    for attribute in granule.AdditionalAttributes.AdditionalAttribute:
        if attribute.Name == "MGRS_TILE_ID":
            value = attribute.Values.Value.cdata
            lat_band = value[3]
            # Case is important for ordinal comparison
            if lat_band.casefold() > "m":
                hemi = "326"
            else:
                hemi = "327"
            epsg = int(hemi + value[0:2])
            item.ext.projection.epsg = epsg


def process_view_geometry(item, granule):
    item.ext.enable("view")
    for attribute in granule.AdditionalAttributes.AdditionalAttribute:
        if attribute.Name == "MEAN_SUN_AZIMUTH_ANGLE":
            item.ext.view.sun_azimuth = float(attribute.Values.Value.cdata)
        if attribute.Name == "MEAN_VIEW_AZIMUTH_ANGLE":
            item.ext.view.azimuth = float(attribute.Values.Value.cdata)


def process_scientific(item, granule):
    item.ext.enable("scientific")
    for attribute in granule.AdditionalAttributes.AdditionalAttribute:
        if attribute.Name == "IDENTIFIER_PRODUCT_DOI":
            item.ext.scientific.doi = attribute.Values.Value.cdata


def cmr_to_item(cmrxml, endpoint, version):
    cmr = untangle.parse(cmrxml)
    granule = cmr.Granule
    item_id = granule.GranuleUR.cdata
    datetime_str = granule.Temporal.RangeDateTime.BeginningDateTime.cdata
    item_datetime = datetime.datetime.strptime(datetime_str,
                                               "%Y-%m-%dT%H:%M:%S.%fZ")

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
    add_assets(item, granule, endpoint, version)
    process_projection(item, granule)
    process_view_geometry(item, granule)
    process_scientific(item, granule)
    item.validate()
    feature = item.to_dict()
    return feature


@click.command()
@click.argument(
    "cmrxml",
    type=click.Path(dir_okay=False),
)
@click.argument(
    "outputfile",
    type=click.Path(dir_okay=False, file_okay=True, writable=True),
)
@click.argument(
    "endpoint",
    type=click.STRING,
)
@click.argument(
    "version",
    type=click.STRING,
)
def main(cmrxml, outputfile, endpoint, version):
    item = cmr_to_item(cmrxml, endpoint, version)
    with open(outputfile, 'w') as outfile:
        json.dump(item, outfile)


if __name__ == "__main__":
    main()
