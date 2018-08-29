FROM python:3.6-alpine

ENV FLASK_APP n0blog.py
ENV FLASK_CONFIG development
ENV POSTS_PATH /posts

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories
RUN apk update
RUN apk add postgresql-libs
RUN apk add --virtual .build-deps gcc musl-dev postgresql-dev

RUN adduser -D n0blog
USER n0blog

WORKDIR /home/n0blog

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

#COPY app app
VOLUME /home/n0blog/app
VOLUME /posts
#COPY migrations migrations
#VOLUME /home/n0blog/migrations
COPY n0blog.py config.py boot.sh ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
	
