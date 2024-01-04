#c1 c2 c3 c4 sırasıyla olacak
#burada hata olabilir hocaya sor
def filter_check_can_be_rectangle(coords):
    c1, c2, c3, c4 = coords
    x1, y1 = c1
    x2, y2 = c2
    x3, y3 = c3
    x4, y4 = c4
    if y1 > y2 and y4 > y3 and x4 > x1 and x3 > x2:
        return True
    else:
        return False

# coords = [[0, 0], [1, 1], [2, 2], [3, 3]]
# result = filter_check_can_be_rectangle(coords)
# print(result)