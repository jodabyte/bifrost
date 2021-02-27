FROM python:3.7-buster

RUN apt-get update 
RUN apt-get install -y portaudio19-dev libatlas-base-dev

COPY asr/requirements.txt /tmp/
COPY libs/snowboy-1.3.0-py3.7-none-any.whl /tmp/
COPY libs/apa102-pi_2.4.1 /tmp/apa102-pi
RUN pip install -r /tmp/requirements.txt

WORKDIR /bifrost
COPY configs configs/
COPY resources resources/
COPY pycommons pycommons/
COPY asr/src asr/
ENV PYTHONPATH=/bifrost

CMD [ "python", "asr/asr.py" ]
