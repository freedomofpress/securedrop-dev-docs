# sha256 as of 2023-10-16
FROM python:3.9-slim-bullseye@sha256:b3415be51b8d2c8f35a6eb3db85e9ccdedf12beaa3b18ed4c2f769889717d02a as sphinx

ARG GIT_BRANCH=main
RUN apt-get -q update && apt-get -qy upgrade && apt-get -qy install git make latexmk texlive-latex-extra
COPY ./ .
RUN pip install poetry==1.7.1
RUN poetry install
RUN deploy/build $GIT_BRANCH

# sha256 as of 2023-10-16
FROM nginx:mainline-alpine-slim@sha256:1b0cb433e90260a96528c987ee78b797e842d510473935304a0931536d10f50d

COPY deploy/nginx.conf /etc/nginx
RUN mkdir -p /opt/nginx/run /opt/nginx/webroot/en/latest && chown -R nginx:nginx /opt/nginx

USER nginx
COPY --from=sphinx --chown=nginx:nginx build/latest/html/ /opt/nginx/webroot/en/latest/
COPY --from=sphinx --chown=nginx:nginx build/latest/latex/SecureDropDevDocs.pdf /opt/nginx/webroot/en/latest/
