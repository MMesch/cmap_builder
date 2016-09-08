#!/usr/bin/env python

"""Simple example for the colormap2d script."""

import numpy as np
import matplotlib.pyplot as plt
from colormap2d import imshow2d

# generate complex input data
npts_real = 400
npts_imag = 400
realaxis = np.linspace(-4, 4, npts_real)
imagaxis = np.linspace(-3, 3, npts_imag)
regrid, imgrid = np.meshgrid(realaxis, imagaxis)

zgrid = regrid + 1j * imgrid
complex_function = (zgrid ** 2 - 2.) * (zgrid - 1 - 1j) ** 2 /\
                   (zgrid + 2j) / (zgrid**2 - 5 - 2j)

# assemble [2, nwidth, nheight] array
data = np.empty((2, npts_imag, npts_real))
data[1] = np.log(np.abs(complex_function))
data[0] = np.angle(complex_function)

# plot to screen
imshow2d(data, cmap2d='wheel')
plt.show()
