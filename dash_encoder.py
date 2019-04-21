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

def build_video_encode_command_vp9(video, dashdir, height=240, bitrate="400k"):

    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_{height}p_{bitrate}.webm")
    cmd = f"""
        ffmpeg -y -hide_banner
        -i "{video}"
        -c:v libvpx-vp9
        -keyint_min 150
        -g 150
        -movflags faststart
        -f webm
        -speed 1
        -threads 4
        -an
        -vf "scale=-2:{height}"
        -b:v {bitrate}
        -dash 1 "{output}" """
    cmd = " ".join(cmd.split())
    return cmd, output


def build_video_encode_command(video, dashdir, height=240, bitrate="400k"):

    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_{height}p_{bitrate}.mp4")
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




def build_audio_encode_command_vp9(video, dashdir):
    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_audio.webm")
    cmd = f"""
        ffmpeg -y -hide_banner
        -i {video}
        -c:a libvorbis
        -b:a 192k -vn
        -f webm -dash 1 {output}
        """
    cmd = " ".join(cmd.split())
    return cmd, output


def build_manifest_command_vp9(video, video_files, audio_files, dashdir):
    manifest_part = " ".join(
        [f"-f webm_dash_manifest -i {i}" for i in video_files + audio_files]
    )

    map_part = " ".join(
        [f"-map {i}" for i in range(len(video_files + audio_files))]
    )

    video_streams = ",".join([str(i) for i in range(len(video_files))])
    audio_streams = ",".join([str(i + len(video_files)) for i in range(len(audio_files))])
    output = os.path.join(dashdir, os.path.splitext(os.path.basename(video))[0] + f"_manifest.mpd")

    cmd = f"""
        ffmpeg -y
        {manifest_part}
        -c copy
        {map_part}
        -f webm_dash_manifest
        -adaptation_sets "id=0,streams={video_streams} id=1,streams={audio_streams}" \
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

    print(a)

    os.makedirs(a["dash_folder"], exist_ok=True)

    bitrate_mapping = {
        240: "400k",
        720: "800k",
        1080: "1500k"
    }

    commands = []
    video_files = []
    for x in bitrate_mapping:
        cmd, outfile = build_video_encode_command(a["video"], a["dash_folder"], x, bitrate_mapping[x])
        commands.append(cmd)
        video_files.append(outfile)

    cmd, audio_file = build_audio_encode_command(a["video"], a["dash_folder"])
    commands.append(cmd)

    print("\n".join(commands))
    print("\n".join(video_files))
    print(audio_file)
    for x in commands:
        print(f"create {x}")
        os.system(x)
    """
    """
    print("create manifest file")
    cmd, outfile = build_manifest_command(a["video"], video_files, [audio_file], a["dash_folder"])
    #print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
