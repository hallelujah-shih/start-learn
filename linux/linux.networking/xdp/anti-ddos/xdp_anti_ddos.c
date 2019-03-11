/*
 * =====================================================================================
 *
 *       Filename:  xdp_anti_ddos.c
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

#define KBUILD_MODNAME "xdp_anti_ddos"

#include <linux/kernel.h>
#include <net/ip.h>
#include <uapi/linux/bpf.h>
#include <uapi/linux/icmp.h>
#include <uapi/linux/if_ether.h>
#include <uapi/linux/in.h>
#include <uapi/linux/ip.h>
#include <uapi/linux/tcp.h>
#include <uapi/linux/types.h>
#include <uapi/linux/udp.h>

// 非完全定义，略过了ECN
#define TCP_URG_FLAG 0x20
#define TCP_ACK_FLAG 0x10
#define TCP_PSH_FLAG 0x08
#define TCP_RST_FLAG 0x04
#define TCP_SYN_FLAG 0x02
#define TCP_FIN_FLAG 0x01
#define TCP_FLAG_ALL 0x3F

#define SEC(NAME) __attribute__((section(NAME), used))

static __always_inline bool parse_eth(struct ethhdr *eth, void *data_end) {
  if (eth + 1 > data_end) return false;
  return true;
}

static bool parse_ip4(struct iphdr *iph, void *data_end) {
  if ((iph + 1) > data_end) return false;
  if (iph->version != 4) return false;
  // TODO 增加TTL检测
  return true;
}

static bool parse_icmp4(struct icmphdr *icmph, void *data_end,
                        struct iphdr *iph, __u16 total_len) {
  if (icmph + 1 > data_end) return false;
  __u16 icmp_data_len = total_len - (iph->ihl << 2) - sizeof(struct icmphdr);

  // 分析IP报文，是否可能存在攻击
  if (iph->frag_off != htons(IP_DF)) return false;

  // 检测ping报文
  if (icmph->type == ICMP_ECHO)
    if (icmp_data_len > 64) return false;

  // TODO 超长报文直接丢弃（需要调研，这写了256，RFC
  // xxx中规定了最长大小756字节？）
  if (icmp_data_len >= 256) return false;
  return true;
}

static bool parse_udp(struct udphdr *udph, void *data_end, struct iphdr *iph,
                      __u16 total_len) {
  if (udph + 1 > data_end) return false;
  // TODO dns检查(query,response)
  // TODO 放过ntp、vrrp等线上必须支持的协议
  if (iph->daddr == iph->saddr) return false;
  if ((udph->dest) == htons(7) || udph->dest == htons(19)) return false;
  return true;
}

static bool parse_tcp(struct tcphdr *tcph, void *data_end, struct iphdr *iph,
                      __u16 total_len) {
  if (tcph + 1 > data_end) return false;
  __u16 playload_len = total_len - (iph->ihl << 2) - (tcph->doff << 2);
  // TODO 实现各种状态分析检查
  if (!tcph->ack && tcph->syn) {
    // 不支持TFO，后续扩展参见https://www.cloudshark.org/captures/62a920c5bab1
    if (playload_len != 0) return false;
  }
  return true;
}

SEC("prog")
int xdp_dummy(struct xdp_md *ctx) {
  struct iphdr *iph;
  struct tcphdr *tcph;
  struct icmphdr *icmph;
  struct udphdr *udph;
  void *data_end = (void *)(long)ctx->data_end;
  void *data = (void *)(long)ctx->data;

  struct ethhdr *eth = (struct ethhdr *)data;
  if (!parse_eth(eth, data_end)) return XDP_DROP;

  if (eth->h_proto != htons(ETH_P_IP)) return XDP_PASS;

  iph = (struct iphdr *)(eth + 1);
  if (!parse_ip4(iph, data_end)) return XDP_DROP;

  __u16 total_len = ntohs(iph->tot_len);

  switch (iph->protocol) {
    case IPPROTO_TCP:
      tcph = (struct tcphdr *)(iph + 1);
      if (!parse_tcp(tcph, data_end, iph, total_len)) return XDP_DROP;
      break;
    case IPPROTO_ICMP:
      icmph = (struct icmphdr *)(iph + 1);
      if (!parse_icmp4(icmph, data_end, iph, total_len)) return XDP_DROP;
      break;
    case IPPROTO_UDP:
      udph = (struct udphdr *)(iph + 1);
      if (!parse_udp(udph, data_end, iph, total_len)) return XDP_DROP;
      break;
  }

  return XDP_PASS;
}

char _license[] SEC("license") = "GPL";
