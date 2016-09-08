#!/usr/bin/env python

"""Simple example for the colormap2d script."""

import numpy as np
import matplotlib.pyplot as plt
from colormap2d import imshow2d

# complex input data
x = np.linspace(-5, 5, 100)
regrid, imgrid = np.meshgrid(x, x)
zgrid = regrid + 1j * imgrid

complex_function = (zgrid ** 2 - 2.) * (zgrid - 1 - 1j) ** 2 /\
                   (zgrid + 2j) / (zgrid**2 - 5 - 2j)


# assemble [2, nwidth, nheight] array
data = np.array([np.angle(complex_function),
                 np.log(np.abs(complex_function))])

# plot to screen
imshow2d(data, cmap2d='wheel')
plt.show()
