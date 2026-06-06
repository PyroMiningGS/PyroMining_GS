from processing.monte_alegre_index import calculate_monte_alegre

def enrich(df):

    df["nesterov"] = df.apply(
        lambda row: calculate_nesterov(
            row["temperature"],
            row["humidity"]
            ),
            axis=1
            )
    
    print("Gold Layer criada.")

    return df