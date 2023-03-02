FROM golang:alpine as builder

ENV GOPROXY=https://goproxy.cn,direct

WORKDIR /hello
COPY . .
RUN go build

FROM alpine

COPY --from=builder /hello/hello /hello
ENTRYPOINT [ "/hello" ]
