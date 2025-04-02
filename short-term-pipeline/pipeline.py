# pylint: disable= broad-exception-caught
"""Script to merge extract, transform and load scripts into a single pipeline"""
import logging
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


def handler(event, context):
    """Lambda Handler to add measurements to db"""
    logging.info('Event: %s', event)
    logging.info('Context: %s', context)
    try:
        load_dotenv()
        logging.info("Getting plant data from API")
        plant_data = get_plant_data_multiprocessing()
        logging.info("Plant data extracted")
        logging.info("Cleaning plant data")
        raw_data = read_data(plant_data)
        logging.info("Created DataFrame")
        cleaned_data = clean_data(raw_data)
        logging.info("Data cleaned")
        logging.info("Inserting clean data to database")
        plant_measurements = get_measurements_from_df(cleaned_data)
        ingress_measurements_to_db(plant_measurements)
        logging.info("Data inserted successfully")

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
