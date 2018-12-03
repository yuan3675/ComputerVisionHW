from PIL import Image
import math

def LaplaceMask1(image, threshold):
    width, height = image.size
    pixels = image.load()
    tmp = Image.new('L', (width+2, height+2), 'black')
    output = Image.new('1', (width, height), 1)
    for j in range(1, height+1):
        for i in range(1, width+1):
            tmp.putpixel((i, j), pixels[i-1, j-1])

    padding = tmp.load()
    for j in range(1, height+1):
        for i in range(1, width+1):
            result = padding[i, j-1] + padding[i-1, j] - 4 * padding[i, j] + padding[i+1, j] + padding[i, j+1] 
            if result > threshold:
                output.putpixel((i-1, j-1), 0)
    return output

def LaplaceMask2(image, threshold):
    width, height = image.size
    pixels = image.load()
    tmp = Image.new('L', (width+2, height+2), 'black')
    output = Image.new('1', (width, height), 1)
    for j in range(1, height+1):
        for i in range(1, width+1):
            tmp.putpixel((i, j), pixels[i-1, j-1])

    padding = tmp.load()
    for j in range(1, height+1):
        for i in range(1, width+1):
            result = 0
            for m in range(-1, 2):
                for n in range(-1, 2):
                    if m == 0 and n == 0:
                        result -= 8 * padding[i+n, j+m]
                    else:
                        result += padding[i+n, j+m]
            if (result/3) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output  

def MinimumVariance(image, threshold):
    width, height = image.size
    pixels = image.load()
    tmp = Image.new('L', (width+2, height+2), 'black')
    output = Image.new('1', (width, height), 1)
    for j in range(1, height+1):
        for i in range(1, width+1):
            tmp.putpixel((i, j), pixels[i-1, j-1])

    padding = tmp.load()
    for j in range(1, height+1):
        for i in range(1, width+1):
            result = 2 * (padding[i-1, j-1] + padding[i+1, j-1] + padding[i-1, j+1] + padding[i+1, j+1]) \
            - (padding[i, j-1] + padding[i-1, j] + padding[i+1, j] + padding[i, j+1]) \
            - 4 * padding[i, j]
            if (result/3) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output

def LaplaceOfGaussian(image, threshold):
    width, height = image.size
    pixels = image.load()
    tmp = Image.new('L', (width+10, height+10), 0)
    output = Image.new('1', (width, height), 1)
    mask = [[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0], [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
    [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0], [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
    [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1], [-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
    [-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1], [-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
    [0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0], [0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
    [0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]]
    
    for j in range(5, height+5):
        for i in range(5, width+5):
            tmp.putpixel((i, j), pixels[i-5, j-5])

    padding = tmp.load()
    for j in range(5, height+5):
        for i in range(5, width+5):
            result = 0
            for m in range(11):
                for n in range(11):
                    result += padding[i+n-5, j+m-5] * mask[m][n] 
            if result > threshold:
                output.putpixel((i-5, j-5), 0)
    return output

def DifferenceOfGaussian(image, threshold):
    width, height = image.size
    pixels = image.load()
    tmp = Image.new('L', (width+10, height+10), 'black')
    output = Image.new('1', (width, height), 0)
    mask = [[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1], [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
    [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4], [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
    [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7], [-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
    [-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7], [-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
    [-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4], [-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
    [-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]]
    
    for j in range(5, height+5):
        for i in range(5, width+5):
            tmp.putpixel((i, j), pixels[i-5, j-5])

    padding = tmp.load()
    for j in range(5, height+5):
        for i in range(5, width+5):
            result = 0
            for m in range(11):
                for n in range(11):
                    result += padding[i+n-5, j+m-5] * mask[m][n] 
            if result > threshold:
                output.putpixel((i-5, j-5), 1)
    return output

# main function
image = Image.open('lena.bmp').convert('L')
mask1 = LaplaceMask1(image, 15)
mask1.save('Mask1.bmp')
mask2 = LaplaceMask2(image, 15)
mask2.save('Mask2.bmp')
minVariance = MinimumVariance(image, 20)
minVariance.save('MinimumVariance.bmp')
laplaceGaussian = LaplaceOfGaussian(image, 3000)
laplaceGaussian.save('LaplaceOfGaussian.bmp')
differenceGaussian = DifferenceOfGaussian(image, 1)
differenceGaussian.save('DifferenceOfGaussian.bmp')