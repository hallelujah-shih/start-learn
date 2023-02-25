#include <arpa/inet.h>
#include <netinet/in.h>
#include <ngx_config.h>
#include <ngx_core.h>
#include <ngx_http.h>
#include <ngx_string.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

typedef union sock_addr_union {
  struct sockaddr sa;
  struct sockaddr_in in;
  struct sockaddr_in6 in6;
  struct sockaddr_un un;
} sock_addr_union;

static ngx_int_t ngx_http_hello_module_init(ngx_conf_t *cf);
static char *ngx_http_hello_cmd_hello_set(ngx_conf_t *cf, ngx_command_t *cmd,
                                          void *conf);
static char *ngx_http_hello_cmd_world_set(ngx_conf_t *cf, ngx_command_t *cmd,
                                          void *conf);

static ngx_str_t hello_string = ngx_string("hello cmd no args!\n");
static ngx_str_t *world_string = NULL;

typedef struct {
  ngx_str_t name;
} ngx_http_hello_loc_conf_t;

static ngx_command_t ngx_http_hello_commands[] = {
    {.name = ngx_string("hello"),
     .type = NGX_HTTP_LOC_CONF | NGX_CONF_NOARGS,
     .set = ngx_http_hello_cmd_hello_set},
    {.name = ngx_string("world"),
     .type = NGX_HTTP_LOC_CONF | NGX_CONF_TAKE1,
     .set = ngx_http_hello_cmd_world_set},
    ngx_null_command};

static void *ngx_http_hello_create_loc_conf(ngx_conf_t *cf) {
  ngx_http_hello_loc_conf_t *conf;
  conf = ngx_pcalloc(cf->pool, sizeof(ngx_http_hello_loc_conf_t));
  if (conf == NULL) {
    return NULL;
  }
  return conf;
}

static ngx_http_module_t ngx_http_hello_module_ctx = {
    NULL, .postconfiguration = ngx_http_hello_module_init,   NULL, NULL, NULL,
    NULL, .create_loc_conf = ngx_http_hello_create_loc_conf, NULL};

ngx_module_t ngx_http_hello_module = {NGX_MODULE_V1,
                                      &ngx_http_hello_module_ctx,
                                      ngx_http_hello_commands,
                                      NGX_HTTP_MODULE,
                                      NULL,
                                      NULL,
                                      NULL,
                                      NULL,
                                      NULL,
                                      NULL,
                                      NULL,
                                      NGX_MODULE_V1_PADDING};

static ngx_int_t ngx_http_hello_handler(ngx_http_request_t *r) {
  ngx_connection_t *c = r->connection;
  const char *current_phase = "hello_handler";
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "into: %s", current_phase);

  ngx_int_t rc;
  ngx_buf_t *b;
  ngx_chain_t out;

  if (!(r->method & (NGX_HTTP_GET | NGX_HTTP_HEAD))) {
    return NGX_HTTP_NOT_ALLOWED;
  }

  rc = ngx_http_discard_request_body(r);
  if (rc != NGX_OK) {
    return rc;
  }

  r->headers_out.content_type_len = sizeof("text/html") - 1;
  r->headers_out.content_type.len = sizeof("text/html") - 1;
  r->headers_out.content_type.data = (u_char *)"text/html";

  if (r->method == NGX_HTTP_HEAD) {
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = hello_string.len;
    return ngx_http_send_header(r);
  }

  b = ngx_pcalloc(r->pool, sizeof(ngx_buf_t));
  if (b == NULL) {
    return NGX_HTTP_INTERNAL_SERVER_ERROR;
  }

  out.buf = b;
  out.next = NULL;

  b->pos = hello_string.data;
  b->last = hello_string.data + hello_string.len;
  b->memory = 1;

  b->last_buf = 1;
  r->headers_out.status = NGX_HTTP_OK;
  r->headers_out.content_length_n = hello_string.len;
  rc = ngx_http_send_header(r);
  if (rc == NGX_ERROR || rc > NGX_OK || r->header_only) {
    return rc;
  }

  return ngx_http_output_filter(r, &out);
}

static ngx_int_t ngx_http_world_handler(ngx_http_request_t *r) {
  ngx_connection_t *c = r->connection;
  const char *current_phase = "world_handler";
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "into: %s", current_phase);

  ngx_int_t rc;
  ngx_buf_t *b;
  ngx_chain_t out;

  if (!(r->method & (NGX_HTTP_GET | NGX_HTTP_HEAD))) {
    return NGX_HTTP_NOT_ALLOWED;
  }

  rc = ngx_http_discard_request_body(r);
  if (rc != NGX_OK) {
    return rc;
  }

  r->headers_out.content_type_len = sizeof("text/html") - 1;
  r->headers_out.content_type.len = sizeof("text/html") - 1;
  r->headers_out.content_type.data = (u_char *)"text/html";

  if (r->method == NGX_HTTP_HEAD) {
    r->headers_out.status = NGX_HTTP_OK;
    r->headers_out.content_length_n = world_string->len;
    return ngx_http_send_header(r);
  }

  b = ngx_pcalloc(r->pool, sizeof(ngx_buf_t));
  if (b == NULL) {
    return NGX_HTTP_INTERNAL_SERVER_ERROR;
  }

  out.buf = b;
  out.next = NULL;

  b->pos = world_string->data;
  b->last = world_string->data + world_string->len;
  b->memory = 1;

  b->last_buf = 1;
  r->headers_out.status = NGX_HTTP_OK;
  r->headers_out.content_length_n = world_string->len;
  rc = ngx_http_send_header(r);
  if (rc == NGX_ERROR || rc > NGX_OK || r->header_only) {
    return rc;
  }

  return ngx_http_output_filter(r, &out);
}

