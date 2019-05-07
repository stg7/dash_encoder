# DASH encoder
basic DASH encoder using ffmpeg

current video streaming provider use dynamic adaptive streaming to deliver videos to end users, however the underlying technology is more or less so successful due to it's simplicity in hosting files.

if you ever wanted to create an own DASH video server, you can use the provided script to create DASH compatible manifest files, and the used audio/video segments, however this script is more a "teaching" script.

to playout the videos you either use the DASH.JS player or SHAKA-Player or something else (see dash.html, change `src="...."` to your corresponding manifest file).

## usage

simply run `./dash_encoder.py --help` to get some initital help.
```
usage: dash_encoder.py [-h] [--dash_folder DASH_FOLDER] [--auto_subfolders]
                       video

create dash representations

positional arguments:
  video                 video to convert to a dash version

optional arguments:
  -h, --help            show this help message and exit
  --dash_folder DASH_FOLDER
                        folder for storing the dash video (default: dash)
  --auto_subfolders, -as
                        create subfolder based on videoname (default: False)

stg7 2019
```
usually you just need to run `./dash_encoder.py <videofile>` to create the corresponding DASH files (segments and manifest).
if you plan to create several dash videos just run the command with `-as` flag, so that for each video a subfolder will be created.


## hints/notes
the provided script  is just a staring point, there are several parameters that should be tuned and changed.

# example service
to run an example service, you can use `./dash_server.py` it will start a web server with `index.html` as default entry, all videos in the configured `dash_folder` are shown (consider to create subfolders for each video in the encoding step, using e.g. `--auto_subfolders` or `-as` flag.

`dash_server.py` will update the `video_index.js` file with new videos during each start, moreover you can just copy `[video_index.js, dash, index.html]` to any static http file server and play the videos.


# How to build something like Youtube, Netflix and so on

if you ever wanted to know how Netflix, Youtube and co are working, or you thought of "creating" your own "Youtube".

in general youtube consists of three main parts:

* videos hosted via DASH, and "infinity" storage
* a search engine component and recommendation system
* social network aspects, e.g. liking videos, having user accounts, connections and so on

more or less all video streaming provider share similar parts, e.g. netflix has nearly no social component, however it still has user accounts, e.g. for billing.

thanks to open source software, there are several parts already available, DASH is the key technology and available (see [dash.js](https://github.com/Dash-Industry-Forum/dash.js)),
the search engine part could be realized using [apache solr](https://lucene.apache.org/solr/) and for recommendation [predictionio](http://predictionio.apache.org/index.html) could be used.
open source social networks are also available, or not needed :)

more or less an advanced encoding pipeline and processing/storage power is also required.

