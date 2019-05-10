#!/bin/bash

wget "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz" -c
tar -xJf ffmpeg-release-amd64-static.tar.xz

ffmpeg_path="$(pwd)/$(dirname $(find ffmpeg-* -name "ffmpeg"))"
echo "use $ffmpeg_path"

PATH="$ffmpeg_path:$PATH"
export PATH
exec /bin/bash
