FROM python:latest

RUN mkdir /app

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8061
CMD ["python", "main.py"]
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

#CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8060"]