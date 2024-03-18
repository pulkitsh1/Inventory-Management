FROM python:3-alpine3.19
RUN apk update && \
    apk add --no-cache mariadb-dev build-base
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV MYSQL_ROOT_PASSWORD=iamthe13002
ENV MYSQL_DATABASE=inventory
# ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=iamthe13002
EXPOSE 5000
CMD ["python", "./app.py"]
