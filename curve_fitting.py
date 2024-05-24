"""Curve Fitting

Get the relationship between pH and RGB values.
Save the fitting function in 'fitting function.csv'.
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
popt, pcov = curve_fit(func, rgb_values, pH_values, maxfev = 200000)
a, n1, b, n2, c, n3 = popt
print("Fitting function:\nConcentration = " + str(a) + " x R^(" + str(n1) + ") + " + str(b) + " x G^(" + str(n2) + ") + " + str(c) + " x B^(" + str(n3) + ")")

# Fitting
r_fit = np.linspace(min(r_values), max(r_values), 30)
g_fit = np.linspace(min(g_values), max(g_values), 30)
b_fit = np.linspace(min(b_values), max(b_values), 30)
R, G, B = np.meshgrid(r_fit, g_fit, b_fit)
pH = a * R**n1 + b * G**n2 + c * B**n3

# Save result
with open('fitting function.csv', 'w') as f:
  writer = csv.writer(f)
  writer.writerow(popt)