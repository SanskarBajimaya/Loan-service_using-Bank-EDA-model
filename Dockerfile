FROM python:3.12-slim

WORKDIR /app
COPY requirement.txt /app/requirement.txt
RUN pip install --no-cache-dir -r /app/requirement.txt

COPY app/ app/
COPY model/ model/
COPY scripts/ scripts/

ENV PYTHONUNBUFFERED=1
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# To run the docker:
#     Step 1: docker build build -t image_name .
#     Step 2: docker run --name container_name -p 8000:8000 image_name
