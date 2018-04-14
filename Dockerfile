FROM debian:latest

RUN apt update && \
    apt install python3 python3-pip -y && \
    apt install nginx supervisor -y 

RUN pip3 install uwsgi

COPY ./requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./nginx.conf /etc/nginx/sites-enabled/default
COPY ./ /server
COPY supervisord.conf /etc/supervisor/supervisord.conf

RUN update-rc.d -f nginx disable

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/usr/bin/supervisord"]
