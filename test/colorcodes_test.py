import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from resistortools.colorcodes import decode_colors
from resistortools.colorcodes import ColorCode, Resistor


def test_comparison():
    r1 = Resistor(100, 1.0)
    r2 = Resistor(100, 1.0)

    assert r1 == r2

    r2 = Resistor(200, 1.0)

    assert r1 != r2

    r2 = Resistor(100, 2.0)

    assert r1 != r2


def test_str():
    res = Resistor(100, 2.0)

    assert str(res) == '100 Ω 2.0 %'

    res = Resistor(2 * 10**3, 3)

    assert str(res) == '2 kΩ 3 %'

    res = Resistor(4 * 10**6, 5.0)

    assert str(res) == '4 MΩ 5.0 %'

    res = Resistor(6 * 10**9, 7)

    assert str(res) == '6 GΩ 7 %'

    res = Resistor(4711, 42.314)

    assert str(res) == '4711 Ω 42.314 %'


def test_decode():
    r1 = Resistor(100, 1.0)

    r2 = decode_colors(ColorCode.brown, ColorCode.black, ColorCode.brown,
                       ColorCode.brown)

    assert r1 == r2
