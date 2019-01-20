/*
 * =====================================================================================
 *
 *       Filename:  hello.c
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  01/20/2019 04:19:08 PM
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  shih (hallelujah), hallelujah.shih@gmail.com
 *   Organization:  
 *
 * =====================================================================================
 */
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

MODULE_LICENSE("GPL");

MODULE_AUTHOR("SHIH");

MODULE_DESCRIPTION("A simple Hello world LKM!");

MODULE_VERSION("0.1");

static int __init hello_init(void)
{
        printk(KERN_INFO "Loading hello module...\n");
        printk(KERN_INFO "hello world\n");
        return 0;
}

static void __exit hello_finit(void)
{
        printk(KERN_INFO "Goodbye hello.\n");
}

module_init(hello_init);
module_exit(hello_finit);

