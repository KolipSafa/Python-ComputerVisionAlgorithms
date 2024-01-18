import cv2
import numpy as np
import os

from functions.filter_7_check_white_ratio import filter_7_check_white_ratio
from functions.filter_5_check_paralel_horizontal_thresholds import filter_5_check_paralel_horizontal_thresholds
from functions.filter_6_check_size_ratio import filter_6_check_size_ratio
from functions.filter_4_check_paralel_thresholds import filter_4_check_paralel_vertical_thresholds
from functions.filter_3_check_direction_thresholds import filter_3_check_direction_thresholds
from functions.calculate_distances import calculate_distances
from functions.filter_2_check_thresholds import filter_2_check_thresholds
from functions.normalize_distances import normalize_distances
from functions.filter_check_can_be_rectangle import filter_check_can_be_rectangle
from functions.calculate_permutations_of_four import calculate_permutations_of_four
from functions.draw_combinations import draw_combinations


INPUT_WIDTH = 800

# Görüntüyü önişleme işlemleri için fonksiyon
def preprocess_image(img):

    
    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Kontrast arttırma (isteğe bağlı)
    alpha = 1.5  # Kontrast artış oranı
    beta = 30    # Parlaklık artışı
    contrast_enhanced = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    
    # Morfolojik operasyonlar
    # kernel = np.ones((5,5),np.uint8)
    # morph_image = cv2.morphologyEx(contrast_enhanced, cv2.MORPH_CLOSE, kernel)
    
    # Kenar tespiti
    
    # Gaus filtresi uygula
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
    for corner in corners[0]:
        x, y = corner
        cv2.circle(image, (x, y), 5, (0, 0, 255), 5)


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
    # cv2.imshow('First Image', drawed_image)
    # cv2.waitKey(0)  
    # cv2.destroyAllWindows()

    # Filter 1
    filtered_permutations = []
    for coords in permutations_of_four:
        filter_result = filter_check_can_be_rectangle(coords)
        if filter_result is True:
            filtered_permutations.append(coords) 
            
    print("After Filter 1")
    print(len(filtered_permutations))
    #print(filtered_permutations)

    # Filter 2
    filtered_permutations_2 = []
    for coords in filtered_permutations:
        distances = calculate_distances(coords)
        normalized_distances = normalize_distances(distances, INPUT_WIDTH)
        filter_result_2 = filter_2_check_thresholds(normalized_distances, 0.4, 0.8, 0.4, 1)
        if filter_result_2 is True:
            filtered_permutations_2.append(coords) 
    
    print("After Filter 2")
    print(len(filtered_permutations_2))
    #print(filtered_permutations_2)
   
    # Filter 3
    filtered_permutations_3 = []
    for coords in filtered_permutations_2:
        filter_result_3 = filter_3_check_direction_thresholds(coords, 90, 85, 10, -10)
        if filter_result_3 is True:
            filtered_permutations_3.append(coords) 
    
    print("After Filter 3")
    print(len(filtered_permutations_3))
    #print(filtered_permutations_3)

    # Filter 4
    filtered_permutations_4 = []
    for coords in filtered_permutations_3:
        filter_result_4 = filter_4_check_paralel_vertical_thresholds(coords, 5)
        if filter_result_4 is True:
            filtered_permutations_4.append(coords) 
    
    print("After Filter 4")
    print(len(filtered_permutations_4))
    #print(filtered_permutations_4)
    
    # Filter 5
    filtered_permutations_5 = []
    for coords in filtered_permutations_4:
        filter_result_5 = filter_5_check_paralel_horizontal_thresholds(coords, 2)
        if filter_result_5 is True:
            filtered_permutations_5.append(coords) 
    
    print("After Filter 5")
    print(len(filtered_permutations_5))
    #print(filtered_permutations_5)
    
    # Filter 6
    filtered_permutations_6 = []
    for coords in filtered_permutations_5:
        distances_6 = calculate_distances(coords)
        normalized_distances_6 = normalize_distances(distances_6, INPUT_WIDTH)
        filter_result_6 = filter_6_check_size_ratio(normalized_distances_6, 0, 5)
        if filter_result_6 is True:
            filtered_permutations_6.append(coords) 
    
    print("After Filter 6")
    print(len(filtered_permutations_6))
    #print(filtered_permutations_6)
    
    # Filter 7
    #noktalar arasında kalan beyaz rengin oranı diğer renklere üstün olmalı
    filtered_permutations_7 = []
    for coords in filtered_permutations_6:
        # coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
        # coords[0] = [0, 0]
        filter_result_7 = filter_7_check_white_ratio(image, coords)
        if filter_result_7 is True:
            filtered_permutations_7.append(coords)

    print("After Filter 7")
    print(len(filtered_permutations_7))
    #print(filtered_permutations_7)
    
    # with open('output.txt', 'w') as file:
    #     # Her bir koordinatı dosyaya yaz
    #     for coord in filtered_permutations_7:
    #         file.write(f"{coord[0]} {coord[1]} {coord[2]} {coord[3]}\n")
    
    after_filter_image = np.copy(preprocessed_image)

    # print(filtered_permutations_2[0])
    # draw_corners(after_filter_image, filtered_permutations_2)

    # print(filtered_permutations)
    # for coords in filtered_permutations:
    #     draw_combinations(after_filter_image, coords)

    # cv2.imshow('Filter Result', after_filter_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Kombinasyonları resimde belirtir
    #for coords in combinations_of_four:
    #    draw_combinations(combinations_of_four[0], drawed_image)

    # Kenarları işaretle
    #result_image_with_edges = draw_edges(image, edges)
    
    # Köşeleri işaretle
    draw_corners(after_filter_image, filtered_permutations_6)

    # Sonucu göster
    # cv2.imshow("Cylinder Detect Result", after_filter_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return after_filter_image

def process_images_in_directory(directory_path, output_directory):
    # Dizin içindeki tüm dosya ve dizinleri listele
    files = os.listdir(directory_path)

    for file_name in files:
        # Dosya yolunu oluştur
        file_path = os.path.join(directory_path, file_name)

        # Eğer bir dosya ise ve resim dosyası uzantısına sahipse
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing image: {file_name}")

            # Görüntüyü oku
            image = cv2.imread(file_path)
            image = cv2.resize(image, (INPUT_WIDTH, INPUT_WIDTH))

            try:
                # Silindir tespiti
                result_image = detect_cylinder(image)

                # Sonuçları ayrı bir dosyaya yaz
                output_file_path = os.path.join(output_directory, f"result_{file_name}")
                cv2.imwrite(output_file_path, result_image)

            except Exception as e:
                print(f"Hata oluştu: {e}")
                continue  # Hata durumunda devam et

# Görüntüyü oku
#image = cv2.imread('C:\\Users\\talha\\OneDrive\\Masaüstü\\Python-Programming-Lecture-Project\\Konsol1\\input\\31.png')
# dosya yolu C:\\Users\\talha\\OneDrive\\Masaüstü\\Python-Programming-Lecture-Project\\Konsol1\\input\\kapi.png
            
input_path = "C:\\Users\\talha\\OneDrive\\Masaüstü\\Python-Programming-Lecture-Project\\Konsol1\\input\\"
output_path = "C:\\Users\\talha\\OneDrive\\Masaüstü\\Python-Programming-Lecture-Project\\Konsol1\\output\\"

process_images_in_directory(input_path, output_path)
