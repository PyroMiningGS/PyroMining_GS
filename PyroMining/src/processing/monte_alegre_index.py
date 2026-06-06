def calculate_monte_alegre(temp, humidity):
    """ Cálculo simplificado do índice de Monte Alegre . """
    return temp * (100 - humidity)

if __name__ == "__main__":
    result = calculate_monte_alegre(35, 30)
    print(result)

