from PIL import Image
import matplotlib.pyplot as plt

def findMinNeighbor(i, j, width, height, label):
	min = width * height + 1
	if j > 0:
		if min > label[i][j - 1] and label[i][j - 1] != 0:
			min = label[i][j - 1]
	if j < (height - 1):
		if min > label[i][j + 1] and label[i][j + 1] != 0:
			min = label[i][j + 1]
	if i > 0:
		if min > label[i - 1][j] and label[i - 1][j] != 0:
			min = label[i - 1][j]
	if i < (width - 1):
		if min > label[i + 1][j] and label[i + 1][j] != 0:
			min = label[i + 1][j]
	return min

def connectedComponent(image):
	# Iterative algorithm (4 connected)
	pixels = image.load()
	width, height = image.size
	label = [[0] * width for i in range(height)]

	# Initialization of each pixel to a unique label
	counter = 1
	for j in range(height):
		for i in range(width):
			if pixels[i, j] == 1:
				label[i][j] = counter
				counter = counter + 1

	# Iteration of top-down followed by bottom-up  passes until no change
	change = True;
	while change:
		change = False
		# top-down
		for j in range(height):
			for i in range(width):
				if label[i][j] > 0:
					min = findMinNeighbor(i, j, width, height, label)
					if label[i][j] > min:
						change = True
						label[i][j] = min
		# bottom-up
		for j in reversed(range(height)):
			for i in reversed(range(width)):
				if label[i][j] > 0:
					min = findMinNeighbor(i, j, width, height, label)
					if label[i][j] > min:
						change = True
						label[i][j] = min
	return label

def drawBounderAndCenter(image, connected):
	width, height = image.size
	pixels = image.load()

	connectedHis = [0] * width * height    # calculate the histogram
	for j in range(height):
		for i in range(width):
			if (connected[i][j] > 0):
				connectedHis[connected[i][j]] += 1

	boundGroup = []
	for i in range(len(connectedHis)):    # filter components which less than 500 pixels
		if connectedHis[i] >= 500:
			boundGroup.append(i)

	# [left, right, up, down] find the 4 corners of the bounding box
	boundedPoints = [[width, -1, height, -1] for i in range(len(boundGroup))]    
	for j in range(height):
		for i in range(width):
			for k in range(len(boundGroup)):
				if connected[i][j] == boundGroup[k]:     
					if i < boundedPoints[k][0]:    # left
						boundedPoints[k][0] = i    
					if i > boundedPoints[k][1]:    # right
						boundedPoints[k][1] = i
					if j < boundedPoints[k][2]:    # up
						boundedPoints[k][2] = j
					if j > boundedPoints[k][3]:    # down
						boundedPoints[k][3] = j
					break

	# draw bounding box
	color = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 102, 0)]
	count = 0
	for i in boundedPoints:
		for j in range(i[0], i[1] + 1):    # draw top and down bounder
			image.putpixel((j, i[2]), color[count % 5])
			image.putpixel((j, i[3]), color[count % 5])
		for j in range(i[2], i[3] + 1):    # draw left and right bounder
			image.putpixel((i[0], j), color[count % 5])
			image.putpixel((i[1], j), color[count % 5])
		count += 1

	# draw center
	count = 0
	for i in boundedPoints:
		centerPoint = [int((i[0] + i[1])/2), int((i[2] + i[3])/2)]
		for j in range(centerPoint[0] - 5, centerPoint[0] + 6):
			image.putpixel((j, centerPoint[1]), color[count % 5])
		for j in range(centerPoint[1] - 5, centerPoint[1] + 6):
			image.putpixel((centerPoint[0], j), color[count % 5])
		count += 1

	return image

image = Image.open('lena.bmp')
width, height = image.size
pixels = image.load()

imageBinary = Image.new('1', (width, height), 'white')
histogram = [0] * 256

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

label = connectedComponent(imageBinary)
imageConnected = drawBounderAndCenter(imageConnected, label)
imageConnected.save('Connected_Components.bmp')