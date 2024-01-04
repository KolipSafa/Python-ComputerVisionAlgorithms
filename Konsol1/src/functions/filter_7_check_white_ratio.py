import cv2
import numpy as np

def filter_7_check_white_ratio(coords, image):
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4

    # Koordinatları düzenle
    x_coords = [x1, x2, x3, x4]
    y_coords = [y1, y2, y3, y4]

    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    # Dikdörtgenin içindeki pikselleri seç
    roi = image[y_min:y_max, x_min:x_max]

    # Beyaz renk için alt ve üst sınır
    lower_white = np.array([180, 180, 180], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    # Belirli bir renk aralığındaki pikselleri maskele
    white_mask = cv2.inRange(roi, lower_white, upper_white)

    # Beyaz olan pikselleri say
    white_pixels = np.count_nonzero(white_mask)

    # ROI içindeki toplam piksel sayısı
    total_pixels = roi.shape[0] * roi.shape[1]

    # Beyaz piksellerin oranı
    white_ratio = white_pixels / total_pixels

    # %80 beyaz olup olmadığını kontrol et
    if white_ratio >= 0.8:
        return True
    else:
        return False


