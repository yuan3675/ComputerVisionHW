from PIL import Image
import math

def Robert(image, threshold):
    width, height = image.size
    pixels = image.load()
    output = Image.new('1', (width, height), 1)

    for j in range(height):
        for i in range(width):
            r1 = 0
            r2 = 0
            if (j+1) < height and (i+1) < width:
                r1 = pixels[i+1, j+1] - pixels[i, j]
            if (j+1) < height and (i-1) >= 0:
                r2 = pixels[i-1, j+1] - pixels[i, j]
            if math.sqrt(r1**2 + r2**2) > threshold:
                output.putpixel((i, j), 0)
    return output

def Prewitt(image, threshold):
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
            p1 = padding[i+1, j-1] + padding[i+1, j] + padding[i+1, j+1] - padding[i-1, j-1] - padding[i-1, j] - padding[i-1, j+1]
            p2 = padding[i-1, j+1] + padding[i, j+1] + padding[i+1, j+1] - padding[i-1, j-1] - padding[i, j-1] - padding[i+1, j-1]
            if math.sqrt(p1**2 + p2**2) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output
# looks not the same
def Sobel(image, threshold):
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
            s1 = padding[i+1, j-1] + (2*padding[i+1, j]) + padding[i+1, j+1] - padding[i-1, j-1] - (2*padding[i-1, j]) - padding[i-1, j+1]
            s2 = padding[i-1, j+1] + (2*padding[i, j+1]) + padding[i+1, j+1] - padding[i-1, j-1] - (2*padding[i, j-1]) - padding[i+1, j-1]
            if math.sqrt(s1**2 + s2**2) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output  

def FreiAndChen(image, threshold):
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
            f1 = padding[i+1, j-1] + (math.sqrt(2)*padding[i+1, j]) + padding[i+1, j+1] - padding[i-1, j-1] - (math.sqrt(2)*padding[i-1, j]) - padding[i-1, j+1]
            f2 = padding[i-1, j+1] + (math.sqrt(2)*padding[i, j+1]) + padding[i+1, j+1] - padding[i-1, j-1] - (math.sqrt(2)*padding[i, j-1]) - padding[i+1, j-1]
            if math.sqrt(f1**2 + f2**2) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output

def Kirsch(image, threshold):
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
            k0 = -3*padding[i-1, j-1] - 3*padding[i, j-1] + 5*padding[i+1, j-1] - 3*padding[i-1, j] + 5*padding[i+1, j] - 3*padding[i-1, j+1] - 3*padding[i, j+1] + 5*padding[i+1, j+1]
            k1 = -3*padding[i-1, j-1] + 5*padding[i, j-1] + 5*padding[i+1, j-1] - 3*padding[i-1, j] + 5*padding[i+1, j] - 3*padding[i-1, j+1] - 3*padding[i, j+1] - 3*padding[i+1, j+1]
            k2 = 5*padding[i-1, j-1] + 5*padding[i, j-1] + 5*padding[i+1, j-1] - 3*padding[i-1, j] - 3*padding[i+1, j] - 3*padding[i-1, j+1] - 3*padding[i, j+1] - 3*padding[i+1, j+1]
            k3 = 5*padding[i-1, j-1] + 5*padding[i, j-1] - 3*padding[i+1, j-1] + 5*padding[i-1, j] - 3*padding[i+1, j] - 3*padding[i-1, j+1] - 3*padding[i, j+1] - 3*padding[i+1, j+1]
            k4 = 5*padding[i-1, j-1] - 3*padding[i, j-1] - 3*padding[i+1, j-1] + 5*padding[i-1, j] - 3*padding[i+1, j] + 5*padding[i-1, j+1] - 3*padding[i, j+1] - 3*padding[i+1, j+1]
            k5 = -3*padding[i-1, j-1] - 3*padding[i, j-1] - 3*padding[i+1, j-1] + 5*padding[i-1, j] - 3*padding[i+1, j] + 5*padding[i-1, j+1] + 5*padding[i, j+1] - 3*padding[i+1, j+1]
            k6 = -3*padding[i-1, j-1] - 3*padding[i, j-1] - 3*padding[i+1, j-1] - 3*padding[i-1, j] - 3*padding[i+1, j] + 5*padding[i-1, j+1] + 5*padding[i, j+1] + 5*padding[i+1, j+1]
            k7 = -3*padding[i-1, j-1] - 3*padding[i, j-1] - 3*padding[i+1, j-1] - 3*padding[i-1, j] + 5*padding[i+1, j] - 3*padding[i-1, j+1] + 5*padding[i, j+1] + 5*padding[i+1, j+1]
            if max(k0, k1, k2, k3, k4, k5, k6, k7) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output

