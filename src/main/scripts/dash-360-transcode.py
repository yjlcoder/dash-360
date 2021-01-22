#!/usr/bin/env python3

import argparse
import json
import shutil
import subprocess


def check_environment():
    ffmpeg_path = shutil.which('ffmpeg')
    assert ffmpeg_path is not None, "Cannot find ffmpeg in your $PATH"


def transcode(src: str, dst: str, config: dict):
    """
    Transcode source video at `src` into DASH-enabled tile-based 360 videos, and save it at `dst`.
    :param src: source video path
    :param dst: destination video path
    :param config: configuration
    :return: None
    """
    tiles_num = len(config["tiles"])
    qualities_num = len(config["qualities"])

    # Split the input into multiple streams
    ffmpeg_filters = []
    for ind, tile in enumerate(config["tiles"]):
        filter = "[0:v]crop=%d:%d:%d:%d[out%d]" % (tile["width"], tile["height"], tile["left"], tile["top"], ind)
        ffmpeg_filters.append(filter)
    for ind, tile in enumerate(config["tiles"]):
        filter = "[out%d]split=%d" % (ind, qualities_num)
        for i in range(qualities_num):
            filter += "[out%d:%d]" % (ind, i)
        ffmpeg_filters.append(filter)
    ffmpeg_filter = ";".join(ffmpeg_filters)

    # Construct qualities: a list where index is in sync with each tile. Each element is a dictionary, key is
    # quality name (such as "4k"), value is a 3-tuple: quality_id, resolution, and bitrate.
    qualities = [{}] * tiles_num
    for quality_id, quality in enumerate(config["qualities"]):
        resolutions = config["qualities"][quality]["resolutions"]
        bitrates = config["qualities"][quality]["bitrates"]
        if type(resolutions) == str:
            resolutions = [resolutions] * tiles_num
        if type(bitrates) == str:
            bitrates = [bitrates] * tiles_num
        assert len(resolutions) == tiles_num and len(bitrates) == tiles_num
        for ind, (resolution, bitrate) in enumerate(zip(resolutions, bitrates)):
            qualities[ind][bitrate] = (quality_id, resolution, bitrate)

    params = []
    adaptation_sets = []
    output_stream_num = 0
    for tile_ind in range(tiles_num):
        map_params = []
        output_streams = []
        for quality_name, (quality_id, resolution, bitrate) in qualities[tile_ind].items():
            tile_out_label = "[out%d:%d]" % (tile_ind, quality_id)
            map_params.extend(["-map", tile_out_label])
            output_streams.append(str(output_stream_num))
            output_stream_num += 1

        # Video Codec: AVC
        map_params.extend(["-vcodec", "libx265", "-preset", "medium"])
        for (quality_name, (quality_id, resolution, bitrate)), output_stream in zip(qualities[tile_ind].items(), output_streams):
            map_params.extend(
                ["-b:v:%s" % output_stream, bitrate, "-s:v:%s" % output_stream, resolution])
        # Extra encoding parameters
        map_params.extend(
            ["-bf", "16", "-keyint_min", str(config["keyint_min"]), "-g", str(config["keyint"]), "-sc_threshold",
             "0"])
        params.extend(map_params)
        adaptation_set = 'id=%d,descriptor=<SupplementalProperty schemeIdUri="urn:mpeg:dash:srd:2014" value="%s"/>,streams=%s' % (tile_ind, config["srd_values"][tile_ind], ",".join(output_streams))
        adaptation_sets.append(adaptation_set)
    # MPD format parameters
    params.extend(["-use_timeline", "1", "-use_template", "1", "-seg_duration", "1"])
    adaptation_sets_params = ["-adaptation_sets", " ".join(adaptation_sets)]

    command = ["ffmpeg", "-i", src, "-filter_complex", ffmpeg_filter, *params, *adaptation_sets_params, "-f", "dash", dst]
    print(" ".join(command))
    subprocess.call(command)


def main():
    check_environment()

    parser = argparse.ArgumentParser(
        description="This script transcodes source video into DASH-enabled tile-based 360 videos")
    parser.add_argument("config", type=str, help="Configuration file for transcoding")
    parser.add_argument("input_video", type=str, help="input video path")
    parser.add_argument("output_mpd", type=str, help="output MPD path")
    args = parser.parse_args()

    with open(args.config) as f:
        config = json.load(f)
    transcode(args.input_video, args.output_mpd, config)


if __name__ == '__main__':
    main()
