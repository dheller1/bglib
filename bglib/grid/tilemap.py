from collections import UserDict
from bglib.grid.hexcoords import HexCoords


def _qr_to_textxy(q, r):
    x = 2 * q
    y = 2 * r + q
    return x, y


def _add_hexascii(target, x, y):
    # y shall go from bottom to top, so reverse to the lines
    # in which a string is printed
    target[x + 1, -y] = '_'  # top
    target[x, -y + 1] = '/'  # left-top
    target[x + 2, -y + 1] = '\\'  # right-top
    target[x, -y + 2] = '\\'  # left-btm
    target[x + 1, -y + 2] = '_'  # btm
    target[x + 2, -y + 2] = '/'  # right-btm


class TileMap(UserDict):
    def add_tilemap(self, tilemap, pos=None):
        if pos is None:
            self.update(tilemap)
        else:
            for coords, tile in tilemap.items():
                self[coords + pos] = tile

    def collides_tilemap(self, other):
        return any([pos in self for pos in other.keys()])

    def rotated(self, steps):
        m = TileMap()
        for coords, val in self.items():
            m[coords.rotate(steps)] = val
        return m

    def to_ascii(self):
        textmap = dict()
        for coord in self.keys():
            x, y = _qr_to_textxy(coord.q, coord.r)
            _add_hexascii(textmap, x, y)

        min_x = min([coord[0] for coord in textmap.keys()])
        min_y = min([coord[1] for coord in textmap.keys()])
        max_x = max([coord[0] for coord in textmap.keys()])
        max_y = max([coord[1] for coord in textmap.keys()])

        string = ''
        for y in range(min_y, max_y + 1):  # start y at bottom
            for x in range(min_x, max_x + 1):
                char = textmap.get((x, y), ' ')
                string += char
            string += '\n'
        return string


class HexShapedTileMap(TileMap):
    def __init__(self, radius, fill_element=None):
        super().__init__()
        for q in range(-radius, radius + 1):
            rmin = max(-radius, -radius - q)  # since s = -q-r we must ensure abs(s) <= radius
            rmax = min(radius, -q + radius)

            for r in range(rmin, rmax + 1):
                self[HexCoords(q, r)] = fill_element