def Robinson(image, threshold):
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
            r0 = -1 * padding[i-1, j-1] + padding[i+1, j-1] - 2*padding[i-1, j] + 2*padding[i+1, j] - padding[i-1, j+1] + padding[i+1, j+1]
            r1 = padding[i, j-1] + 2*padding[i+1, j-1] - padding[i-1, j] + padding[i+1, j] - 2*padding[i-1, j+1] - padding[i, j+1]
            r2 = padding[i-1, j-1] + 2*padding[i, j-1] + padding[i+1, j-1] - padding[i-1, j+1] - 2*padding[i, j+1] - padding[i+1, j+1]
            r3 = 2*padding[i-1, j-1] + padding[i, j-1] + padding[i-1, j] - padding[i+1, j] - padding[i, j+1] - 2*padding[i+1, j+1]
            r4 = padding[i-1, j-1] - padding[i+1, j-1] + 2*padding[i-1, j] - 2*padding[i+1, j] + padding[i-1, j+1] - padding[i+1, j+1]
            r5 = -1 * padding[i, j-1] - 2*padding[i+1, j-1] + padding[i-1, j] - padding[i+1, j] + 2*padding[i-1, j+1] + padding[i, j+1]
            r6 = -1*padding[i-1, j-1] - 2*padding[i, j-1] - padding[i+1, j-1] + padding[i-1, j+1] + 2*padding[i, j+1] + padding[i+1, j+1]
            r7 = -2*padding[i-1, j-1] - padding[i, j-1] - padding[i-1, j] + padding[i+1, j] + padding[i, j+1] + 2*padding[i+1, j+1]
            if max(r0, r1, r2, r3, r4, r5, r6, r7) > threshold:
                output.putpixel((i-1, j-1), 0)
    return output

def NevatiaAndBabu(image, threshold):
    width, height = image.size
    pixels = image.load()
    tmp = Image.new('L', (width+4, height+4), 'black')
    output = Image.new('1', (width, height), 1)
    masks = [[[100, 100, 100, 100, 100], [100, 100, 100, 100, 100], [0, 0, 0, 0, 0], [-100, -100, -100, -100, -100], [-100, -100, -100, -100, -100]],
    [[100, 100, 100, 100, 100], [100, 100, 100, 78, -32], [100, 92, 0, -92, -100], [32, -78, -100, -100, -100], [-100, -100, -100, -100, -100]],
    [[100, 100, 100, 32, -100], [100, 100, 92, -78, -100], [100, 100, 0, -100, -100], [100, 78, -92, -100, -100], [100, -32, -100, -100, -100]],
    [[-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, 0, 100, 100]],
    [[-100, 32, 100, 100, 100], [-100, -78, 92, 100, 100], [-100, -100, 0, 100, 100], [-100, -100, -92, 78, 100], [-100, -100, -100, -32, 100]],
    [[100, 100, 100, 100, 100], [-32, 78, 100, 100, 100], [-100, -92, 0, 92, 100], [-100, -100, -100, -78, 32], [-100, -100, -100, -100, -100]]]

    for j in range(2, height+2):
        for i in range(2, width+2):
            tmp.putpixel((i, j), pixels[i-2, j-2])

    padding = tmp.load()
    for j in range(2, height+2):
        for i in range(2, width+2):
            rList = []
            for k in range(len(masks)):
                r = 0
                for m in range(5):
                    for n in range(5):
                        r += padding[i+n-2, j+m-2] * masks[k][m][n]
                rList.append(r) 
            if max(rList) > threshold:
                output.putpixel((i-2, j-2), 0)
    return output

# main function
image = Image.open('lena.bmp').convert('L')
roberts = Robert(image, 12)
roberts.save('Roberts.bmp')
prewitt = Prewitt(image, 24)
prewitt.save('Prewitt.bmp')
sobel = Sobel(image, 38)
sobel.save('Sobel.bmp')
frei = FreiAndChen(image, 30)
frei.save('Frei.bmp')
kirsch = Kirsch(image, 135)
kirsch.save('Kirsch.bmp')
robinson = Robinson(image, 43)
robinson.save('Robinson.bmp')
nev = NevatiaAndBabu(image, 12500)
nev.save('Nevatia.bmp')