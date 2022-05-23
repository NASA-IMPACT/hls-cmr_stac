from setuptools import find_packages, setup

setup(
    name="hls_cmr_stac",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "click~=7.1.0",
        "pystac[validation]==1.0.0rc2",
        "untangle",
        "geojson",
        "shapely",
        "rasterio==1.2.10",
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
