#! /usr/bin/env python


import colorsys
import random
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
sns.set()


__date__ = '14 Dec 2016'
__email__ = 'f.asnicar@unitn.it'
__author__ = 'Francesco Asnicar'
__version__ = '0.02'


def scale_color(hsv, factor=1.0):
    """
    Takes as input a tuple that represents a color in HSV format, and optionally a scale factor.
    Return an RGB string that is the converted HSV color, scaled by the given factor.
    """
    h, s, v = hsv

    if (h < 0.) or (h > 360.):
        raise Exception('[scale_color()] Hue value out of range (0, 360): ' + str(h))

    if (s < 0.) or (s > 100.):
        raise Exception('[scale_color()] Saturation value out of range (0, 100): ' + str(s))

    if (v < 0.) or (v > 100.):
        raise Exception('[scale_color()] Value value out of range (0, 100): ' + str(v))
    if (factor < 0.) or (factor > 1.):
        raise Exception('[scale_color()] Factor value out of range (0.0, 1.0): ' + str(factor))

    v *= factor
    r, g, b = colorsys.hsv_to_rgb(h/360., s/100., v/100.)

    return '#{0:02x}{1:02x}{2:02x}'.format(int(round(r*255.)), int(round(g*255.)), int(round(b*255.)))


def get_palette(num_colors, my_seed=None):
    """
    """
    colorss = []
    step = 36.0

    random.seed(my_seed)

    if num_colors < 20:
        step = 360.0 / ((num_colors+1) / 2)

    hue = random.random()*360.0

    while len(colorss) < num_colors:
        if hue + step > 360.0:
            hue = random.random()*360.0

        colorss.append(scale_color((hue, 89.0, 100.0)))
        colorss.append(scale_color((hue, 100.0, 58.0)))
        hue += step

    random.shuffle(colorss)
    return colorss[:num_colors]


def print_palette(palette, output_filename):
    """
    """
    plot = sns.palplot(palette)
    plot.savefig(output_filename)
