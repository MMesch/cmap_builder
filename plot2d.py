#!/usr/bin/env python
"""
This script demonstrates how to use matplotlib for 2d or 3d colormaps
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.ndimage.interpolation import map_coordinates


def main():
    # some parameters
    npts_real = 200
    npts_imag = 100
    realaxis = np.linspace(-2 * np.pi, 2 * np.pi, npts_real)
    imagaxis = np.linspace(-1., 1., npts_imag)
    regrid, imgrid = np.meshgrid(realaxis, imagaxis)

    # put complex magnitude and argument in 2d array
    complex_sine = np.sin(regrid + 1j * imgrid)
    data = np.empty((2, npts_imag, npts_real))
    data[0] = np.abs(complex_sine)
    data[1] = np.angle(complex_sine)

    # normalize array
    norm0 = plt.Normalize(0, data[0].max())
    norm1 = plt.Normalize(-np.pi, np.pi)
    data[0] = norm0(data[0])
    data[1] = norm1(data[1])

    fig, axes = plt.subplots(3, 2, figsize=(15, 10))

    # black CAM02 colormap
    ax00, ax01 = axes[0, 0], axes[0, 1]
    ax00.set(title='CAM02-USC colormap (black)')
    ax01.set(title='complex sine (magnitude=luminosity, argument=hue)')

    cmap = np.load('orbit2d_black.npy')
    rgb_colors = cmap_file2d(data, cmap)
    ax00.imshow(cmap, aspect='auto')
    ax01.imshow(rgb_colors, aspect='auto')

    # white CAMO2 colormap
    ax10, ax11 = axes[1, 0], axes[1, 1]
    ax10.set(title='CAM02-USC colormap (white)')
    ax11.set(title='complex sine (magnitude=luminosity, argument=hue)')

    cmap = np.load('orbit2d_white.npy')
    rgb_colors = cmap_file2d(data, cmap)
    ax10.imshow(cmap, aspect='auto')
    ax11.imshow(rgb_colors, aspect='auto')

    # hsv colormap
    ax20, ax21 = axes[2, 0], axes[2, 1]
    ax20.set(title='HSV colormap')
    ax21.set(title='complex sine (magnitude=luminosity, argument=hue)')

    xx, yy = np.meshgrid(np.linspace(0., 1., 100), np.linspace(0., 1., 100))
    cmap_grid = np.array([yy, xx])
    cmap = cmap_multidim_hsv(cmap_grid)
    cmap = np.roll(cmap, 48, axis=1)
    rgb_colors = cmap_file2d(data, cmap)
    ax20.imshow(cmap, aspect='auto')
    ax21.imshow(rgb_colors, aspect='auto')

    fig.tight_layout(pad=0.5)
    plt.show()


def cmap_multidim_hsv(data, mapping={'sat': 0, 'hue': 1, 'val': 0}):
    ihue = mapping['hue']
    if isinstance(ihue, basestring):
        fill_value = float(ihue.strip('_fill'))
        hue = np.ones_like(data[0]) * fill_value
    else:
        hue = data[ihue]
    isat = mapping['sat']
    if isinstance(isat, basestring):
        fill_value = float(isat.strip('_fill'))
        sat = np.ones_like(data[0]) * fill_value
    else:
        sat = data[isat]
    ival = mapping['val']
    if isinstance(ival, basestring):
        fill_value = float(ival.strip('_fill'))
        val = np.ones_like(data[0]) * fill_value
    else:
        val = data[ival]

    hsvcolors = np.array([hue, sat, val]).T
    rgb = mpl.colors.hsv_to_rgb(hsvcolors).transpose((1, 0, 2))
    return rgb


def cmap_file2d(data, cmap):
    data_dim, nrows, ncols = data.shape
    data2 = np.copy(data)
    data2[1] = (data2[1] - 0.45) % 1.0
    data2 = data2.reshape(data_dim, nrows, ncols)
    r = map_coordinates(cmap[:, :, 0], data2 * 100., order=1, mode='nearest')
    g = map_coordinates(cmap[:, :, 1], data2 * 100., order=1, mode='nearest')
    b = map_coordinates(cmap[:, :, 2], data2 * 100., order=1, mode='nearest')
    rgb = np.array([r, g, b])
    rgb = rgb.reshape(3, nrows, ncols).transpose(1, 2, 0)

    return rgb


if __name__ == "__main__":
    main()
