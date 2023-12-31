def filter_6_check_size_ratio(normalized_distances, HWTreshL,HWTreshH):
    Siz12, Siz23, Siz34, Siz41 = normalized_distances
    #yatay/dikey
    ratio = (Siz23 + Siz41) /(Siz12 + Siz34)

    if HWTreshL < ratio < HWTreshH:
        return True
    else:
        return False


