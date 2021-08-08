FROM debian:buster-slim

ARG ARCH=aarch64

ARG GRAALVM_VERSION=21.2.0

ARG MAVEN_VERSION=3.8.1

ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade && apt install -y wget

RUN wget https://github.com/graalvm/graalvm-ce-builds/releases/download/vm-${GRAALVM_VERSION}/graalvm-ce-java11-linux-${ARCH}-${GRAALVM_VERSION}.tar.gz 

RUN tar -xzvf graalvm-ce-java11-linux-${ARCH}-${GRAALVM_VERSION}.tar.gz

ENV JAVA_HOME=/graalvm-ce-java11-${GRAALVM_VERSION}

ENV PATH=$PATH:/graalvm-ce-java11-${GRAALVM_VERSION}/bin

RUN wget https://downloads.apache.org/maven/maven-3/${MAVEN_VERSION}/binaries/apache-maven-${MAVEN_VERSION}-bin.tar.gz

RUN tar -xzvf ./apache-maven-${MAVEN_VERSION}-bin.tar.gz

ENV M2_HOME=/apache-maven-${MAVEN_VERSION}/

ENV PATH=$PATH:/apache-maven-${MAVEN_VERSION}/bin

ENTRYPOINT ['java', '-version']