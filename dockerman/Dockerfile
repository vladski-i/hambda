FROM debian:buster-slim

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade && apt install -y python3 docker.io python3-pip && python3 -m pip install Flask && python3 -m pip install docker

ADD ./dockerman-web /dockerman-web

ENV FLASK_APP=dockerman-web

WORKDIR /dockerman-web

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]