from itertools import permutations

def calculate_permutations_of_four(coords):
    result = []
    for perm in permutations(coords, 4):
        result.append(list(perm))
    return result


coords = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]
result = calculate_permutations_of_four(coords)
print(len(result))
print(result[1][0][0])