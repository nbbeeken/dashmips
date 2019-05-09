FROM python:3.7.3-stretch

COPY . /app
WORKDIR /app

RUN python -m pip install -r requirements.txt
RUN python setup.py install

CMD python -m dashmips run tests/mips/strings.mips
