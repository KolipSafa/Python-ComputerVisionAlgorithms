import numpy as np

def filter_5_check_paralel_horizontal_thresholds(coords, ParalellTresh):
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4

    Dir12 = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
    Dir23 = np.arctan2(y3 - y2, x3 - x2) * 180 / np.pi
    Dir34 = np.arctan2(y4 - y3, x4 - x3) * 180 / np.pi
    Dir41 = np.arctan2(y1 - y4, x1 - x4) * 180 / np.pi

    if abs(Dir23 - Dir41) < ParalellTresh:
        return True
    else:
        return False