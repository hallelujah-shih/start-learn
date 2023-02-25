#!/bin/bash

SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"

set +x
# install lua pkg
# luarocks install lua-resty-http
# luarocks install lua-resty-logger-socket
# luarocks install lua-resty-dns

default_max_timeout=60
default_conn_timeout=5

download_url=""
dst_name=""
force_download () {
	if [[ ! -f "$dst_name" ]]; then
		while [[ true ]]
		do
			curl --connect-timeout ${default_conn_timeout} -m ${default_max_timeout} -fL ${download_url} -o ${dst_name}
			if [[ "$?" -eq 0 ]]; then
				break
			fi
			sleep 3
		done
	fi
}

set -x

# ndk download
download_url=https://github.com/vision5/ngx_devel_kit/archive/refs/tags/v0.3.1.tar.gz
dst_name=ndk.tar.gz
force_download
tar -xzf ndk.tar.gz
NGX_DEV_KIT_ROOT_DIR=ngx_devel_kit-0.3.1

# lua_ngx module
download_url=https://github.com/openresty/lua-nginx-module/archive/refs/tags/v0.10.22.tar.gz
dst_name=lua_ngx.tar.gz
force_download
tar -xzf lua_ngx.tar.gz
LUA_NGX_MODULE_ROOT_DIR=lua-nginx-module-0.10.22

# lua-resty-core
download_url=https://codeload.github.com/openresty/lua-resty-core/tar.gz/refs/tags/v0.1.24
dst_name=lua-resty-core.tar.gz
force_download
tar -xzf lua-resty-core.tar.gz
LUA_RESTY_CORE_ROOT_DIR=lua-resty-core-0.1.24
cd ${LUA_RESTY_CORE_ROOT_DIR} && make install
cd ${SRC_DIR}

# lua-resty-lrucache
download_url=https://github.com/openresty/lua-resty-lrucache/archive/refs/tags/v0.13.tar.gz
dst_name=lua-resty-lrucache.tar.gz
force_download
tar -xzf lua-resty-lrucache.tar.gz
LUA_RESTY_LRUCACHE_ROOT_DIR=lua-resty-lrucache-0.13
cd ${LUA_RESTY_LRUCACHE_ROOT_DIR} && make install
cd ${SRC_DIR}

# luajit2
download_url=https://github.com/openresty/luajit2/archive/refs/tags/v2.1-20220915.tar.gz
dst_name=luajit2.tar.gz
force_download
tar xvf luajit2.tar.gz
LUAJIT_DIR_NAME=luajit-2.1
LUAJIT_ROOT_DIR=luajit2-2.1-20220915
cd ${LUAJIT_ROOT_DIR}
make -j8 && make install
cd ${SRC_DIR}

# pre modify cfg
cat <<EOF >>${LUA_NGX_MODULE_ROOT_DIR}/config
echo '
#ifndef LUA_DEFAULT_PATH
#define LUA_DEFAULT_PATH "./?.lua;/usr/local/share/lua/5.1/?.lua;/usr/local/share/lua/5.1/?/init.lua;/usr/local/lib/lua/5.1/?.lua;/usr/local/lib/lua/5.1/?/init.lua;/usr/local/lib/lua/?.lua;/usr/local/lib/lua/?/init.lua;/usr/share/lua/5.1/?.lua;/usr/share/lua/5.1/?/init.lua"
#endif

#ifndef LUA_DEFAULT_CPATH
#define LUA_DEFAULT_CPATH "./?.so;/usr/local/lib/lua/5.1/?.so;/usr/local/lib/lua/?.so;/usr/lib/x86_64-linux-gnu/lua/5.1/?.so;/usr/lib/lua/5.1/?.so;/usr/local/lib/lua/5.1/loadall.so"
#endif
' >> "\$ngx_addon_dir/src/ngx_http_lua_autoconf.h"
EOF

# nginx
download_url=https://openresty.org/download/nginx-1.19.3.tar.gz
dst_name=nginx.tar.gz
force_download
tar -xzf nginx.tar.gz
NGX_ROOT_DIR=nginx-1.19.3

NGX_MOD_DIR=third_modules
mkdir -p ${NGX_ROOT_DIR}/${NGX_MOD_DIR}
cp ${NGX_DEV_KIT_ROOT_DIR} ${NGX_ROOT_DIR}/${NGX_MOD_DIR}/${NGX_DEV_KIT_ROOT_DIR} -r
cp ${LUA_NGX_MODULE_ROOT_DIR} ${NGX_ROOT_DIR}/${NGX_MOD_DIR}/${LUA_NGX_MODULE_ROOT_DIR} -r

cd ${NGX_ROOT_DIR}
export LUAJIT_INC=/usr/local/include/${LUAJIT_DIR_NAME}
export LUAJIT_LIB=/usr/local/lib
./configure --prefix=/var/www/html \
    --with-cc-opt="-g -O0" \
    --with-ld-opt="-Wl,-rpath,/usr/local/lib" \
    --sbin-path=/usr/sbin/nginx \
    --conf-path=/etc/nginx/nginx.conf \
    --http-log-path=/var/log/nginx/access.log \
    --error-log-path=/var/log/nginx/error.log \
    --with-pcre --with-pcre-jit \
    --lock-path=/var/lock/nginx.lock \
    --pid-path=/var/run/nginx.pid \
    --modules-path=/etc/nginx/modules \
    --with-stream \
    --with-stream_ssl_module \
    --with-stream_ssl_preread_module \
    --with-http_addition_module \
    --with-http_v2_module \
    --with-http_ssl_module \
    --with-http_realip_module \
    --with-http_auth_request_module \
    --with-http_gzip_static_module \
    --add-module=${NGX_MOD_DIR}/${NGX_DEV_KIT_ROOT_DIR} \
    --add-module=${NGX_MOD_DIR}/${LUA_NGX_MODULE_ROOT_DIR} \
    --add-module=../ngx_http_hello_module

make -j8 && make install
