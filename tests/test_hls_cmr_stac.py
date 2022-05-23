import os

from hls_cmr_stac.hls_cmr_stac import cmr_to_item

current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_cmr_to_item_s30():
    cmr_xml = os.path.join(test_dir, "HLS.S30.T35VLJ.2021168T100559.v2.0.cmr.xml")
    item = cmr_to_item(cmr_xml, "data.lpdaac.earthdatacloud.nasa.gov", "020")
    assert item["id"] == "HLS.S30.T35VLJ.2021168T100559.v2.0"
    assert item["properties"]["proj:epsg"] == 32635
    assert item["properties"]["proj:shape"] == [3660, 3660]
    assert item["bbox"] == [23.157434, 61.619859, 23.737787, 62.193391]
    assert (
        item["assets"]["B01"]["href"] == "https://data.lpdaac."
        "earthdatacloud.nasa.gov/lp-prod-protected/HLSS30.020/"
        "HLS.S30.T35VLJ.2021168T100559.v2.0/"
        "HLS.S30.T35VLJ.2021168T100559.v2.0.B01.tif"
    )
    assert (
        item["assets"]["thumbnail"]["href"] == "https://data.lpdaac."
        "earthdatacloud.nasa.gov/lp-prod-public/HLSS30.020/"
        "HLS.S30.T35VLJ.2021168T100559.v2.0/"
        "HLS.S30.T35VLJ.2021168T100559.v2.0.jpg"
    )
    assert (
        item["links"][0]["href"] == "https://data.lpdaac."
        "earthdatacloud.nasa.gov/lp-prod-public/HLSS30.020/"
        "HLS.S30.T35VLJ.2021168T100559.v2.0/"
        "HLS.S30.T35VLJ.2021168T100559.v2.0_stac.json"
    )
    assert item["assets"]["B01"]["roles"][0] == "data"
    assert item["assets"]["thumbnail"]["roles"][0] == "thumbnail"
    assert item["properties"]["sci:doi"] == "10.5067/HLS/HLSS30.002"


def test_cmr_to_item_l30():
    cmr_xml = os.path.join(test_dir, "HLS.L30.T19LBJ.2020239T144556.v2.0.cmr.xml")
    item = cmr_to_item(cmr_xml, "data.lpdaac.earthdatacloud.nasa.gov", "020")
    assert item["id"] == "HLS.L30.T19LBJ.2020239T144556.v2.0"
    assert item["properties"]["proj:epsg"] == 32619
    assert item["properties"]["proj:shape"] == [3660, 3660]
    assert item["bbox"] == [-70.850164, -10.835104, -70.737014, -10.298666]
    assert (
        item["assets"]["B01"]["href"] == "https://data.lpdaac."
        "earthdatacloud.nasa.gov/lp-prod-protected/HLSL30.020/"
        "HLS.L30.T19LBJ.2020239T144556.v2.0/"
        "HLS.L30.T19LBJ.2020239T144556.v2.0.B01.tif"
    )
    assert (
        item["assets"]["thumbnail"]["href"] == "https://data.lpdaac."
        "earthdatacloud.nasa.gov/lp-prod-public/HLSL30.020/"
        "HLS.L30.T19LBJ.2020239T144556.v2.0/"
        "HLS.L30.T19LBJ.2020239T144556.v2.0.jpg"
    )
    assert (
        item["links"][0]["href"] == "https://data.lpdaac."
        "earthdatacloud.nasa.gov/lp-prod-public/HLSL30.020/"
        "HLS.L30.T19LBJ.2020239T144556.v2.0/"
        "HLS.L30.T19LBJ.2020239T144556.v2.0_stac.json"
    )
    assert item["assets"]["B01"]["roles"][0] == "data"
    assert item["assets"]["thumbnail"]["roles"][0] == "thumbnail"
    assert item["properties"]["sci:doi"] == "10.5067/HLS/HLSL30.002"
