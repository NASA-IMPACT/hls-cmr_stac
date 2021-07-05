from setuptools import setup, find_packages

setup(
    name="hls_cmr_stac",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click~=7.1.0",
        "pystac[validation]",
        "untangle",
        "geojson",
        "shapely",
    ],
    include_package_data=True,
    extras_require={"dev": ["flake8", "black"], "test": ["flake8", "pytest"]},
    entry_points={"console_scripts": ["cmr_to_stac_item=hls_cmr_stac.hls_cmr_stac:main", ]},
)
