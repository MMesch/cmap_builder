#!/usr/bin/env python
"""2d colormap obspy."""

import numpy as np
import matplotlib.pyplot as plt

from colormap2d import imshow2d
import obspy
from obspy.signal.tf_misfit import cwt


tr = obspy.read()[0]
f_min, f_max = 1, 50

scalogram = cwt(tr.data, tr.stats.delta, 8, f_min, f_max)
huelight = np.array([np.angle(scalogram), np.abs(scalogram)])

imshow2d(huelight, cmap2d='brightwheel', origin='lower', aspect='auto')
plt.show()
