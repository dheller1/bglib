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
        self._tilewidgets = dict()

        self._last_hovered_widget = None
        for coords, tile in self._tilemap.items():
            widget = HexTile(radius=tile_radius, pos=self.hex_to_pixel(coords))
            self._tilewidgets[coords] = widget
            self.add_widget(widget)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def hex_to_pixel(self, coords):
        """ :param coords: HexCoords instance"""
        x = self.x + self._tile_radius * 1.5 * coords.q
        y = self.y + self._tile_radius * _sqrt3 * (0.5 * coords.q + coords.r)
        return x, y

    def pixel_to_hex(self, coords):
        """ :param coords: (x,y) screen coordinates"""
        px, py = coords[0] - self.x, coords[1] - self.y
        qfloat = 2./3 * px / self._tile_radius
        rfloat = (-1./3 * px + _sqrt3/3 * py) / self._tile_radius
        return HexCoords.round(qfloat, rfloat)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # nothing to do if not on screen
        pos = self.to_widget(*args[1])
        hexcoords = self.pixel_to_hex(pos)
        hovered_tile = self._tilewidgets.get(hexcoords)
        if hovered_tile:
            hovered_tile.is_hovered = True
            if self._last_hovered_widget not in (None, hovered_tile):
                self._last_hovered_widget.is_hovered = False

            if hovered_tile is not self._last_hovered_widget:
                # remove and re-add to get in on top of other widgets
                self.remove_widget(hovered_tile)
                self.add_widget(hovered_tile, index=0)

            self._last_hovered_widget = hovered_tile
        else:
            if self._last_hovered_widget:
                self._last_hovered_widget.is_hovered = False
                self._last_hovered_widget = None


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    #runTouchApp(HexagonalCompoundHexTile(radius=20, repetitions=4, pos=(Window.size[0]/2, Window.size[1]/2)))

    from kivy.factory import Factory
    from kivy.lang import Builder
    from bglib.util.resource import get_kv
    Builder.load_file(get_kv('hextile.kv'))
    Factory.register('HexTile', HexTile)

    h2 = HexShapedTileMap(2)
    gp = TileMap()
    gp.add_tilemap(h2)
    for offset in [(3, -5), (5, -2), (2, 3), (-3, 5), (-5, 2), (-2, -3)]:
        gp.add_tilemap(h2, offset)

    m = HexShapedTileMap(2, 'empty')
    runTouchApp(TileMapWidget(tile_radius=20, tilemap=gp, pos=(Window.size[0]/2, Window.size[1]/2)))
