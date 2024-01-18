import cv2
import numpy as np
import filter_1_check_height_width_thresholds
import filter_2_check_direction_thresholds
import filter_3_check_direction_thresholds
import filter_4_check_parallel_threshold
import filter_5_check_height_width_ratio

from itertools import permutations

def preprocess_image(image_path):
    # Read and grayscale conversion
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian smoothing for noise reduction and corner elimination
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return blurred

def detect_corners(image):
    # Apply Canny edge detection
    edges = cv2.Canny(image, 50, 150)

    # Apply He and Yung corner detector
    corners = cv2.cornerHarris(edges, 2, 3, 0.04)

    return corners

def permutations_of_four(coords):
    result = []
    for perm in permutations(coords, 4):
        result.append(list(perm))
    return result


def filter_1_check_height_width_thresholds(normalized_distances, HeightThresL, HeightThresH, WidthThresL, WidthThresH):
    Siz12, Siz23, Siz34, Siz41 = normalized_distances
    height_condition = HeightThresL < Siz12 < HeightThresH and HeightThresL < Siz34 < HeightThresH
    width_condition = WidthThresL < Siz23 < WidthThresH and WidthThresL < Siz41 < WidthThresH
    return height_condition and width_condition

# Filtre 2: DirectionThresL
def filter_2_check_direction_thresholds(normalized_distances, DirectionThresL):
    _, Dir23, _, Dir41 = normalized_distances
    return Dir23 < DirectionThresL and Dir41 < DirectionThresL

# Filtre 3: DirectionThresH
def filter_3_check_direction_thresholds(normalized_distances, DirectionThresH):
    Dir12, _, Dir34, _ = normalized_distances
    return Dir12 > DirectionThresH and Dir34 > DirectionThresH

# Filtre 4: ParallelThres
def filter_4_check_parallel_threshold(normalized_distances, ParallelThres):
    Dir12, _, Dir34, _ = normalized_distances
    return abs(Dir12 - Dir34) < ParallelThres

# Filtre 5: HWThresL ve HWThresH
def filter_5_check_height_width_ratio(normalized_distances, HWThresL, HWThresH):
    Siz12, Siz23, Siz34, Siz41 = normalized_distances
    ratio = (Siz12 + Siz34) / (Siz23 + Siz41)
    return HWThresL < ratio < HWThresH

def filter_cylinder_corners(corners, image_diagonal):
    # Filtre 1
    filtered_permutations_1 = []
    for coords in permutations_of_four:
        filter_result_1 = filter_1_check_height_width_thresholds(normalized_distances, 0.1, 0.9, 0.1, 0.9)
        if filter_result_1:
            filtered_permutations_1.append(coords)

    print("After Filter 1")
    print(len(filtered_permutations_1))
    
    # Filtre 2
    filtered_permutations_2 = []
    for coords in filtered_permutations_1:
        filter_result_2 = filter_2_check_direction_thresholds(normalized_distances, 0.9)
        if filter_result_2:
            filtered_permutations_2.append(coords)

    print("After Filter 2")
    print(len(filtered_permutations_2))
    
    # Filtre 3
    filtered_permutations_3 = []
    for coords in filtered_permutations_2:
        filter_result_3 = filter_3_check_direction_thresholds(normalized_distances, 0.9)
        if filter_result_3:
            filtered_permutations_3.append(coords)

    print("After Filter 3")
    print(len(filtered_permutations_3))
    
    # Filtre 4
    filtered_permutations_4 = []
    for coords in filtered_permutations_3:
        filter_result_4 = filter_4_check_parallel_threshold(normalized_distances, ParallelThres)
        if filter_result_4:
            filtered_permutations_4.append(coords)

    print("After Filter 4")
    print(len(filtered_permutations_4))
    
    # Filtre 5
    filtered_permutations_5 = []
    for coords in filtered_permutations_4:
        filter_result_5 = filter_5_check_height_width_ratio(normalized_distances, HWThresL, HWThresH)
        if filter_result_5:
            filtered_permutations_5.append(coords)

    print("After Filter 5")
    print(len(filtered_permutations_5))

    return filtered_permutations_5

# Bu fonksiyonun çalıştırılması
normalized_distances = [0.5, 0.3, 0.4, 0.6]  # Bu değerler örnek olarak verilmiştir, gerçek değerleri kullanmalısınız
filtered_coordinates = filter_cylinder_corners(normalized_distances)
print("Final Filtered Coordinates:")
print(filtered_coordinates)

def main(image_path):
    # Preprocess image
    blurred_image = preprocess_image(image_path)

    # Detect corners
    corners = detect_corners(blurred_image)

    # Filter cylinder-corner candidates
    image_diagonal = np.linalg.norm(blurred_image.shape)
    cylinder_candidates = filter_cylinder_corners(corners, image_diagonal)

    # Draw cylinder candidates
    for candidate in cylinder_candidates:
        cv2.drawContours(blurred_image, [candidate], -1, (0, 0, 255), 2)

    # Show the image
    cv2.imshow('Cylinder candidates', blurred_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    image_path = r'C:\Users\safak\Desktop\103.png'
    main(image_path)