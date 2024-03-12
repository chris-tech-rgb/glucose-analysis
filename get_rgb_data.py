"""Get RGB From Images

This script get RGB values from images in folder 'training data'.
And then, save these data in 'training data.csv'.

The script remove the background of an image before geting the average RGB values of it.
The comprison of processed images and their RGB values is shown as a figure.
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

def comparison(imgs):
  """Display the comparison of processed images and their the RGB values."""
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
  concentrations = np.array([float(i.split('mM')[0]) for i in image_names])
  rgb = []
  for i in image_names:
    rgb.append(get_rgb(imgs[i]))
  # Plots of R
  red = np.array([i[0] for i in rgb])
  p1 = axes[1, 0].plot(concentrations, red, color="lightcoral", marker="o")
  # Plots of G
  green = np.array([i[1] for i in rgb])
  p2 = axes[1, 0].plot(concentrations, green, color="yellowgreen", marker="D")
  # Plots of B
  blue = np.array([i[2] for i in rgb])
  p3 = axes[1, 0].plot(concentrations, blue, color="cornflowerblue", marker="s")
  # Show RGB values
  for a, b in zip(concentrations, red):
    axes[1, 0].text(a, b, str("{:.2f}".format(b)), color="lightcoral")
  for a, b in zip(concentrations, green):
    axes[1, 0].text(a, b, str("{:.2f}".format(b)), color="yellowgreen")
  for a, b in zip(concentrations, blue):
    axes[1, 0].text(a, b, str("{:.2f}".format(b)), color="cornflowerblue")
  # Add legends
  axes[1, 0].legend((p1[0], p2[0], p3[0]), ("R", "G", "B"), loc='center left', bbox_to_anchor=(1, 0.5))
  plt.show()
  # Save data
  with open('training data.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(concentrations)
    writer.writerow(["{:.2f}".format(i[0]) for i in rgb])
    writer.writerow(["{:.2f}".format(i[1]) for i in rgb])
    writer.writerow(["{:.2f}".format(i[2]) for i in rgb])

def main():
  image_dict = load_images('training data')
  comparison(image_dict)


if __name__ == "__main__":
    main()
