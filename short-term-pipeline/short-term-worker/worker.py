"""Lambda function to retrieve plant data from API for given ID"""
import logging
import json
import uuid
import boto3

logger = logging.getLogger()
logger.setLevel("INFO")

PLANT_COUNT = 51


def get_plant_data_lambda():
    """Function to get all the plant measurements using multiple lambdas"""

    lambda_client = boto3.client('lambda')

    for plant_id in range(PLANT_COUNT):
        payload = {
            'plant_id': plant_id,
            'task_id': str(uuid.uuid4())
        }

        lambda_client.invoke(
            FunctionName='arn:aws:lambda:eu-west-2:129033205317:function:c16-louis-measurements-etl',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        logger.info("Created lambda %s for plant %s",
                    payload['task_id'], payload['plant_id'])


def handler(event, context):
    """Lambda handler for HTTP requests"""
    logger.info("Event: %s", event)
    logger.info("Context: %s", context)
    # plant_id = event.get('plant_id')
    get_plant_data_lambda()

    return {'status': 200}


if __name__ == '__main__':
    handler(None, None)
