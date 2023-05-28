# Imports PIL module
import queue
import sys

from PIL import Image
import numpy as np

#sys.setrecursionlimit(5000)


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

    # step 1: markieren (bearbeiten)
    # step 2: nächste Werte in queue packen

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

im.show()

## TODO: Continue here -> eventuell 2 Klassen -> erste Repräsentiert Pixelfarbe (z.B. einfach Enum Weiß/schwarz oder so) -> zweite Repräsentiert ganzes Bild
## Eventuell senkst du die Rechenleistung, wenn du statt auf einem richtigen Bild auf einer einfache Abstraktion arbeitest