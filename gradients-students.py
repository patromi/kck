#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('TkAgg')  # Set interactive backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from matplotlib import colors

def plot_color_gradients(gradients, names):
    # Disable LaTeX to avoid missing package errors
    matplotlib.rcParams['text.usetex'] = False
    rc('font', family='serif', size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    plt.show()
import colorsys
def hsv2rgb(h, s, v):
    return (h, s, v)

def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    if v < 0.5:
        # green to blue
        return (0, 1 - 2*v, 2*v)
    else:
        #blue to red
        return (2*(v-0.5), 0 , 1 - 2*(v-0.5))
def gradient_rgb_gbr_full(v):
    if v < 0.25:
        return (0, 1, 4*v)
    elif v < 0.5:
        return (0, 1 - (4 * (v - 0.25)), 1)
    elif v < 0.75:
        return (4*(v - 0.5), 0, 1)
    else:
        return (1, 0, 1 - 4*(v - 0.75))



def gradient_rgb_wb_custom(v):
    if v < 1 / 7:
        return (1, 1 - (7 * v), 1)
    elif v < 2 / 7:
        return (1 - (7 * (v - 1 / 7)), 0, 1)
    elif v < 3 / 7:
        return (0, (7 * (v - 2 / 7)), 1)

    elif v < 4 / 7:
        return (0, 1, 1 - (7 * (v - 3 / 7)))
    elif v < 5 / 7:
        return ((7 * (v - 4 / 7), 1, 0))

    elif v < 6 / 7:
        return (1, 1 - 7 * (v - 5 / 7), 0)
    else:
        return 1 - 7 * (v - 6 / 7), 0, 0


def gradient_hsv_bw(v):
    """Black-to-white gradient in HSV space."""
    return hsv2rgb(0, 0, v)

def gradient_hsv_gbr(v):
    """Green-blue-red gradient in HSV space."""
    if v < 0.5:
        h = 1/3 + (v/0.5) * (1/3)  # Green to Blue
    else:
        h = 2/3 + ((v-0.5)/0.5) * (1/3)  # Blue to Red
    return hsv2rgb(h, 1.0, 1.0)

def gradient_hsv_unknown(v):
    """Unknown gradient using HSV space."""
    return hsv2rgb(0.6, v, 1.0-0.3*v)

def gradient_hsv_custom(v):
    """Custom rainbow gradient in HSV space."""
    return hsv2rgb(v, 0.8, 0.9)

if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
