FROM python:3.6

RUN pip install \
    pytest==3.3.0

RUN mkdir /usr/src/code
COPY . /usr/src/code
WORKDIR /usr/src/code
RUN pip install .

CMD pytest
