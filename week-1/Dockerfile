FROM python:3.10

RUN apt-get install wget

RUN useradd -ms /bin/bash datazoomcamp
USER datazoomcamp

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src/ .
COPY entrypoint.sh entrypoint.sh
ENTRYPOINT ["bash", "entrypoint.sh"]