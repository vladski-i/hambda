FROM graalvm-java-maven-base AS builder

ADD . /app

WORKDIR /app

RUN mvn clean package && native-image -jar ./target/app*.jar

ENTRYPOINT /app/target/app-0.1