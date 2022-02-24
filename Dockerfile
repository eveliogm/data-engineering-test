FROM python:3.9-slim

WORKDIR /src
COPY ./src /src

RUN pip install -r /src/requirements.txt

ENTRYPOINT [ "python" , "app.py" ]
