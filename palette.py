from colorsys import hsv_to_rgb


__date__ = '26 May 2015'
__email__ = 'f.asnicar@unitn.it'
__author__ = 'Francesco Asnicar'
__version__ = '0.01'


def scale_color((h, s, v), factor=1.):
    """
    Takes as input a tuple that represents a color in HSV format, and optionally a scale factor.
    Return an RGB string that is the converted HSV color, scaled by the given factor.
    """
    if (h < 0.) or (h > 360.):
        raise Exception('[scale_color()] Hue value out of range (0, 360): ' + str(h))

    if (s < 0.) or (s > 100.):
        raise Exception('[scale_color()] Saturation value out of range (0, 100): ' + str(s))

    if (v < 0.) or (v > 100.):
        raise Exception('[scale_color()] Value value out of range (0, 100): ' + str(v))

    if (factor < 0.) or (factor > 1.):
        raise Exception('[scale_color()] Factor value out of range (0.0, 1.0): ' + str(factor))

    v *= factor
    r, g, b = hsv_to_rgb(h/360., s/100., v/100.)

    return '#{0:02x}{1:02x}{2:02x}'.format(int(round(r*255.)), int(round(g*255.)), int(round(b*255.)))


def get_palette(num_colors):
    """
    """
    colorss = []
    step = 33.

    if num_colors < 10:
        step = 360. / ((num_colors+1) / 2)

    hue = 10.
    nsteps = 1
    while len(colorss) < num_colors:
        if hue + step > 360.:
            nsteps += 1
            hue = (nsteps**3) + 10.

        colorss.append(scale_color((hue, 66., 99.)))
        colorss.append(scale_color((hue, 77., 45.)))
        hue += step

    return colorss[:num_colors]
