# Dashify tile-based adaptive 360° videos

## About

This tool helps you convert a 360° videos into a **tile-based, quality-adaptive,
MPEG-DASH streamable** video. The manifest file (MPD) uses the spatial
relationship description (SRD) feature, which wasintroduced in the second
amendment of DASH standard part 1, 23009-1:2014\[1\].
Click [here](https://dl.acm.org/doi/10.1145/2910017.2910606) to read more.

## Installation:

```shell
sudo apt install ffmpeg # Make sure FFMpeg is installed on your computer
sudo pip3 install pybuilder
git clone https://github.com/yang-jace-liu/dash-360
cd dash-360 && pyb install
```

## Usage: 

```
usage: dash-360-transcode.py [-h] config input_video output_mpd

This script transcodes source video into DASH-enabled tile-based 360 videos

positional arguments:
  config       Configuration file for transcoding
  input_video  input video path
  output_mpd   output MPD path

optional arguments:
  -h, --help   show this help message and exit

```

## Common Errors

#### Conflicting stream par values in Adaptation Set
All qualities for one tile should have the same aspect ratio.

#### Width (or Height) not divisible by 2
FFMpeg requires video width and height are even numbers. In our case, the
 width and height of each resolution for each tile should be even numbers.

## A working example

- Download the 360° video from [here](https://vimeo.com/214402865), and
  rename it to "origin.mp4".
- We will create a DASH-streamable video containing 8 tiles (8x1), so each
  tile is 45°. The original resolution is 4096x2048 (4K), and we will create 3
  resolutions: origin, 1080P(2160x1080), and 720P(1440x720).
- You need to give the SRD values based on it's spatial relation. Check
[here](https://github.com/gpac/gpac/wiki/MPEG-DASH-SRD-and-HEVC-tiling-for-VR-videos) and
[here](https://www.semanticscholar.org/paper/4-.-MPEG-DASH-SRD-%3A-DESIGN-PRINCIPLES-%2C-DEFINITIONS-Buerenplein-Mic%C3%B3/73bb96a1d8415f675857704ce77739a4fd46f992) to get the
  meaning of each number.
- We create the following json file based on our needs, saving it as "config
  .json".
- Run `dash-360-transcode.py config.json origin.mp4 out.mpd`
- **Note** that tiles here have equal sizes. You may have tiles of different
  sizes. You can change the string values under
  `config["qualities"][quality_name]["resolutions"]` and
  `config["qualities"][quality_name]["bitrates"]` to a list of strings, and
   each element is correspond to a tile. You need to make sure the length of
   these strings are equal to the number of tiles.
```json
{
    "tiles": [
        {
            "left": 0,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 512,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 1024,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 1536,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 2048,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 2560,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 3072,
            "top": 0,
            "width": 512,
            "height": 2048
        },
        {
            "left": 3584,
            "top": 0,
            "width": 512,
            "height": 2048
        }
    ],
    "qualities": {
        "4k": {
            "resolutions": "512x2048",
            "bitrates": "3000k"
        },
        "1080p": {
            "resolutions": "270x1080",
            "bitrates": "1500k"
        },
        "720p": {
            "resolutions": "180x720",
            "bitrates": "600k"
        }
    },
    "srd_values": [
        "0,0,0,1,1,8,1",
        "0,1,0,1,1,8,1",
        "0,2,0,1,1,8,1",
        "0,3,0,1,1,8,1",
        "0,4,0,1,1,8,1",
        "0,5,0,1,1,8,1",
        "0,6,0,1,1,8,1",
        "0,7,0,1,1,8,1"
    ],
    "keyint": 30,
    "keyint_min": 30
}
```