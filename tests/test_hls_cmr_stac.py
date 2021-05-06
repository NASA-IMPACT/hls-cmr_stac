import os
from hls_cmr_stac.hls_cmr_stac import cmr_to_item


current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_cmr_to_item_s30():
    cmr_xml = os.path.join(test_dir, "HLS.S30.T01LAH.2020097T222759.v1.5.xml")
    item = cmr_to_item(cmr_xml, "data.lpdaac.earthdatacloud.nasa.gov", "015")
    assert item["id"] == "HLS.S30.T01LAH.2020097T222759.v1.5"
    assert item["properties"]["proj:epsg"] == 32701
    assert item["bbox"] == [-180.0, -11.223189, 180.0, -10.833754]
    assert item["assets"]["B01"]["href"] == "https://data.lpdaac." \
        "earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.015/" \
        "HLS.S30.T01LAH.2020097T222759.v1.5.B01.tif"
    assert item["assets"]["thumbnail"]["href"] == "https://data.lpdaac." \
        "earthdatacloud.nasa.gov/lp-prod-public/HLSS30.015/" \
        "HLS.S30.T01LAH.2020097T222759.v1.5.jpg"
    assert item["links"][0]["href"] == "https://data.lpdaac." \
        "earthdatacloud.nasa.gov/lp-prod-public/HLSS30.015/" \
        "HLS.S30.T01LAH.2020097T222759.v1.5_stac.json"
    assert item["assets"]["B01"]["roles"][0] == "data"
    assert item["assets"]["thumbnail"]["roles"][0] == "thumbnail"
    assert item["properties"]["sci:doi"] == "10.5067/HLS/HLSS30.015"


def test_cmr_to_item_l30():
    cmr_xml = os.path.join(test_dir, "HLS.L30.39TVF.2020158.165.v1.5.xml")
    item = cmr_to_item(cmr_xml, "data.lpdaac.earthdatacloud.nasa.gov", "015")
    assert item["id"] == "HLS.L30.39TVF.2020158.165.v1.5"
    assert item["properties"]["proj:epsg"] == 32639
    assert item["bbox"] == [49.800551, 40.556707, 51.117032, 41.551785]
    assert item["assets"]["B01"]["href"] == "https://data.lpdaac." \
        "earthdatacloud.nasa.gov/lp-prod-protected/HLSL30.015/" \
        "HLS.L30.39TVF.2020158.165.v1.5.B01.tif"
    assert item["assets"]["thumbnail"]["href"] == "https://data.lpdaac." \
        "earthdatacloud.nasa.gov/lp-prod-public/HLSL30.015/" \
        "HLS.L30.39TVF.2020158.165.v1.5.jpg"
    assert item["links"][0]["href"] == "https://data.lpdaac." \
        "earthdatacloud.nasa.gov/lp-prod-public/HLSL30.015/" \
        "HLS.L30.39TVF.2020158.165.v1.5_stac.json"
    assert item["assets"]["B01"]["roles"][0] == "data"
    assert item["assets"]["thumbnail"]["roles"][0] == "thumbnail"
    assert item["properties"]["sci:doi"] == "10.5067/HLS/HLSL30.015"
