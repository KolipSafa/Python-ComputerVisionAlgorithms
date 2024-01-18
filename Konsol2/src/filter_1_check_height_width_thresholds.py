def filter_1_check_height_width_thresholds(normalized_distances, HeightThresL, HeightThresH, WidthThresL, WidthThresH):
    Siz12, Siz23, Siz34, Siz41 = normalized_distances
    
    # Yükseklik ve genişlik sınırlarını kontrol et
    height_condition = HeightThresL < Siz12 < HeightThresH and HeightThresL < Siz34 < HeightThresH
    width_condition = WidthThresL < Siz23 < WidthThresH and WidthThresL < Siz41 < WidthThresH
    
    if height_condition and width_condition:
        return True
    else:
        return False