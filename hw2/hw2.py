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
		if min > pixels[i, j - 1] and pixels[i, j - 1] != 0:
			min = pixels[i, j - 1]
	if j < (height - 1):
		if min > pixels[i, j + 1] and pixels[i, j + 1] != 0:
			min = pixels[i, j + 1]
	if i > 0:
		if min > pixels[i - 1, j] and pixels[i - 1, j] != 0:
			min = pixels[i - 1, j]
	if i < (width - 1):
		if min > pixels[i + 1, ｊ] and pixels[i + 1, j] != 0:
			min = pixels[i + 1, j]
	return min

def top_down(width, height, pixels):
	change = False
	for i in range(height):
		for j in range(width):
			if pixels[j, i] != 0:
				min = findMinNeighbor(j, i, width, height, pixels)
				if pixels[j, i] != min:
					change = True
					pixels[j, i] = min
	return not change, pixels 

def bottom_up(width, height, pixels):
	change = False
	for i in reversed(range(height)):
		for j in range(width):
			if pixels[j, i] != 0:
				min = findMinNeighbor(j, i, width, height, pixels)
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
	noChange = False;
	while not noChange:
		noChange, pixels = top_down(width, height, pixels)
		if not noChange:
			break
		noChange, pixels = bottom_up(width, height, pixels)
	return pixels

def drawBounderAndCenter(image, connected):
	width, height = image.size
	pixels = image.load()

	connectedHis = [0] * width * height    # calculate the histogram
	for j in range(height):
		for i in range(width):
			if (connected[i, j] != 0):
				connectedHis[connected[i, j]] += 1

	boundGroup = []
	for i in range(len(connectedHis)):    # filter components which less than 500 pixels
		if connectedHis[i] >= 500:
			boundGroup.append(i)

	boundedPoints = [[width, -1, height, -1] for i in range(len(boundGroup))]    # [left, right, up, down] find the 4 corners of the bounding box
	for j in range(height):
		for i in range(width):
			for k in range(len(boundGroup)):
				if connected[i, j] == boundGroup[k]:    # Don't know why affect others 
					if i < boundedPoints[k][0]:    # left
						boundedPoints[k][0] = i    
					if i > boundedPoints[k][1]:    # right
						boundedPoints[k][1] = i
					if j < boundedPoints[k][2]:    # up
						boundedPoints[k][2] = j
					if j > boundedPoints[k][3]:    # down
						boundedPoints[k][3] = j
					break
	#print(boundedPoints)

	# draw bounding box
	lime = (0, 255, 0)
	for i in boundedPoints:
		for j in range(i[0], i[1] + 1):    # draw top and down bounder
			image.putpixel((j, i[2]), lime)
			image.putpixel((j, i[3]), lime)
		for j in range(i[2], i[3] + 1):    # draw left and right bounder
			image.putpixel((i[0], j), lime)
			image.putpixel((i[1], j), lime)

	# draw center
	for i in boundedPoints:
		centerPoint = [int((i[0] + i[1])/2), int((i[2] + i[3])/2)]
		for j in range(centerPoint[0] - 5, centerPoint[0] + 6):
			image.putpixel((j, centerPoint[1]), lime)
		for j in range(centerPoint[1] - 5, centerPoint[1] + 6):
			image.putpixel((centerPoint[0], j), lime)

	return image



# Main Function
for i in range(width):
	for j in range(height):
		# threshold 128
		if pixels[i, j] < 128:
			imageBinary.putpixel((i, j), 0)
		else:
			imageBinary.putpixel((i, j), 1)
		# calculate the histogram
		histogram[pixels[i, j]] += 1

imageBinary.save('BinaryLena.bmp')

# draw the bar chart, x-axis ranges from 0 to 255, y-axis is the calculated result
plt.bar(range(256), height = histogram)
plt.savefig('histogram.jpg')

imageConnected = Image.new('RGB', (width, height))

pixels = imageBinary.load()
for i in range(width) :
    for j in range(height) :
        if pixels[i,j] == 1 :
            imageConnected.putpixel((i,j), (255,255,255))
        elif pixels[i,j] == 0 :
            imageConnected.putpixel((i,j), (0,0,0))

binaryPixels = connectedComponent(imageBinary)
imageConnected = drawBounderAndCenter(imageConnected, binaryPixels)
imageConnected.save('Connected_Components.bmp')