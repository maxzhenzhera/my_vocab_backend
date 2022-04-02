FROM nginx


WORKDIR /etc/nginx/conf.d

RUN rm default.conf

COPY my_vocab.conf .
COPY "./certs/backend.myvocab.com+3.pem" .
COPY "./certs/backend.myvocab.com+3-key.pem" .