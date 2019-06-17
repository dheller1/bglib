from bglib.grid.hexcoords import HexCoords
import pytest
from random import randint


def test_instantiate():
    a = HexCoords(0, 0, 0)
    b = HexCoords(+1, 0, -1)
    c = HexCoords(-3, +1)

    assert a.q == a.r == a.s == b.r == 0
    assert b.q == -b.s == c.r == 1
    assert c.s == +2

    with pytest.raises(ValueError):
        HexCoords(+3, -1, 0)  # wrong!


def test_add():
    a = HexCoords(0, 0, 0)
    b = HexCoords(+1, 0, -1)
    c = HexCoords(-3, +1)

    assert a + b == b
    assert a + b + c == HexCoords(-2, +1, +1)
    assert a + b + c - b == c

    assert a + (+1, 0) == a + (+1, 0, -1) == b

    b += c
    assert b == HexCoords(-2, +1, +1)

    b -= c
    assert b == HexCoords(+1, 0, -1)

    b -= b
    assert b == a == 0


def test_no_set_coordinates():
    a = HexCoords(0, 0, 0)
    b = HexCoords(+1, 0, -1)
    c = HexCoords(-3, +1)

    with pytest.raises(AttributeError):
        a.q += 1
    with pytest.raises(AttributeError):
        b.r = 5
    with pytest.raises(AttributeError):
        c.s = 0


def test_distance():
    for repetition in range(200):
        coords_a = [randint(-5, 5) for i in range(2)]
        coords_b = [randint(-5, 10) for i in range(2)]
        a, b = HexCoords(*coords_a), HexCoords(*coords_b)

        delta = abs(a.q - b.q), abs(a.r - b.r), abs(a.s - b.s)
        maxdelta = max(delta)
        assert a.distance(b) == maxdelta
        if maxdelta == 1:
            assert a in b.neighbors
            assert b in a.neighbors


def test_neighbors():
    a = HexCoords(0, 0, 0)
    b = HexCoords(+1, 0, -1)
    c = HexCoords(-3, +1)

    assert a in b.neighbors
    assert b in a.neighbors

    for coords in [(-2, 1, 1), (-4, 1, 3), (-3, 2, 1), (-3, 0, 3), (-2, 0, 2), (-4, 2, 2)]:
        assert HexCoords(*coords) in c.neighbors
        assert c.distance(HexCoords(*coords)) == 1


def test_iter():
    hc = HexCoords(-4, 1, 3)
    for number, coord in zip([-4, 1, 3], hc):
        assert number == coord


def test_rotate():
    hc = HexCoords(+2, +1, -3)
    assert hc.rotate(0) == hc == hc.rotate(6) == hc.rotate(-6)
    assert hc.rotate(1) == hc.rotate(-5) == HexCoords(+3, -2, -1)
    assert hc.rotate(2) == hc.rotate(-4) == HexCoords(+1, -3, +2)
    assert hc.rotate(3) == hc.rotate(-3) == HexCoords(-2, -1, +3) == -hc
    assert hc.rotate(4) == hc.rotate(-2) == HexCoords(-3, +2, +1) == -hc.rotate(1)
    assert hc.rotate(5) == hc.rotate(-1) == HexCoords(-1, +3, -2) == -hc.rotate(2)