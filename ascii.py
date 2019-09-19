import argparse
import math
import sys
from time import sleep

from PIL import Image, ImageDraw
from ProgressPrinter import ProgressBar
import numpy

CONVERSION_STRING_LOW_CONTRAST = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"[::-1]
CONVERSION_STRING_HIGH_CONTRAST = " .`',°^:;~-_+\"#MW&8%B@$"
CONVERSION_STRING = " .`',:;~-°^\"_!+\\/mwqp#MW&8%B@$"

DEBUG = False


def convert_to_brightness_matrix(rgb_matrix, method):
    col_s, row_s = len(rgb_matrix[0]), len(rgb_matrix)  # TODO check if order is right
    pixel_c = col_s * row_s
    bm = []
    pre = f'Converting RGB-Matrix to Brightness-Matrix [RGB ==({method})==> Brightness]...\nPixel matrix size: {col_s} cols x {row_s} rows.'
    pb = ProgressBar(pixel_c, 'pixels', pre=pre, post='Finished conversion!')
    pb.print_progress()

    p_count = 0

    # Use the Luminosity formula to convert RGB values to a single brightness value
    for y in range(0, row_s):
        bm.append([])
        for x in range(0, col_s):
            if method == "lum":  # Luminosity
                bm[y].append(int((0.21 * rgb_matrix[y, x, 0]) + (0.72 * rgb_matrix[y, x, 1]) +
                                 (0.07 * rgb_matrix[y, x, 2])))
            elif method == "avg":  # Average
                bm[y].append(int((int(rgb_matrix[y, x, 0]) + int(rgb_matrix[y, x, 1]) + int(rgb_matrix[y, x, 2])) / 3))
            elif method == "light":  # Lightness
                bm[y].append(int(int((max(rgb_matrix[y, x, 0], rgb_matrix[y, x, 1], rgb_matrix[y, x, 2])) +
                             int(min(rgb_matrix[y, x, 0], rgb_matrix[y, x, 1], rgb_matrix[y, x, 2])) / 2)))
            else:
                print("The method {} does't exist.".format(method))
                return -1
            p_count += 1
            pb.print_progress(p_count)
    return bm


def downscale_image(image, max_width):
    current_img_width = image.width
    current_img_height = image.height
    while current_img_width > max_width:
        current_img_width = round(current_img_width * 0.99)
        current_img_height = round(current_img_height * 0.99)
    return img.resize((current_img_width, current_img_height))


