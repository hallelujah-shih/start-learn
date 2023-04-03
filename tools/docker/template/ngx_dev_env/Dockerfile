FROM ubuntu:18.04 as builder

WORKDIR /nginx

RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y build-essential gdb curl libpcre3 libpcre3-dev zlib1g zlib1g-dev libssl-dev libgd-dev libxml2 libxml2-dev uuid-dev lua-cjson-dev luarocks

# RUN git config --global --add safe.directory '*'

COPY . .

RUN bash ./auto_build.sh

# FROM ubuntu:18.04

# WORKDIR /etc/nginx

# RUN sed -i 's@//.*archive.ubuntu.com@//mirrors.ustc.edu.cn@g' /etc/apt/sources.list
# RUN sed -i 's/security.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

# RUN apt-get update && apt-get install --no-install-recommends -y libssl1.1 luarocks

# COPY --from=builder /usr/local/lib/libluajit-5.1.so.2 /usr/local/lib/libluajit-5.1.so.2
# COPY --from=builder /usr/local/lib/lua /usr/local/lib/lua
# COPY --from=builder /var/www/html /var/www/html
# COPY --from=builder /var/log/nginx /var/log/nginx
# COPY --from=builder /usr/sbin/nginx /usr/sbin/nginx
# COPY --from=builder /etc/nginx /etc/nginx

CMD [ "/usr/sbin/nginx", "-g", "daemon off;" ]
