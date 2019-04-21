#!/usr/bin/env python3
import argparse
import sys
import os

"""
based on:
    * https://www.crookm.com/journal/2018/transcoding-to-dash-and-hls-with-ffmpeg/
    * https://ffmpeg.org/ffmpeg-formats.html#dash-2
    * https://www.jungledisk.com/blog/2017/07/03/live-streaming-mpeg-dash-with-raspberry-pi-3/
    * https://rybakov.com/blog/mpeg-dash/
"""


def build_video_encode_command(video, dashdir, height=240):
    # TODO: currently only CRF encoding possible
    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_{height}p.mp4")
    cmd = f"""
        ffmpeg -y -hide_banner
        -i "{video}"
        -preset slow -tune film
        -an -c:v libx264
        -x264opts 'keyint=25:min-keyint=25:no-scenecut'
        -crf 23
        -pix_fmt yuv420p
        -vf "scale=-2:{height}"
        -f mp4
        "{output}" """
    cmd = " ".join(cmd.split())
    return cmd, output


def build_audio_encode_command(video, dashdir):
    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_audio.m4a")
    cmd = f"""
        ffmpeg -y -hide_banner
        -i {video}
        -c:a aac
        -b:a 192k
        -vn
         {output}
        """
    cmd = " ".join(cmd.split())
    return cmd, output


def build_manifest_command(video, video_files, audio_files, dashdir):
    manifest_part = " ".join(
        [f"-i {i}" for i in video_files + audio_files]
    )

    map_part = " ".join(
        [f"-map {i}" for i in range(len(video_files + audio_files))]
    )

    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_manifest.mpd")

    cmd = f"""
        ffmpeg -y
        {manifest_part}
        -c copy
        {map_part}
        -f dash
        -use_template 1 -use_timeline 0
        -seg_duration 2
        -adaptation_sets "id=0,streams=v id=1,streams=a"
        {output}
        """
    cmd = " ".join(cmd.split())
    return cmd, output


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='create dash representations',
                                     epilog="stg7 2019",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("video", type=str, help="video to convert to a dash version")
    parser.add_argument("--dash_folder", type=str, default="dash", help="folder for storing the dash video")

    a = vars(parser.parse_args())

    print(f"used cli parmeters: {a}")

    os.makedirs(a["dash_folder"], exist_ok=True)

    resolutions = [240, 720, 1080]  # TODO: extend, check, update

    # collect all commands and output files
    commands = []
    video_files = []
    for resolution in resolutions:
        cmd, outfile = build_video_encode_command(a["video"], a["dash_folder"], resolution)
        commands.append(cmd)
        video_files.append(outfile)

    # for audio only one quality is considered
    cmd, audio_file = build_audio_encode_command(a["video"], a["dash_folder"])
    commands.append(cmd)

    # print("\n".join(commands))
    # print("\n".join(video_files))
    # print(audio_file)
    for x in commands:
        print(f"run {x}")
        os.system(x)

    # print("create manifest file")
    cmd, outfile = build_manifest_command(a["video"], video_files, [audio_file], a["dash_folder"])
    #print(cmd)
    os.system(cmd)
    print(f"done :-) use {outfile} in your player")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
