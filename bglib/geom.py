class Rect:
    """ Simple 2D-rectangle. """
    def __init__(self, left, top, width, height):
        self._top = top
        self._left = left
        self._sizex, self._sizey = width, height

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._left + self._sizex

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._top + self._sizey

    @property
    def centerx(self):
        return self._left + 0.5 * self._sizex

    @property
    def centery(self):
        return self._top + 0.5 * self._sizey

    @property
    def center(self):
        return self.centerx, self.centery

    @property
    def area(self):
        return self._sizex * self._sizey

    @property
    def size(self):
        return self._sizex, self._sizey

    def scale(self, scale, scaley=None):
        self._sizex *= scale
        if scaley is not None:
            self._sizey *= scale


class Square(Rect):
    def __init__(self, left, top, length):
        super().__init__(left, top, length, length)
