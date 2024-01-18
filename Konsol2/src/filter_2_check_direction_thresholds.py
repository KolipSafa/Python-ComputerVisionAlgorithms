def filter_2_check_direction_thresholds(normalized_distances, DirectionThresL):
    _, Dir23, _, Dir41 = normalized_distances
    
    # Yönlendirme eşiğini kontrol et
    direction_condition = Dir23 < DirectionThresL and Dir41 < DirectionThresL
    
    return direction_condition