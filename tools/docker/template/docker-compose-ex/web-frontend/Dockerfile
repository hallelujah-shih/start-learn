FROM golang:alpine as builder

WORKDIR /web-frontend
ENV GOPROXY=https://goproxy.cn,direct

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o frontend


FROM alpine

WORKDIR /web-frontend

COPY --from=builder /web-frontend/frontend .
CMD [ "/web-frontend/frontend"]
