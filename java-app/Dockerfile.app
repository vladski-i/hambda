FROM graalvm-builder AS builder

ARG DEBIAN_FRONTEND=noninteractive

COPY . /app

WORKDIR /app

RUN mvn clean package && \
    native-image -jar ./target/app*.jar

# ENTRYPOINT /bin/sh
FROM ubuntu:latest

WORKDIR /

COPY --from=builder /app/app-0.1 /app

ENTRYPOINT /app