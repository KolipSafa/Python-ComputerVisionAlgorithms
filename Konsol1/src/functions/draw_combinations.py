import cv2

def draw_combinations(coords, image):
    print(coords)
    for i, coord in enumerate(coords):
        x, y = coord
        cv2.putText(image, f'C{i+1}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)