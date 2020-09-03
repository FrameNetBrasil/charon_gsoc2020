FROM framenetbrasil/apache-php:v3.5.0

#ENV APACHE_DOCUMENT_ROOT /var/www/html
#RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
#RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf

ENV PATH="/var/www/html/src/server/FFmpeg:/var/www/html/src/server/FFmpeg/bin;/var/www/html/build/server/Tesseract-OCR:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils > /dev/null
RUN apt-get install -y software-properties-common

#RUN apt-get install -y python3.7
#RUN apt-get install -y python3-pip python3-dev python3-venv
#RUN apt-get install -y build-essential tcl
#RUN apt-get install -y systemd-sysv
#RUN apt-get update  > /dev/null
#RUN apt-get install  -y wget > /dev/null
#RUN apt-get install  -y zip > /dev/null
#RUN apt-get install  -y libaio1 > /dev/null
#RUN apt-get update > /dev/null
#RUN apt-get install  -y alien > /dev/null
#RUN apt-get install -y libsm6 libxext6
#RUN apt-get install -y libxrender-dev
#RUN apt-get install -y python3-tk
#RUN apt-get install -y libgirepository1.0-dev
#WORKDIR /
#RUN python3 -m pip install --upgrade pip
#RUN pip install --upgrade pip
#COPY ./requirements.txt /var/www/html/public/server/requirements.txt
#RUN pip install -r /var/www/html/public/server/requirements.txt

RUN add-apt-repository ppa:mc3man/trusty-media
RUN apt-get install -y nodejs npm
RUN apt-get install -y tesseract-ocr
RUN apt-get install -y ffmpeg
RUN npm i npm -g
#RUN apt-get -y install python3.7
#RUN apt-get -y install python-pip python-dev
#RUN pip install numpy matplotlib Keras tensorflow opencv-python scikit-learn scikit-image scipy argparse mysql-connector-python Pillow pickle-mixin glob3 Flask
#WORKDIR /var/www/html

#RUN npm install
#RUN npm run-script build


