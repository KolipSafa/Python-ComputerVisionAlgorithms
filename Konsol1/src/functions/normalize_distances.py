def normalize_distances(distances, diagonal):
    return [L / diagonal for L in distances]


# distances = [10,10,5,4]
# normalized_distances = normalize_distances(distances, 400)
# print(normalized_distances)