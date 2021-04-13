#
# Makefile
# shih, 2020-12-28 16:22
#
LIBNL_CFLAGS=$(shell pkg-config --cflags libnl-3.0)
LIBNL_LD=$(shell pkg-config --libs libnl-3.0)

all: multicast send

%:%.c
	gcc $< $(LIBNL_CFLAGS) -o $@ $(LIBNL_LD)

clean:
	rm -rf multicast send

# vim:ft=make
#
