# DASH encoder
basic DASH encoder using ffmpeg
current video streaming provider use dynamic adaptive streaming to deliver videos to end users, however the underlying technology is more or less so successful due to it's simplicity in hosting files.

if you ever wanted to create an own DASH video server, you can use the provided script to create DASH compatible manifest files.

to playout the videos you either use the DASH.JS player or SHAKA-Player or something else (see dash.html, change `src="...."` to your corresponding manifest file).

## usage

simply run `dash_encoder.py --help` to get some initital help.
usually you just need to run `./dash_encoder.py <videofile>` to create the corresponding DASH parts.

