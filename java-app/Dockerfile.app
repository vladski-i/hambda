FROM graalvm-java-maven-base AS builder

ADD . /app

WORKDIR /app

RUN apt update && apt upgrade && apt install -y gcc && \
    gu install native-image && mvn clean package && \
    native-image -jar ./target/app*.jar

ENTRYPOINT /app/target/app-0.1