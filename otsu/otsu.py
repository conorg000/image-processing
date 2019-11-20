from PIL import Image
import numpy as np
from matplotlib import image
import matplotlib.pyplot as plt

def otsu_thresh(intense_array):
    """Converts greyscale array to binary image using Otsu thresholding

    Args:
        intense_array (2d numpy array): The greyscale image as an intensity array

    Returns:
        otsu (2d numpy array): The resulting image as a binary array
    """
    # Get dimensions of array
    dims = intense_array.shape
    print('\nIntensity array:')
    print(intense_array)
    # Make intensity histogram (in dictionary)
    intensity, count = np.unique(intense_array, return_counts=True)
    histo = dict(zip(intensity, count))
    #print('\nIntensity histogram:')
    #print(histo)

    # Otsu's technique
    # For each intensity value as threshold
    # Calculate "intra-class variance" (sigma squared)
    # Keep the threshold which gives maximum intra-class variance

    # Initialise maximum threshold
    max_t = 0
    # Initialise maximum sigma squared
    max_sig_sq = 0
    # Total pixels (could also get this from the image array)
    hist_count = sum(histo.values())
    # Loop through different threshold values
    # Calculate sigma squared each time
    for t in range(0, 256):
        # Total background frequencies
        b_count = 0
        # Pixel vals * frequencies
        b_numer = 0
        # Find weight and mean of background
        for i in range(0, t):
            # Handle case when intensity not found
            try:
                # Increase total sum of intensity frequencies
                b_count += histo[i]
                # Increase total sum of pixel values for the mean
                b_numer += (i * histo[i])
            except:
                # Otherwise add nothing
                b_count += 0
                b_numer += 0
            #print('\nb_count: ', b_count)
        # Background weight
        b_weight = b_count / hist_count
        # Background mean
        # Handle "divide by 0" error
        if b_count > 0:
            b_mean = b_numer / b_count
        else:
            #print('\nNo mean due to "divide by 0" error')
            b_mean = 0

        # Total foreground frequencies
        f_count = 0
        # Pixel vals * frequencies
        f_numer = 0
        # Find weight and mean of foreground
        for j in range(t, 256):
            # Handle case when intensity not found
            try:
                # Increase total sum of intensity frequencies
                f_count += histo[j]
                # Increase total sum of pixel values for the mean
                f_numer += (j * histo[j])
            except:
                # Otherwise add nothing
                f_count += 0
                f_numer += 0
        # Foreground weight
        f_weight = f_count / hist_count
        # Foreground mean
        # Handle "divide by 0" error
        if f_count > 0:
            f_mean = f_numer / f_count
        else:
            #print('\nNo mean due to "divide by 0" error')
            f_mean = 0

        # Calculate sigma squared
        sig_sq = b_weight * f_weight * ((b_mean - f_mean)**2)
        #print('\nSigma squared: ', sig_sq)
        # Set the max sigma and corresponding threshold
        if sig_sq > max_sig_sq:
            max_sig_sq = sig_sq
            max_t = t
    print('\nMax intra-class variance is for threshold', max_t)

    # Apply thresholding with max_t
    # All pixels with intensity less than max_t become 0
    # All pixels with intensity greater than or equal to max_t become 255
    # PIL Image array is read-only, so we copy it into a new array
    otsu = np.copy(intense_array)
    # Loop through each pixel, adjusting as necessary
    for row in range(0, dims[0]):
        for col in range(0, dims[1]):
            pix = otsu[row, col]
            if pix < max_t:
                otsu[row, col] = 0
            else:
                otsu[row, col] = 255
    print('\nBinary array:')
    print(otsu)
    return otsu

# Load greyscale image as intensity array
source = input('Enter filename of greyscale jpg: ')
image = (Image.open(source))
new = np.asarray(image)
# Apply otsu's technique
# Get binary array
target = otsu_thresh(new)
# Save the array as an image
binary = Image.fromarray(target)
binary.save('otsu_result.jpg')
binary.show()
