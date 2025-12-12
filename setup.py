from setuptools import find_packages, setup

setup(
    name="hls_cmr_stac",
    version="1.8",
    packages=find_packages(),
    install_requires=[
        "click",
        # we can't use pystac>=1.12.0 because they did a major/breaking bump to
        # the projection extension (v1.x to v2) that renamed proj:epsg -> proj:code.
        "pystac[validation]>=1.0.0rc2,<1.12.0",
        "untangle",
        "geojson",
        "shapely",
        "rasterio",
    ],
    include_package_data=True,
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "black==21.6b0",
            "flake8",
            "isort",
        ],
        "dev": [
            "pytest",
            "black==21.6b0",
            "flake8",
            "isort",
            "pre-commit",
            "pre-commit-hooks",
        ],
    },
    entry_points={
        "console_scripts": [
            "cmr_to_stac_item=hls_cmr_stac.hls_cmr_stac:main",
        ]
    },
)
