FROM debian:8

# SIMULATE PI USER
RUN useradd -ms /bin/bash pi
WORKDIR /home/pi


RUN apt-get update && apt-get install -y most\
					 nginx \
					 git \
					 gunicorn \
					 supervisor \
					 python-pip \
					 python-dev \
					 gpsd \
					 gpsd-clients \
					 python-gps
					 #matchbox-window-manager \
					 #unclutter \
					 #chromium \
					 #x11-xserver-utils 

# forward request and error logs to docker log collector
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log


# RUN pip install Django==1.7 \
#		django-modeltranslation

# SUPERVISOR
RUN chmod 777 /var/log/gunicorn
COPY files/supervisor/supervisord.conf /etc/supervisor/conf.d/

# NGINX 
COPY files/nginx/paccotest.conf /etc/nginx/sites-available/
RUN rm -rf /etc/nginx/sites-enabled/default
RUN ln -s /etc/nginx/sites-available/paccotest.conf /etc/nginx/sites-enabled/paccotest.conf
RUN mkdir -p /var/www/paccotest/logs
RUN chmod 777 /var/www/paccotest/logs

# Copy scripts to make shell nicer
COPY files/homeScripts/ /root/



# JUST FOR DEBUG
RUN apt-get install -y curl netcat nano

# GIT
RUN git clone https://github.com/pacco-leo/Pacco-test/ /home/pi/Pacco-test/
ENV PACCO_DIR=/home/pi/Pacco-test/app
WORKDIR /home/pi/Pacco-test/
#RUN /home/pi/Pacco-test/djangoEnv/linux/bin/pip install -r requirements.txt
RUN pip install -r /home/pi/Pacco-test/requirements.txt

# Put DEBUG MODE 'ON'
RUN sed -i "s/IS_DEBUGGING = False/IS_DEBUGGING = True/g" /home/pi/Pacco-test/app/paccotest/views.py


ADD files/scripts/run.sh /run.sh
RUN chmod a+x /run.sh 
EXPOSE 22 80
ENTRYPOINT ["/run.sh"]



# gunicorn 
