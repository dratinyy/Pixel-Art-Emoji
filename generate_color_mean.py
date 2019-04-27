from PIL import Image

# We want to exclude some emojis that give us trouble
# In particular, the family emojis and romanian flag are usually misinterpreted
# for green emojis by the Pixel Art generator.
exclude_list = [ "1f469-2764-1f469", "1f468-2764-1f468", "1f469-2764-1f48b-1f469", "1f468-2764-1f48b-1f468", "1f468-1f469-1f467", "1f468-1f469-1f467-1f466", "1f468-1f469-1f466-1f466", "1f468-1f469-1f467-1f467", "1f469-1f469-1f466", "1f469-1f469-1f467", "1f469-1f469-1f467-1f466", "1f469-1f469-1f466-1f466", "1f469-1f469-1f467-1f467", "1f468-1f468-1f466", "1f468-1f468-1f467", "1f468-1f468-1f467-1f466", "1f468-1f468-1f466-1f466", "1f468-1f468-1f467-1f467", "c6a786,1f1f7-1f1f4" ]


def main():
    # The set which will contain emojis and the average color
    emojiset = {}

    # Iterate through all the emojis
    for line in open("rocket_chat_emoji_list.txt", encoding="utf8"):
        emoji = line[:-1].split(',')
        if emoji[0] not in exclude_list:
            
            # Load the emoji image
            im = Image.open("emojis/" + emoji[0] + ".png").convert("RGBA")
            matrix = im.load()
            w, h = im.size

            # This will contain the total RGB values, and the pixel count
            total = [0, 0, 0, 0]
            for row in range(h):
                for col in range(w):
                    pix = matrix[row, col]
                    if pix[3] == 0:
                        pix = (255, 255, 255, 255)
                    total[0] += pix[0]
                    total[1] += pix[1]
                    total[2] += pix[2]
                    total[3] += 1

            # Generate an average, and add it to the set
            # No duplicate averages are added
            key = '%02x%02x%02x' % (total[0]//total[3], total[1]//total[3], total[2]//total[3])
            if key not in emojiset:
                emojiset[key] = emoji

    # The results are saved in the output file
    kz = list(emojiset.items())
    kz.sort()
    output = [f"{k[0]},{k[1][0]},{k[1][1]},{k[1][2]}\n" for k in kz]
    outf = open("hexcolor_emojicode_rocketchatcode_emoji.txt", "w", encoding="utf8")
    outf.write("".join(output))
    outf.close


if __name__ == '__main__':
    main()