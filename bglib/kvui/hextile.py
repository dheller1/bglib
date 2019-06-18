"""
Regular hexagonal widget class defined by its center position and a radius.
"""

from kivy.graphics import Mesh, Color, Line
from kivy.graphics.tesselator import Tesselator
from kivy.uix.widget import Widget
from math import sin, cos, radians


def _point_inside_polygon(x, y, poly):
    """ Taken from http://www.ariel.com.au/a/python-point-int-poly.html """
    n = len(poly)
    inside = False
    p1x = poly[0]
    p1y = poly[1]
    for i in range(0, n + 2, 2):
        p2x = poly[i % n]
        p2y = poly[(i + 1) % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


class HexTile(Widget):
    def __init__(self, radius, **kwargs):
        super().__init__(**kwargs)

        self._polygon = []
        for alpha in (0, 60, 120, 180, 240, 300):
            self._polygon.append(cos(radians(alpha)) * radius + self.x)
            self._polygon.append(sin(radians(alpha)) * radius + self.y)

        tess = Tesselator()
        tess.add_contour(self._polygon)
        if not tess.tesselate():
            raise ValueError('Unable to tesselate.')

        with self.canvas:
            Color(.1, .1, .1)
            for vertices, indices in tess.meshes:
                Mesh(vertices=vertices, indices=indices, mode='triangle_fan')

            Color(.46, .46, .6)
            Line(points=self._polygon + self._polygon[:2], width=1.2)

    def collide_point(self, x, y):
        x, y = self.to_local(x, y)
        return _point_inside_polygon(x, y, self._polygon)


if __name__ == '__main__':
    from kivy.base import runTouchApp
    from kivy.core.window import Window
    runTouchApp(HexTile(radius=100, pos=(Window.size[0]/2, Window.size[1]/2)))
