FROM amazon/aws-lambda-python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY detect_anomalies.py send_email.py ./

CMD [ "send_email.lambda_handler" ]