from math import log2, ceil
import numpy as np
import imageio.v2 as imageio

inPath = "input1.jpg"
outPath = "output.png"

kernelMin, kernelMax = -5, 21
kernelSize = (
						3, 3, 3
						)
# количество, высота, ширина

img = imageio.imread(inPath)
print(img.shape)
width, height, num_color = img.shape

def main():
	result_image = img
	kernelsdata = genKernel(kernelMin, kernelMax, kernelSize, 2)
	result_image = convolution(img, kernelsdata)
	result_image = normalize(result_image)
	
	print(result_image.shape)
	imageio.imwrite(outPath, result_image)

def convolution(img, kernelsdata):
	kernels, steps = kernelsdata
	img_width, img_height = len(img[0]), len(img)
	activation_map = []
	
	for k in range(len(kernels)):
		kernel_width, kernel_height = len(kernels[k]), len(kernels[k, 0])
		delta_width = delta_height = 0
		kernel_img = img
		if kernel_width > img_width or kernel_height > img_height:
			delta_width = ceil((kernel_width - img_width) / 2)
			delta_height = ceil((kernel_height - img_height) / 2)
			
			kernel_img = np.pad(img, pad_width=((delta_height, delta_height), (delta_width, delta_width), (0, 0)), mode="constant")
		
		outImg_width = ceil((img_width - kernel_width + 2 * delta_width) / steps[k])
		outImg_height = ceil((img_height - kernel_height + 2 * delta_height) / steps[k])
		
		activation_map.append(np.empty((outImg_height, outImg_width)))
		
		for h in range(outImg_height):
			for w in range(outImg_width):
				h_start = h * steps[k]
				h_end = h_start + kernel_height
				w_start = w * steps[k]
				w_end = w_start + kernel_width
				patch = kernel_img[h_start:h_end, w_start:w_end, k]
				
				activation_map[k][h][w] = np.sum(patch * kernels[k])
	
	return np.transpose(np.stack(activation_map), (1, 2, 0))

def genKernel(min, max, size, steps=None):
	if steps == None:
		steps = (1,) * size[0]
	else:
		steps = (steps,) * size[0]
	return np.random.randint(min, max, (size)), steps

def normalize(activation_map):
	i = 0
	for sub_array in activation_map:
		min_val = np.min(sub_array)
		max_val = np.max(sub_array)
        
		if max_val == min_val:
			normalized_sub_array = np.zeros_like(sub_array)
		else:
			normalized_sub_array = np.round((sub_array - min_val) / (max_val - min_val) * 255)
		
		activation_map[i] = normalized_sub_array
		i += 1
	
	return activation_map.astype(np.uint8)


main()