# Imports PIL module
import queue
import sys

from PIL import Image
import numpy as np


class RectangleType:
    LONG = 1
    WIDE = 2


# Returns new start_x -> if start_x is the same as given start_x -> cant extend
def extend_rectangle_to_the_left(pixel_array, _start_x, _start_y, _end_y, tolerance_threshold):
    black = (0, 0, 0)
    amount_of_new_pixels = _end_y + 1 - _start_y
    target_x = _start_x - 1

    while 1:
        amount_of_black_pixels = 0
        current_y = _end_y

        if target_x < 0:
            return target_x + 1

        while _start_y <= current_y:
            if pixel_array[target_x, current_y] == black:
                amount_of_black_pixels = amount_of_black_pixels + 1
            current_y = current_y - 1

        amount_of_white_pixels = amount_of_new_pixels - amount_of_black_pixels

        if amount_of_white_pixels > amount_of_new_pixels * tolerance_threshold:
            return target_x + 1

        target_x = target_x - 1


# Returns new end_x -> if end_x is the same as given end_x -> cant extend
def extend_rectangle_to_the_right(pixel_array, _end_x, _start_y, _end_y, x_length, tolerance_threshold):
    black = (0, 0, 0)
    amount_of_new_pixels = _end_y + 1 - _start_y
    target_x = _end_x + 1

    while 1:
        amount_of_black_pixels = 0
        current_y = _end_y

        if target_x >= x_length:
            return target_x - 1

        while _start_y <= current_y:
            if pixel_array[target_x, current_y] == black:
                amount_of_black_pixels = amount_of_black_pixels + 1
            current_y = current_y - 1

        amount_of_white_pixels = amount_of_new_pixels - amount_of_black_pixels

        if amount_of_white_pixels > amount_of_new_pixels * tolerance_threshold:
            return target_x - 1

        target_x = target_x + 1


# Returns new start_y -> if start_y is the same as given start_y -> cant extend
def extend_rectangle_upwards(pixel_array, _start_x, _end_x, _start_y, tolerance_threshold):
    black = (0, 0, 0)
    amount_of_new_pixels = _end_x + 1 - _start_x
    target_y = _start_y - 1

    while 1:
        amount_of_black_pixels = 0
        current_x = _end_x

        if target_y < 0:
            return target_y + 1

        while _start_x <= current_x:
            if pixel_array[current_x, target_y] == black:
                amount_of_black_pixels = amount_of_black_pixels + 1
            current_x = current_x - 1

        amount_of_white_pixels = amount_of_new_pixels - amount_of_black_pixels

        if amount_of_white_pixels > amount_of_new_pixels * tolerance_threshold:
            return target_y + 1

        target_y = target_y - 1


# Returns new end_y -> if end_y is the same as given end_y -> cant extend
def extend_rectangle_downwards(pixel_array, _start_x, _end_x, _end_y, y_length, tolerance_threshold):
    black = (0, 0, 0)
    amount_of_new_pixels = _end_x + 1 - _start_x
    target_y = _end_y + 1

    while 1:
        amount_of_black_pixels = 0
        current_x = _end_x

        if target_y >= y_length:
            return target_y - 1

        while _start_x <= current_x:
            if pixel_array[current_x, target_y] == black:
                amount_of_black_pixels = amount_of_black_pixels + 1
            current_x = current_x - 1

        amount_of_white_pixels = amount_of_new_pixels - amount_of_black_pixels

        if  amount_of_white_pixels > amount_of_new_pixels * tolerance_threshold:
            return target_y - 1

        target_y = target_y + 1


def color_long_rectangle(pixel_array, x, y, x_length, y_length, new_color, tolerance_threshold):
    black = (0, 0, 0)
    if pixel_array[x, y] != black:
        sys.exit("Can't color a long rectangle, if starting pixel is not black")

    start_y = y
    end_y = y

    start_x = x
    end_x = x

    while 1:
        new_end_y = extend_rectangle_downwards(pixel_array, start_x, end_x, end_y, y_length, tolerance_threshold)
        new_start_y = extend_rectangle_upwards(pixel_array, start_x, end_x, start_y, tolerance_threshold)
        new_end_x = extend_rectangle_to_the_right(pixel_array, end_x, new_start_y, new_end_y, x_length, tolerance_threshold)
        new_start_x = extend_rectangle_to_the_left(pixel_array, start_x, new_start_y, new_end_y, tolerance_threshold)

        if new_start_y == start_y and new_end_y == end_y and new_start_x == start_x and new_end_x == end_x:
            break

        start_y = new_start_y
        end_y = new_end_y
        start_x = new_start_x
        end_x = new_end_x

    for ii in range(start_x, end_x + 1):
        for jj in range(start_y, end_y + 1):
            if pixel_array[ii, jj] == black:
                pixel_array[ii, jj] = new_color


