# NGINX http 2.0环境搭建
```
nginx > 1.9.5 (ngx_http_v2_module)
openssl >= 1.0.2 (需要对ALPN的支持)
```

## 搭建nginx_lua环境
```
准备测试环境
```

### nginx编译
```
准备工作：
系统ubuntu 14.04, gcc等编译套件, 下载nginx 1.10.1, openssl 1.0.2, lua-nginx-module 0.10.5, ngx_devel_kit 0.3.0

luajit 2.0.2
> tar xzvf LuaJIT-2.0.2.tar.gz
> cd LuaJIT-2.0.2 && make && make install
> export LUAJIT_LIB=/usr/local/lib
> export LUAJIT_INC=/usr/local/include/luajit-2.0

openssl(如果需要使用这个客户端的)
> tar xzvf openssl-1.0.2h.tar.gz
> cd openssl-1.0.2h && ./config
> make depend && make -j 4
> make test
> make install 

nginx 1.10.1
> tar xzvf nginx-1.10.1.tar.gz
> cd nginx-1.10.1
> ./configure --prefix=/opt/nginx --with-openssl=../openssl-1.0.2h/ --with-http_ssl_module --with-http_v2_module --add-module=../ngx_devel_kit-0.3.0 --add-module=../lua-nginx-module-0.10.5 --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --pid-path=/var/run/nginx.pid --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --user=nginx --group=nginx
> make -j 4
> make install
> nginx -V
```

### 自签名证书制作
```
> openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
> openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
```

### 配置并测试nginx h2 & lua
```
self-signed.conf
内容如下:
ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

ssl-params.conf
内容见下面外网h2服务配置
```

## 搭建一个外网的源站(我的网站start-learn.win)
```
centos 7
nginx 1.10.1, libressl 2.4.2, joomla
```

### 编译nginx
```
> ./configure --with-http_v2_module --with-http_ssl_module --prefix=/usr --sbin-path=/usr/sbin/nginx --pid-path=/var/run/nginx.pid --conf-path=/etc/nginx/nginx.conf --user=nginx --group=nginx

> make -j 4 && make install

系统增加nginx组和用户
> groupadd -f nginx
> useradd -g nginx nginx
```

### 安装Mariadb
```
> yum -y install mariadb-server mariadb
> systemctl start mariadb
> mysql_secure_installation
> systemctl enable mariadb

如果只是单机使用，可以在防火墙上限制访问，还可以listen localhost
my.conf 
[mysqld]
bind-address=127.0.0.1
```

### 安装PHP
```
> yum install php php-mysql php-fpm

> vi /etc/php.ini

  cgi.fix_pathinfo=0

> vi /etc/php-fpm.d/www.conf
  listen = /var/run/php-fpm/php-fpm.sock

  listen.owner = nobody
  listen.group = nobody

  user = nginx
  group = nginx

> systemctl enable php-fpm
> systemctl start php-fpm
```

### 安装joomla
```
目录暂时定为/var/www/start-learn.win
> unzip -q Joomla*.zip -d /var/www/start-learn.win
目录权限改变为php-fpm中配置的user,group
> chown -R nginx:nginx /var/www/start-learn.win
> chmod -R 755 /var/www/start-learn.win
```

### 配置nginx
```
start-learn.win.conf
内容如下:
server {
    listen 80 default_server;
    server_name start-learn.win www.start-learn.win;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2 default_server;
    server_name start-learn.win www.start-learn.win;

    include ssl-start-learn.win.conf;
    include ssl-params.conf;

    root   /var/www/start-learn.win;
    index  index.php index.html index.htm default.html default.htm;

    location / {
        try_files $uri $uri/ /index.php?$args;
    }

    location ~* /(images|cache|media|logs|tmp)/.*\.(php|pl|py|jsp|asp|sh|cgi)$ {
        return 403;
        error_page 403 /403_error.html;
    }

    location ~ \.php$ {
        fastcgi_pass  127.0.0.1:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include /etc/nginx/fastcgi.conf;
    }

    location ~* \.(ico|pdf|flv)$ {
        expires 1y;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|swf|xml|txt)$ {
        expires 14d;
    }

    access_log  /var/log/nginx/start-learn.win.access.log  main;
}


ssl-start-learn.win.conf
内容如下：
ssl_certificate /etc/letsencrypt/live/start-learn.win/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/start-learn.win/privkey.pem;


ssl-params.conf
内容如下：
# from https://cipherli.st/
# and https://raymii.org/s/tutorials/Strong_SSL_Security_On_nginx.html

ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
ssl_prefer_server_ciphers on;
ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";
ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0
ssl_session_cache shared:SSL:10m;
ssl_session_tickets off; # Requires nginx >= 1.5.9
ssl_stapling on; # Requires nginx >= 1.3.7
ssl_stapling_verify on; # Requires nginx => 1.3.7
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;

# openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
ssl_dhparam /etc/ssl/certs/dhparam.pem;
```

### 使用letsencrypt做证书签名
```
修改nginx.conf，增加location并启动nginx
server {
    listen 80;
    server_name localhost;

    location ~/.well-known {
        root /var/www/start-learn.win;
        allow all;
    }
}

> git clone https://github.com/letsencrypt/letsencrypt /opt/letsencrypt
> cd /opt/letsencrypt
> ./letsencrypt-auto certonly -a webroot --webroot-path=/var/www/start-learn.win -d start-learn.win -d www.start-learn.win
> openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

注意.注意.注意 在用letsencrypt的时候如果执行的时候由于py通信问题，记得切换pip的源
我的配置如下
$HOME/.config/pip/pip.conf

[global]
timeout = 60
index-url = https://pypi.doubanio.com/simple/
trusted-host = pypi.doubanio.com
```


## 名词解释
```
ALPN(Application Layer Protocol Negotiation) 
    ClientHello携带着ALPN的extension进行应用层协议的协商（详见rfc7301）
```

## REFERENCE
1. [自签名证书生成](https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-nginx-in-ubuntu-16-04)
2. [letsencrypt生成证书](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04)
3. [ngix with h2 support](https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-with-http-2-support-on-ubuntu-16-04)
4. [install joomla on centos 7](https://www.unixmen.com/install-joomla-cms-centos-7/)
5. [implementing h2 in production env](https://blog.newrelic.com/2016/02/17/http2-production/)
