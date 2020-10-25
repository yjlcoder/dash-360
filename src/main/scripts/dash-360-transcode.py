import argparse
import json
import shutil


def check_environment():
    ffmpeg_path = shutil.which('ffmpeg')
    assert (ffmpeg_path is not None, "Cannot find ffmpeg in your $PATH")


def transcode(src: str, dst: str, config: dict):
    """
    Transcode source video at `src` into DASH-enabled tile-based 360 videos, and save it at `dst`.
    :param src: source video path
    :param dst: destination video path
    :param config: configuration
    :return: None
    """
    pass


def main():
    check_environment()

    parser = argparse.ArgumentParser("This script transcodes source video into DASH-enabled tile-based 360 videos")
    parser.add_argument("config", type=str, help="Configuration file for transcoding")
    parser.add_argument("input-video", type=str, help="input video path")
    parser.add_argument("output-video", type=str, help="output video path")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    transcode(args.input_video, args.ouatput_video, config)


if __name__ == '__main__':
    main()
