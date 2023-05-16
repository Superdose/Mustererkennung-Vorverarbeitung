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

#(pixelCount)

mostRGB = (0, 0, 0)
count = 0

for red in range(256):
    for green in range(256):
        for blue in range(256):
            if pixelCount[red, green, blue] > count:
                count = pixelCount[red, green, blue]
                mostRGB = (red, green, blue)

print("Most common rgb color is: " + str(mostRGB) + " with count: " + str(count))

colorRange = 40

imageWidth = im.width
imageHeight = im.height

for i in range(im.size[0]):
    for j in range(im.size[1]):
        red = pixels[i, j][0]
        green = pixels[i, j][1]
        blue = pixels[i, j][2]
        if (mostRGB[0] - colorRange <= red <= mostRGB[0] + colorRange) or (
               mostRGB[1] - colorRange <= green <= mostRGB[1] + colorRange) or (
               mostRGB[2] - colorRange <= blue <= mostRGB[2] + colorRange):
            pixels[i, j] = (255, 255, 255)
        else:
            pixels[i, j] = (0, 0, 0)
        #pixels[i, j] = (red, green, blue)

#data = np.zeros((imageHeight, imageWidth, 3), dtype=np.uint8) # np.uint8

#for row in img:
#    for px in row:
#        #print(px)
#        #print(type(px)) # px ist ein numpy.ndarray -> eventuell musst du ein neues Erstellen und darüber die RGB-Werte eintragen -> kein Tupel/Array??
#        red = px[0]
#        green = px[1]
#        blue = px[2]
#        arr = np.array([red, green, blue])
#        print(arr)
        #if (mostRGB[0] - colorRange <= red <= mostRGB[0] + colorRange) or (
        #        mostRGB[1] - colorRange <= green <= mostRGB[1] + colorRange) or (
        #        mostRGB[2] - colorRange <= blue <= mostRGB[2] + colorRange):
        #    data[row, px] = white
#        data[row, px] = arr #(red, green, blue)

im.show()

#plt.im

#newImage = Image.fromarray(data.astype('uint8'), 'RGB')# Image.fromarray(data, 'RGB')
#newImage.save("images/result.png")
#newImage.show()


#im.putdata(img)
#im.show()

#for p in img:
#    print(p)


#import cv2
#import matplotlib.pyplot as plt

#img = cv2.imread('images/image.jpg', 0)



#plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#plt.show()