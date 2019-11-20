# input: intensity image (2D array of ints)
from PIL import Image
import numpy as np
from matplotlib import image
import matplotlib.pyplot as plt

# Load greyscale image as intensity array
image = (Image.open('new_ro.jpg'))
new = np.asarray(image)
#print(new.shape)
dims = new.shape
print('\nIntensity array:')
print(new)

# Make intensity histogram
intensity, count = np.unique(new, return_counts=True)
histo = dict(zip(intensity, count))
#print('\nIntensity histogram:')
#print(histo)

# Do the otsu boogie
# For each intensity value as threshold
# Calculate "intra-class variance"
# Keep the maximum one

max_t = 0
max_sig_sq = 0
# Total pixels (could also get this from the image)
hist_count = sum(histo.values())
#print(hist_count)

for t in range(0, 256):
    #print('\nThreshold at ', t)
    # Find weight and mean of background
    # Total background frequencies
    b_count = 0
    # Pixel vals * frequencies
    b_numer = 0
    for i in range(0, t):
        # Handle case when intensity not found
        try:
            b_count += histo[i]
            b_numer += (i * histo[i])
        except:
            b_count += 0
            b_numer += 0
        #print('\nb_count: ', b_count)
    b_weight = b_count / hist_count
    if b_count > 0:
        b_mean = b_numer / b_count
    else:
        #print('\nNo mean due to "divide by 0" error')
        b_mean = 0
    #print('\nb_weight: ', b_weight)
    #print('\nb_mean: ', b_mean)

    # Find weight of foreground
    # Total foreground frequencies
    f_count = 0
    # Pixel vals * frequencies
    f_numer = 0
    for j in range(t, 256):
        # Handle case when intensity not found
        try:
            f_count += histo[j]
            f_numer += (j * histo[j])
        except:
            f_count += 0
            f_numer += 0
        #print('\nf_count: ', f_count)
    f_weight = f_count / hist_count
    if f_count > 0:
        f_mean = f_numer / f_count
    else:
        #print('\nNo mean due to "divide by 0" error')
        f_mean = 0
    #print('\nf_weight: ', f_weight)
    #print('\nf_mean: ', f_mean)

    # Find sigma squared
    sig_sq = b_weight * f_weight * ((b_mean - f_mean)**2)
    #print('\nSigma squared: ', sig_sq)
    # Set the max sigma and corresponding threshold
    if sig_sq > max_sig_sq:
        max_sig_sq = sig_sq
        max_t = t
print('\nMax intra-class variance is for threshold ', max_t)

# Apply thresholding
# All pixels with intensity less than threshold become 0
# All pixels with intensity greater than threshold become 1
otsu = np.copy(new)
#print(dims[0])

for row in range(0, dims[0]):
    for col in range(0, dims[1]):
        pix = otsu[row, col]
        if pix < max_t:
            otsu[row, col] = 0
        else:
            otsu[row, col] = 255
print(otsu)
binary = Image.fromarray(otsu)
binary.save('bin_row.jpg')
binary.show()
    #for pix in row:
        #print(otsu[row, pix])
#print(otsu)

# Histogram chart for visual aid
#plt.bar(histo.keys(), histo.values(), color='b')
#plt.show()
