from PIL import Image
import matplotlib.pyplot as plt

def binarize(image):
	width, height = image.size
	binaryImage = Image.new('1', (width, height), 'white')
	pixels = image.load()

	for j in range(height):
		for i in range(width):
			# threshold 128
			if pixels[i, j] < 128:
				binaryImage.putpixel((i, j), 0)
			else:
				binaryImage.putpixel((i, j), 1)
	return binaryImage

def downSampling(image):
	output = Image.new('1', (64, 64))
	width, height = image.size
	pixels = image.load()

	for j in range(64):
		for i in range(64):
			output.putpixel((i, j), pixels[i*8, j*8])
	return output

def countYokoiNumber(image):
	width, height = image.size
	output = Image.new('I', (width, height), 0)
	pixels = image.load()

	# initialize a bigger image
	bigImage = []
	for j in range(height+2):
		tmp = [0] * (width+2)
		bigImage.append(tmp)

	for i in range(1, height+1):
		for j in range(1, width+1):
			bigImage[i][j] = pixels[j-1, i-1]

	for i in range(1, height+1):
		for j in range(1, width+1):
			qCounter = 0
			rCounter = 0
			# a1
			if (bigImage[i][j] == 1):
				if bigImage[i][j] == bigImage[i+1][j] and bigImage[i][j] == bigImage[i][j-1] and bigImage[i][j] == bigImage[i+1][j-1]:
					rCounter += 1
				elif bigImage[i][j] == bigImage[i+1][j]:
					qCounter += 1
				# a2
				if bigImage[i][j] == bigImage[i][j-1] and bigImage[i][j] == bigImage[i-1][j-1] and bigImage[i][j] == bigImage[i-1][j]:
					rCounter += 1
				elif bigImage[i][j] == bigImage[i][j-1]:
					qCounter += 1
				# a3
				if bigImage[i][j] == bigImage[i-1][j] and bigImage[i][j] == bigImage[i][j+1] and bigImage[i][j] == bigImage[i-1][j+1]:
					rCounter += 1
				elif bigImage[i][j] == bigImage[i-1][j]:
					qCounter += 1
				# a4
				if bigImage[i][j] == bigImage[i][j+1] and bigImage[i][j] == bigImage[i+1][j] and bigImage[i][j] == bigImage[i+1][j+1]:
					rCounter += 1
				elif bigImage[i][j] == bigImage[i][j+1]:
					qCounter += 1

				if rCounter == 4:
					output.putpixel((j-1, i-1), 5)
				elif qCounter != 0:
					output.putpixel((j-1, i-1), qCounter)

	return output

# Main Function
image = Image.open('lena.bmp')
binaryImage = binarize(image)
smallImage = downSampling(binaryImage)
output = countYokoiNumber(smallImage)
output.save('Yokoi.tif')
pixels = output.load()
width, height = output.size
for j in range(height):
	for i in range(width):
		print(pixels[i, j], end = ' ')
	print()