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
	output = Image.new('1', (66, 66))
	width, height = image.size
	pixels = image.load()

	for j in range(1, 65):
		for i in range(1, 65):
			output.putpixel((i, j), pixels[(i-1)*8, (j-1)*8])
	return output

def pairRelationship(image):
	width, height = image.size
	pixels = image.load()
	output = Image.new('1',(width, height), 0)

	# p = 1, q = 0
	for j in range(1, height-1):
		for i in range(1, width-1):
			# if pixel(i, j) is border
			if pixels[i, j] == 1: 
				if pixels[i+1, j] == 1 or pixels[i-1, j] == 1 or pixels[i, j+1] == 1 or pixels[i, j-1] == 1:
					output.putpixel((i, j), 1)
	return output

def yokoi(image):
	width, height = image.size
	output = Image.new('I', (width, height), 0)
	pixels = image.load()
	
	for j in range(1, height-1):
		for i in range(1, width-1):
			rCounter = 0
			qCounter = 0
			
			if (pixels[i, j] == 1):
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
				output.putpixel((i, j), 5)
			elif qCounter != 0:
				output.putpixel((i, j), qCounter)

	return output

def shrink(image, border, pair):
	width, pixel = image.size
	pixels = image.load()
	pixels_b = border.load()
	pixels_p = pair.load()
	output = Image.new('1', (width, height), 0)

	for j in range(height):
		for i in range(width):
			output.putpixel((i, j), pixels[i, j])
	counter = 0
	for j in range(1, height-1):
		for i in range(1, width-1):
			if pixels[i, j] == 1:
				if pixels_b[i, j] == 1 and pixels_p[i, j] == 1:
					output.putpixel((i, j), 0)
					counter += 1
	print(counter)
	return output

# Main Function
image = Image.open('lena.bmp')
binaryImage = binarize(image)
nowImage = downSampling(binaryImage)
width, height = nowImage.size
preImage = Image.new('1', (width, height), 0)

counter = 0
while preImage != nowImage:
	counter += 1
	preImage = nowImage
	border = yokoi(nowImage)
	pair = pairRelationship(border)
	nowImage = shrink(nowImage, border, pair)

print(counter)
pixels = nowImage.load()
output = Image.new('1', (64, 64), 0)
for j in range(64):
	for i in range(64):
		output.putpixel((i, j), pixels[i+1, j+1])


output.save('Thinning.bmp')