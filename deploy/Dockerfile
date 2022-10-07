# sha256 as of 2022-09-13
FROM python:3.9-slim-bullseye@sha256:09c9438d7b13587df2b1b798d372442fb2bdda6cd408aa89dda2e995868c0b31 AS sphinx

ARG GIT_BRANCH=main
RUN apt-get -q update && apt-get -qy upgrade && apt-get -qy install git make latexmk texlive-latex-extra
COPY ./ .
RUN pip install -r requirements/requirements.txt
RUN deploy/build $GIT_BRANCH

# sha256 as of 2022-09-13
FROM nginx:mainline-alpine@sha256:2959a35e1b1e61e2419c01e0e457f75497e02d039360a658b66ff2d4caab19c4

COPY deploy/nginx.conf /etc/nginx
RUN mkdir -p /opt/nginx/run /opt/nginx/webroot/en/latest && chown -R nginx:nginx /opt/nginx

USER nginx
COPY --from=sphinx --chown=nginx:nginx build/latest/html/ /opt/nginx/webroot/en/latest/
COPY --from=sphinx --chown=nginx:nginx build/latest/latex/SecureDropDevDocs.pdf /opt/nginx/webroot/en/latest/
