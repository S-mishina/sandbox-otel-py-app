# Dockerfile
FROM python:3.13
RUN apt update && apt install -y python3-dev && apt install -y build-essential
RUN pip install requests
RUN pip install flask
RUN pip install joblib
COPY main.py main.py
# CMD ["python", "main.py"]
