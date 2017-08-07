import matplotlib
import numpy as np
from scipy.ndimage import uniform_filter

def extract_features(imgs, feature_fns, verbose=False):
  """
  Given pixel data for images and several feature functions that can operate on
  single images, apply all feature functions to all images, concatenating the
  feature vectors for each image and storing the features for all images in
  a single matrix.

  Inputs:
  - imgs: N x H x W x C array of pixel data for N images.
  - feature_fns: List of k feature functions. The ith feature function should
    take as input an H x W x D array and return a (one-dimensional) array of
    length F_i.
  - verbose: Boolean; if true, print progress.

  Returns:
  An array of shape (N, F_1 + ... + F_k) where each column is the concatenation
  of all features for a single image.
  """
  num_images = imgs.shape[0]
  if num_images == 0:
    return np.array([])

  # Use the first image to determine feature dimensions
  feature_dims = []
  first_image_features = []
  for feature_fn in feature_fns:
    feats = feature_fn(imgs[0].squeeze()) # (144,) for hog_feature, (10,) for color_histogram_hsv
    # numpy.squeeze() : Remove single-dimensional entries from the shape of an array
    assert len(feats.shape) == 1, 'Feature functions must be one-dimensional'
    feature_dims.append(feats.size)
    first_image_features.append(feats)

  # Now that we know the dimensions of the features, we can allocate a single
  # big array to store all features as columns.
  total_feature_dim = sum(feature_dims)
  imgs_features = np.zeros((num_images, total_feature_dim))
  imgs_features[0] = np.hstack(first_image_features).T

  # Extract features for the rest of the images.
  for i in xrange(1, num_images):
    idx = 0
    for feature_fn, feature_dim in zip(feature_fns, feature_dims):
      next_idx = idx + feature_dim
      imgs_features[i, idx:next_idx] = feature_fn(imgs[i].squeeze())
      idx = next_idx
    if verbose and i % 1000 == 0:
      print 'Done extracting features for %d / %d images' % (i, num_images)

  return imgs_features


def rgb2gray(rgb):
  """Convert RGB image to grayscale

    Parameters:
      rgb : RGB image

    Returns:
      gray : grayscale image

  """
  return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])


def hog_feature(im):
  """Compute Histogram of Gradient (HOG) feature for an image

       Modified from skimage.feature.hog
       http://pydoc.net/Python/scikits-image/0.4.2/skimage.feature.hog

     Reference:
       Histograms of Oriented Gradients for Human Detection
       Navneet Dalal and Bill Triggs, CVPR 2005

    Parameters:
      im : an input grayscale or rgb image

    Returns:
      feat: Histogram of Gradient (HOG) feature

  """

  # convert rgb to grayscale if needed
  if im.ndim == 3:
    image = rgb2gray(im)
  else:
    image = np.at_least_2d(im)

  sx, sy = image.shape # image size # 32, 32
  orientations = 9 # number of gradient bins
  cx, cy = (8, 8) # pixels per cell

  gx = np.zeros(image.shape) # (32,32)
  gy = np.zeros(image.shape) # (32,32)
  gx[:, :-1] = np.diff(image, n=1, axis=1) # compute gradient on x-direction
  gy[:-1, :] = np.diff(image, n=1, axis=0) # compute gradient on y-direction
  grad_mag = np.sqrt(gx ** 2 + gy ** 2) # gradient magnitude
  grad_ori = np.arctan2(gy, (gx + 1e-15)) * (180 / np.pi) + 90 # gradient orientation

  n_cellsx = int(np.floor(sx / cx))  # number of cells in x # 4
  n_cellsy = int(np.floor(sy / cy))  # number of cells in y # 4
  # compute orientations integral images
  orientation_histogram = np.zeros((n_cellsx, n_cellsy, orientations)) # (4,4,9)
  for i in range(orientations):
    # create new integral image for this orientation
    # isolate orientations in this range
    temp_ori = np.where(grad_ori < 180 / orientations * (i + 1),
                        grad_ori, 0)
    temp_ori = np.where(grad_ori >= 180 / orientations * i,
                        temp_ori, 0)
    # select magnitudes for those orientations
    cond2 = temp_ori > 0
    temp_mag = np.where(cond2, grad_mag, 0)
    orientation_histogram[:,:,i] = uniform_filter(temp_mag, size=(cx, cy))[cx/2::cx, cy/2::cy].T
    # print orientation_histogram[0,0,0]

  return orientation_histogram.ravel() # (144,)


def color_histogram_hsv(im, nbin=10, xmin=0, xmax=255, normalized=True):
  """
  Compute color histogram for an image using hue.

  Inputs:
  - im: H x W x C array of pixel data for an RGB image.
  - nbin: Number of histogram bins. (default: 10)
  - xmin: Minimum pixel value (default: 0)
  - xmax: Maximum pixel value (default: 255)
  - normalized: Whether to normalize the histogram (default: True)

  Returns:
    1D vector of length nbin giving the color histogram over the hue of the
    input image.
  """
  ndim = im.ndim # 3, im's shape is (32, 32, 3)
  bins = np.linspace(xmin, xmax, nbin+1) # (11,)
  
  hsv = matplotlib.colors.rgb_to_hsv(im/xmax) * xmax # (32, 32, 3)
  # (Andy) We divide im by 255 because im is between 0 and 255, and hsv should be between 0 and 1. 
  # (Andy) Finally we revert it by multiplying 255 again.
  # (Andy) http://www.rapidtables.com/convert/color/rgb-to-hsv.htm
  # (Andy) http://matplotlib.org/api/colors_api.html#matplotlib.colors.rgb_to_hsv
  
  imhist, bin_edges = np.histogram(hsv[:,:,0], bins=bins, density=normalized)
  # https://docs.scipy.org/doc/numpy/reference/generated/numpy.histogram.html
  # print imhist.shape # (10,)
  # print bin_edges.shape # (11,)
  
  imhist = imhist * np.diff(bin_edges)
  # https://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.diff.html

  # return histogram
  return imhist # (10,)

pass
