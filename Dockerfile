# Dockerfile
FROM python:3.13
COPY main.py main.py
RUN pip install requests
RUN pip install flask
CMD ["python", "main.py"]
