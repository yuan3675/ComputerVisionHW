from PIL import Image
import matplotlib.pyplot as plt


image = Image.open('lena.bmp')
width, height = image.size
pixels = image.load()

imageBinary = Image.new('1', (width, height), 'white')
histogram = [0] * 256

def findMinNeighbor(i, j, width, height, pixels):
	min = pixels[i, j]
	if j > 0:
		if min > pixels[j - 1, i] and pixels[j - 1, i] != 0:
			min = pixels[j - 1, i]
	if j < (width - 1):
		if min > pixels[j + 1, i] and pixels[j + 1, i] != 0:
			min = pixels[j + 1, i]
	if i > 0:
		if min > pixels[j, i - 1] and pixels[j, i - 1] != 0:
			min = pixels[j, i - 1]
	if i < (height - 1):
		if min > pixels[j, i + 1] and pixels[j, i + 1] != 0:
			min = pixels[j, i + 1]
	return min

def top_down(width, height, pixels):
	change = False
	for i in range(height):
		for j in range(width):
			if pixels[j, i] != 0:
				min = indMinNeighbor(j, i, width, height, pixels)
				if pixels[i, j] != min:
					change = True
					pixels[i, j] = min
	return not change, pixels 

def bottom_up(width, height, pixels):
	change = False
	for i in reversed(range(height)):
		for j in range(width):
			if pixels[j, i] != 0:
				min = indMinNeighbor(j, i, width, height, pixels)
				if pixels[j, i] != min:
					change = True
					pixels[j, i] = min
	return not change, pixels

def connectedComponent(image):
	# Iterative algorithm (4 connected)
	pixels = image.load()
	width, height = image.size

	# Initialization of each pixel to a unique label
	counter = 0
	for i in range(height):
		for j in range(width):
			if pixels[j, i] == 1:
				pixels[j, i] = pixels[j, i] + counter
				counter = counter + 1

	# Iteration of top-down followed by bottom-up  passes until no change
	bool noChange = False;
	while not noChange:
		noChange, pixels = top_down(width, height, pixels)
		if not noChange:
			break
		noChange, pixels = bottom_up(width, height, pixels)
	return pixels

def drawBounderAndCenter(image, connectedComponent):
	width, height = image.size
	pixels = image.load()

	connectedHis = [0] * width * height
	for i in range(width):
		for j in range(height):
			if (connectedComponent[i, j] != 0):
				connectedHis[connectedComponent[i, j]] += 1

	boundGroup = []
	for i in range(len(connectedHis)):
		if connectedHis[i] >= 500:
			boundGroup.append(i)

	boundedPoints = [[width, -1, height, -1]] * len(boundGroup)
	for i in range(width):
		for j in range(height):
			if connectedComponent[i, j]  in boundGroup:
				


# Main Function
for i in range(width):
	for j in range(height):
		# threshold 128
		if pixels[i, j] < 128:
			imageBinary.putpixel((i, j), 0)
		else:
			imageBinary.putpixel((i, j), 1)
		# calculate the histogram
		histogram[pixels[i, j]] = histogram[pixels[i, j]] + 1

binaryPixels = connectedComponent(imageBinary)
# 

imageBinary.save('BinaryLena.bmp')

# draw the bar chart, x-axis ranges from 0 to 255, y-axis is the calculated result
plt.bar(range(256), height = histogram)
plt.savefig('histogram.jpg')