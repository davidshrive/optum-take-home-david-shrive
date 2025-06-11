FROM python:latest
COPY script.py ./
CMD ["python", "./script.py"]

## Need to add input/output dir