FROM python:3.14

WORKDIR /server

COPY ./requirements.txt /server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /server/requirements.txt

COPY ./app /server/app

CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
