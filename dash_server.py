#!/usr/bin/env python3
import argparse
import sys
import os
import glob
import json
import bottle


app = application = bottle.Bottle()


@app.error(404)
def error404(error):
    return 'he is dead jim'


@app.route('/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='.')


@app.route('/')
def main():
    '''
    The front "index" page
    '''
    return bottle.template("index.html")


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='dash example server',
                                     epilog="stg7 2019",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--dash_folder", type=str, default="dash", help="folder for storing the dash video")
    parser.add_argument("--index_file", type=str, default="video_index.js", help="file where all videos are stored as javascript json object")
    parser.add_argument("--webserver_port", type=int, default=8081, help="webserver port")


    a = vars(parser.parse_args())
    print(f"used cli parmeters: {a}")

    manifest_files = list(glob.glob(a["dash_folder"] + "/*/*.mpd"))
    print(f"there are {len(manifest_files)} dash videos stored, build index")

    videos = []
    for manifest in manifest_files:
        print(f"handle {manifest}")
        thumbail = list(glob.glob(os.path.dirname(manifest) + "/*_thumb.png"))[0]
        name = os.path.splitext(os.path.basename(manifest))[0]
        video = {
            "thumbail": thumbail,
            "name": name,
            "manifest": manifest
        }
        print(video)
        videos.append(video)

    with open(a["index_file"], "w") as idx_fp:
        idx_fp.write("var video_index =\n")
        idx_fp.write(json.dumps(videos, indent=4) + ";\n")

    bottle.run(
        app=app,
        host='0.0.0.0',
        port=a["webserver_port"],
        debug=True,
        reloader=True
    )


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
