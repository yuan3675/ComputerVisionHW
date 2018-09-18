from PIL import Image

image = Image.open('lena.bmp')
width, height = image.size
pixels = image.load()

imageUpDown = Image.new('L', (width, height), 'white')
imageLeftRight = Image.new('L', (width, height), 'white')
imageDiagonal = Image.new('L', (width, height), 'white')

for i in range(0, width):
	for j in range(0, height):
		imageUpDown.putpixel((i, j), pixels[i, height - j - 1])
		imageLeftRight.putpixel((i, j), pixels[width - i - 1, j])
		imageDiagonal.putpixel((i, j), pixels[j, i])

imageUpDown.save('upside-down lena.bmp')
imageLeftRight.save('right-side-left lena.bmp')
imageDiagonal.save('diagonally mirrored lena.bmp')