FROM ubuntu:18.04 AS builder

RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get --no-install-recommends install -y curl git pkg-config build-essential

WORKDIR /openssl

COPY . .

RUN ./config && make && make install

FROM ubuntu:18.04

RUN tee /etc/ld.so.conf.d/myopenssl.conf <<EOF
/usr/local/lib
EOF

COPY --from=builder /usr/local  /usr/local

CMD ["bash", "-c",  "ldconfig && ldd /usr/local/bin/openssl" ]