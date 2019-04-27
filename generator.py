import json
from math import pow, sqrt
import os
import sys
import time

import requests
import PIL.Image
import numpy as np

ROCKET_CHAT_USERNAME = "?"
ROCKET_CHAT_PASSWORD = "?"
ROCKET_CHAT_ADDRESS = "https://chat.innovation.astek.fr"
ROCKET_CHAT_ROOMID = "u2frw5rDZnK385dve"  # "EmgSBCkfh2ngw498xEmgSBCkfh2ngw498x"
ROCKET_CHAT_MSGID = "Sn8J5MgyXeGJRQXW4"  # "8MccojBtTjieJaZ9C"

# Login to Rocket.Chat
payload = {'user': ROCKET_CHAT_USERNAME, 'password': ROCKET_CHAT_PASSWORD}
r = requests.post(ROCKET_CHAT_ADDRESS + "/api/v1/login", data=payload)
auth = json.loads(r.text)["data"]
headers = {'X-User-Id': auth["userId"], 'X-Auth-Token': auth["authToken"]}

# Read the text file to retrieve all the emojis and their hex color code averages
available_colors = []
f = open("hexcolor_emojicode_rocketchatcode_emoji.txt", encoding="utf8")
for line in f:
    # Insert tuple with RGB values and the emoji itself
    available_colors.append((int(line[0:2], 16), int(line[2:4], 16), int(line[4:6], 16), line.split(",")[3][:-1]))


def autocrop(image):
    """
    Helper function for cropping images, removing empty alpha lines and columns
    """
    image_data = np.asarray(image)
    image_data_transp = np.asarray([pix[3] for pix in image_data.reshape((image_data.shape[0] * image_data.shape[1], 4))]).reshape((image_data.shape[0], image_data.shape[1]))
    non_empty_columns = np.where(np.amax(image_data_transp, axis=0)>0)[0]
    non_empty_rows = np.where(np.amax(image_data_transp, axis=1)>0)[0]
    cropBox = (non_empty_rows.min(), non_empty_rows.max(), non_empty_columns.min(), non_empty_columns.max())
    return image_data[cropBox[0]: cropBox[1] + 1,
                      cropBox[2]: cropBox[3] + 1, :]


def send_rocket_chat(text):
    payload = {'roomId': ROCKET_CHAT_ROOMID, 'msgId': ROCKET_CHAT_MSGID, 'text': text}
    r = requests.post(ROCKET_CHAT_ADDRESS + "/api/v1/chat.update", headers=headers, data=payload, timeout=30)


def main(filename):

    # Load the image file
    image = PIL.Image.open(filename).convert("RGBA")
    image.load()
    cropped_image = PIL.Image.fromarray(autocrop(image))
    im_width, im_height = cropped_image.size
    pixel_matrix = cropped_image.load()

    # Add an emoji to the output string for each pixel
    tab = ""
    for y in range(im_height):
        for x in range(im_width):
            if pixel_matrix[x, y][3] == 0:
                # Spoon is used in place of transparent pixels
                # Small white square may also be used : ▫
                tab += "🥄"
            else:
                # Append the emoji that closest matches the pixel
                distances = [sqrt(pow(k[0] - pixel_matrix[x, y][0], 2) +
                                  pow(k[1] - pixel_matrix[x, y][1], 2) +
                                  pow(k[2] - pixel_matrix[x, y][2], 2)) for k in available_colors]
                tab += available_colors[distances.index(min(distances))][3]
                # Zero-width Non-joiner to prevent letters from forming flags
                tab += "‌"
        if y < im_height - 1:
            tab += "\n"
    send_rocket_chat(tab)


def sort_file_list(x):
    try:
        n = x.replace(".png", "").split("-")
        result = float(n[0]) + (float(n[1]) / 100 if len(n) > 1 else 0)
        return result
    except ValueError:
        return 0


if __name__ == '__main__':

    # When a filename is passed
    if len(sys.argv) == 2:
        if os.path.isfile("./sprites/" + sys.argv[1] + ".png"):
            main("./sprites/" + sys.argv[1] + ".png")
        else:
            print("File not found.")
    # Iterate through all the files:
    else:
        file_list = os.listdir(os.getcwd() + "\\sprites")
        file_list.sort(key=sort_file_list)
        for file in file_list:
            print(file)
            main("./sprites/" + file)
            time.sleep(2)