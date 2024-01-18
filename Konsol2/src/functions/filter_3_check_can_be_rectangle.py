import numpy as np

def filter_3_check_can_be_rectangle(horizontal_edges):
    top_left = find_top_left(horizontal_edges)
    bottom_right = find_bottom_right(horizontal_edges)
    return [top_left,bottom_right]

def find_top_left(coords):
    # Koordinatları numpy dizisine dönüştürün
    coords = np.array(coords)
    #x,y
    point = [coords[0,0],coords[0,1]]

    # En sol ve en üstteki koordinatı bulun
    for edge in coords:
        x1,y1,x2,y2 = edge
        if x1 <= point[0] and y1 < point[1]:
            point = [x1,y1]
        elif x2 <= point[0] and y2 < point[1]:
            point = [x2,y2]
    
    return point

def find_bottom_right(coords):
    # Koordinatları numpy dizisine dönüştürün
    coords = np.array(coords)
    #x,y
    point = [coords[0,2],coords[0,3]]

    # En sol ve en üstteki koordinatı bulun
    for edge in coords:
        x1,y1,x2,y2 = edge
        if x2 >= point[0] and y2 > point[1]:
            point = [x2,y2]
        elif x1 >= point[0] and y1 > point[1]:
            point = [x1,y1]
    
    return point