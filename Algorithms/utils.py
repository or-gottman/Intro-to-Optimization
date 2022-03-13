import random

def problemGenerator(nCities):
    matrix = []
    for i in range(nCities):
        distances = []
        for j in range(nCities):
            if j == i:
                distances.append(0)
            elif j < i:
                distances.append(matrix[j][i])
            else:
                distances.append(random.randint(10, 100))
        matrix.append(distances)
    return matrix