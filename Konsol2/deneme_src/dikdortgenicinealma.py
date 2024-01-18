import cv2
import numpy as np

def are_points_close(point1, point2, threshold=5):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) <= threshold and abs(y1 - y2) <= threshold

def filter_edges_by_orientation(edges, orientation, angle_threshold=10):
    filtered_edges = []

    for edge in edges:
        x1, y1 = edge[0]
        x2, y2 = edge[1]

        # Hesaplanan eğim
        angle = np.arctan2(y2 - y1, x2 - x1) * (180 / np.pi)

        # Eğim aralığı kontrolü
        if orientation == 'horizontal' and abs(angle) < angle_threshold:
            filtered_edges.append(edge)
        elif orientation == 'vertical' and abs(angle - 90) < angle_threshold:
            filtered_edges.append(edge)

    return filtered_edges

# Görüntüyü oku
image_path = r'C:\Users\safak\Desktop\yandan kirpilmis\30.jpg'
image = cv2.imread(image_path)

# Görüntüyü gri tonlamaya çevir
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gaussian düzeltme için kernel boyutu ve standart sapma ayarları
kernel_size = (5, 5)  # Kernel boyutu, örneğin (5, 5)
sigma = 1.0           # Gaussian dağılımının standart sapması

# Gaussian düzeltme uygula
smoothed_image = cv2.GaussianBlur(gray_image, kernel_size, sigma)

# Canny Edge Detection
edges = cv2.Canny(smoothed_image, 50, 150)  # Eşik değerlerini ihtiyacınıza göre ayarlayın

# Hough dönüşümü için parametre ayarları
rho = 1              # Dönüşüm parametre
theta = np.pi / 180  # Dönüşüm parametre
threshold = 30       # Eşik değeri
min_line_length = 100  # Minimum çizgi uzunluğu
max_line_gap = 5      # Maksimum boşluk

# Hough dönüşümü uygula
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

# Kenarları belirleyen çizgileri saklamak için boş bir liste oluştur
detected_edges = []

# Hough dönüşümü sonuçlarını orijinal görüntü üzerine çiz ve uygun kenarları kaydet
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
    # Kenarları saklama
    detected_edges.append(((x1, y1), (x2, y2)))

# Yatay kenarları filtrele
horizontal_edges = filter_edges_by_orientation(detected_edges, 'horizontal', angle_threshold=10)

# Dikey kenarları filtrele
vertical_edges = filter_edges_by_orientation(detected_edges, 'vertical', angle_threshold=10)

# Filtrelenmiş yatay kenarları ve dikey kenarları içeren dikdörtgeni çiz
rect_image = image.copy()

# Filtrelenmiş yatay kenarları içeren dikdörtgen
if horizontal_edges:
    min_x = min(min(p[0][0], p[1][0]) for p in horizontal_edges)
    max_x = max(max(p[0][0], p[1][0]) for p in horizontal_edges)
    min_y = min(min(p[0][1], p[1][1]) for p in horizontal_edges)
    max_y = max(max(p[0][1], p[1][1]) for p in horizontal_edges)
    cv2.rectangle(rect_image, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

# Filtrelenmiş dikey kenarları içeren dikdörtgen
if vertical_edges:
    min_x = min(min(p[0][0], p[1][0]) for p in vertical_edges)
    max_x = max(max(p[0][0], p[1][0]) for p in vertical_edges)
    min_y = min(min(p[0][1], p[1][1]) for p in vertical_edges)
    max_y = max(max(p[0][1], p[1][1]) for p in vertical_edges)
    cv2.rectangle(rect_image, (min_x, min_y), (max_x, max_y), (0, 0, 255), 2)

# Orijinal, kenarlar, düzeltilmiş ve filtrelenmiş görüntüyü göster
cv2.imshow('Filtered Horizontal and Vertical Edges with Rectangles', rect_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
