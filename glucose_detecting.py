"""
This script get RGB values from images in a specific folder.
And then, calculate the glucose concentrations according to the fitting function and RGB values of images.
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import os
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

def average_rgb(img):
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

def fitting_function(rgb):
  """A fitting function of the relationship between concentration and RGB."""
  with open('fitting function.csv') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]
  popt = [float(i) for i in rows[0]]
  return popt[0] * rgb[0]**popt[1] + popt[2] * rgb[1]**popt[3] + popt[4] * rgb[2]**popt[5]

def concentration(imgs):
  """Display the result."""
  # Count number
  number = len(imgs)
  if number < 1:
    return
  # Remove background
  image_names = list(imgs.keys())
  # Display images
  fig = plt.figure(figsize=(8, 8))
  axes = np.zeros((2, number), dtype=object)
  for i in range(0, number):
    axes[0, i] = fig.add_subplot(2, number, 1+i)
    axes[0, i].axis("off")
    axes[0, i].imshow(imgs[image_names[i]])
    axes[0, i].set_title(image_names[i].split('mM')[0])
  axes[1, 0] = fig.add_subplot(2, 1, 2)
  # Show RGB values
  rgb = []
  for i in image_names:
    rgb.append(average_rgb(imgs[i]))
  # Show values of R
  red = np.array([i[0] for i in rgb])
  p1 = axes[1, 0].plot(range(0, number), red, color="lightcoral", marker=".", linestyle=":")
  # Show values of G
  green = np.array([i[1] for i in rgb])
  p2 = axes[1, 0].plot(range(0, number), green, color="yellowgreen", marker="x", linestyle=":")
  # Show values of B
  blue = np.array([i[2] for i in rgb])
  p3 = axes[1, 0].plot(range(0, number), blue, color="blue", marker="+", linestyle=":")
  # Hide x axis
  axes[1, 0].axes.get_xaxis().set_visible(False)
  # Y label
  axes[1, 0].set_ylabel('RGB')
  # Show predicted value of pH
  axe_ph = axes[1, 0].twinx()
  axe_ph.set_ylabel('Concentration (mM)')
  pH = [fitting_function(i) for i in rgb]
  axe_ph.plot(range(0, number), pH, color="purple", marker="o")
  for a, b in zip(range(0, number), pH):
    axe_ph.text(a, b + 0.25, str("{:.2f}".format(b)), color="purple")
  # Add legends
  axes[1, 0].legend((p1[0], p2[0], p3[0]), ("R", "G", "B"), loc='upper center', bbox_to_anchor=(0.05, 1.3))
  plt.show()

def main():
  image_dict = load_images('training data')
  concentration(image_dict)


if __name__ == "__main__":
    main()