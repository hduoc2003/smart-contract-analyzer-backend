FROM ubuntu:latest
LABEL image.author="ppppHHHuuuu"

RUN apt-get update && apt-get install -y apache2 \
libapache2-mod-wsgi-py3 \
python3 \
python3-pip \
curl \
&& apt-get clean \
&& apt-get autoremove \
&& rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/node-v18.17.0-linux-x64/bin:${PATH}"
RUN curl https://nodejs.org/dist/v18.17.0/node-v18.17.0-linux-x64.tar.gz | tar xzf - -C /opt/
# TODO: DONE
# RUN curl -fsSL https://get.docker.com | sh

# ENV OF BACKEND
ENV ENVIRONMENT=production
ENV PORT=80
ENV MONGO_CONNECTION_STRING=mongodb+srv://shodydosh:dT8NJQfeB25rAtj@cluster0.l96vywb.mongodb.net/
ENV DATABASE_NAME=TOOL

# COPY FOR CONFIG
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
#COPY files from frontend, backend UBUNTU to DOCKER 
COPY ./ /var/www/apache-flask/

RUN mv /var/www/apache-flask/app/build /var/www/apache-flask/
# RUN chmod -R 666 /var/run/docker.sock

# install requirement for BE   
RUN pip install -r /var/www/apache-flask/app/requirements.txt
RUN a2dissite 000-default.conf
RUN a2ensite apache-flask.conf
RUN a2enmod headers
RUN echo 'ServerName localhost' >> /etc/apache2/apache2.conf
    

# RUN front end
RUN cd /var/www/apache-flask/front-end/smart-contract-analyzer-frontend/ && npm install && npm run build

RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
ln -sf /proc/self/fd/1 /var/log/apache2/error.log


# ... (các bước cài đặt khác)

# Sao chép script vào image
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Thiết lập script làm entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Các bước cài đặt và cấu hình ứng dụng của bạn
# ...

EXPOSE 80

WORKDIR /var/www/apache-flask

CMD /usr/sbin/apache2ctl -D FOREGROUND

