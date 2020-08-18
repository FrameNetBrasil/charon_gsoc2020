FROM python:3.7
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils > /dev/null
RUN apt-get install -y build-essential tcl
RUN apt-get install -y systemd-sysv
RUN apt-get update  > /dev/null
RUN apt-get install  -y wget > /dev/null
RUN apt-get install  -y zip > /dev/null
RUN apt-get install  -y libaio1 > /dev/null
RUN apt-get update > /dev/null
RUN apt-get install  -y alien > /dev/null
RUN apt-get install -y libsm6 libxext6
RUN apt-get install -y libxrender-dev
RUN apt-get install -y python3-tk
RUN apt-get install -y libgirepository1.0-dev
WORKDIR /
RUN pip install --upgrade pip
COPY ./requirements.txt /var/www/html/public/server/requirements.txt
RUN pip install -r /var/www/html/public/server/requirements.txt