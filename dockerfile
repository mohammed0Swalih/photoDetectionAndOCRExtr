# start with Python 3.10
FROM python:3.10-slim

# set working directory inside container
WORKDIR /app

# install tesseract
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng

# copy requirements first (for caching)
COPY requirements.txt .

# install python packages
RUN pip install -r requirements.txt

# copy rest of the code
COPY . .

# run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]