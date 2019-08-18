import math
import sys
from time import sleep

from PIL import Image, ImageDraw
import numpy

CONVERSION_STRING_LOW_CONTRAST = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"[::-1]
CONVERSION_STRING_HIGH_CONTRAST = " .`',°^:;~-_+\"#MW&8%B@$"
CONVERSION_STRING = " .`',:;~-°^\"_!+\\/mwqp#MW&8%B@$"


def convert_to_brightness_matrix(rgb_matrix, method):
    # Use the Luminosity formula to convert RGB values to a single brightness value
    bm = []
    if method == "lum":  # Luminosity
        for y in range(0, len(rgb_matrix)):
            bm.append([])
            for x in range(0, len(rgb_matrix[y])):
                bm[y].append(int((0.21 * rgb_matrix[y, x, 0]) + (0.72 * rgb_matrix[y, x, 1]) +
                                 (0.07 * rgb_matrix[y, x, 2])))
        return bm
    elif method == "avg":  # Average
        for y in range(0, len(rgb_matrix)):
            bm.append([])
            for x in range(0, len(rgb_matrix[y])):
                bm[y].append(int((int(rgb_matrix[y, x, 0]) + int(rgb_matrix[y, x, 1]) + int(rgb_matrix[y, x, 2])) / 3))
        return bm
    elif method == "light":  # Lightness
        for y in range(0, len(rgb_matrix)):
            bm.append([])
            for x in range(0, len(rgb_matrix[y])):
                bm[y].append(int(int((max(rgb_matrix[y, x, 0], rgb_matrix[y, x, 1], rgb_matrix[y, x, 2])) +
                                     int(min(rgb_matrix[y, x, 0], rgb_matrix[y, x, 1], rgb_matrix[y, x, 2])) / 2)))
        return bm
    else:
        print("The method {} does't exist.".format(method))


def downscale_image(image, max_width):
    current_img_width = image.width
    current_img_height = image.height
    while current_img_width > max_width:
        current_img_width = round(current_img_width * 0.99)
        current_img_height = round(current_img_height * 0.99)
    return img.resize((current_img_width, current_img_height))


def create_ascii_matrix(image, max_with, method="luminosity"):
    print("Image {} loaded successfully...".format(IMAGE))
    print("Image size: {}x{}".format(image.width, image.height))
    print("Image format: {} ; Image mode: {}".format(image.format, image.mode))
    image = downscale_image(image, max_with)
    print("Image size after downscaling: {}x{}".format(image.width, image.height))

    pixel_matrix = numpy.asarray(image)
    print("Pixel matrix size: {} cols x {} rows".format(len(pixel_matrix[0]), len(pixel_matrix)))

    brightness_matrix = convert_to_brightness_matrix(pixel_matrix, method)

    # Find max and min values -> [Min: 0, Max: 255]
    max_b, min_b = -1000, 1000
    for row in brightness_matrix:
        for pixel in row:
            if pixel > max_b:
                max_b = pixel
            if pixel < min_b:
                min_b = pixel
    print("Brightness Min: {} ; Max: {}".format(min_b, max_b))

    # Convert brightness to ascii chars and append to new matrix
    variance = max_b - min_b
    print("variance: {}".format(variance))
    m = math.ceil(variance / len(CONVERSION_STRING))  # calculates the brightness range a single char has to cover
    print("m: {}".format(m))

    sleep(2.75)

    ascii_matrix = []
    for y in range(0, len(brightness_matrix)):
        ascii_matrix.append([])
        for x in range(0, len(brightness_matrix[y])):
            char_index = round(brightness_matrix[y][x] / m)
            if char_index > len(CONVERSION_STRING) - 1:
                print("Char index out of bounds: {} => ~{}; The value was corrected to {}"
                      .format(brightness_matrix[y][x] / m, char_index, len(CONVERSION_STRING) - 1))
                char_index = len(CONVERSION_STRING) - 1
            ascii_matrix[y].append(CONVERSION_STRING[char_index])
    return ascii_matrix


if __name__ == '__main__':
    IMAGE = sys.argv[1]
    METHOD = sys.argv[2]
    IN_PATH = "in/" + IMAGE
    OUT_PATH = "out/" + IMAGE

    img = Image.open(IN_PATH)

    ascii_matrix = create_ascii_matrix(img, 300, METHOD)

    if img:
        f = open(OUT_PATH.split(".")[0] + ".html", "w+")
        f.write('<html style="background-color: #0b0d0a;">\r\n<head>\r\n<style>\r\n'  # alt: #664A46 ; #BAA87E
                + '.rainbow {'
                + 'background-image: -webkit-gradient( linear, left top, right top, color-stop(0, #f22), '
                + 'color-stop(0.15, #f2f), color-stop(0.45, #2ff), color-stop(0.6, #2f2),color-stop(0.75, #2f2), '
                + 'color-stop(0.9, #ff2), color-stop(1, #f22) );'
                  'background-image: gradient( linear, left top, right top, color-stop(0, #f22), color-stop(0.15, #f2f)'
                + ', color-stop(0.45, #2ff), color-stop(0.6, #2f2),color-stop(0.75, #2f2), '
                + 'color-stop(0.9, #ff2), color-stop(1, #f22) );'
                  'color: transparent;'
                  '-webkit-background-clip: text;'
                  'background-clip: text;'
                  '</style>\r\n</head>\r\n'
                '<pre style="font-family: monospace;line-height: 4px; font-size: 4px;" class="rainbow">\r\n')
        for r in ascii_matrix:
            line = ""
            for p in r:
                line += p * 3
            f.write(line + "\r\n")
        f.write("</pre>\r\n</html>")
        f.close()

        for r in ascii_matrix:
            line = ""
            for p in r:
                line += p * 2
            print(line)
        ascii_img = Image.new("RGB", (len(ascii_matrix[0]) * 7, len(ascii_matrix) * 7), (29, 29, 29))
        draw = ImageDraw.Draw(ascii_img)
        y_position = 0
        for l in range(0, len(ascii_matrix)):
            x_position = 0
            y_position = 7 * l
            for r in range(0, len(ascii_matrix[l])):
                x_position = 7 * r
                draw.text((x_position, y_position), ascii_matrix[l][r], fill=(255, 213, 175))
        ascii_img.save(OUT_PATH.split(".")[0] + ".jpg")

    else:
        print("Couldn't load image.")