static char *ngx_http_hello_cmd_hello_set(ngx_conf_t *cf, ngx_command_t *cmd,
                                          void *conf) {
  ngx_log_error(NGX_LOG_INFO, cf->log, 0, "into: %s", "http_hello_set");
  ngx_http_core_loc_conf_t *clcf;
  clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
  clcf->handler = ngx_http_hello_handler;
  ngx_log_error(NGX_LOG_INFO, cf->log, 0, "exit: %s", "http_hello_set");
  return NGX_CONF_OK;
}

static char *ngx_http_hello_cmd_world_set(ngx_conf_t *cf, ngx_command_t *cmd,
                                          void *conf) {
  ngx_log_error(NGX_LOG_INFO, cf->log, 0, "into: %s", "http_world_set");
  ngx_http_core_loc_conf_t *clcf;
  ngx_str_t *value;
  value = cf->args->elts;
  world_string = &value[1];

  clcf = ngx_http_conf_get_module_loc_conf(cf, ngx_http_core_module);
  clcf->handler = ngx_http_world_handler;
  ngx_log_error(NGX_LOG_INFO, cf->log, 0, "exit: %s", "http_world_set");
  return NGX_CONF_OK;
}

static int get_real_saddr(ngx_http_request_t *r, char *buf, size_t buf_len) {
  if (buf_len <= 1) {
    return 0;
  }

  ngx_connection_t *conn = r->connection;
  size_t max_size = conn->listening->addr_text.len < buf_len
                        ? conn->listening->addr_text.len
                        : buf_len - 1;
  if (conn->proxy_protocol) {
    max_size = conn->proxy_protocol->dst_addr.len < buf_len
                   ? conn->proxy_protocol->dst_addr.len
                   : buf_len - 1;
    memcpy(buf, conn->proxy_protocol->dst_addr.data, max_size);
    buf[max_size] = 0;
    return max_size;
  }

  char server_addr[128] = {0};
  sock_addr_union saddr;
  socklen_t saddr_len = sizeof(saddr);
  if (getsockname(conn->fd, (struct sockaddr *)&saddr, &saddr_len) >= 0) {
    if (inet_ntop(saddr.sa.sa_family, &saddr.in.sin_addr, server_addr,
                  sizeof(server_addr))) {
      return snprintf(buf, buf_len, "%s", server_addr);
    }
  }
  memcpy(buf, conn->listening->addr_text.data, max_size);
  buf[max_size] = 0;
  return max_size;
}

static ngx_int_t
ngx_http_hello_post_read_process_handler(ngx_http_request_t *r) {
  const char *current_phase = "hello_post_read";
  ngx_connection_t *c = r->connection;
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "into: %s", current_phase);

  char real_server_addr[128] = {0};
  get_real_saddr(r, real_server_addr, sizeof(real_server_addr));
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "family: %d: real server addr: %s",
                c->sockaddr->sa_family, real_server_addr);

  ngx_log_error(NGX_LOG_INFO, c->log, 0, "exit: %s", current_phase);
  return NGX_DECLINED;
}

static ngx_int_t ngx_http_hello_content_process_handler(ngx_http_request_t *r) {
  const char *current_phase = "hello_content";
  ngx_connection_t *c = r->connection;
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "into: %s", current_phase);
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "exit: %s", current_phase);
  return NGX_DECLINED;
}

static ngx_int_t ngx_http_hello_log_process_handler(ngx_http_request_t *r) {
  const char *current_phase = "hello_log";
  ngx_connection_t *c = r->connection;
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "into: %s", current_phase);
  ngx_log_error(NGX_LOG_INFO, c->log, 0, "exit: %s", current_phase);
  return NGX_DECLINED;
}

static ngx_int_t ngx_http_hello_module_init(ngx_conf_t *cf) {
  ngx_http_handler_pt *h;
  ngx_http_core_main_conf_t *cmcf;
  cmcf = ngx_http_conf_get_module_main_conf(cf, ngx_http_core_module);

  h = ngx_array_push(&cmcf->phases[NGX_HTTP_POST_READ_PHASE].handlers);
  if (h == NULL) {
    return NGX_ERROR;
  }
  *h = ngx_http_hello_post_read_process_handler;

  h = ngx_array_push(&cmcf->phases[NGX_HTTP_CONTENT_PHASE].handlers);
  if (h == NULL) {
    return NGX_ERROR;
  }
  *h = ngx_http_hello_content_process_handler;

  h = ngx_array_push(&cmcf->phases[NGX_HTTP_LOG_PHASE].handlers);
  if (h == NULL) {
    return NGX_ERROR;
  }
  *h = ngx_http_hello_log_process_handler;

  return NGX_OK;
}