def count_connected_pixels_in_row_from(pixel_array, x, y, x_length):
    black = (0, 0, 0)
    if pixel_array[x, y] != black:
        return 0

    amount = 1
    current_x = x
    while 1:
        current_x = current_x - 1
        if current_x < 0:
            break
        if pixel_array[current_x, y] == black:
            amount = amount + 1
        else:
            break

    current_x = x
    while 1:
        current_x = current_x + 1
        if current_x >= x_length:
            break
        if pixel_array[current_x, y] == black:
            amount = amount + 1
        else:
            break

    print("Amount of connected pixels in row from x (" + str(x) + ") and y (" + str(y) + "), amount: " + str(amount))
    return amount


def count_connected_pixels_in_column_from(pixel_array, x, y, y_length):
    black = (0, 0, 0)
    if pixel_array[x, y] != black:
        return 0

    amount = 1
    current_y = y
    while 1:
        current_y = current_y - 1
        if current_y < 0:
            break
        if pixel_array[x, current_y] == black:
            amount = amount + 1
        else:
            break

    current_y = y
    while 1:
        current_y = current_y + 1
        if current_y >= y_length:
            break
        if pixel_array[x, current_y] == black:
            amount = amount + 1
        else:
            break

    print("Amount of connected pixels in a column from x (" + str(x) + ") and y (" + str(y) + "), amount: " + str(amount))
    return amount


def get_rectangle_type_from(pixel_array, x, y, x_length, y_length):
    row_count = count_connected_pixels_in_row_from(pixel_array, x, y, x_length)
    column_count = count_connected_pixels_in_column_from(pixel_array, x, y, y_length)

    if row_count > column_count:
        return RectangleType.WIDE
    else:
        return RectangleType.LONG


## returns -> (x, y, rectangle_type)
def check_rectangle_type_of_first_left_upper_rectangle_and_get_coordinates(pixel_array, x_length, y_length):
    for ii in range(x_length):
        for jj in range(y_length):
            if pixel_array[ii, jj] == (0, 0, 0):
                return ii, jj, get_rectangle_type_from(pixel_array, ii, jj, x_length, y_length)


def count_same_color_pixel(pixel_array, x, y, color, x_length, y_length):
    same_color_pixel = 0
    if y > 0:
        if pixel_array[x, y-1] == color:
            same_color_pixel = same_color_pixel + 1
    if x < x_length - 1:
        if pixel_array[x+1, y] == color:
            same_color_pixel = same_color_pixel + 1
    if y < y_length - 1:
        if pixel_array[x, y+1] == color:
            same_color_pixel = same_color_pixel + 1
    if x > 0:
        if pixel_array[x-1, y] == color:
            same_color_pixel = same_color_pixel + 1

    return same_color_pixel


def recolor_and_determine_size_of_island(pixel_array, x, y, x_length, y_length, new_color):
    size = 0
    black = (0, 0, 0)

    pixel_queue = queue.Queue(maxsize=0)

    pixel_array[x, y] = new_color
    size = size + 1
    pixel_queue.put((x, y))

    while not pixel_queue.empty():
        current_pixel = pixel_queue.get()
        current_x = current_pixel[0]
        current_y = current_pixel[1]

        #size = size + 1
        #pixel_array[current_x, current_y] = new_color

        if current_y > 0:
            if pixel_array[current_x, current_y-1] == black:
                pixel_array[current_x, current_y-1] = new_color
                size = size + 1
                pixel_queue.put((current_x, current_y-1))

        if current_x < x_length - 1:
            if pixel_array[current_x+1, current_y] == black:
                pixel_array[current_x+1, current_y] = new_color
                size = size + 1
                pixel_queue.put((current_x+1, current_y))

        if current_y < y_length - 1:
            if pixel_array[current_x, current_y+1] == black:
                pixel_array[current_x, current_y+1] = new_color
                size = size + 1
                pixel_queue.put((current_x, current_y+1))

        if current_x > 0:
            if pixel_array[current_x-1, current_y] == black:
                pixel_array[current_x - 1, current_y] = new_color
                size = size + 1
                pixel_queue.put((current_x-1, current_y))

    ## Recursion - sadly to many recursions - replace with iterative approach
    #if y > 0:
    #    if pixel_array[x, y-1] == black:
    #        size = size + recolor_and_determine_size_of_island(pixel_array, x, y-1, x_length, y_length, new_color)
    #if x < x_length - 1:
    #    if pixel_array[x+1, y] == black:
    #        size = size + recolor_and_determine_size_of_island(pixel_array, x+1, y, x_length, y_length, new_color)
    #if y < y_length - 1:
    #    if pixel_array[x, y+1] == black:
    #        size = size + recolor_and_determine_size_of_island(pixel_array, x, y+1, x_length, y_length, new_color)
    #if x > 0:
    #    if pixel_array[x-1, y] == black:
    #        size = size + recolor_and_determine_size_of_island(pixel_array, x-1, y, x_length, y_length, new_color)

    return size


