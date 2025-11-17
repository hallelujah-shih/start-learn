FROM golang:1.24.3 AS builder

ENV GOPROXY=https://goproxy.cn,direct

WORKDIR /fetch
COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o /fetch/fetch
COPY ./google-chrome-stable_current_amd64.deb /

FROM debian:bookworm AS runtime

WORKDIR /fetch

# Create app user
RUN groupadd -r app && useradd -r -g app -d /home/app app && \
    mkdir -p /home/app && chown -R app:app /home/app

# Update sources list to use USTC mirror
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources

# DOCKER_BUILDKIT=1 docker build . -t fetch:latest
RUN --mount=type=bind,from=builder,source=/google-chrome-stable_current_amd64.deb,target=/tmp/google-chrome-stable_current_amd64.deb \
    apt-get update && \
    apt-get install -y --no-install-recommends /tmp/google-chrome-stable_current_amd64.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /fetch/fetch .
COPY --from=builder /fetch/stealth.min.js .

RUN chown app:app -R /fetch

USER app

CMD [ "./fetch", "-h" ]