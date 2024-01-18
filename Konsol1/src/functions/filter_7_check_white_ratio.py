import cv2
import numpy as np

def filter_7_check_white_ratio(image, coords):
    

    # Koordinatları al
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4

    # Dikdörtgen sınırlarını belirle
    x_min = min(x1, x2, x3, x4)
    x_max = max(x1, x2, x3, x4)
    y_min = min(y1, y2, y3, y4)
    y_max = max(y1, y2, y3, y4)

    # Dikdörtgeni kırp
    cropped_region = image[y_min:y_max, x_min:x_max]

    # Beyaz pikselleri say
    white_pixel_count = np.sum(cropped_region >= 170)

    # Toplam piksel sayısı
    total_pixel_count = cropped_region.size
    # Dir12 = np.arctan([np.abs(x2 - x1)/(np.abs(y2 - y1)+5)])[0] * 180 / np.pi
    # Dir23 = np.arctan([np.abs(x3 - x2)/(np.abs(y3 - y2)+5)])[0] * 180 / np.pi
    # Dir34 = np.arctan([np.abs(x4 - x3)/(np.abs(y4 - y3)+5)])[0] * 180 / np.pi
    # Dir41 = np.arctan([np.abs(x1 - x4)/(np.abs(y1 - y4)+5)])[0] * 180 / np.pi
    # print(Dir12)
    # print(Dir23)
    # print(Dir34)
    # print(Dir41)
    # Beyaz piksellerin yüzdesini hesapla
    white_pixel_percentage = (white_pixel_count / total_pixel_count) * 100
    if white_pixel_percentage > 0.6:
        return True
    else:
        return False
    