def filter_5_check_height_width_ratio(normalized_distances, HWThresL, HWThresH):
    Siz12, Siz23, Siz34, Siz41 = normalized_distances
    
    # Yükseklik ve genişlik oranını kontrol et
    ratio = (Siz12 + Siz34) / (Siz23 + Siz41)
    ratio_condition = HWThresL < ratio < HWThresH
    
    return ratio_condition