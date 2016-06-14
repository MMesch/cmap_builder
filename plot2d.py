#!/usr/bin/env python
"""
This script demonstrates how to use matplotlib for 2d or 3d colormaps
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import glob
import os
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

    paths_cmap = glob.glob('colormaps/*.npy')
    ncmaps = len(paths_cmap) + 1  # one extra cmap for hsv
    fig, axes = plt.subplots(ncmaps, 2, figsize=(10, ncmaps * 3))
    for path_cmap, (col1, col2) in zip(paths_cmap, axes):
        dirname, fname = os.path.split(path_cmap)
        cmap = np.load(path_cmap).transpose((1, 0, 2))
        #ihalf = int(cmap.shape[0] * 0.5)
        #cmap = cmap[::-1]
        #cmap = cmap[:ihalf]
        col1.set(title='{}'.format(fname))
        col2.set(title='complex sine')

        rgb_colors = cmap_file2d(data, cmap)

        col1.imshow(cmap, aspect='auto')
        col2.imshow(rgb_colors, aspect='auto')

    # hsv colormap
    ax20, ax21 = axes[-1, 0], axes[-1, 1]
    ax20.set(title='HSV colormap')
    ax21.set(title='complex sine')

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

    hsvcolors = np.array([(-hue + 0.4) % 1.0, sat, val]).T
    rgb = mpl.colors.hsv_to_rgb(hsvcolors).transpose((1, 0, 2))
    return rgb


def cmap_file2d(data, cmap, roll_x=0.):
    cmap[:, -1] = cmap[:, 0]
    data_dim, nrows, ncols = data.shape
    data2 = np.copy(data)
    #data2[1] = (data2[1] - roll_x) % 1.0
    data2[0] *= cmap.shape[0]
    data2[1] *= cmap.shape[1]
    plt.figure()
    plt.imshow(cmap)
    data2 = data2.reshape(data_dim, nrows, ncols)
    r = map_coordinates(cmap[:, :, 0], data2, order=1, mode='nearest')
    g = map_coordinates(cmap[:, :, 1], data2, order=1, mode='nearest')
    b = map_coordinates(cmap[:, :, 2], data2, order=1, mode='nearest')
    rgb = np.array([r, g, b])
    rgb = rgb.reshape(3, nrows, ncols).transpose(1, 2, 0)

    return rgb


if __name__ == "__main__":
    main()
