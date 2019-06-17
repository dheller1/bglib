class HexCoords:
    """
    (q, r, s) define cube coordinates where q+r+s == 0
    (q, r) define axial coordinates where implicitly s := -q -r

    Individual coordinates may not be modified because they might break
    the constraint q+r+s == 0
    """
    _Neighbors = ((+1, 0), (-1, 0), (0, +1), (0, -1), (+1, -1), (-1, +1))

    __slots__ = ('_q', '_r')  # save some memory by avoiding __dict__

    def __init__(self, q, r, s=None):
        if s is not None and q + r + s != 0:
            raise ValueError('Invalid coordinates: q+r+s not equal to zero.')
        self._q = q
        self._r = r

    def __getitem__(self, index):
        return (self._q, self._r, self.s)[index]

    def __iter__(self):
        return iter((self._q, self._r, self.s))

    def __hash__(self):
        return hash((self._q, self._r))

    @property
    def q(self):
        return self._q

    @property
    def r(self):
        return self._r

    @property
    def s(self):
        return -self.q - self.r

    def adjacent(self, other):
        delta = self - other
        return (delta.q, delta.r) in self.__class__._Neighbors

    def distance(self, other):
        return len(self - other)

    @property
    def neighbors(self):
        return [self + n for n in self.__class__._Neighbors]

    def rotate(self, n=+1, rot_center=None):
        """ n=+1 means 1 step (60 degrees) in clockwise direction """
        if rot_center is None:
            rot_center = HexCoords(0, 0)
        rel_coords = self - rot_center
        sign = (-1) ** abs(n)
        # shift coordinates n steps to the right
        newcoords = [sign * rel_coords[(i - n) % 3] for i in range(3)]
        return HexCoords(*newcoords) + rot_center

    def __repr__(self):
        return f'HexCoords({self.q}, {self.r}, {self.s})'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._q == other._q and self._r == other._r
        elif other == 0:
            return self._q == self._r == 0
        else:
            raise TypeError(f'Invalid operand type {type(other)}')

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.q + other.q, self.r + other.r)
        elif (len(other) == 2 or
              len(other) == 3 and sum(other) == 0):
            return self.__class__(self.q + other[0], self.r + other[1])
        else:
            raise TypeError('Invalid operand.')

    def __neg__(self):
        return self.__class__(-self.q, -self.r)

    def __sub__(self, other):
        return self + (-other)

    def __len__(self):
        return (abs(self.q) + abs(self.r) + abs(self.s)) // 2