from bglib.grid.tilemap import TileMap
import pytest


def test_setitem_getitem():
    g = TileMap(50)
    g[(0, 0)] = 'tile1'
    g[(1, 0)] = 'tile2'

    assert g[(0, 0)] == 'tile1'
    assert g[(1, 0)] == 'tile2'
    assert len(g) == 2

    with pytest.raises(KeyError):
        _ = g[(2, -1)]

    assert (0, 0) in g
    assert (1, 0) in g
    assert (2, 2) not in g
