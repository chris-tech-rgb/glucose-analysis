"""Curve Fitting

Get the relationship between pH and RGB values.
Save the curve function in 'fitting curve.csv'.
Show this relationship as a colorbar figure.
"""
import csv
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np

# Fitting function
def func(rgb, a, n1, b, n2, c, n3):
    return a * rgb[:, 0]**n1 + b * rgb[:, 1]**n2 + c * rgb[:, 2]**n3

# Experimental data points
with open('training data.csv') as f:
    reader = csv.reader(f)
    rows = [row for row in reader]
pH_values = np.array(rows[0])
rgb_values = np.array([list(t) for t in list(zip([float(i) for i in rows[2]], [float(i) for i in rows[4]], [float(i) for i in rows[6]]))])
r_values = rgb_values[:, 0]
g_values = rgb_values[:, 1]
b_values = rgb_values[:, 2]

# Perform the curve-fit
popt, pcov = curve_fit(func, rgb_values, pH_values, maxfev = 20000)
a, n1, b, n2, c, n3 = popt
print("Fitting function:\npH = " + str(a) + " x R^(" + str(n1) + ") + " + str(b) + " x G^(" + str(n2) + ") + " + str(c) + " x B^(" + str(n3) + ")")

# Create figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Fitting
r_fit = np.linspace(min(r_values), max(r_values), 30)
g_fit = np.linspace(min(g_values), max(g_values), 30)
b_fit = np.linspace(min(b_values), max(b_values), 30)
R, G, B = np.meshgrid(r_fit, g_fit, b_fit)
pH = a * R**n1 + b * G**n2 + c * B**n3

# Scatter plot
img = ax.scatter(R, G, B, c=pH, cmap='viridis_r')

# Colorbar
colorbar = fig.colorbar(img, location='left')  # Set position to 'left'
colorbar.set_label('pH')

# Set labels
ax.set_xlabel('R')
ax.set_ylabel('G')
ax.set_zlabel('B')
# Color of labels
ax.xaxis.label.set_color('red')
ax.yaxis.label.set_color('green')
ax.zaxis.label.set_color('blue')
# Color of axes
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='green')
ax.tick_params(axis='z', colors='blue')
# Show figure
plt.show()

# Save result
with open('fitting curve.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(popt)