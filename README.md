# DASH 360 Project \[Working in progress\]

## Example config file

- 8 tiles, and each tile is 45°. Original video resolution: 4096x2048(4K)

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
            "bitrates": "3Mbps"
        },
        "1080p": {
            "resolutions": "135x540",
            "bitrates": "800Kbps"
        },
        "720p": {
            "resolutions": "90x360",
            "bitrates": "300Kbps"
        }
    }
}
```