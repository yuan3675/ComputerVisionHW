from PIL import Image

def convertToBinary(image, threshold):
	pixels = image.load()
	width, height = image.size
	imageBinary = Image.new('1', (width, height), 'white')

	for i in range(width):
		for j in range(height):
			if pixels[i, j] < threshold:
				imageBinary.putpixel((i, j), 0)
			else:
				imageBinary.putpixel((i, j), 1)
	return imageBinary

def dilation(image, kernel):
	pixels = image.load()
	width, height = image.size
	dilation = Image.new('1', (width, height), 'black')

	for i in range(width):
		for j in range(height):
			if pixels[i, j] == 1:
				for k in kernel:
					if (i + k[0]) >= 0 and (i + k[0]) < width and (j + k[1]) >= 0 and (j + k[1]) < height:
						dilation.putpixel((i + k[0], j + k[1]), 1)
	return dilation			

def erosion(image, kernel):
	pixels = image.load()
	width, height = image.size
	erosion = Image.new('1', (width, height), 'black')

	for i in range(width):
		for j in range(height):
			f = True
			for k in kernel:
				if (i + k[0]) >= 0 and (i + k[0]) < width and (j + k[1]) >= 0 and (j + k[1]) < height:
					if pixels[i+k[0], j+k[1]] == 0:
						f = False
						break
			if f:
				erosion.putpixel((i,j), 1)
	return erosion

def opening(image, kernel):
	ero = erosion(image, kernel)
	return dilation(ero, kernel)

def closing(image, kernel):
	dil = dilation(image, kernel)
	return erosion(dil, kernel)

def hit_and_miss(image, J, K):
	pixels = image.load()
	width, height = image.size
	HM = Image.new('1', (width, height), 'black')
	image_C = Image.new('1', (width, height), 'black')
	imJ = erosion(image, J)
	
	for i in range(width):
		for j in range(height):
			if pixels[i, j] == 1:
				image_C.putpixel((i, j), 0)
			else:
				image_C.putpixel((i, j), 1)

	imK = erosion(image_C, K)

	pixelsJ = imJ.load()
	pixelsK = imK.load()
	for i in range(width):
		for j in range(height):
			if pixelsJ[i, j] == 1 and pixelsK[i, j] == 1:
				HM.putpixel((i, j), 1)

	return HM

# main
kernel = [[0,0], [0,1], [0, 2], [-1,0], [-2, 0],
          [-2,1], [-1,1], [0,1], [1,1], [2,1],
          [-2,-1], [-1,-1], [0,-1], [1,-1], [2,-1],
          [-1,2], [0,2], [1,2], [-1,-2], [0,-2], [1,-2]]
J = [[0,0], [0,-1], [1,0]]
K = [[0,1], [-1,0], [-1,1]]

image = Image.open('lena.bmp').convert('L')
imageBinary = convertToBinary(image, 128)
dilation(imageBinary, kernel).save('Dilation.bmp')
erosion(imageBinary, kernel).save('Erosion.bmp')
opening(imageBinary, kernel).save('Opening.bmp')
closing(imageBinary, kernel).save('Closing.bmp')
hit_and_miss(imageBinary, J, K).save('Hit-and-miss.bmp')

