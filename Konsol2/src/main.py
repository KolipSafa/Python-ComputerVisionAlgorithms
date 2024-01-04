import cv2
import numpy as np

def preprocess_image(image_path):
    # Görüntüyü oku ve gri tonlamaya çevir
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Gürültüyü azaltmak için Gauss filtresi uygula
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return blurred

def detect_lines(image):
    # Kenar tespiti için Canny kullan
    edges = cv2.Canny(image, 50, 150)

    # Hough dönüşümü ile doğru çizgileri tespit et
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)

    # Hough dönüşümü ile doğru çizgileri tespit et (probabilistic)
    # lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, minLineLength=50, maxLineGap=10)

    return lines

def draw_lines(image, lines):
    # Doğru çizgileri görüntü üzerine çiz
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    return image

def main(image_path):
    # Görüntüyü önişleme
    preprocessed_image = preprocess_image(image_path)

    # Doğru çizgileri tespit et
    lines = detect_lines(preprocessed_image)

    # Doğru çizgileri görüntü üzerine çiz
    result_image = draw_lines(preprocessed_image.copy(), lines)

    # Sonucu göster
    cv2.imshow('Detected Lines', result_image)
    cv2.imwrite("C:\\Users\\talha\\OneDrive\\Masaüstü\\Python-Programming-Lecture-Project\\Konsol2\\output\\result_deneme.png", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = 'C:\\Users\\talha\\OneDrive\\Masaüstü\\Python-Programming-Lecture-Project\\Konsol1\\input\\deneme.png'  # Görüntü dosya yolu
    main(image_path)
