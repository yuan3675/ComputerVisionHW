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
	output = Image.new('1', (66, 66), 0)
	width, height = image.size
	pixels = image.load()

	for j in range(64):
		for i in range(64):
			output.putpixel((i+1, j+1), pixels[i*8, j*8])
	return output

def pairRelationship(image):
	width, height = image.size
	pixels = image.load()
	output = Image.new('1',(width, height), 0)

	# p = 1, q = 0
	for j in range(1, height-1):
		for i in range(1, width-1):
			# if pixel(i, j) is 1-connected
			if pixels[i, j] == 1: 
				if pixels[i+1, j] == 1 or pixels[i-1, j] == 1 or pixels[i, j+1] == 1 or pixels[i, j-1] == 1:
					output.putpixel((i, j), 1)
	return output

def yokoi(image, i, j):
	pixels = image.load()
	rCounter = 0
	qCounter = 0
			
	# a1
	if pixels[i, j] == pixels[i+1, j] and pixels[i, j] == pixels[i, j-1] and pixels[i, j] == pixels[i+1, j-1]:
		rCounter += 1
	elif pixels[i, j] == pixels[i+1, j]:
		qCounter += 1
	# a2
	if pixels[i, j] == pixels[i, j-1] and pixels[i, j] == pixels[i-1, j-1] and pixels[i, j] == pixels[i-1, j]:
		rCounter += 1
	elif pixels[i, j] == pixels[i, j-1]:
		qCounter += 1
	# a3
	if pixels[i, j] == pixels[i-1, j] and pixels[i, j] == pixels[i, j+1] and pixels[i, j] == pixels[i-1, j+1]:
		rCounter += 1
	elif pixels[i, j] == pixels[i-1, j]:
		qCounter += 1
	# a4
	if pixels[i, j] == pixels[i, j+1] and pixels[i, j] == pixels[i+1, j] and pixels[i, j] == pixels[i+1, j+1]:
		rCounter += 1
	elif pixels[i, j] == pixels[i, j+1]:
		qCounter += 1
			
	if rCounter == 4:
		return 5
	else:
		return qCounter

def totalYokoi(image):
	width, height = image.size
	output = Image.new('I', (width, height), 0)
	pixels = image.load()
	
	for j in range(1, height-1):
		for i in range(1, width-1):
			if pixels[i, j] == 1:
				output.putpixel((i, j), yokoi(image, i, j))

	return output

def shrink(image, pair):
	width, height = image.size
	pixels = image.load()
	pixels_p = pair.load()
	output = Image.new('1', (width, height), 0)

	for j in range(height):
		for i in range(width):
			output.putpixel((i, j), pixels[i, j])

	for j in range(1, height-1):
		for i in range(1, width-1):
			if pixels[i, j] == 1:
				if yokoi(output, i, j) == 1 and pixels_p[i, j] == 1:
					output.putpixel((i, j), 0)
	
	return output

# Main Function
image = Image.open('lena.bmp')
binaryImage = binarize(image)
nowImage = downSampling(binaryImage)
width, height = nowImage.size
preImage = Image.new('1', (width, height), 0)

while preImage != nowImage:
	preImage = nowImage
	border = totalYokoi(nowImage)
	pair = pairRelationship(border)
	nowImage = shrink(nowImage, pair)

pixels = nowImage.load()
output = Image.new('1', (64, 64), 0)
for j in range(64):
	for i in range(64):
		output.putpixel((i, j), pixels[i+1, j+1])


output.save('Thinning.bmp')