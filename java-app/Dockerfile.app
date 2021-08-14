FROM graalvm-builder AS builder

ARG DEBIAN_FRONTEND=noninteractive

COPY . /app

WORKDIR /app

RUN mvn clean package && \
    native-image -jar ./target/app*.jar

# ENTRYPOINT /bin/sh
FROM alpine:latest

WORKDIR /

COPY --from=builder /app/target/app-0.1.jar /app

ENTRYPOINT /bin/sh