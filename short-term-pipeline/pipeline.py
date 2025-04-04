# pylint: disable= broad-exception-caught
"""Script to merge extract, transform and load scripts into a single pipeline"""
import logging
from extract import get_plant_data_multiprocessing
from transform import read_data, clean_data
from load import get_measurements_from_df, ingress_measurements_to_db
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)


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
    handler(None, None)
