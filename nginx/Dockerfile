FROM nginx:latest as nginx
RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/nginx.conf
COPY app.conf  /etc/nginx/conf.d/default.conf