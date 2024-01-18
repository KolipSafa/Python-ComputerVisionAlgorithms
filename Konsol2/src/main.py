import os
import cv2
import numpy as np
from functions.filter_1_check_horizontal_thresholds import filter_1_check_horizontal_thresholds
from functions.filter_2_check_vertical_thresholds import filter_2_check_vertical_thresholds
from functions.filter_3_check_can_be_rectangle import filter_3_check_can_be_rectangle
from functions.filter_4_check_length_ratios import filter_4_check_length_ratios
from functions.draw_rectangle import draw_rectangle


def filter_points_close(point1, point2, threshold=10):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) <= threshold and abs(y1 - y2) <= threshold

def sarı_nokta_koy(img, coords):
    x, y = coords
    img = cv2.circle(img, (x, y), 5, (0, 255, 255), -1)
    return img

def main(image_path):
    # Görüntüyü oku
    # image_path = r'C:\Users\tkaan\Documents\GitHub\Python-Programming-Lecture-Project\Konsol2\input\2.jpg'
    image = cv2.imread(image_path)

    # Görüntüyü gri tonlamaya çevir
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Canny Edge Detection
    edges = cv2.Canny(gray_image, 50, 150)  # Eşik değerlerini ihtiyacınıza göre ayarlayın

    # Gaussian düzeltme için kernel boyutu ve standart sapma ayarları
    kernel_size = (5, 5)  # Kernel boyutu, örneğin (5, 5)
    sigma = 1.0           # Gaussian dağılımının standart sapması

    # Gaussian düzeltme uygula
    smoothed_image = cv2.GaussianBlur(edges, kernel_size, sigma)

    # Hough dönüşümü için parametre ayarları
    rho = 1              # Dönüşüm parametre
    theta = np.pi / 180  # Dönüşüm parametre
    threshold = 30       # Eşik değeri
    min_line_length = 100  # Minimum çizgi uzunluğu
    max_line_gap = 5      # Maksimum boşluk

    # Hough dönüşümü uygula
    lines = cv2.HoughLinesP(smoothed_image, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    # Kenarları belirleyen çizgileri saklamak için boş bir liste oluştur
    detected_edges = lines.reshape(-1, lines.shape[-1])
    # print(detected_edges)

    # Hough dönüşümü sonuçlarını orijinal görüntü üzerine çiz ve uygun kenarları kaydet
    for line in detected_edges:
        x1, y1, x2, y2 = line
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Yatay kenarları filtrele
    horizontal_edges = filter_1_check_horizontal_thresholds(detected_edges)

    # Dikey kenarları filtrele
    vertical_edges = filter_2_check_vertical_thresholds(detected_edges)

    # Filtrelenmiş yatay kenarları orijinal görüntü üzerine çiz
    for edge in horizontal_edges:
        x1, y1, x2, y2 = edge
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Filtrelenmiş dikey kenarları orijinal görüntü üzerine çiz
    for edge in vertical_edges:
        x1, y1, x2, y2 = edge
        cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    top_left, bottom_right = filter_3_check_can_be_rectangle(horizontal_edges)

    sarı_nokta_koy(image, top_left)
    sarı_nokta_koy(image, bottom_right)
    draw_rectangle(image, top_left, bottom_right)

    # Orijinal, kenarlar, düzeltilmiş ve filtrelenmiş görüntüyü göster
    # cv2.imshow('Filtered Horizontal and Vertical Edges', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return image

def process_images_in_directory(directory_path, output_directory):
    # Dizin içindeki tüm dosya ve dizinleri listele
    files = os.listdir(directory_path)

    for file_name in files:
        # Dosya yolunu oluştur
        file_path = os.path.join(directory_path, file_name)

        # Eğer bir dosya ise ve resim dosyası uzantısına sahipse
        if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            print(f"Processing image: {file_name}")

            try:
                result_image = main(file_path)
                # Sonuçları ayrı bir dosyaya yaz
                output_file_path = os.path.join(output_directory, f"result_{file_name}")
                cv2.imwrite(output_file_path, result_image)

            except Exception as e:
                print(f"Hata oluştu: {e}")
                continue  # Hata durumunda devam et

input_path = r"C:\Users\talha\OneDrive\Masaüstü\Python-Programming-Lecture-Project\Konsol2\input"
output_path = r"C:\Users\talha\OneDrive\Masaüstü\Python-Programming-Lecture-Project\Konsol2\output"

process_images_in_directory(input_path, output_path)