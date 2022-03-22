#include <linux/ip.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/netfilter.h>
#include <linux/netfilter_ipv4.h>
#include <linux/tcp.h>
#include <net/net_namespace.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("shih");
MODULE_DESCRIPTION("A simple netfilter register test");
MODULE_VERSION("0.1");

static unsigned int same_port_filter(void *priv, struct sk_buff *skb,
                                     const struct nf_hook_state *state) {
  struct iphdr *iph = ip_hdr(skb);
  if (iph->protocol == IPPROTO_TCP) {
    struct tcphdr *tcph = (struct tcphdr *)((__u32 *)iph + iph->ihl);
    if (tcph->dest == tcph->source) {
      printk(KERN_INFO "same_port_filter: dropping packet, %u:%u -> %u:%u\n",
           iph->saddr, tcph->source, iph->daddr, tcph->dest);
      return NF_DROP;
    }
  }
  return NF_ACCEPT;
}

static const struct nf_hook_ops same_port_filter_ops = {
    .hook = same_port_filter,
    .pf = NFPROTO_IPV4,
    .hooknum = NF_INET_LOCAL_IN,
    .priority = NF_IP_PRI_RAW - 1,
};

static int same_port_filter_init(void) {
  int ret;
  printk(KERN_INFO "same_port_filter: init\n");
  ret = nf_register_net_hook(&init_net, &same_port_filter_ops);
  if (ret < 0) {
    printk(KERN_INFO "same_port_filter: nf_register_net_hook failed\n");
    goto hook_fail;
  }
  return 0;
hook_fail:
  return ret;
}

static void same_port_filter_exit(void) {
  printk(KERN_INFO "same_port_filter: exit\n");
  nf_unregister_net_hook(&init_net, &same_port_filter_ops);
}

module_init(same_port_filter_init);
module_exit(same_port_filter_exit);