import cv2

def draw_rectangle(img, top_left,bottom_right):
    en_sol, en_ust = top_left
    en_sag, en_alt = bottom_right
    img = cv2.rectangle(img, (en_sol, en_ust), (en_sag, en_alt), (0, 255, 255), 5)
    return img