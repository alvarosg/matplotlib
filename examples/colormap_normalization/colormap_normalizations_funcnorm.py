"""
=====================================================================
Examples of normalization using  :class:`~matplotlib.colors.FuncNorm`
=====================================================================

This is an example on how to perform a normalization using an arbitrary
function with :class:`~matplotlib.colors.FuncNorm`. A logarithm normalization
and a square root normalization will be use as examples.

"""

import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt

import numpy as np


def main():
    fig, ((ax11, ax12),
          (ax21, ax22),
          (ax31, ax32)) = plt.subplots(3, 2, gridspec_kw={
                        'width_ratios': [1, 2]}, figsize=plt.figaspect(0.6))

    cax = make_plot(None, 'Regular linear scale', fig, ax11, ax12)
    fig.colorbar(cax, format='%.3g', ax=ax12)

    # Example of logarithm normalization using FuncNorm
    norm = colors.FuncNorm(f=np.log10,
                           finv=lambda x: 10.**(x), vmin=0.01)
    cax = make_plot(norm, 'Log normalization using FuncNorm', fig, ax21, ax22)
    fig.colorbar(cax, format='%.3g', ticks=cax.norm.ticks(5), ax=ax22)
    # The same can be achieved with
    # norm = colors.FuncNorm(f='log10', vmin=0.01)

    # Example of root normalization using FuncNorm
    norm = colors.FuncNorm(f=lambda x: x**0.5,
                           finv=lambda x: x**2, vmin=0.0)
    cax = make_plot(norm, 'Root normalization using FuncNorm', fig, ax31, ax32)
    fig.colorbar(cax, format='%.3g', ticks=cax.norm.ticks(5), ax=ax32)
    # The same can be achieved with
    # norm = colors.FuncNorm(f='sqrt', vmin=0.0)
    # or with
    # norm = colors.FuncNorm(f='root{2}', vmin=0.)

    fig.subplots_adjust(hspace=0.4, wspace=0.15)
    plt.show()


def make_plot(norm, label, fig, ax1, ax2):
    X, Y, data = get_data()
    cax = ax2.imshow(data, cmap=cm.gray, norm=norm)

    d_values = np.linspace(cax.norm.vmin, cax.norm.vmax, 100)
    cm_values = cax.norm(d_values)
    ax1.plot(d_values, cm_values)
    ax1.set_xlabel('Data values')
    ax1.set_ylabel('Colormap values')
    ax2.set_title(label)
    ax2.axes.get_xaxis().set_ticks([])
    ax2.axes.get_yaxis().set_ticks([])
    return cax


def get_data(_cache=[]):
    if len(_cache) > 0:
        return _cache[0]
    x = np.linspace(0, 1, 300)
    y = np.linspace(-1, 1, 90)
    X, Y = np.meshgrid(x, y)

    data = np.zeros(X.shape)

    def gauss2d(x, y, a0, x0, y0, wx, wy):
        return a0 * np.exp(-(x - x0)**2 / wx**2 - (y - y0)**2 / wy**2)
    N = 15
    for x in np.linspace(0., 1, N):
        data += gauss2d(X, Y, x, x, 0, 0.25/N, 0.25)

    data = data - data.min()
    data = data / data.max()
    _cache.append((X, Y, data))

    return _cache[0]

main()
