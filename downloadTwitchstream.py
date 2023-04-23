import json
from twitchdl import twitch
import twitchdl.commands.videos as twitch_videos
import twitchdl.commands.download as twitch_download
from os import system

"""
Download all archive videos from a given twitch stream automatically.
Avoid re-downloading those previously retreived.
TEF - 20230423
"""
channel_name = "stthomasglassboro"
debug = 5

# Get highest id already downloaded
highest_downloaded = 0
try:
    with open("downloaded.json", "r") as f:
        highest_downloaded = json.load(f)
except FileNotFoundError as e:
    # no previous run; download them all!
    pass

if debug >= 10:
    print(f"DEBUG: highest_downloaded={highest_downloaded}")

# Get generator of id's available online
total_count, generator = twitch.channel_videos_generator(
    channel_name, 9999, "time", "archive", game_ids=[]
)

# Get list of videos to download
# TODO: exclude some based on date or brevity?
to_download = []
for video in generator:
    if int(video["id"]) > highest_downloaded:
        to_download.append(video)
# Place the list in order from oldest to newest
to_download.reverse()

if debug > 9:
    print(f"DEBUG: to_download={*to_download,}")
if debug > 1:
    print(f"DEBUG: to_download count={len(to_download)}")

# Download videos
# src: https://github.com/ihabunek/twitch-dl/issues/107
class DotDict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


for video in to_download:
    video_id = video["id"]
    if debug > 1:
        print(f"DEBUG download id {video_id}")
    download_args = DotDict(
        {
            "videos": [video_id],
            "format": "mkv",
            "keep": False,
            "quality": "source",
            "max_workers": 20,
            "no_join": False,
            "overwrite": True,
            "start": None,
            "end": None,
            "output": "{channel_login}_{datetime}.{format}",
        }
    )
    twitch_download(download_args)

    # Set new highest_downloaded
    if int(video_id) > highest_downloaded:
        highest_downloaded = int(video_id)

# Save highest downloaded id for next time
with open("downloaded.json", "w") as f:
    json.dump(highest_downloaded, f, indent=2)
