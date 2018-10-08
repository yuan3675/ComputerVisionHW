from PIL import Image
import matplotlib.pyplot as plt

image = Image.open('lena.bmp')
width, height = image.size
pixels = image.load()

imageCopy = Image.new('L', (width, height), 'white')

# calculate histogram
histogram = [0] * 256
for i in range(0, width):
	for j in range(0, height):
		histogram[pixels[i, j]] += 1

# equalization function
S = [0] * 256
totalPixels = width * height
for i in range(len(histogram)):
	for j in range(i):
		S[i] = S[i] + (histogram[j] / totalPixels)
	S[i] = (int) (S[i] * 255)

histogramEqualization = [0] * 256
# put S value into image
for i in range(0, width):
	for j in range(0, height):
		imageCopy.putpixel((i, j), S[pixels[i, j]])
		histogramEqualization[S[pixels[i, j]]] += 1

imageCopy.save('HistogramEqualization.bmp')

plt.bar(range(256), height = histogramEqualization)
plt.savefig('histogram.jpg')