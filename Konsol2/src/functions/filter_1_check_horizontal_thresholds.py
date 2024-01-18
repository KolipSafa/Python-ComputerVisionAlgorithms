import numpy as np

def filter_1_check_horizontal_thresholds(edges, angle_thresholdDOWN = -10, angle_thresholdUP = 10):
    filtered_edges = []

    for edge in edges:
        x1, y1, x2, y2 = edge
        # Hesaplanan eğim
        angle = np.arctan([np.abs(x1 - x2)/(np.abs(y1 - y2)+5)])[0] * 180 / np.pi

        # Eğim aralığı kontrolü
        if  angle_thresholdDOWN < abs(angle - 90) < angle_thresholdUP:
            filtered_edges.append(edge)

    return np.array(filtered_edges)