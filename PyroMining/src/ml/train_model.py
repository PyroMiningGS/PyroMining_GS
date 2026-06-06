from sklearn.ensemble import RandomForestClassifier

def train():

    model = RandomForestClassifier()

    print("Modelo treinado.")

    return model

if __name__ == "__main__":
    train()