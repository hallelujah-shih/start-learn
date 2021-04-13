/*
 * send.c
 * Copyright (C) 2020 shih <shih@localhost.localdomain>
 *
 * Distributed under terms of the MIT license.
 */

#include <errno.h>
#include <netlink/netlink.h>
#include <stdio.h>
#include <stdlib.h>

int my_func(struct nl_msg *nlmsg, void *arg) {
  printf("recv msg...\n");
  return 0;
}

int main(int argc, char const *argv[]) {
  int err;
  struct nl_sock *sk;
  struct rtgenmsg rt_hdr = {
      .rtgen_family = AF_UNSPEC,
  };

  sk = nl_socket_alloc();
  if (!sk) {
    printf("malloc nl socket error\n");
  }
  if (err = nl_connect(sk, NETLINK_ROUTE)) {
    printf("nl connect error, errno: %d\n", err);
  }

  if (err =
          nl_send_simple(sk, RTM_GETLINK, NLM_F_DUMP, &rt_hdr, sizeof(rt_hdr)),
      err < 0) {
    printf("nl send simple error, errno: %d\n", err);
  }

  nl_socket_modify_cb(sk, NL_CB_VALID, NL_CB_CUSTOM, my_func, NULL);

  nl_recvmsgs_default(sk);
  return 0;
}
