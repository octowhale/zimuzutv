FROM python:3.6

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ENV IMAGE_VERSION 0.0.7
COPY . /root/zimuzutv/

WORKDIR /root/zimuzutv/
# CMD ["bash", "/root/zimuzutv/main.sh"]
ENTRYPOINT ["python","main.py"]
