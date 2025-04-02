"""Script to merge extract, transform and load scripts into a single pipeline"""

from extract import get_plant_data_multiprocessing, save_to_csv
from transform import read_data, save_clean_data_to_csv
from load import get_measurements, ingress_measurements_to_db
from dotenv import load_dotenv


def pipeline():
    """Combining all scripts"""
    load_dotenv()
    plant_data = get_plant_data_multiprocessing()
    save_to_csv(plant_data, "data/plant-measurements.csv")
    final_data = read_data("data/plant-measurements.csv")
    save_clean_data_to_csv(final_data)
    plant_measurements = get_measurements()
    ingress_measurements_to_db(plant_measurements)


def lambda_handler(event, context):
    try:
        pipeline()
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

    pipeline()
