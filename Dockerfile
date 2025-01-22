# Dockerfile
FROM python:3.12
RUN apt update && apt install -y python3-dev && apt install -y build-essential
RUN pip install requests
RUN pip install flask
COPY main.py main.py
# CMD ["python", "main.py"]
