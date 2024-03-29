FROM ubuntu:18.04

RUN apt-get -qq update
RUN apt-get install -qq -y python3-pip python3-dev 
RUN pip3 install --upgrade pip

ENV APP_DIR=/app/sudoku/
COPY . $APP_DIR
WORKDIR $APP_DIR

RUN pip install -e .
