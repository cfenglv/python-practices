#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/3/9 16:56
# @Author  : cfenglv
# @File    : img_to_charpaint.py
# @Software: PyCharm

from PIL import Image
import argparse
import random
charList = list("!@#$%^&*()-=+1234567890AQZXSWCDERFVBGTYHNMJUIKLOP[]{}qazxswedcvfrtgbnhyujmkilop/")


def pixel_to_char(r, g, b, alpha=256):
    """To translate the pixel to a single char
    Calculating the rgb value to grayscale value by the formula
    Then map the grayscale value to the char that we have
    So that a single char can be mapping to a single integer grayscale value(0-255)

    :param r: the r value of the pixel rgb value
    :param g: the r value of the pixel rgb value
    :param b: the r value of the pixel rgb value
    :param alpha: the alpha value of the pixel, 0 means transparent, return a ' '
    :return: a single char that mapping to the specific grayscale value
    """
    if alpha == 0:
        return " "
    gray = round((r * 30 + g * 59 + b * 11) / 100)
    index = int((gray / 256.0) * len(charList))
    return charList[index]

# Set up the argument parser
parser = argparse.ArgumentParser()
parser.add_argument("file", action="store",
                    help="the name of the img which will be trans to char paint")
parser.add_argument("-o", "--output", action="store",
                    help="the name of the char paint file")
parser.add_argument("-w", "--width", action="store", type=int,
                    help="the width of the char paint", default=-1)
parser.add_argument("-ht", "--height", action="store", type=int,
                    help="the height of the char paint", default=-1)

args = parser.parse_args()
file_name = args.file
output_name = args.output
width = args.width
height = args.height

if __name__ == "__main__":
    img = Image.open(file_name)
    char_paint = ""
    random.shuffle(charList)
    charList[0] = " "

    # Get the proportion of the native image
    nativeWidth, nativeHeight = img.size
    proportion = nativeWidth / nativeHeight

    if width == -1 and height == -1:
        width = 80
        height = round(width / proportion)
    elif width == -1:
        width = round(height * proportion)
    elif height == -1:
        height = round(width / proportion)
    height //= 2
    # resize the img by the proportion
    # then trans the pixels to char
    # because the txt indent, need to half the height
    img = img.resize((width, height), Image.NEAREST)
    img = img.convert("RGB")
    for i in range(height):
        for j in range(width):
            char_paint += pixel_to_char(*img.getpixel((j, i)))
        char_paint += "\n"

    # print the char paint to the console
    print(char_paint)

    # if user specify the output file name
    # then print the result to that file
    # otherwise print to the default file named "output.txt"
    if output_name:
        with open(output_name, "w") as output:
            output.write(char_paint)
    else:
        with open("output.txt", "w") as output:
            output.write(char_paint)
