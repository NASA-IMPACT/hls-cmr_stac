import os
from hls_cmr_stac.hls_cmr_stac import cmr_to_item


current_dir = os.path.dirname(__file__)
test_dir = os.path.join(current_dir, "data")


def test_cmr_to_item_s30():
    sentinel_cmr_xml = os.path.join(test_dir,
                                    "HLS.S30.T01LAH.2020097T222759.v1.5.xml")
    item = cmr_to_item(sentinel_cmr_xml)
    assert item["id"] == "HLS.S30.T01LAH.2020097T222759.v1.5"
    assert item["bbox"] == [-180.0, -11.223189, 180.0, -10.833754]
