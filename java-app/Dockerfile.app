FROM graalvm-java-maven-base AS builder

ADD . /app

WORKDIR /app

RUN mvn clean package

ENTRYPOINT /bin/sh