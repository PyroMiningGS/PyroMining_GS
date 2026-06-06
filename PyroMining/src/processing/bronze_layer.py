from ingestion.inmet_collector import collect_data

def run():
    data = collect_data()

    print("Bronze Layer criada.")

    return data

if __name__ == "__main__":
    run()