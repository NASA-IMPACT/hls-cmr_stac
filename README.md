# hls-cmr_stac
## Generate STAC items for HLS products

## Usage
```bash
$ cmr_to_stac_item [OPTIONS] CMRXML OUTPUTFILE ENDPOINT VERSION

$ cmr_to_stac_item ./HLS.S30.T35VLJ.2021168T100559.v2.0.cmr.xml ./stac_item.json data.lpdaac.earthdatacloud.nasa.gov 020
```
This command assumes that CMR XML file's associated COG files will be in the same directory and searches for `HLS.S30.T35VLJ.2021168T100559.v2.0.B01.tif` in order to read the files projection information.

### Tests
Run Tests
```bash
$ tox
```

### Development
For active stack development run
```
$ tox -e dev
```
This creates a local virtualenv in the directory `devenv`.  To use it for development
```
$ source devenv/bin/activate
```
Then run the following to install the project's pre-commit hooks
```
$ pre-commit install
```
