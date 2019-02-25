/*
 * =====================================================================================
 *
 *       Filename:  xdp_drop.c
 *
 *    Description:
 *
 *        Version:  1.0
 *        Created:  02/22/2019 03:12:33 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  shih (hallelujah), hallelujah.shih@gmail.com
 *   Organization:
 *
 * =====================================================================================
 */

#define KBUILD_MODNAME "xdp_dummy"

#include <linux/kernel.h>
#include <uapi/linux/bpf.h>
#include <uapi/linux/if_ether.h>
#include <uapi/linux/in.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/tcp.h>
#include <uapi/linux/types.h>

#define SEC(NAME) __attribute__((section(NAME), used))

SEC("prog")
int xdp_dummy(struct xdp_md *ctx) {
  struct iphdr *iph;
  struct tcphdr *tcph;
  void *data_end = (void *)(long)ctx->data_end;
  void *data = (void *)(long)ctx->data;

  struct ethhdr *eth = data;
  if (eth + 1 > data_end) return XDP_DROP;

  if (eth->h_proto != ntohs(ETH_P_IP)) return XDP_PASS;

  iph = (struct iphdr *)(eth + 1);
  if ((iph + 1) > data_end || iph->ihl != 5) return XDP_DROP;

  if (iph->protocol != IPPROTO_TCP) return XDP_PASS;

  tcph = (struct tcphdr *)(iph + 1);

  if ((tcph + 1) > data_end) return XDP_DROP;

  if (ntohs(tcph->dest) != 22) return XDP_DROP;

  return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
