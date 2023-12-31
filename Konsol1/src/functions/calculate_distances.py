from math import sqrt

def calculate_distances(coords):
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4

    L12 = sqrt((x1 - x2)**2 + (y1 - y2)**2)
    L23 = sqrt((x2 - x3)**2 + (y2 - y3)**2)
    L34 = sqrt((x3 - x4)**2 + (y3 - y4)**2)
    L41 = sqrt((x4 - x1)**2 + (y4 - y1)**2)

    return [L12, L23, L34, L41]

# coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
# result = calculate_distances(coords)
# print(result)