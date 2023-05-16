# Imports PIL module
from PIL import Image
import numpy as np

# open method used to open different extension image file
im = Image.open("images/image.jpg")

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

im.show()
