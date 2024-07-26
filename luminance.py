"""Get Luminance From Images
"""
import math
import numpy as np
import os
import pandas as pd
import skimage as ski
from natsort import natsorted


def load_images(folder_name):
  """Load images in the folder."""
  folder_path = os.path.join(os.getcwd(), folder_name)
  list_files = os.listdir(folder_path)
  list_files = natsorted(list_files)
  image_dict = {}
  for filename in list_files:
    file_path = os.path.join(folder_path, filename)
    image_dict[filename] = ski.io.imread(file_path)
  return image_dict

def get_rgb(img):
  """Get the average RGB of an image."""
  # Create a mask for white regions
  white_mask = np.all(img == [255, 255, 255], axis=-1)
  # Invert the mask to select non-white regions
  non_white_mask = ~white_mask
  # Extract non-white pixels from the image
  non_white_pixels = img[non_white_mask]
  # Calculate the average RGB values for non-white regions
  average_rgb = np.mean(non_white_pixels, axis=0)
  return average_rgb

def get_data(imgs):
  # Count number
  number = len(imgs)
  if number < 1:
    return
  # Remove background
  image_names = list(imgs.keys())
  concentrations = np.array([float(i.split('mM')[0]) for i in image_names])
  rgb = []
  for i in image_names:
    rgb.append(get_rgb(imgs[i]))
  # Save data
  luminance = [(0.299*i[0] + 0.587*i[1] + 0.114*i[2]) for i in rgb]
  log = [math.log1p(i) for i in luminance]
  df = pd.DataFrame([[a] + ["{:.2f}".format(b)] + ["{:.2f}".format(c)] for a, b, c in zip(concentrations, luminance, log)],
                    columns=['Concentration (mM)', 'Luminance', 'Logarithmic luminance'])
  df.to_excel("excel/luminance.xlsx", index=False)

def main():
  image_dict = load_images('calibration curve')
  get_data(image_dict)


if __name__ == "__main__":
    main()