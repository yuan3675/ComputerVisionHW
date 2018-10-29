from PIL import Image

def dilation(image, kernel):
	pixels = image.load()
	width, height = image.size
	dilation = Image.new('L', (width, height))
	
	for i in range(width):
		for j in range(height):
			dilation.putpixel((i, j), pixels[i, j])
			if pixels[i, j] > 0:
				maximun = pixels[i, j]
				# find the maximun pixel
				for k in kernel:
					if (i + k[0]) >= 0 and (i + k[0]) < width and (j + k[1]) >= 0 and (j + k[1]) < height:
						if pixels[i + k[0], j + k[1]] > maximun:
							maximun = pixels[i + k[0], j + k[1]]
				# assign maximun value
				for k in kernel:
					if (i + k[0]) >= 0 and (i + k[0]) < width and (j + k[1]) >= 0 and (j + k[1]) < height:
						dilation.putpixel((i + k[0], j + k[1]), maximun)
	
	return dilation

def erosion(image, kernel):
	pixels = image.load()
	width, height = image.size
	erosion = Image.new('L', (width, height))

	for i in range(width):
		for j in range(height):
			minimun = 255
			# find the minimun pixel
			for k in kernel:
				if (i + k[0]) >= 0 and (i + k[0]) < width and (j + k[1]) >= 0 and (j + k[1]) < height:
					if pixels[i+k[0], j+k[1]] < minimun:
						minimun = pixels[i+k[0], j+k[1]]

			f = True
			for k in kernel:
				if (i + k[0]) >= 0 and (i + k[0]) < width and (j + k[1]) >= 0 and (j + k[1]) < height:
					if pixels[i+k[0], j+k[1]] == 0:
						f = False
						break
			if f:
				erosion.putpixel((i,j), minimun)
	return erosion

def opening(image, kernel):
	ero = erosion(image, kernel)
	return dilation(ero, kernel)

def closing(image, kernel):
	dil = dilation(image, kernel)
	return erosion(dil, kernel)

# main
kernel = [[0,0], [0,1], [0, 2], [-1,0], [-2, 0],
          [-2,1], [-1,1], [0,1], [1,1], [2,1],
          [-2,-1], [-1,-1], [0,-1], [1,-1], [2,-1],
          [-1,2], [0,2], [1,2], [-1,-2], [0,-2], [1,-2]]

image = Image.open('lena.bmp').convert('L')
dilation(image, kernel).save('Dilation.bmp')
erosion(image, kernel).save('Erosion.bmp')
opening(image, kernel).save('Opening.bmp')
closing(image, kernel).save('Closing.bmp')

