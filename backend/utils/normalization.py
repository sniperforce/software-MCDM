import numpy as np

def vector_normalization(matrix):
    """"Vectorial normalization (euclidean)"""
    norms = np.sqrt(np.sum(matrix**2,axis=0))
    norms[norms == 0] = 1 #Avoid division by zero
    return matrix / norms

def linear_normalization(matrix, is_benefit):
    """Linear normalization (Max-Min)"""
    normalized = np.zeros_like(matrix, dtype=float)

    for j in range(matrix.shape[1]):
        col = matrix[:, j]
        col_min = np.min(col)
        col_max = np.max(col)

        if col_max == col_min:
            normalized[:, j] = 1 if is_benefit[j] else 0
        else:
            if is_benefit[j]:
                #For benefit criterian, bigger is better
                normalized[:, j] = (col - col_min) / (col_max - col_min)
            else:
                #For cost criteria, smaller is better
                normalized[:, j] = (col_max - col) / (col_max - col_min)
    
    return normalized
