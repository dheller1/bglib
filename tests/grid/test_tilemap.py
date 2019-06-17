from bglib.grid.tilemap import TileMap, HexShapedTileMap
from bglib.grid.hexcoords import HexCoords
import pytest


class Tile:
    def __init__(self, *args):
        pass


def test_setitem_getitem():
    g = TileMap()
    g[(0, 0)] = 'tile1'
    g[(1, 0)] = 'tile2'

    assert g[(0, 0)] == 'tile1'
    assert g[(1, 0)] == 'tile2'
    assert len(g) == 2

    with pytest.raises(KeyError):
        print(g[(2, -1)])

    assert (0, 0) in g
    assert (1, 0) in g
    assert (2, 2) not in g


def test_add_tilemap():
    a = TileMap()
    b = TileMap()
    for q in range(-1, 2):
        for r in range(-1, 2):
            if q == r == 0:
                b[HexCoords(q, r)] = Tile('center of galaxy')
            else:
                b[HexCoords(q, r)] = Tile()

    assert len(a) == 0
    a.add_tilemap(b)

    assert len(a) == len(b)
    for key, val in a.items():
        assert b[key] is val


def test_collide():
    pass


def test_hexshape():
    h0 = HexShapedTileMap(0)
    h1 = HexShapedTileMap(1)
    h2 = HexShapedTileMap(2)
    assert len(h0) == 1
    assert HexCoords(0, 0, 0) in h0

    assert len(h1) == 7
    for coords in h1.keys():
        assert len(coords) <= 1
        assert coords in h2.keys()

    assert len(h2) == 19
    for coords in h2.keys():
        assert len(coords) <= 2


def test_gp_map():
    h2 = HexShapedTileMap(2)

    gp = TileMap()
    gp.add_tilemap(h2)

    for offset in [(3, -5), (5, -2), (2, 3), (-3, 5), (-5, 2), (-2, -3)]:
        gp.add_tilemap(h2, offset)

    print(gp.to_ascii())
    assert len(gp) == 7 * len(h2)
    print(len(gp))


def test_rotate_map():
    s = TileMap()
    center = Tile('center')
    outer = Tile('outer')
    s[HexCoords(0, 0)] = center
    s[HexCoords(1, 0)] = outer

    rotation_and_expected_coords = [
        (0, [(0, 0), (1, 0)]),
        (1, [(0, 0), (1, -1)]),
        (2, [(0, 0), (0, -1)]),
        (3, [(0, 0), (-1, 0)]),
        (4, [(0, 0), (-1, 1)]),
        (5, [(0, 0), (0, 1)]),
        (6, [(0, 0), (1, 0)]),
        (-6, [(0, 0), (1, 0)]),
        (-5, [(0, 0), (1, -1)]),
        (-4, [(0, 0), (0, -1)]),
        (-3, [(0, 0), (-1, 0)]),
        (-2, [(0, 0), (-1, 1)]),
        (-1, [(0, 0), (0, 1)])
    ]
    for rot, expected in rotation_and_expected_coords:
        rotated = s.rotated(rot)
        assert len(rotated) == 2
        # rotated tiles must not lose their identity
        assert rotated[HexCoords(*expected[0])] is center
        assert rotated[HexCoords(*expected[1])] is outer

    m = TileMap()

    for c in [(0, 0), (0, 1), (1, 0), (-1, 1), (2, 0), (3, -1)]:
        m[HexCoords(*c)] = Tile()

    #print(m.to_ascii())
    #print(m.rotated(1).to_ascii())
    #print(m.rotated(2).to_ascii())
    #print(m.rotated(3).to_ascii())
    #print(m.rotated(4).to_ascii())
    #print(m.rotated(5).to_ascii())