# downloadTwitchstream

Twitch dumps archived videos after a week. I want to keep them. Downloading them all is the kind of repetitive work computers were made for.

Files are saved in the current working directory as .mkv's. Time to post-process!

(I have found ffmpeg's libx265 video library radically decreases file-sizes with no quality loss to my eyes.)

## Prerequisites

[twitch-dl](https://github.com/ihabunek/twitch-dl) does all the hard work.

## Getting started

- Install the requirements (e.g., `pip install -r /path/to/requirements.txt`)
- edit the script (downloadTwitchstream.py) to specify the `channel_name` you want to follow
- Run it! (`python3 downloadTwitchstream.py`)

