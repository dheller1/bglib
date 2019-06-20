import os


_kvdir = os.path.join(os.path.dirname(__file__), '..', 'kv')


def get_kv(path):
    return os.path.abspath(os.path.join(_kvdir, path))