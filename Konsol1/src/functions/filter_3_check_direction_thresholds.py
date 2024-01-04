import numpy as np

def filter_3_check_direction_thresholds(coords, DirectionTreshL, DirectionTreshH):
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4

    Dir12 = np.arctan([np.abs(x2 - x1)/np.abs(y2 - y1+5)])[0] * 180 / np.pi
    Dir23 = np.arctan([np.abs(x3 - x2)/np.abs(y3 - y2+5)])[0] * 180 / np.pi
    Dir34 = np.arctan([np.abs(x4 - x3)/np.abs(y4 - y3+5)])[0] * 180 / np.pi
    Dir41 = np.arctan([np.abs(x1 - x4)/np.abs(y1 - y4+5)])[0] * 180 / np.pi

    if (Dir23 < DirectionTreshL) and (Dir41 < DirectionTreshL) and (Dir12 > DirectionTreshH) and (Dir34 > DirectionTreshH):
        return True
    else:
        return False