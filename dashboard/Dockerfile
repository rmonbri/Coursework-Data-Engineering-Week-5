FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY .streamlit /app/.streamlit

COPY carl_linnaeus.jpeg .

COPY dashboard.py .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py"]

