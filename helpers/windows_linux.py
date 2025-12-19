import os

def normalize_path(path):
    path = os.path.expanduser(path)
    path = os.path.expandvars(path)
    return os.path.normpath(path)