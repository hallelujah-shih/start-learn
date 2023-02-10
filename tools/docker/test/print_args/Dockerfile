FROM golang:alpine as builder

WORKDIR /print_args

COPY go.mod .
COPY main.go .

RUN go build -o print

FROM alpine

COPY --from=builder /print_args/print /print

ENTRYPOINT [ "/print" ]

CMD [ "-from-docker-file-cmd" ]