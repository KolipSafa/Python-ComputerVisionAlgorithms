def filter_4_check_parallel_threshold(normalized_distances, ParallelThres):
    Dir12, _, Dir34, _ = normalized_distances
    
    # Paralellik eşiğini kontrol et
    parallel_condition = abs(Dir12 - Dir34) < ParallelThres
    
    return parallel_condition