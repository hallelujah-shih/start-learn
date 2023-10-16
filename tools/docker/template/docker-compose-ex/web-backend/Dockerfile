FROM golang:alpine as builder

WORKDIR /web-backend
ENV GOPROXY=https://goproxy.cn,direct

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o backend


FROM alpine

WORKDIR /web-backend

COPY --from=builder /web-backend/backend .
CMD [ "/web-backend/backend"]
