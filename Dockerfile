FROM debian:latest

RUN apt-get -q update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -q install -y -o Dpkg::Options::="--force-confnew" --no-install-recommends \
        python3 python3-pip nginx supervisor

#   DEBIAN_FRONTEND="noninteractive" apt-get -q upgrade -y -o Dpkg::Options::="--force-confnew" --no-install-recommends
    
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
