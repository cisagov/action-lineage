ARG GIT_COMMIT=unspecified
ARG GIT_REMOTE=unspecified
ARG VERSION=unspecified

FROM python:alpine

ARG GIT_COMMIT
ARG GIT_REMOTE
ARG VERSION

LABEL org.opencontainers.image.authors="@felddy"
LABEL org.opencontainers.image.licenses="CC0-1.0"
LABEL org.opencontainers.image.revision=${GIT_COMMIT}
LABEL org.opencontainers.image.source=${GIT_REMOTE}
LABEL org.opencontainers.image.title="Lineage GitHub Action"
LABEL org.opencontainers.image.vendor="Cyber and Infrastructure Security Agency"
LABEL org.opencontainers.image.version=${VERSION}

COPY . ./
RUN pip install -r requirements.txt
ENTRYPOINT ["/src/entrypoint.py"]
