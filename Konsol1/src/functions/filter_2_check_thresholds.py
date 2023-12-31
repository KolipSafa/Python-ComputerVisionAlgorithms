def filter_2_check_thresholds(normalized_distances, HeightTreshL, HeightTreshH, WidthTreshL, WidthTreshH):
    Siz12, Siz23, Siz34, Siz41 = normalized_distances
    if (HeightTreshL < Siz12 < HeightTreshH) and (HeightTreshL < Siz34 < HeightTreshH) and (WidthTreshL < Siz23 < WidthTreshH) and (WidthTreshL < Siz41 < WidthTreshH):
        return True
    else:
        return False

# normalized_distances = [0.025, 0.025, 0.0125, 0.01]
# result = filter_1_check_thresholds(normalized_distances, 0.5, 1.5, 0.5, 1.5)