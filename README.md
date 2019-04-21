# DASH encoder
basic DASH encoder using ffmpeg

current video streaming provider use dynamic adaptive streaming to deliver videos to end users, however the underlying technology is more or less so successful due to it's simplicity in hosting files.

if you ever wanted to create an own DASH video server, you can use the provided script to create DASH compatible manifest files, and the used audio/video segments, however this script is more a "teaching" script.

to playout the videos you either use the DASH.JS player or SHAKA-Player or something else (see dash.html, change `src="...."` to your corresponding manifest file).

## usage

simply run `./dash_encoder.py --help` to get some initital help.
usually you just need to run `./dash_encoder.py <videofile>` to create the corresponding DASH files (segments and manifest).


## hints/notes
the provided script is just a staring point, there are several parameters that should be tuned and changed.