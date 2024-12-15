#!/usr/bin/python3

import json
# from twitchdl import twitch
# import twitchdl.commands.videos as twitch_videos
# import twitchdl.commands.download as twitch_download
from subprocess import run
import os
import sys
import re

"""
Download all archive videos from a given twitch stream automatically.
Avoid re-downloading those previously retreived.
TEF - 20230423
"""
channel_name = "stthomasglassboro"
debug = 5
dest_dir = "/home/todd/Videos"

video_extract = re.compile("\\d{10}")
publish_extract = re.compile("(\\d{4}-\\d\\d-\\d\\d) @ (\\d\\d:\\d\\d:\\d\\d)")

os.chdir(os.path.expanduser(dest_dir))

#######################################
# Get highest id already downloaded
#######################################
highest_downloaded = 0
try:
    with open("downloaded.json", "r") as f:
        highest_downloaded = int(json.load(f))
except FileNotFoundError as e:
    # no previous run; download them all!
    pass
if debug >= 10:
    print(f"DEBUG: highest_downloaded={highest_downloaded}")

#######################################
# Get the videos available for download
# TODO: exclude some based on date or brevity?
#######################################
to_download = []

lines = run(["twitch-dl", "videos", channel_name], capture_output=True).stdout.decode()
if debug > 19:
    print(f"DEBUG: videos in channel:\n{lines}----------\n")

video = ""
for l in lines.split('\n'):
    if "Video " in l:
        if debug > 10:
            print(f"DEBUG: possible download candidate: {l}")
        video = video_extract.search(l).group()
        if int(video) > highest_downloaded:
            to_download.append(video)
if debug > 9:
    print(f"DEBUG: to_download={*to_download,}")
if debug > 1:
    print(f"DEBUG: to_download count={len(to_download)}")
        
# Place the list in order from oldest to newest
to_download.reverse()

#######################################
# Download videos
#######################################
for video in to_download:
    if debug > 1:
        print(f"DEBUG download id {video}")
    run(["twitch-dl", "download", video, "--overwrite", "--quality", "source", "--output", "{channel_login}_{datetime}.{format}"]).check_returncode()

    # Set new highest_downloaded
    if int(video) > highest_downloaded:
        highest_downloaded = int(video)

#######################################
# Save highest downloaded id for next time
#######################################
if debug >= 10:
    print(f"DEBUG: New highest_downloaded={highest_downloaded}")
with open("downloaded.json", "w") as f:
    json.dump(highest_downloaded, f, indent=2)
