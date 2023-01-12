# staples-dl

A downloader for [staples.ca](https://staples.ca) 3D models

## Installation

Make `staples-dl.py` executable and copy it to a directory in your `PATH`.

```bash
  chmod +x staples-dl.py
  cp staples-dl.py /usr/bin/staples-dl
```

Requires Python 3 or newer.

## Usage

```bash
staples-dl <URL> [glb/usdz]
```
`URL` - Required, URL of the [staples.ca](https://staples.ca) product page
`glb/usdz` - Optional, the desired filetype to download

## License

`staples-dl` is released under the MIT license. See `LICENSE.txt` for more details.