#c1 c2 c3 c4 sırasıyla olacak
#burada hata olabilir hocaya sor
def filter_check_can_be_rectangle(coords):
    # Sort the points by x-coordinate and then by y-coordinate   
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4
    # print("x1: ", x1, "y1: ", y1)
    # print("x2: ", x2, "y2: ", y2)
    # print("x3: ", x3, "y3: ", y3)
    # print("x4: ", x4, "y4: ", y4)
    # Check if the points form a rectangle
    if y1 > y2 and y4 > y3 and x4 > x1 and x3 > x2:
        return True
    else:
        return False

# coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
# result = filter_check_can_be_rectangle(coords)
# print(result)