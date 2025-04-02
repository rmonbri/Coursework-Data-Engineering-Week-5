FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY extract.py transform.py load.py pipeline.py ./

CMD [ "pipeline.lambda_handler" ]