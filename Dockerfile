FROM python:3.6

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /root/zimuzutv/
CMD ["bash", "/root/zimuzutv/main.sh"]
