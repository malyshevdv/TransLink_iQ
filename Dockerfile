FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL authors="denis"
WORKDIR /code

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./python /code

CMD ["fastapi", "run", "--port", "6678", "deviceEmulator.py"]