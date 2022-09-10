From traefik:v2.8
WORKDIR /etc/traefik/
COPY static.yml ./static.yml
COPY configs ./configs
RUN sed -i 's/acme-staging/acme/g' ./static.yml && mkdir /etc/traefik/acme && chmod 600 /etc/traefik/acme
EXPOSE 80
EXPOSE 443
