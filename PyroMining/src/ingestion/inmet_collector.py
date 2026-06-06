import pandas as pd

def collect_data():
    """ Simulação de coleta de dados meteorológicos. """
    print("Coletando dados meteorológicos...")

    data = pd.DataFrame({
        "temperature": [32, 35, 30],
        "humidity": [45, 30, 55],
        "rainfall": [0, 0, 5]
        })
    
    return data

if __name__ == "__main__":
    df = collect_data()
    print(df.head())