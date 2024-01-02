import cv2
import numpy as np
from functions.filter_7_check_white_ratio import filter_7_check_white_ratio
from functions.filter_5_check_paralel_horizontal_thresholds import filter_5_check_paralel_horizontal_thresholds
from functions.filter_6_check_size_ratio import filter_6_check_size_ratio
from functions.filter_4_check_paralel_thresholds import filter_4_check_paralel_thresholds
from functions.filter_3_check_direction_thresholds import filter_3_check_direction_thresholds
from functions.calculate_distances import calculate_distances
from functions.filter_2_check_thresholds import filter_2_check_thresholds
from functions.normalize_distances import normalize_distances
from functions.filter_check_can_be_rectangle import filter_check_can_be_rectangle
from functions.calculate_permutations_of_four import calculate_permutations_of_four
from functions.draw_combinations import draw_combinations


INPUT_WIDTH = 600

# Görüntüyü önişleme işlemleri için fonksiyon
def preprocess_image(image):
    # Görüntüyü gri tonlama
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gauss filtresi uygula
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    return blurred

# Kenar ve köşeleri tespit etmek için fonksiyon
def detect_edges_and_corners(image):
    # Canny kenar tespiti
    edges = cv2.Canny(image, 50, 150)
    
    # Shi-Tomasi köşe tespiti
    corners = cv2.goodFeaturesToTrack(image, maxCorners=100, qualityLevel=0.05, minDistance=10)
    corners = np.intp(corners)
    # x = np.array(corners)
    # corners[0] = [[293 294]]
    # corners shape (100, 1, 2)
    #[[293 294],[650 164]]
    # print(corners[0:2,0,0:2])
    return edges, corners

# Kenarları işaretleme fonksiyonu
def draw_edges(image, edges):
    # Kenarları yeşil renkte işaretle
    result_image = image.copy()
    result_image[edges != 0] = [0, 255, 0]
    
    return result_image

# Köşeleri işaretleme fonksiyonu
def draw_corners(image, corners):
    # Köşeleri beyaz renkte işaretle
    for corner in corners:
        x, y = corner.ravel()
        cv2.circle(image, (x, y), 3, (255, 255, 255), -1)


# Silindir tespiti fonksiyonu
def detect_cylinder(image):
    # Görüntüyü önişle
    preprocessed_image = preprocess_image(image)
    
    #1. Kenar ve köşe tespiti
    edges, corners = detect_edges_and_corners(preprocessed_image)

    corners_2d = corners.reshape(corners.shape[0], -1).tolist()

    #2. Kombinasyonlar tespiti
    permutations_of_four = calculate_permutations_of_four(corners_2d)

    drawed_image = np.copy(preprocessed_image)
    cv2.imshow('First Image', drawed_image)
    cv2.waitKey(0)  
    cv2.destroyAllWindows()

    # Filter 1
    filtered_permutations = []
    for coords in permutations_of_four:
        filter_result = filter_check_can_be_rectangle(coords)
        if filter_result is True:
            filtered_permutations.append(coords) 
            
    # print("After Filter 1")
    # print(len(filtered_permutations))
    # print(filtered_permutations)

    # Filter 2
    filtered_permutations_2 = []
    for coords in filtered_permutations:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        distances = calculate_distances(coords)
        normalized_distances = normalize_distances(distances, INPUT_WIDTH)
        filter_result_2 = filter_2_check_thresholds(normalized_distances, 0.5, 1.5, 0.5, 1.5)
        if filter_result_2 is True:
            filtered_permutations_2.append(coords) 
            
    # Filter 3
    filtered_permutations_3 = []
    for coords in filtered_permutations_2:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        filter_result_3 = filter_3_check_direction_thresholds(coords, 0.5, 1.5)
        if filter_result_3 is True:
            filtered_permutations_3.append(coords) 

    # Filter 4
    filtered_permutations_4 = []
    for coords in filtered_permutations_3:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        filter_result_4 = filter_4_check_paralel_thresholds(coords, 1)
        if filter_result_4 is True:
            filtered_permutations_4.append(coords) 

    # Filter 5
    filtered_permutations_5 = []
    for coords in filtered_permutations_4:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        filter_result_5 = filter_5_check_paralel_horizontal_thresholds(coords, 1)
        if filter_result_5 is True:
            filtered_permutations_5.append(coords) 

    # Filter 6
    filtered_permutations_6 = []
    for coords in filtered_permutations_5:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        distances_6 = calculate_distances(coords)
        normalized_distances_6 = normalize_distances(distances_6, INPUT_WIDTH)
        filter_result_6 = filter_6_check_size_ratio(normalized_distances_6, 1,1)
        if filter_result_6 is True:
            filtered_permutations_6.append(coords) 
    
    # Filter 7
    #noktalar arasında kalan beyaz rengin oranı diğer renklere üstün olmalı
    filtered_permutations_7 = []
    for coords in filtered_permutations_6:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        filter_result_7 = filter_7_check_white_ratio(coords, 1,1)
        if filter_result_7 is True:
            filtered_permutations_7.append(coords)

    after_filter_image = np.copy(preprocessed_image)

    # print(filtered_permutations_2[0])
    # draw_corners(after_filter_image, filtered_permutations_2)

    # print(filtered_permutations)
    # for coords in filtered_permutations:
    #     draw_combinations(after_filter_image, coords)

    cv2.imshow('Filter Result', after_filter_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Kombinasyonları resimde belirtir
    # for coords in combinations_of_four:
    # draw_combinations(combinations_of_four[0], drawed_image)

    # Kenarları işaretle
    result_image_with_edges = draw_edges(image, edges)
    
    # Köşeleri işaretle
    draw_corners(result_image_with_edges, corners)

    # Sonucu göster
    cv2.imshow('Cylinder Detection Result', result_image_with_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Görüntüyü oku
image = cv2.imread('C:\\Users\\talha\\OneDrive\\Masaüstü\\yandan kirpilmis\\deneme.png')
image = cv2.resize(image, (INPUT_WIDTH, INPUT_WIDTH))

# Silindir tespiti
detect_cylinder(image)
