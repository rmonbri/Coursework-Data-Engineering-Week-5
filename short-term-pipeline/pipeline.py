"""Script to merge extract, transform and load scripts into a single pipeline"""

from extract import get_plant_data_multiprocessing, save_to_csv
from transform import read_data, save_clean_data_to_csv, read_csv_data, clean_data
from load import get_measurements_from_df, ingress_measurements_to_db, get_measurements_from_csv
from dotenv import load_dotenv


def local_pipeline():
    """Combining all scripts"""
    load_dotenv()
    plant_data = get_plant_data_multiprocessing()
    save_to_csv(plant_data, "data/plant-measurements.csv")
    final_data = read_csv_data("data/plant-measurements.csv")
    save_clean_data_to_csv(final_data)
    plant_measurements = get_measurements_from_csv()
    ingress_measurements_to_db(plant_measurements)


def lambda_handler(event, context):
    try:
        load_dotenv()
        print("Getting plant data from API")
        plant_data = get_plant_data_multiprocessing()
        print("Plant data extracted")
        print("Cleaning plant data")
        raw_data = read_data(plant_data)
        cleaned_data = clean_data(raw_data)
        print("Data cleaned")
        print("Inserting clean data to database")
        plant_measurements = get_measurements_from_df(cleaned_data)
        ingress_measurements_to_db(plant_measurements)
        print("Data inserted successfully")

        return {
            'statusCode': 200,
            'body': 'Pipeline completed successfully!'
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Pipeline failed with error: {str(e)}"
        }


if __name__ == "__main__":

    local_pipeline()