def create_ascii_matrix(image, max_width, method="luminosity"):
    print("Image {} loaded successfully...".format(IMAGE))
    print("Image size: {}x{}".format(image.width, image.height))
    print("Image format: {} ; Image mode: {}".format(image.format, image.mode))
    image = downscale_image(image, max_width)
    print("Image size after downscaling: {}x{}".format(image.width, image.height))

    pixel_matrix = numpy.asarray(image)

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
    print(f"variance: {variance}")
    m = math.ceil(variance / len(CONVERSION_STRING))  # calculates the brightness range a single char has to cover
    print(f"Brightness range per char: {m}")

    ascii_matrix = []
    col_s, row_s = len(brightness_matrix[0]), len(brightness_matrix)
    pixel_c = col_s * row_s
    pre = f'Converting Brightness-Matrix to ASCII-Matrix using the conversion string\n\n"{CONVERSION_STRING}"\n'
    pb = ProgressBar(pixel_c, 'pixels', pre=pre, post='Finished conversion!')
    pb.print_progress()

    p_count = 0

    for y in range(0, len(brightness_matrix)):
        ascii_matrix.append([])
        for x in range(0, len(brightness_matrix[y])):
            p_count += 1
            char_index = round(brightness_matrix[y][x] / m)
            if char_index > len(CONVERSION_STRING) - 1:
                if DEBUG:
                    pb.print_progress(p_count, f"Char index out of bounds: {brightness_matrix[y][x] / m} => ~{char_index};"
                                               f" The value was corrected to {len(CONVERSION_STRING) - 1}")
                char_index = len(CONVERSION_STRING) - 1
            else:
                pb.print_progress(p_count)
            ascii_matrix[y].append(CONVERSION_STRING[char_index])
    return ascii_matrix


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Takes in options on how the image should be processed.")
    parser.add_argument("image", type=str, action="store", default=None, help=
                        "The full name of the image. The image must be contained"
                        " inside a folder that is named in that lives in the "
                        "same location as the ascii.py script.")
    parser.add_argument("-m", "--mode", type=str,
                        help="Specifies the mode that is used to convert RGB color values to single "
                             "brightness values. Modes supported lum[inosity], light[ness], "
                             "or avg [average]. Defaults to lum", default="lum", dest="conversion_mode")
    parser.add_argument("--rainbow", action="store_const", const="rainbow", dest="output_mode", default="b/w")
    parser.add_argument("--no-console", action="store_false", dest="console_flag")

    args = parser.parse_args()

    IMAGE = args.image
    METHOD = args.conversion_mode
    IN_PATH = "in/" + IMAGE
    OUT_PATH = "out/" + IMAGE

    img = Image.open(IN_PATH)

    ascii_matrix = create_ascii_matrix(img, 300, METHOD)
    ascii_count = len(ascii_matrix) * len(ascii_matrix[0])

    if ascii_matrix:
        # SAVE TO HTML
        file_name = (OUT_PATH.split(".")[0] + ".html")
        f = open(file_name, "w+", encoding="utf-8")
        f.write('<html style="background-color: #0b0d0a;">\r\n<head>\r\n'
                '<meta charset="UTF-8">\r\n'
                '<style>\r\n'  # alt: #664A46 ; #BAA87E
                '.rainbow {'
                'background-image: -webkit-gradient( linear, left top, right top, color-stop(0, #f22), '
                'color-stop(0.15, #f2f), color-stop(0.45, #2ff), color-stop(0.6, #2f2),color-stop(0.75, #2f2), '
                'color-stop(0.9, #ff2), color-stop(1, #f22) );'
                'background-image: gradient( linear, left top, right top, color-stop(0, #f22), color-stop(0.15, #f2f)'
                ', color-stop(0.45, #2ff), color-stop(0.6, #2f2),color-stop(0.75, #2f2), '
                'color-stop(0.9, #ff2), color-stop(1, #f22) );'
                'color: transparent;'
                '-webkit-background-clip: text;'
                'background-clip: text;'
                'width: max-content;}\r\n'
                '</style>\r\n</head>\r\n'
                '<pre style="font-family: monospace;line-height: 3px; font-size: 3px;" class="rainbow">\r\n')

        pb = ProgressBar(ascii_count, 'characters',
                         pre=f'Inserting {ascii_count} ASCII characters into {file_name}...',
                         post='Finished generating HTML file!')
        pb.print_progress()
        c = 1
        for r in ascii_matrix:
            line = ""
            for p in r:
                line += p * 3
                pb.print_progress(c)
                c += 1
            f.write(line + "\r\n")
        f.write("</pre>\r\n</html>")
        f.close()

        # SAVE AS NEW ASCII IMAGE
        file_name = OUT_PATH.split(".")[0] + ".jpg"
        ascii_img = Image.new("RGB", (len(ascii_matrix[0]) * 7, len(ascii_matrix) * 7), (29, 29, 29))
        draw = ImageDraw.Draw(ascii_img)
        pb = ProgressBar(ascii_count, 'characters',
                         pre=f'Rendering {ascii_count} ASCII characters onto {file_name}...',
                         post='Finished generating JPEG file!')

        y_position = 0
        ascii_count = 1

        pb.print_progress()

        for l in range(0, len(ascii_matrix)):
            x_position = 0
            y_position = 7 * l
            for r in range(0, len(ascii_matrix[l])):
                x_position = 7 * r
                draw.text((x_position, y_position), ascii_matrix[l][r], fill=(255, 213, 175))
                pb.print_progress(ascii_count)
                ascii_count += 1
        ascii_img.save(file_name)

        # PRINT TO CONSOLE
        if args.console_flag:
            sleep(1.5)
            for r in ascii_matrix:
                line = ""
                for p in r:
                    line += p * 2
                print(line)
    else:
        print("Couldn't load image.")
