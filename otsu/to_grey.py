from PIL import Image
import numpy as np
from matplotlib import image

image = (Image.open('ro.jpg'))
#image.thumbnail((100, 100))
# Load image as array of RGB
#img = img.astype(float)
new = np.asarray(image)
print(new.shape)
#print(new.shape)
#print(img)
dims = new.shape
print('OG')
print(dims)
print(new)
new = new.astype(float)
grey_arr = np.array([0.2126, 0.7152, 0.0722])
#grey_arr = np.array([0.75, 0.75, 0.75])
#new *= grey_arr
new = np.dot(new, grey_arr)
# Round array to int
new = np.rint(new).astype(np.uint8)
print('NEW')
print(new.shape)
print(new)
# Load as 255 RGB
grey = Image.fromarray(new)
grey.save('new_ro.jpg')
grey.show()
