class TileMap:
    def __init__(self, radius):
        self._radius = radius
        self._tilemap = dict()  # maps coordinates to tiles in that position (if existing)

    def __getitem__(self, key):
        return self._tilemap[key]

    def __setitem__(self, key, value):
        self._tilemap[key] = value

    def __contains__(self, key):
        return key in self._tilemap

    def __len__(self):
        return len(self._tilemap)
