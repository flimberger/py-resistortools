'''This module contains logic to decode electrical color codes of resistors
'''

import enum
import math


class InvalidColorCodeException(Exception):
    '''Signals an invalid color code
    '''

    def __init__(self, message, color_code):
        super().__init__(message)
        self.color_code = color_code


class ColorCode(enum.Enum):
    '''Possible colors for resistor color bands
    '''

    black = 0
    brown = 1
    red = 2
    orange = 3
    yellow = 4
    green = 5
    blue = 6
    violet = 7
    gray = 8
    white = 9
    gold = 10
    silver = 11


class Resistor:
    '''Represent resistor characteristics
    '''

    def __init__(self, value, tolerance):
        self.value = value
        self.tolerance = tolerance

    def __eq__(self, other):
        return (self.value == other.value and
                math.isclose(self.tolerance, other.tolerance))

    def __repr__(self):
        return 'Resistor({}, {})'.format(self.value, self.tolerance)

    def __str__(self):
        display_value = self.value
        unit_prefix = ''
        # Calculate iso prefixes
        if display_value % _ISO_G == 0:
            display_value = int(display_value / _ISO_G)
            unit_prefix = 'G'
        elif display_value % _ISO_M == 0:
            display_value = int(display_value / _ISO_M)
            unit_prefix = 'M'
        elif display_value % _ISO_K == 0:
            display_value = int(display_value / _ISO_K)
            unit_prefix = 'k'

        return '{} {}Ω {} %'.format(display_value, unit_prefix, self.tolerance)


_ISO_G = 10 ** 9
_ISO_M = 10 ** 6
_ISO_K = 10 ** 3

_FIGURE = 0
_MULTIPLICATOR = 1
_TOLERANCE = 2

# Figure, Multiplier (10^x), Tolerance (%)
_RESISTOR_TABLE = {
    ColorCode.black:  (0,     0, None),
    ColorCode.brown:  (1,     1,  1.0),
    ColorCode.red:    (2,     2,  2.0),
    ColorCode.orange: (3,     3, None),
    ColorCode.yellow: (4,     4, None),
    ColorCode.green:  (5,     5,  0.5),
    ColorCode.blue:   (6,     6,  0.25),
    ColorCode.violet: (7,     7,  0.1),
    ColorCode.gray:   (8,     8,  0.05),
    ColorCode.white:  (9,     9, None),
    ColorCode.gold:   (None, -1,  5.0),
    ColorCode.silver: (None, -2, 10.0)
}


def _get_figure(color):
    figure = _RESISTOR_TABLE[color][_FIGURE]
    if figure is None:
        raise InvalidColorCodeException(''.join('The color ', color.name,
                                                ' does not describe a '
                                                'significant figure'),
                                        color)

    return figure


def _get_multiplicator(color):
    return _RESISTOR_TABLE[color][_MULTIPLICATOR]


def _get_tolerance(color):
    tolerance = _RESISTOR_TABLE[color][_TOLERANCE]
    if tolerance is None:
        raise InvalidColorCodeException(''.join('The color ', color.name,
                                                'does not describe a '
                                                'tolerance'),
                                        color)

    return tolerance


def _recognize_3_band_resistor(bands):
    value  = _get_figure(bands[0])
    value *= 10 ** _get_multiplicator(bands[1])
    tolerance = _get_tolerance(bands[2])

    return Resistor(value, tolerance)


def _recognize_4_band_resistor(bands):
    value  = _get_figure(bands[0]) * 10
    value += _get_figure(bands[1])
    value *= 10 ** _get_multiplicator(bands[2])
    tolerance = _get_tolerance(bands[3])

    return Resistor(value, tolerance)


def _recognize_5_band_resistor(bands):
    value  = _get_figure(bands[0]) * 100
    value += _get_figure(bands[1]) * 10
    value += _get_figure(bands[2])
    value *= 10 ** _get_multiplicator(bands[3])
    tolerance = _get_tolerance(bands[4])

    return Resistor(value, tolerance)


def decode_colors(*args):
    '''Return a Resistor object with the values encoded by the colors
    '''

    number_of_bands = len(args)
    if number_of_bands > 6:
        raise Exception('Too many color bands')
    if number_of_bands < 3:
        raise Exception('Not enough color bands')

    tolerance = _get_tolerance(args[-1])
    multiplicator = 10 ** _get_multiplicator(args[-2])
    significant_figures = number_of_bands - 2
    value = 0
    for i, color in enumerate(args[:significant_figures]):
        value += _get_figure(color) * (10 ** (significant_figures - 1 - i))

    return Resistor(value * multiplicator, tolerance)


if __name__ == '__main__':
    print(decode_colors(ColorCode.brown, ColorCode.black,
                        ColorCode.orange, ColorCode.brown))
    print(decode_colors(ColorCode.brown, ColorCode.black, ColorCode.black,
                        ColorCode.red, ColorCode.brown))
    print(decode_colors(ColorCode.red, ColorCode.black, ColorCode.yellow,
                        ColorCode.brown))
