# Emoji Pixel Art Generator

Welcome to dratinyy's Emoji Pixel Art Generator !

This repository contains a helper that lets you generate pixel arts using emojis, from png files. It does several things, including :
- slicing an emoji sheet into seperate .png files. This is useful, because Rocket.Chat provides an emoji sheet, and later uses CSS to determine which emojito display.
- determining each emoji's mean coloration and storing.
- and finally, producing a pixel art (which can automatically be uploaded to Rocket.Chat using the [Rocket.Chat API](https://rocket.chat/docs/developer-guides/rest-api/)).

## Installation

Python version 3.6.7+ is required. The use of a [virtual environment](https://docs.python.org/3/library/venv.html), although not mendatory, is recommended. Once your environment is ready, simply install the required modules with the use of the following command.

```bash
$ pip install -r python_requirements.txt
```

## Usage

### Slicing a grid of emojis

The *emoji_grid_slicer.py* script will slice a emoji_grid.png file at the root of the project, into multiples png files containing one emoji each, in the *emoji* directory.
```bash
$ python emoji_grid_slicer.py
```

### Generating the emojis' average colorations

The *generate_color_mean.py* script takes a *rocket_chat_emoji_list.txt* and the emoji stored in the *emoji* directory under their emoji codes, and generates a *hexcolor_emojicode_rocketchatcode_emoji.txt* output file.
```bash
$ python generate_color_mean.py
```

### Generating a Pixel Art


