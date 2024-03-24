import matplotlib.pyplot as plt
import numpy as np
import os
import re
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
  normalized_rgb = [i*100/255 for i in average_rgb]
  return normalized_rgb

def comparison(imgs):
  """Display the result of comparison and the RGB value of each one."""
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
    axes[0, i].set_title(image_names[i][:-4])
  axes[1, 0] = fig.add_subplot(2, 1, 2)
  # Show RGB values
  time = np.array([int(re.findall(r'\d+', i)[0]) for i in image_names])
  rgb = []
  for i in image_names:
    color = get_rgb(imgs[i])
    rgb.append(color)
  # Plots and errorbars of R
  red = np.array([i[0] for i in rgb])
  p1 = axes[1, 0].plot(time, red, color="lightcoral", marker="o")
  # Plots and errorbars of G
  green = np.array([i[1] for i in rgb])
  p2 = axes[1, 0].plot(time, green, color="yellowgreen", marker="D")
  # Plots and errorbars of B
  blue = np.array([i[2] for i in rgb])
  p3 = axes[1, 0].plot(time, blue, color="cornflowerblue", marker="s")
  # Add legends
  axes[1, 0].legend((p1[0], p2[0], p3[0]), ("R", "G", "B"), loc='center right')
  # axis label
  axes[1, 0].set_ylabel('Percentage of RGB color (%)')
  axes[1, 0].set_xlabel('Time (h)')
  plt.ylim(0, 100)
  plt.show()

def main():
  image_dict = load_images('0.1mM 6h')
  comparison(image_dict)


if __name__ == "__main__":
    main()