def delete_islands_without_color_and_recolor_target_island_to_black(pixel_array, x_length, y_length, target_color):
    for ii in range(x_length):
        for jj in range(y_length):
            if pixel_array[ii, jj] == target_color:
                pixel_array[ii, jj] = (0, 0, 0)
            else:
                pixel_array[ii, jj] = (255, 255, 255)




# open method used to open different extension image file
im = Image.open("images/image3.jpg")

pixelCount = np.full((256, 256, 256), 0, dtype=int)

pixels = im.load()

for i in range(im.size[0]):
    for j in range(im.size[1]):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        pixelCount[red, green, blue] = pixelCount[red, green, blue] + 1

mostRGB = (0, 0, 0)
count = 0

for red in range(256):
    for green in range(256):
        for blue in range(256):
            if pixelCount[red, green, blue] > count:
                count = pixelCount[red, green, blue]
                mostRGB = (red, green, blue)

print("Most common rgb color is: " + str(mostRGB) + " with count: " + str(count))

contrast_cut = 200

imageWidth = im.width
imageHeight = im.height

for i in range(im.size[0]):
    for j in range(im.size[1]):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]

        color_contrast = abs(red - mostRGB[0]) + abs(green - mostRGB[1]) + abs(blue - mostRGB[2])

        if color_contrast >= contrast_cut:
            pixels[i, j] = (0, 0, 0)
        else:
            pixels[i, j] = (255, 255, 255)

for i in range(im.size[0]):
    for j in range(im.size[1]):

        if pixels[i, j] == (0, 0, 0):
            same_color_count = count_same_color_pixel(pixels, i, j, (0, 0, 0), im.size[0], im.size[1])
            if same_color_count == 1:
                pixels[i, j] = (255, 255, 255)
        else:
            same_color_count = count_same_color_pixel(pixels, i, j, (255, 255, 255), im.size[0], im.size[1])
            if same_color_count == 1:
                pixels[i, j] = (0, 0, 0)

most_pixels = 0
green_counter = 0
blue_counter = 0

color_of_biggest_island = (255, 255, 255)

for i in range(im.size[0]):
    for j in range(im.size[1]):
        if pixels[i, j] == (0, 0, 0):

            if blue_counter == 255:
                green_counter = green_counter + 1
                blue_counter = 0

            blue_counter = blue_counter + 1
            current_island_color = (255, green_counter, blue_counter)
            pixels_in_island = recolor_and_determine_size_of_island(pixels, i, j, im.size[0], im.size[1], current_island_color)

            if pixels_in_island > most_pixels:
                most_pixels = pixels_in_island
                color_of_biggest_island = current_island_color

            #im.show()


delete_islands_without_color_and_recolor_target_island_to_black(pixels, im.size[0], im.size[1], color_of_biggest_island)

## first left hit needs to be y axis -> check if long or wide -> if long -> draw (tolerant) rectangle with priority on length

upper_left_rectangle = check_rectangle_type_of_first_left_upper_rectangle_and_get_coordinates(pixels, im.size[0], im.size[1])

if upper_left_rectangle[2] == RectangleType.WIDE:
    sys.exit("The first upper left rectangle supposedly is a wide rectangle. "
             "This shouldn't be the case, as this should be the y-axis, which should be a long rectangle")

color_long_rectangle(pixels, upper_left_rectangle[0], upper_left_rectangle[1], im.size[0], im.size[1], (0, 255, 0), 0.1)

## TODO: als nächstes x-Achse erkennen und danach die einzelnen Balken


im.show()

## TODO: Continue here -> eventuell 2 Klassen -> erste Repräsentiert Pixelfarbe (z.B. einfach Enum Weiß/schwarz oder so) -> zweite Repräsentiert ganzes Bild
## Eventuell senkst du die Rechenleistung, wenn du statt auf einem richtigen Bild auf einer einfache Abstraktion arbeitest