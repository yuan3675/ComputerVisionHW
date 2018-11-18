from PIL import Image
import numpy as np
import math

def genNoises(image):
	width, height = image.size
	pixels = image.load()
	Gau10 = Image.new('L', (width, height))
	Gau30 = Image.new('L', (width, height))
	Salt01 = Image.new('L', (width, height))
	Salt005 = Image.new('L', (width, height))

	for j in range(height):
		for i in range(width):
			# generate Gaussian 30
			Gau10.putpixel((i, j), int(pixels[i, j] + 10 * np.random.normal(0.0, 1.0, None)))
			Gau30.putpixel((i, j), int(pixels[i, j] + 30 * np.random.normal(0.0, 1.0, None)))

			# generate salt and pepper
			if np.random.uniform(0.0, 1.0, None) < 0.05:
				Salt005.putpixel((i, j), 0)
			elif np.random.uniform(0.0, 1.0, None) > (1 - 0.05):
				Salt005.putpixel((i, j), 255)
			else:
				Salt005.putpixel((i, j), pixels[i, j])

			if np.random.uniform(0.0, 1.0, None) < 0.1:
				Salt01.putpixel((i, j), 0)
			elif np.random.uniform(0.0, 1.0, None) > (1 - 0.1):
				Salt01.putpixel((i, j), 255)
			else:
				Salt01.putpixel((i, j), pixels[i, j])

	return Gau10, Gau30, Salt01, Salt005

def SNR(origin, noises):
	width, height = origin.size
	pixlesO = origin.load()
	pixlesN = noises.load()

	u = 0.0
	un = 0.0
	for j in range(height):
		for i in range(width):
			u = u + pixlesO[i, j]
			un = un + (pixlesN[i, j] - pixlesO[i, j])
	u = u / (width * height)
	un = un / (width * height)

	VS = 0.0
	VN = 0.0
	for j in range(height):
		for i in range(width):
			VS = VS + (pixlesO[i, j] - u)**2
			VN = VN + (pixlesN[i, j] - pixlesO[i, j] - un)**2
	VS = VS / (width * height)
	VN = VN / (width * height)

	return 20 * math.log10(math.sqrt(VS) / math.sqrt(VN))

