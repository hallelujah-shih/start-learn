#!/bin/bash

BUILD_CPU=8

NGX_NAME=nginx
NGX_VER=1.19.3
LUAJIT_NAME=luajit2
LUAJIT_VER=2.1-20220915
NGX_DEV_KIT_NAME=ngx_devel_kit
NGX_DEV_KIT_VER=0.3.1
LUA_NGX_MODULE_NAME=lua-nginx-module
LUA_NGX_MODULE_VER=0.10.22
LUA_RESTY_CORE_NAME=lua-resty-core
LUA_RESTY_CORE_VER=0.1.24
LUA_RESTY_LRUCACHE_NAME=lua-resty-lrucache
LUA_RESTY_LRUCACHE_VER=0.13
PCRE_NAME=pcre
PCRE_VER=8.45
ZLIB_NAME=zlib
ZLIB_VER=1.2.11
OPENSSL_NAME=openssl
OPENSSL_VER=1.1.1q

default_max_timeout=60
default_conn_timeout=5

download_url=""
dst_name=""
decompress_dir_name=""
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

check_and_extra_tar () {
	if [[ -f "$dst_name" ]]; then
		tar ztf "$dst_name" > /dev/null 2>&1
		if [[ "$?" -ne 0 ]]; then
			force_download
		fi
	else
		force_download
	fi
	rm -rf ${decompress_dir_name}
	tar -xzf ${dst_name}
}

set -x

download_url=https://openresty.org/download/${NGX_NAME}-${NGX_VER}.tar.gz
decompress_dir_name=${NGX_NAME}-${NGX_VER}
NGX_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://github.com/openresty/${LUAJIT_NAME}/archive/refs/tags/v${LUAJIT_VER}.tar.gz
decompress_dir_name=${LUAJIT_NAME}-${LUAJIT_VER}
LUAJIT_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://github.com/vision5/ngx_devel_kit/archive/refs/tags/v${NGX_DEV_KIT_VER}.tar.gz
decompress_dir_name=${NGX_DEV_KIT_NAME}-${NGX_DEV_KIT_VER}
NGX_DEV_KIT_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://github.com/openresty/lua-nginx-module/archive/refs/tags/v${LUA_NGX_MODULE_VER}.tar.gz
decompress_dir_name=${LUA_NGX_MODULE_NAME}-${LUA_NGX_MODULE_VER}
LUA_NGX_MODULE_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://codeload.github.com/openresty/lua-resty-core/tar.gz/refs/tags/v${LUA_RESTY_CORE_VER}
decompress_dir_name=${LUA_RESTY_CORE_NAME}-${LUA_RESTY_CORE_VER}
LUA_RESTY_CORE_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://github.com/openresty/lua-resty-lrucache/archive/refs/tags/v${LUA_RESTY_LRUCACHE_VER}.tar.gz
decompress_dir_name=${LUA_RESTY_LRUCACHE_NAME}-${LUA_RESTY_LRUCACHE_VER}
LUA_RESTY_LRUCACHE_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://udomain.dl.sourceforge.net/project/pcre/pcre/${PCRE_VER}/${PCRE_NAME}-${PCRE_VER}.tar.gz
# download_url=https://downloads.sourceforge.net/project/pcre/pcre/${PCRE_VER}/${PCRE_NAME}-${PCRE_VER}.tar.gz
decompress_dir_name=${PCRE_NAME}-${PCRE_VER}
PCRE_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
old_default_max_timeout=$default_max_timeout
default_max_timeout=300
check_and_extra_tar
default_max_timeout=$old_default_max_timeout

download_url=http://www.zlib.net/fossils/zlib-${ZLIB_VER}.tar.gz
decompress_dir_name=${ZLIB_NAME}-${ZLIB_VER}
ZLIB_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


download_url=https://www.openssl.org/source/${OPENSSL_NAME}-${OPENSSL_VER}.tar.gz
decompress_dir_name=${OPENSSL_NAME}-${OPENSSL_VER}
OPENSSL_ROOT_DIR=${decompress_dir_name}
dst_name=${decompress_dir_name}.tar.gz
check_and_extra_tar


# ------------ build ngx ------------
SRC_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PREFIX_DIR=/opt/build
DSO_LIB_DIR=/opt/libs
NGX_PREFIX=/opt/nginx
sudo mkdir -p ${PREFIX_DIR} -p ${PREFIX_DIR}

## -- build luajit --
cd ${LUAJIT_ROOT_DIR}
sed -i "s|^export PREFIX=.*|export PREFIX=${PREFIX_DIR}|g" Makefile
sed -i "s|^INSTALL_LIB=.*|INSTALL_LIB=${DSO_LIB_DIR}|g" Makefile
make -j ${BUILD_CPU} && sudo make install
cd ${SRC_DIR}

## -- build pcre2 --
cd ${PCRE_ROOT_DIR} && ./autogen.sh && ./configure --prefix=${PREFIX_DIR} --libdir=${DSO_LIB_DIR} && make -j ${BUILD_CPU} && sudo make install
cd ${SRC_DIR}

## -- build ngx --
export LUAJIT_LIB=${DSO_LIB_DIR}
export LUAJIT_INC=${PREFIX_DIR}/include/luajit-2.1
cd ${NGX_ROOT_DIR}
./configure --prefix=${NGX_PREFIX} \
	--with-cc-opt="-g -O0" \
	--with-ld-opt="-Wl,-rpath,${DSO_LIB_DIR}" \
	--with-pcre=../${PCRE_ROOT_DIR} --with-pcre-jit \
	--with-zlib=../${ZLIB_ROOT_DIR} \
	--with-openssl=../${OPENSSL_ROOT_DIR} --with-openssl-opt="-d" --with-http_ssl_module --with-stream_ssl_module \
	--with-http_v2_module \
        --add-module=../${NGX_DEV_KIT_ROOT_DIR} \
        --add-module=../${LUA_NGX_MODULE_ROOT_DIR}
make -j ${BUILD_CPU}
lua_pkg_path_str="lua_package_path \"${NGX_PREFIX}/lib/lua/?.lua;;\";"
# sed -i '/http {/a     lua_package_path "/opt/nginx/lib/lua/?.lua;;";' conf/nginx.conf
sed -i "/http {/a     ${lua_pkg_path_str}" conf/nginx.conf
sudo make install
cd ${SRC_DIR}

## -- build lua-resty-core --
cd ${LUA_RESTY_CORE_ROOT_DIR}
sudo make install PREFIX=${NGX_PREFIX}
cd ${SRC_DIR}


## -- build lua-resty-lrucache --
cd ${LUA_RESTY_LRUCACHE_ROOT_DIR}
sudo make install PREFIX=${NGX_PREFIX}
cd ${SRC_DIR}

