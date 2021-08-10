FROM graalvm-java-maven-base AS builder

ADD . /app

WORKDIR /app

RUN apt update && apt upgrade && apt install -y gcc build-essential libz-dev zlib1g-dev && \
    gu install native-image && mvn clean package && \
    native-image -jar ./target/app*.jar

ENTRYPOINT /bin/bash