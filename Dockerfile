FROM ubuntu:20.04

ENV TZ=America/US
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    git \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/conan-io/conan.git
WORKDIR /conan
RUN pip install -r conans/requirements.txt
RUN pip install -r conans/requirements_server.txt
RUN pip install gunicorn
RUN mkdir -p  /root/.conan_server
RUN mkdir -p  /root/.conan_server/data
COPY ./server.conf /root/.conan_server/server.conf
#CMD ["gunicorn","--bind", ":9300", "-w", "4", "-t", "300", "conans.server.server_launcher:app"]
CMD ["gunicorn","--bind", ":9300", "--log-level", "debug", "conans.server.server_launcher:app"]