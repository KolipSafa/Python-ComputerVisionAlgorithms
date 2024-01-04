from itertools import permutations

def calculate_permutations_of_four(coords):
    result = []
    for perm in permutations(coords, 4):
        result.append(list(perm))
    return result


