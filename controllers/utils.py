def hamming_distance(v1, v2):
    if len(v1) != len(v2):
        return float('inf')
    return sum(a != b for a, b in zip(v1, v2))

def normalizar_vector(vector, largo=600):
    if len(vector) == largo:
        return vector
    elif len(vector) > largo:
        return vector[:largo]
    else:
        return vector + [0] * (largo - len(vector))