#!/bin/bash

wget "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz" -c
atool -x ffmpeg-release-amd64-static.tar.xz

ffmpeg_path="./$(dirname $(find ffmpeg-* -name "ffmpeg"))"

PATH=$ffmpeg_path:$PATH
export PATH

