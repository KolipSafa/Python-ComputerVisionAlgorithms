import numpy as np

def filter_4_check_length_ratios(edges, ratio_threshold=0.8):
    filtered_edges = []

    for edge in edges:
        x1, y1, x2, y2 = edge

        # Calculate the length of the edge
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        # Check if the length ratio is below the threshold
        if length_ratio_check(length, ratio_threshold):
            filtered_edges.append(edge)

    return np.array(filtered_edges)

def length_ratio_check(length, threshold):
    # You can customize the length ratio condition as needed
    # For example, if you want to filter edges longer than twice the average length
    # you can use the condition length > 2 * average_length
    if length > threshold:
        return True