def boxAndMedFilter(image):
	width, height = image.size
	pixles = image.load()
	output3 = Image.new('L', (width, height))
	output5 = Image.new('L', (width, height))
	medOutput3 = Image.new('L', (width, height))
	medOutput5 = Image.new('L', (width, height))

	# 3X3 and 5X5 box filter
	for j in range(height):
		for i in range(width):
			average3 = 0
			average5 = 0
			medianList = []
			counter = 0
			for a in range(-1, 2):
				for b in range(-1, 2):
					if i+b > -1 and i+b < width and j+a > -1 and j+a < height:
						counter += 1
						medianList.append(pixles[i+b, j+a])
						average3 = average3 + pixles[i+b, j+a]
			medianList.sort()
			output3.putpixel((i, j), int(average3/counter))
			medOutput3.putpixel((i, j), medianList[int(counter/2)])
			medianList.clear()
			counter = 0
			for a in range(-2, 3):
				for b in range(-2, 3):
					if i+b > -1 and i+b < width and j+a > -1 and j+a < height:
						counter += 1
						medianList.append(pixles[i+b, j+a])
						average5 = average5 + pixles[i+b, j+a]
			medianList.sort()
			output5.putpixel((i, j), int(average5/counter))
			medOutput5.putpixel((i, j), medianList[int(counter/2)])
	return output3, output5, medOutput3, medOutput5

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
gau10, gau30, salt01, salt005 = genNoises(image)
box3_gau10, box5_gau10, med3_gau10, med5_gau10 = boxAndMedFilter(gau10)
box3_gau30, box5_gau30, med3_gau30, med5_gau30 = boxAndMedFilter(gau30)
box3_salt01, box5_salt01, med3_salt01, med5_salt01 = boxAndMedFilter(salt01)
box3_salt005, box5_salt005, med3_salt005, med5_salt005 = boxAndMedFilter(salt005)
oc_gau10 = closing(opening(gau10, kernel), kernel)
oc_gau30 = closing(opening(gau30, kernel), kernel)
oc_salt01 = closing(opening(salt01, kernel), kernel)
oc_salt005 = closing(opening(salt005, kernel), kernel)
co_gau10 = opening(closing(gau10, kernel), kernel)
co_gau30 = opening(closing(gau30, kernel), kernel)
co_salt01 = opening(closing(salt01, kernel), kernel)
co_salt005 = opening(closing(salt005, kernel), kernel)
print('Gaussian10 box3 SNR:', SNR(image, box3_gau10))
print('Gaussian10 box5 SNR:', SNR(image, box5_gau10))
print('Gaussian10 med3 SNR:', SNR(image, med3_gau10))
print('Gaussian10 med5 SNR:', SNR(image, med5_gau10))
print('Gaussian10 open close SNR:', SNR(image, oc_gau10))
print('Gaussian10 close open SNR:', SNR(image, co_gau10))
print('Gaussian30 box3 SNR:', SNR(image, box3_gau30))
print('Gaussian30 box5 SNR:', SNR(image, box5_gau30))
print('Gaussian30 med3 SNR:', SNR(image, med3_gau30))
print('Gaussian30 med5 SNR:', SNR(image, med5_gau30))
print('Gaussian30 open close SNR:', SNR(image, oc_gau30))
print('Gaussian30 close open SNR:', SNR(image, co_gau30))
print('Salt and pepper 0.05 box3 SNR:', SNR(image, box3_salt005))
print('Salt and pepper 0.05 box5 SNR:', SNR(image, box5_salt005))
print('Salt and pepper 0.05 med3 SNR:', SNR(image, med3_salt005))
print('Salt and pepper 0.05 med5 SNR:', SNR(image, med5_salt005))
print('Salt and pepper 0.05 open close SNR:', SNR(image, oc_salt005))
print('Salt and pepper 0.05 close open SNR:', SNR(image, co_salt005))
print('Salt and pepper 0.1 box3 SNR:', SNR(image, box3_salt01))
print('Salt and pepper 0.1 box5 SNR:', SNR(image, box3_salt01))
print('Salt and pepper 0.1 med3 SNR:', SNR(image, med3_salt01))
print('Salt and pepper 0.1 med5 SNR:', SNR(image, med5_salt01))
print('Salt and pepper 0.1 open close SNR:', SNR(image, oc_salt01))
print('Salt and pepper 0.1 close open SNR:', SNR(image, co_salt01))
gau10.save('Gaussian10.bmp')
gau30.save('Gaussian30.bmp')
salt005.save('SaltAndPepper005.bmp')
salt01.save('SaltAndPepper01.bmp')
box3_gau10.save('Box3_gau10.bmp')
box5_gau10.save('Box5_gau10.bmp')
box3_gau30.save('Box3_gau30.bmp')
box5_gau30.save('Box5_gau30.bmp')
med3_gau10.save('Med3_gau10.bmp')
med5_gau10.save('Med5_gau10.bmp')
med3_gau30.save('Med3_gau30.bmp')
med5_gau30.save('Med5_gau30.bmp')
oc_gau10.save('OC_gau10.bmp')
co_gau10.save('CO_gau10.bmp')
oc_gau30.save('OC_gau30.bmp')
co_gau30.save('CO_gau30.bmp')
box3_salt01.save('Box3_salt01.bmp')
box5_salt01.save('Box5_salt01.bmp')
box3_salt005.save('Box3_salt005.bmp')
box5_salt005.save('Box5_salt005.bmp')
med3_salt01.save('Med3_salt01.bmp')
med5_salt01.save('Med5_salt01.bmp')
med3_salt005.save('Med3_salt005.bmp')
med5_salt005.save('Med5_salt005.bmp')
oc_salt01.save('OC_salt01.bmp')
co_salt01.save('CO_salt01.bmp')
oc_salt005.save('OC_salt005.bmp')
co_salt005.save('CO_salt005.bmp')