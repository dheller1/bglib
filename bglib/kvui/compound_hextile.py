from bglib.kvui.hextile import HexTile

from kivy.uix.widget import Widget
from math import sqrt

from bglib.grid.tilemap import TileMap, HexShapedTileMap
from bglib.grid.hexcoords import HexCoords


class HexagonalCompoundHexTile(Widget):
    """ Compound tile of multiple HexTiles arranged in a 'hexagonal' pattern:
    Starting from a single central HexTile, an arbitrary number of additional tiles ('repetitions') is added to each
    of the six edges of the initial tile. The outer tiles define the corners of the compound 'hexagon'.
    These corners are then connected (with 'edge' tiles) and finally all holes are closed. """

    def __init__(self, repetitions, radius, **kwargs):
        super().__init__(**kwargs)
        if repetitions < 0:
            raise ValueError('Negative number of repetitions invalid.')

        # some constants for calculation
        tile_height = sqrt(3) * radius
        y_of_bottom_tile_col0 = self.y - repetitions * tile_height

        # add columns of individual HexTiles.
        # The center column (where 'col'==0) has exactly 'repetitions' tiles to its top and bottom, plus one
        # at the center, for 2*rep + 1 in total. Going to the left and right sides, one less tile is placed
        # in each column.
        for col in range(repetitions+1):
            # each execution of this loop body adds tiles to the left and right (except for col==0)
            tiles_in_col = (2 * repetitions + 1) - col
            tile_x_pos = self.x + 1.5 * col * radius
            if col > 0:
                tile_x_neg = self.x - 1.5 * col * radius
            y_of_bottom_tile_thiscol = y_of_bottom_tile_col0 + 0.5 * col * tile_height

            for row in range(tiles_in_col):
                tile_y = y_of_bottom_tile_thiscol + row * tile_height
                self.add_widget(HexTile(radius=radius, pos=(tile_x_pos, tile_y)))
                if col > 0:
                    self.add_widget(HexTile(radius=radius, pos=(tile_x_neg, tile_y)))

        print(f'Added {len(self.children)} tiles.')


_sqrt3 = sqrt(3)


class TileMapWidget(Widget):
    def __init__(self, tile_radius, tilemap, **kwargs):
        super().__init__(**kwargs)
        self._tilemap = tilemap
        self._tile_radius = tile_radius
        for coords, tile in self._tilemap.items():
            self.add_widget(HexTile(radius=tile_radius, pos=self.hex_to_pixel(coords)))

    def hex_to_pixel(self, coords):
        """ :param coords: HexCoords instance"""
        x = self.x + self._tile_radius * 1.5 * coords.q
        y = self.y + self._tile_radius * _sqrt3 * (0.5 * coords.q + coords.r)
        return x, y


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    #runTouchApp(HexagonalCompoundHexTile(radius=20, repetitions=4, pos=(Window.size[0]/2, Window.size[1]/2)))

    h2 = HexShapedTileMap(2)
    gp = TileMap()
    gp.add_tilemap(h2)
    for offset in [(3, -5), (5, -2), (2, 3), (-3, 5), (-5, 2), (-2, -3)]:
        gp.add_tilemap(h2, offset)

    m = HexShapedTileMap(2, 'empty')
    runTouchApp(TileMapWidget(tile_radius=20, tilemap=gp, pos=(Window.size[0]/2, Window.size[1]/2)))
