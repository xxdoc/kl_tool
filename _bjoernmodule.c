/***********************************************
 ************** common.h  *************
 ***********************************************/

#include <stdlib.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>

#define TYPE_ERROR_INNER(what, expected, ...) \
  PyErr_Format(PyExc_TypeError, what " must be " expected " " __VA_ARGS__)
#define TYPE_ERROR(what, expected, got) \
  TYPE_ERROR_INNER(what, expected, "(got '%.200s' object instead)", Py_TYPE(got)->tp_name)

typedef struct { char* data; size_t len; } string;

enum http_status { HTTP_BAD_REQUEST = 1, HTTP_LENGTH_REQUIRED, HTTP_SERVER_ERROR };

size_t unquote_url_inplace(char* url, size_t len);
void _init_common(void);

PyObject *_REMOTE_ADDR, *_PATH_INFO, *_QUERY_STRING, *_REQUEST_METHOD, *_GET,
         *_HTTP_CONTENT_LENGTH, *_CONTENT_LENGTH, *_HTTP_CONTENT_TYPE,
         *_CONTENT_TYPE, *_SERVER_PROTOCOL, *_SERVER_NAME, *_SERVER_PORT,
         *_HTTP_1_1, *_HTTP_1_0, *_wsgi_input, *_close, *_empty_string,
         *_empty_bytes, *_BytesIO, *_write, *_read, *_seek;

#ifdef DEBUG
  #define DBG_REQ(request, ...) \
    do { \
      printf("[DEBUG Req %ld] ", request->id); \
      DBG(__VA_ARGS__); \
    } while(0)
  #define DBG(...) \
    do { \
      printf(__VA_ARGS__); \
      printf("\n"); \
    } while(0)
#else
  #define DBG(...) do{}while(0)
  #define DBG_REQ(...) DBG(__VA_ARGS__)
#endif

#define DBG_REFCOUNT(obj) \
  DBG(#obj "->obj_refcnt: %d", obj->ob_refcnt)

#define DBG_REFCOUNT_REQ(request, obj) \
  DBG_REQ(request, #obj "->ob_refcnt: %d", obj->ob_refcnt)

#ifdef WITHOUT_ASSERTS
  #undef assert
  #define assert(...) do{}while(0)
#endif


/*************************************/

#define UNHEX(c) ((c >= '0' && c <= '9') ? (c - '0') : \
                  (c >= 'a' && c <= 'f') ? (c - 'a' + 10) : \
                  (c >= 'A' && c <= 'F') ? (c - 'A' + 10) : NOHEX)
#define NOHEX ((char) -1)

size_t unquote_url_inplace(char* url, size_t len)
{
  for(char *p=url, *end=url+len; url != end; ++url, ++p) {
    if(*url == '%') {
      if(url >= end-2) {
        /* Less than two characters left after the '%' */
        return 0;
      }
      char a = UNHEX(url[1]);
      char b = UNHEX(url[2]);
      if(a == NOHEX || b == NOHEX) return 0;
      *p = a*16 + b;
      url += 2;
      len -= 2;
    } else {
      *p = *url;
    }
  }
  return len;
}

void _init_common()
{

#define _(name) _##name = _Unicode_FromString(#name)
  _(REMOTE_ADDR);
  _(PATH_INFO);
  _(QUERY_STRING);
  _(close);

  _(REQUEST_METHOD);
  _(SERVER_PROTOCOL);
  _(SERVER_NAME);
  _(SERVER_PORT);
  _(GET);
  _(HTTP_CONTENT_LENGTH);
  _(CONTENT_LENGTH);
  _(HTTP_CONTENT_TYPE);
  _(CONTENT_TYPE);

  _(BytesIO);
  _(write);
  _(read);
  _(seek);
#undef _

  _HTTP_1_1 = _Unicode_FromString("HTTP/1.1");
  _HTTP_1_0 = _Unicode_FromString("HTTP/1.0");
  _wsgi_input = _Unicode_FromString("wsgi.input");
  _empty_string = _Unicode_FromString("");
  _empty_bytes = _Bytes_FromString("");
}


#include <ev.h>
#include "http_parser.h"

/***********************************************
 **************  request.h  *************
 ***********************************************/


void _initialize_request_module(void);

typedef struct {
  unsigned error_code : 2;
  unsigned parse_finished : 1;
  unsigned start_response_called : 1;
  unsigned wsgi_call_done : 1;
  unsigned keep_alive : 1;
  unsigned response_length_unknown : 1;
  unsigned chunked_response : 1;
  unsigned use_sendfile : 1;
} request_state;

typedef struct {
  http_parser parser;
  string field;
  string value;
  string body;
} bj_parser;

typedef struct {
#ifdef DEBUG
  unsigned long id;
#endif
  bj_parser parser;
  ev_io ev_watcher;

  ServerInfo* server_info;
  int client_fd;
  PyObject* client_addr;

  request_state state;

  PyObject* status;
  PyObject* headers;
  PyObject* current_chunk;
  Py_ssize_t current_chunk_p;
  PyObject* iterable;
  PyObject* iterator;
} Request;

#define REQUEST_FROM_WATCHER(watcher) \
  (Request*)((size_t)watcher - (size_t)(&(((Request*)NULL)->ev_watcher)));

Request* Request_new(ServerInfo*, int client_fd, const char* client_addr);
void Request_parse(Request*, const char*, const size_t);
void Request_reset(Request*);
void Request_clean(Request*);
void Request_free(Request*);


/*************************************/


static inline void PyDict_ReplaceKey(PyObject* dict, PyObject* k1, PyObject* k2);
static PyObject* wsgi_http_header(string header);
static http_parser_settings parser_settings;
static PyObject* wsgi_base_dict = NULL;

static PyObject *IO_module;

Request* Request_new(ServerInfo* server_info, int client_fd, const char* client_addr)
{
  Request* request = malloc(sizeof(Request));
#ifdef DEBUG
  static unsigned long request_id = 0;
  request->id = request_id++;
#endif
  request->server_info = server_info;
  request->client_fd = client_fd;
  request->client_addr = _Unicode_FromString(client_addr);
  http_parser_init((http_parser*)&request->parser, HTTP_REQUEST);
  request->parser.parser.data = request;
  Request_reset(request);
  return request;
}

void Request_reset(Request* request)
{
  memset(&request->state, 0, sizeof(Request) - (size_t)&((Request*)NULL)->state);
  request->state.response_length_unknown = true;
  request->parser.body = (string){NULL, 0};
}

void Request_free(Request* request)
{
  Request_clean(request);
  Py_DECREF(request->client_addr);
  free(request);
}

void Request_clean(Request* request)
{
  if(request->iterable) {
    /* Call 'iterable.close()' if available */
    PyObject* close_method = PyObject_GetAttr(request->iterable, _close);
    if(close_method == NULL) {
      if(PyErr_ExceptionMatches(PyExc_AttributeError))
        PyErr_Clear();
    } else {
      PyObject_CallObject(close_method, NULL);
      Py_DECREF(close_method);
    }
    if(PyErr_Occurred()) PyErr_Print();
    Py_DECREF(request->iterable);
  }
  Py_XDECREF(request->iterator);
  Py_XDECREF(request->headers);
  Py_XDECREF(request->status);
}

/* Parse stuff */

void Request_parse(Request* request, const char* data, const size_t data_len)
{
  assert(data_len);
  size_t nparsed = http_parser_execute((http_parser*)&request->parser,
                                       &parser_settings, data, data_len);
  if(nparsed != data_len)
    request->state.error_code = HTTP_BAD_REQUEST;
}

#define REQUEST ((Request*)parser->data)
#define PARSER  ((bj_parser*)parser)
#define UPDATE_LENGTH(name) \
  /* Update the len of a header field/value.
   *
   * Short explaination of the pointer arithmetics fun used here:
   *
   *   [old header data ] ...stuff... [ new header data ]
   *   ^-------------- A -------------^--------B--------^
   *
   * A = XXX- PARSER->XXX.data
   * B = len
   * A + B = old header start to new header end
   */ \
  do { PARSER->name.len = (name - PARSER->name.data) + len; } while(0)

#define _set_header(k, v) PyDict_SetItem(REQUEST->headers, k, v);
  /* PyDict_SetItem() increases the ref-count for value */
#define _set_header_free_value(k, v) \
  do { \
    PyObject* val = (v); \
    _set_header(k, val); \
    Py_DECREF(val); \
  } while(0)


#define _set_header_from_http_header() \
  do { \
    PyObject* key = wsgi_http_header(PARSER->field); \
    if (key) { \
      _set_header_free_value(key, _Unicode_FromStringAndSize(PARSER->value.data, PARSER->value.len)); \
      Py_DECREF(key); \
    } \
  } while(0) \

static int
on_message_begin(http_parser* parser)
{
  REQUEST->headers = PyDict_New();
  PARSER->field = (string){NULL, 0};
  PARSER->value = (string){NULL, 0};
  return 0;
}

static int
on_path(http_parser* parser, const char* path, size_t len)
{
  if(!(len = unquote_url_inplace((char*)path, len)))
    return 1;
  _set_header_free_value(_PATH_INFO, _Unicode_FromStringAndSize(path, len));
  return 0;
}

static int
on_query_string(http_parser* parser, const char* query, size_t len)
{
  _set_header_free_value(_QUERY_STRING, _Unicode_FromStringAndSize(query, len));
  return 0;
}

static int
on_header_field(http_parser* parser, const char* field, size_t len)
{
  if(PARSER->value.data) {
    /* Store previous header and start a new one */
    _set_header_from_http_header();
  } else if(PARSER->field.data) {
    UPDATE_LENGTH(field);
    return 0;
  }
  PARSER->field = (string){(char*)field, len};
  PARSER->value = (string){NULL, 0};
  return 0;
}

static int
on_header_value(http_parser* parser, const char* value, size_t len)
{
  if(PARSER->value.data) {
    UPDATE_LENGTH(value);
  } else {
    /* Start a new value */
    PARSER->value = (string){(char*)value, len};
  }
  return 0;
}

static int
on_headers_complete(http_parser* parser)
{
  if(PARSER->field.data) {
    _set_header_from_http_header();
  }
  return 0;
}

static int
on_body(http_parser* parser, const char* data, const size_t len)
{
  PyObject *body;

  body = PyDict_GetItem(REQUEST->headers, _wsgi_input);
  if (body == NULL) {
    if(!parser->content_length) {
      REQUEST->state.error_code = HTTP_LENGTH_REQUIRED;
      return 1;
    }
    body = PyObject_CallMethodObjArgs(IO_module, _BytesIO, NULL);
    if (body == NULL) {
      return 1;
    }
    _set_header_free_value(_wsgi_input, body);
  }
  PyObject *temp_data = _Bytes_FromStringAndSize(data, len);
  PyObject *tmp = PyObject_CallMethodObjArgs(body, _write, temp_data, NULL);
  Py_DECREF(tmp); /* Never throw away return objects from py-api */
  Py_DECREF(temp_data);
  return 0;
}

static int
on_message_complete(http_parser* parser)
{
  /* HTTP_CONTENT_{LENGTH,TYPE} -> CONTENT_{LENGTH,TYPE} */
  PyDict_ReplaceKey(REQUEST->headers, _HTTP_CONTENT_LENGTH, _CONTENT_LENGTH);
  PyDict_ReplaceKey(REQUEST->headers, _HTTP_CONTENT_TYPE, _CONTENT_TYPE);

  /* SERVER_PROTOCOL (REQUEST_PROTOCOL) */
  _set_header(_SERVER_PROTOCOL, parser->http_minor == 1 ? _HTTP_1_1 : _HTTP_1_0);

  /* SERVER_NAME and SERVER_PORT */
  if (REQUEST->server_info->host) {
    _set_header(_SERVER_NAME, REQUEST->server_info->host);
    _set_header(_SERVER_PORT, REQUEST->server_info->port);
  }

  /* REQUEST_METHOD */
  if(parser->method == HTTP_GET) {
    /* I love useless micro-optimizations. */
    _set_header(_REQUEST_METHOD, _GET);
  } else {
    _set_header_free_value(_REQUEST_METHOD,
      _Unicode_FromString(http_method_str(parser->method))
      );
  }

  /* REMOTE_ADDR */
  _set_header(_REMOTE_ADDR, REQUEST->client_addr);

  PyObject* body = PyDict_GetItem(REQUEST->headers, _wsgi_input);
  if(body) {
    /* first do a seek(0) and then read() returns all data */
    PyObject *buf = PyObject_CallMethodObjArgs(body, _seek, _FromLong(0), NULL);
    Py_DECREF(buf); /* Discard the return value */
  } else {
    /* Request has no body */
    body = PyObject_CallMethodObjArgs(IO_module, _BytesIO, NULL);
    _set_header_free_value(_wsgi_input, body);
  }

  PyDict_Update(REQUEST->headers, wsgi_base_dict);

  REQUEST->state.parse_finished = true;
  return 0;
}


static PyObject*
wsgi_http_header(string header)
{
  const char *http_ = "HTTP_";
  int size = header.len+strlen(http_);
  char dest[size];
  int i = 5;

  memcpy(dest, http_, i);

  while(header.len--) {
    char c = *header.data++;
    if (c == '_') {
      // CVE-2015-0219
      return NULL;
    }
    else if(c == '-')
      dest[i++] = '_';
    else if(c >= 'a' && c <= 'z')
      dest[i++] = c - ('a'-'A');
    else
      dest[i++] = c;
  }

  return (PyObject *)_Unicode_FromStringAndSize(dest, size);
}

static inline void
PyDict_ReplaceKey(PyObject* dict, PyObject* old_key, PyObject* new_key)
{
  PyObject* value = PyDict_GetItem(dict, old_key);
  if(value) {
    Py_INCREF(value);
    PyDict_DelItem(dict, old_key);
    PyDict_SetItem(dict, new_key, value);
    Py_DECREF(value);
  }
}


static http_parser_settings
parser_settings = {
  on_message_begin, on_path, on_query_string, NULL, NULL, on_header_field,
  on_header_value, on_headers_complete, on_body, on_message_complete
};

void _initialize_request_module()
{
  IO_module = PyImport_ImportModule("io");
  if (IO_module == NULL) {
    /* PyImport_ImportModule should have exception set already */
    return;
  }

  if(wsgi_base_dict == NULL) {
    wsgi_base_dict = PyDict_New();

    /* dct['wsgi.file_wrapper'] = FileWrapper */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.file_wrapper",
      (PyObject*)&FileWrapper_Type
    );

    /* dct['SCRIPT_NAME'] = '' */
    PyDict_SetItemString(
      wsgi_base_dict,
      "SCRIPT_NAME",
      _empty_string
    );

    /* dct['wsgi.version'] = (1, 0) */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.version",
      PyTuple_Pack(2, _FromLong(1), _FromLong(0))
    );

    /* dct['wsgi.url_scheme'] = 'http'
     * (This can be hard-coded as there is no TLS support in bjoern.) */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.url_scheme",
      _Unicode_FromString("http")
    );

    /* dct['wsgi.errors'] = sys.stderr */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.errors",
      PySys_GetObject("stderr")
    );

    /* dct['wsgi.multithread'] = False
     * (Tell the application that it is being run
     *  in a single-threaded environment.) */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.multithread",
      Py_False
    );

    /* dct['wsgi.multiprocess'] = True
     * (Tell the application that it is being run
     *  in a multi-process environment.) */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.multiprocess",
      Py_True
    );

    /* dct['wsgi.run_once'] = False
     * (bjoern is no CGI gateway) */
    PyDict_SetItemString(
      wsgi_base_dict,
      "wsgi.run_once",
      Py_False
    );
  }
}

#include <arpa/inet.h>
#include <fcntl.h>
#include <ev.h>

#if defined(__FreeBSD__) || defined(__DragonFly__)
# include <netinet/in.h> /* for struct sockaddr_in */
# include <sys/types.h>
# include <sys/socket.h>
#endif

#ifdef WANT_SIGINT_HANDLING
# include <sys/signal.h>
#endif

/***********************************************
 **************  server.h  *************
 ***********************************************/

typedef struct {
  int sockfd;
  PyObject* wsgi_app;
  PyObject* host;
  PyObject* port;
} ServerInfo;

void server_run(ServerInfo*);

/*************************************/

#define READ_BUFFER_SIZE 64*1024
#define Py_XCLEAR(obj) do { if(obj) { Py_DECREF(obj); obj = NULL; } } while(0)
#define GIL_LOCK(n) PyGILState_STATE _gilstate_##n = PyGILState_Ensure()
#define GIL_UNLOCK(n) PyGILState_Release(_gilstate_##n)

static const char* http_error_messages[4] = {
  NULL, /* Error codes start at 1 because 0 means "no error" */
  "HTTP/1.1 400 Bad Request\r\n\r\n",
  "HTTP/1.1 406 Length Required\r\n\r\n",
  "HTTP/1.1 500 Internal Server Error\r\n\r\n"
};

enum _rw_state {
  not_yet_done = 1,
  done,
  aborted,
};
typedef enum _rw_state read_state;
typedef enum _rw_state write_state;

typedef struct {
  ServerInfo* server_info;
  ev_io accept_watcher;
} ThreadInfo;

typedef void ev_io_callback(struct ev_loop*, ev_io*, const int);

#if WANT_SIGINT_HANDLING
typedef void ev_signal_callback(struct ev_loop*, ev_signal*, const int);
static ev_signal_callback ev_signal_on_sigint;
#endif

static ev_io_callback ev_io_on_request;
static ev_io_callback ev_io_on_read;
static ev_io_callback ev_io_on_write;
static write_state on_write_sendfile(struct ev_loop*, Request*);
static write_state on_write_chunk(struct ev_loop*, Request*);
static bool do_send_chunk(Request*);
static bool do_sendfile(Request*);
static bool handle_nonzero_errno(Request*);
static void close_connection(struct ev_loop*, Request*);


void server_run(ServerInfo* server_info)
{
  struct ev_loop* mainloop = ev_loop_new(0);

  ThreadInfo thread_info;
  thread_info.server_info = server_info;
  ev_set_userdata(mainloop, &thread_info);

  ev_io_init(&thread_info.accept_watcher, ev_io_on_request, server_info->sockfd, EV_READ);
  ev_io_start(mainloop, &thread_info.accept_watcher);

#if WANT_SIGINT_HANDLING
  ev_signal signal_watcher;
  ev_signal_init(&signal_watcher, ev_signal_on_sigint, SIGINT);
  ev_signal_start(mainloop, &signal_watcher);
#endif

  /* This is the program main loop */
  Py_BEGIN_ALLOW_THREADS
  ev_run(mainloop, 0);
  ev_loop_destroy(mainloop);
  Py_END_ALLOW_THREADS
}

#if WANT_SIGINT_HANDLING
static void
pyerr_set_interrupt(struct ev_loop* mainloop, struct ev_cleanup* watcher, const int events)
{
  PyErr_SetInterrupt();
  free(watcher);
}

static void
ev_signal_on_sigint(struct ev_loop* mainloop, ev_signal* watcher, const int events)
{
  /* Clean up and shut down this thread.
   * (Shuts down the Python interpreter if this is the main thread) */
  ev_cleanup* cleanup_watcher = malloc(sizeof(ev_cleanup));
  ev_cleanup_init(cleanup_watcher, pyerr_set_interrupt);
  ev_cleanup_start(mainloop, cleanup_watcher);

  ev_io_stop(mainloop, &((ThreadInfo*)ev_userdata(mainloop))->accept_watcher);
  ev_signal_stop(mainloop, watcher);
}
#endif

static void
ev_io_on_request(struct ev_loop* mainloop, ev_io* watcher, const int events)
{
  int client_fd;
  struct sockaddr_in sockaddr;
  socklen_t addrlen;

  addrlen = sizeof(struct sockaddr_in);
  client_fd = accept(watcher->fd, (struct sockaddr*)&sockaddr, &addrlen);
  if(client_fd < 0) {
    DBG("Could not accept() client: errno %d", errno);
    return;
  }

  int flags = fcntl(client_fd, F_GETFL, 0);
  if(fcntl(client_fd, F_SETFL, (flags < 0 ? 0 : flags) | O_NONBLOCK) == -1) {
    DBG("Could not set_nonblocking() client %d: errno %d", client_fd, errno);
    return;
  }

  Request* request = Request_new(
    ((ThreadInfo*)ev_userdata(mainloop))->server_info,
    client_fd,
    inet_ntoa(sockaddr.sin_addr)
  );

  DBG_REQ(request, "Accepted client %s:%d on fd %d",
          inet_ntoa(sockaddr.sin_addr), ntohs(sockaddr.sin_port), client_fd);

  ev_io_init(&request->ev_watcher, &ev_io_on_read,
             client_fd, EV_READ);
  ev_io_start(mainloop, &request->ev_watcher);
}

static void
ev_io_on_read(struct ev_loop* mainloop, ev_io* watcher, const int events)
{
  static char read_buf[READ_BUFFER_SIZE];

  Request* request = REQUEST_FROM_WATCHER(watcher);
  read_state read_state;

  ssize_t read_bytes = read(
    request->client_fd,
    read_buf,
    READ_BUFFER_SIZE
  );

  GIL_LOCK(0);

  if (read_bytes == 0) {
    /* Client disconnected */
    read_state = aborted;
    DBG_REQ(request, "Client disconnected");
  } else if (read_bytes < 0) {
    /* Would block or error */
    if(errno == EAGAIN || errno == EWOULDBLOCK) {
      read_state = not_yet_done;
    } else {
      read_state = aborted;
      DBG_REQ(request, "Hit errno %d while read()ing", errno);
    }
  } else {
    /* OK, either expect more data or done reading */
    Request_parse(request, read_buf, (size_t)read_bytes);
    if(request->state.error_code) {
      /* HTTP parse error */
      read_state = done;
      DBG_REQ(request, "Parse error");
      request->current_chunk = _Bytes_FromString(
        http_error_messages[request->state.error_code]);
      assert(request->iterator == NULL);
    } else if(request->state.parse_finished) {
      /* HTTP parse successful */
      read_state = done;
      bool wsgi_ok = wsgi_call_application(request);
      if (!wsgi_ok) {
        /* Response is "HTTP 500 Internal Server Error" */
        DBG_REQ(request, "WSGI app error");
        assert(PyErr_Occurred());
        PyErr_Print();
        assert(!request->state.chunked_response);
        Py_XCLEAR(request->iterator);
        request->current_chunk = _Bytes_FromString(
          http_error_messages[HTTP_SERVER_ERROR]);
      }
    } else {
      /* Wait for more data */
      read_state = not_yet_done;
    }
  }

  switch (read_state) {
  case not_yet_done:
    break;
  case done:
    DBG_REQ(request, "Stop read watcher, start write watcher");
    ev_io_stop(mainloop, &request->ev_watcher);
    ev_io_init(&request->ev_watcher, &ev_io_on_write,
               request->client_fd, EV_WRITE);
    ev_io_start(mainloop, &request->ev_watcher);
    break;
  case aborted:
    close_connection(mainloop, request);
    break;
  }

  GIL_UNLOCK(0);
}

static void
ev_io_on_write(struct ev_loop* mainloop, ev_io* watcher, const int events)
{
  /* Since the response writing code is fairly complex, I'll try to give a short
   * overview of the different control flow paths etc.:
   *
   * On the very top level, there are two types of responses to distinguish:
   * A) sendfile responses
   * B) iterator/other responses
   *
   * These cases are handled by the 'on_write_sendfile' and 'on_write_chunk'
   * routines, respectively.  They use the 'do_sendfile' and 'do_send_chunk'
   * routines to do the actual write()-ing. The 'do_*' routines return true if
   * there's some data left to send in the current chunk (or, in the case of
   * sendfile, the end of the file has not been reached yet).
   *
   * When the 'do_*' routines return false, the 'on_write_*' routines have to
   * figure out if there's a next chunk to send (e.g. in the case of a response iterator).
   */
  Request* request = REQUEST_FROM_WATCHER(watcher);

  GIL_LOCK(0);

  write_state write_state;
  if(request->state.use_sendfile) {
    write_state = on_write_sendfile(mainloop, request);
  } else {
    write_state = on_write_chunk(mainloop, request);
  }

  switch(write_state) {
  case not_yet_done:
    break;
  case done:
    if(request->state.keep_alive) {
      DBG_REQ(request, "done, keep-alive");
      ev_io_stop(mainloop, &request->ev_watcher);
      Request_clean(request);
      Request_reset(request);
      ev_io_init(&request->ev_watcher, &ev_io_on_read,
                 request->client_fd, EV_READ);
      ev_io_start(mainloop, &request->ev_watcher);
    } else {
      DBG_REQ(request, "done, close");
      close_connection(mainloop, request);
    }
    break;
  case aborted:
    /* Response was aborted due to an error. We can't do anything graceful here
     * because at least one chunk is already sent... just close the connection. */
    close_connection(mainloop, request);
    break;
  }

  GIL_UNLOCK(0);
}

static write_state
on_write_sendfile(struct ev_loop* mainloop, Request* request)
{
  /* A sendfile response is split into two phases:
   * Phase A) sending HTTP headers
   * Phase B) sending the actual file contents
   */
  if(request->current_chunk) {
    /* Phase A) -- current_chunk contains the HTTP headers */
    if (do_send_chunk(request)) {
      // data left to send in the current chunk
      return not_yet_done;
    } else {
      assert(request->current_chunk == NULL);
      assert(request->current_chunk_p == 0);
      /* Transition to Phase B) -- abuse current_chunk_p to store the file fd */
      request->current_chunk_p = PyObject_AsFileDescriptor(request->iterable);
      // don't stop yet, Phase B is still missing
      return not_yet_done;
    }
  } else {
    /* Phase B) -- current_chunk_p contains file fd */
    if (do_sendfile(request)) {
      // Haven't reached the end of file yet
      return not_yet_done;
    } else {
      // Done with the file
      return done;
    }
  }
}


static write_state
on_write_chunk(struct ev_loop* mainloop, Request* request)
{
  if (do_send_chunk(request))
    // data left to send in the current chunk
    return not_yet_done;

  if(request->iterator) {
    /* Reached the end of a chunk in the response iterator. Get next chunk. */
    PyObject* next_chunk = wsgi_iterable_get_next_chunk(request);
    if(next_chunk) {
      /* We found another chunk to send. */
      if(request->state.chunked_response) {
        request->current_chunk = wrap_http_chunk_cruft_around(next_chunk);
        Py_DECREF(next_chunk);
      } else {
        request->current_chunk = next_chunk;
      }
      assert(request->current_chunk_p == 0);
      return not_yet_done;

    } else {
      if(PyErr_Occurred()) {
        /* Trying to get the next chunk raised an exception. */
        PyErr_Print();
        DBG_REQ(request, "Exception in iterator, can not recover");
        return aborted;
      } else {
        /* This was the last chunk; cleanup. */
        Py_CLEAR(request->iterator);
        goto send_terminator_chunk;
      }
    }
  } else {
    /* We have no iterator to get more chunks from, so we're done.
     * Reasons we might end up in this place:
     * A) A parse or server error occurred
     * C) We just finished a chunked response with the call to 'do_send_chunk'
     *    above and now maybe have to send the terminating empty chunk.
     * B) We used chunked responses earlier in the response and
     *    are now sending the terminating empty chunk.
     */
    goto send_terminator_chunk;
  }

  assert(0); // unreachable

send_terminator_chunk:
  if(request->state.chunked_response) {
    /* We have to send a terminating empty chunk + \r\n */
    request->current_chunk = _Bytes_FromString("0\r\n\r\n");
    assert(request->current_chunk_p == 0);
    // Next time we get here, don't send the terminating empty chunk again.
    // XXX This is kind of a hack and should be refactored for easier understanding.
    request->state.chunked_response = false;
    return not_yet_done;
  } else {
    return done;
  }
}

/* Return true if there's data left to send, false if we reached the end of the chunk. */
static bool
do_send_chunk(Request* request)
{
  Py_ssize_t bytes_sent;

  assert(request->current_chunk != NULL);
  assert(!(request->current_chunk_p == _Bytes_GET_SIZE(request->current_chunk)
           && _Bytes_GET_SIZE(request->current_chunk) != 0));

  bytes_sent = write(
    request->client_fd,
    _Bytes_AS_DATA(request->current_chunk) + request->current_chunk_p,
    _Bytes_GET_SIZE(request->current_chunk) - request->current_chunk_p
  );

  if(bytes_sent == -1)
    return handle_nonzero_errno(request);

  request->current_chunk_p += bytes_sent;
  if(request->current_chunk_p == _Bytes_GET_SIZE(request->current_chunk)) {
    Py_CLEAR(request->current_chunk);
    request->current_chunk_p = 0;
    return false;
  }
  return true;
}

/* Return true if there's data left to send, false if we reached the end of the file. */
static bool
do_sendfile(Request* request)
{
  Py_ssize_t bytes_sent = portable_sendfile(
      request->client_fd,
      request->current_chunk_p /* current_chunk_p stores the file fd */
  );
  if(bytes_sent == -1)
    return handle_nonzero_errno(request);
  return bytes_sent != 0;
}

static bool
handle_nonzero_errno(Request* request)
{
  if(errno == EAGAIN || errno == EWOULDBLOCK) {
    /* Try again later */
    return true;
  } else {
    /* Serious transmission failure. Hang up. */
    fprintf(stderr, "Client %d hit errno %d\n", request->client_fd, errno);
    Py_XDECREF(request->current_chunk);
    Py_XCLEAR(request->iterator);
    request->state.keep_alive = false;
    return false;
  }
}

static void
close_connection(struct ev_loop *mainloop, Request* request)
{
  DBG_REQ(request, "Closing socket");
  ev_io_stop(mainloop, &request->ev_watcher);
  close(request->client_fd);
  Request_free(request);
}



/***********************************************
 **************  wsgi.h  *************
 ***********************************************/

 
bool wsgi_call_application(Request*);
PyObject* wsgi_iterable_get_next_chunk(Request*);
PyObject* wrap_http_chunk_cruft_around(PyObject* chunk);

PyTypeObject StartResponse_Type;

/*************************************/

static size_t wsgi_getheaders(Request*, PyObject* buf);

typedef struct {
  PyObject_HEAD
  Request* request;
} StartResponse;

bool
wsgi_call_application(Request* request)
{
  StartResponse* start_response = PyObject_NEW(StartResponse, &StartResponse_Type);
  start_response->request = request;

  /* From now on, `headers` stores the _response_ headers
   * (passed by the WSGI app) rather than the _request_ headers */
  PyObject* request_headers = request->headers;
  request->headers = NULL;

  /* application(environ, start_response) call */
  PyObject* retval = PyObject_CallFunctionObjArgs(
    request->server_info->wsgi_app,
    request_headers,
    start_response,
    NULL /* sentinel */
  );

  Py_DECREF(request_headers);
  Py_DECREF(start_response);

  if(retval == NULL)
    return false;

  /* The following code is somewhat magic, so worth an explanation.
   *
   * If the application we called was a generator, we have to call .next() on
   * it before we do anything else because that may execute code that
   * invokes `start_response` (which might not have been invoked yet).
   * Think of the following scenario:
   *
   *   def app(environ, start_response):
   *     start_response('200 Ok', ...)
   *     yield 'Hello World'
   *
   * That would make `app` return an iterator (more precisely, a generator).
   * Unfortunately, `start_response` wouldn't be called until the first item
   * of that iterator is requested; `start_response` however has to be called
   * _before_ the wsgi body is sent, because it passes the HTTP headers.
   *
   * If the application returned a list this would not be required of course,
   * but special-handling is painful - especially in C - so here's one generic
   * way to solve the problem:
   *
   * Look into the returned iterator in any case. This allows us to do other
   * optimizations, for example if the returned value is a list with exactly
   * one string in it, we can pick the string and throw away the list so bjoern
   * does not have to come back again and look into the iterator a second time.
   */
  PyObject* first_chunk;

  if(PyList_Check(retval) && PyList_GET_SIZE(retval) == 1 &&
     _Bytes_Check(PyList_GET_ITEM(retval, 0)))
  {
    /* Optimize the most common case, a single string in a list: */
    PyObject* tmp = PyList_GET_ITEM(retval, 0);
    Py_INCREF(tmp);
    Py_DECREF(retval);
    retval = tmp;
    goto string; /* eeevil */
  } else if(_Bytes_Check(retval)) {
    /* According to PEP 333 strings should be handled like any other iterable,
     * i.e. sending the response item for item. "item for item" means
     * "char for char" if you have a string. -- I'm not that stupid. */
    string:
    if(_Bytes_GET_SIZE(retval)) {
      first_chunk = retval;
    } else {
      Py_DECREF(retval);
      first_chunk = NULL;
    }
  } else if(FileWrapper_CheckExact(retval)) {
    request->state.use_sendfile = true;
    request->iterable = ((FileWrapper*)retval)->file;
    Py_INCREF(request->iterable);
    Py_DECREF(retval);
    request->iterator = NULL;
    first_chunk = NULL;
  } else {
    /* Generic iterable (list of length != 1, generator, ...) */
    request->iterable = retval;
    request->iterator = PyObject_GetIter(retval);
    if(request->iterator == NULL)
      return false;
    first_chunk = wsgi_iterable_get_next_chunk(request);
    if(first_chunk == NULL && PyErr_Occurred())
      return false;
  }

  if(request->headers == NULL) {
    /* It is important that this check comes *after* the call to
     * wsgi_iterable_get_next_chunk(), because in case the WSGI application
     * was an iterator, there's no chance start_response could be called
     * before. See above if you don't understand what I say. */
    PyErr_SetString(
      PyExc_RuntimeError,
      "wsgi application returned before start_response was called"
    );
    Py_XDECREF(first_chunk);
    return false;
  }
  
  /* keep-alive cruft */
  if(http_should_keep_alive(&request->parser.parser)) { 
    if(request->state.response_length_unknown) {
      if(request->parser.parser.http_major > 0 && request->parser.parser.http_minor > 0) {
        /* On HTTP 1.1, we can use Transfer-Encoding: chunked. */
        request->state.chunked_response = true;
        request->state.keep_alive = true;
      } else {
        /* On HTTP 1.0, we can only resort to closing the connection.  */
        request->state.keep_alive = false;
      }
    } else {
      /* We know the content-length. Can always keep-alive. */
      request->state.keep_alive = true;
    }
  } else {
    /* Explicit "Connection: close" (HTTP 1.1) or missing "Connection: keep-alive" (HTTP 1.0) */
    request->state.keep_alive = false;
  }

  /* Get the headers and concatenate the first body chunk.
   * In the first place this makes the code more simple because afterwards
   * we can throw away the first chunk PyObject; but it also is an optimization:
   * At least for small responses, the complete response could be sent with
   * one send() call (in server.c:ev_io_on_write) which is a (tiny) performance
   * booster because less kernel calls means less kernel call overhead. */
  PyObject* buf = _Bytes_FromStringAndSize(NULL, 1024);
  Py_ssize_t length = wsgi_getheaders(request, buf);

  if(first_chunk == NULL) {
    _Bytes_Resize(&buf, length);
    goto out;
  }

  if(request->state.chunked_response) {
    PyObject* new_chunk = wrap_http_chunk_cruft_around(first_chunk);
    Py_DECREF(first_chunk);
    assert(_Bytes_GET_SIZE(new_chunk) >= _Bytes_GET_SIZE(first_chunk) + 5);
    first_chunk = new_chunk;
  }

  assert(buf);
  _Bytes_Resize(&buf, length + _Bytes_GET_SIZE(first_chunk));
  memcpy((void *)(_Bytes_AS_DATA(buf)+length), _Bytes_AS_DATA(first_chunk),
         _Bytes_GET_SIZE(first_chunk));

  Py_DECREF(first_chunk);

out:
  request->state.wsgi_call_done = true;
  request->current_chunk = buf;
  request->current_chunk_p = 0;
  return true;
}

static inline bool
inspect_headers(Request* request)
{
  Py_ssize_t i;
  PyObject* tuple;

  for(i=0; i<PyList_GET_SIZE(request->headers); ++i) {
    tuple = PyList_GET_ITEM(request->headers, i);

    if(!PyTuple_Check(tuple) || PyTuple_GET_SIZE(tuple) != 2)
      goto err;

    PyObject* field = PyTuple_GET_ITEM(tuple, 0);
    PyObject* value = PyTuple_GET_ITEM(tuple, 1);

    if(!_Unicode_Check(field) || !_Unicode_Check(value))
      goto err;

    if(!strncasecmp(_Unicode_AS_DATA(field), "Content-Length", _Unicode_GET_SIZE(field)))
      request->state.response_length_unknown = false;
  }
  return true;

err:
  TYPE_ERROR_INNER("start_response argument 2", "a list of 2-tuples",
    "(found invalid '%.200s' object at position %zd)", Py_TYPE(tuple)->tp_name, i);
  return false;
}


static size_t
wsgi_getheaders(Request* request, PyObject* buf)
{
  char* bufp = (char *)_Bytes_AS_DATA(buf);

  #define buf_write(src, len) \
    do { \
      size_t n = len; \
      const char* s = src;  \
      while(n--) *bufp++ = *s++; \
    } while(0)
  #define buf_write2(src) buf_write(src, strlen(src))

  /* First line, e.g. "HTTP/1.1 200 Ok" */
  buf_write2("HTTP/1.1 ");
  buf_write(_Unicode_AS_DATA(request->status),
        _Unicode_GET_SIZE(request->status));

  /* Headers, from the `request->headers` mapping.
   * [("Header1", "value1"), ("Header2", "value2")]
   * --> "Header1: value1\r\nHeader2: value2"
   */
  for(Py_ssize_t i=0; i<PyList_GET_SIZE(request->headers); ++i) {
    PyObject *tuple = PyList_GET_ITEM(request->headers, i);
    PyObject *field = PyTuple_GET_ITEM(tuple, 0),
         *value = PyTuple_GET_ITEM(tuple, 1);
    buf_write2("\r\n");
    buf_write(_Unicode_AS_DATA(field), _Unicode_GET_SIZE(field));
    buf_write2(": ");
    buf_write(_Unicode_AS_DATA(value), _Unicode_GET_SIZE(value));
  }

  /* See `wsgi_call_application` */
  if(request->state.keep_alive) {
    buf_write2("\r\nConnection: Keep-Alive");
    if(request->state.chunked_response) {
      buf_write2("\r\nTransfer-Encoding: chunked");
    }
  } else {
    buf_write2("\r\nConnection: close");
  }

  buf_write2("\r\n\r\n");

  return bufp - _Bytes_AS_DATA(buf);
}

inline PyObject*
wsgi_iterable_get_next_chunk(Request* request)
{
  /* Get the next item out of ``request->iterable``, skipping empty ones. */
  PyObject* next;
  while(true) {
    next = PyIter_Next(request->iterator);
    if(next == NULL)
      return NULL;
    if(!_Bytes_Check(next)) {
      TYPE_ERROR("wsgi iterable items", "bytes", next);
      Py_DECREF(next);
      return NULL;
    }
    if(_Bytes_GET_SIZE(next))
      return next;
    Py_DECREF(next);
  }
}

static inline void
restore_exception_tuple(PyObject* exc_info, bool incref_items)
{
  if(incref_items) {
    Py_INCREF(PyTuple_GET_ITEM(exc_info, 0));
    Py_INCREF(PyTuple_GET_ITEM(exc_info, 1));
    Py_INCREF(PyTuple_GET_ITEM(exc_info, 2));
  }
  PyErr_Restore(
    PyTuple_GET_ITEM(exc_info, 0),
    PyTuple_GET_ITEM(exc_info, 1),
    PyTuple_GET_ITEM(exc_info, 2)
  );
}

static PyObject*
start_response(PyObject* self, PyObject* args, PyObject* kwargs)
{
  Request* request = ((StartResponse*)self)->request;

  if(request->state.start_response_called) {
    /* not the first call of start_response --
     * throw away any previous status and headers. */
    Py_CLEAR(request->status);
    Py_CLEAR(request->headers);
    request->state.response_length_unknown = true;
  }

  PyObject* status = NULL;
  PyObject* headers = NULL;
  PyObject* exc_info = NULL;
  if(!PyArg_UnpackTuple(args, "start_response", 2, 3, &status, &headers, &exc_info))
    return NULL;

  if(exc_info && exc_info != Py_None) {
    if(!PyTuple_Check(exc_info) || PyTuple_GET_SIZE(exc_info) != 3) {
      TYPE_ERROR("start_response argument 3", "a 3-tuple", exc_info);
      return NULL;
    }

    restore_exception_tuple(exc_info, /* incref items? */ true);

    if(request->state.wsgi_call_done) {
      /* Too late to change headers. According to PEP 333, we should let
       * the exception propagate in this case. */
      return NULL;
    }

    /* Headers not yet sent; handle this start_response call as if 'exc_info'
     * would not have been passed, but print and clear the exception. */
    PyErr_Print();
  }
  else if(request->state.start_response_called) {
    PyErr_SetString(PyExc_TypeError, "'start_response' called twice without "
                     "passing 'exc_info' the second time");
    return NULL;
  }

  if(!_Unicode_Check(status)) {
    TYPE_ERROR("start_response argument 1", "a 'status reason' string", status);
    return NULL;
  }
  if(!PyList_Check(headers)) {
    TYPE_ERROR("start response argument 2", "a list of 2-tuples", headers);
    return NULL;
  }

  request->headers = headers;

  if(!inspect_headers(request)) {
    request->headers = NULL;
    return NULL;
  }

  request->status = status;

  Py_INCREF(request->status);
  Py_INCREF(request->headers);

  request->state.start_response_called = true;

  Py_RETURN_NONE;
}

PyTypeObject StartResponse_Type = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "start_response",           /* tp_name (__name__)                         */
  sizeof(StartResponse),      /* tp_basicsize                               */
  0,                          /* tp_itemsize                                */
  (destructor)PyObject_FREE,  /* tp_dealloc                                 */
  0, 0, 0, 0, 0, 0, 0, 0, 0,  /* tp_{print,getattr,setattr,compare,...}     */
  start_response              /* tp_call (__call__)                         */
};


PyObject*
wrap_http_chunk_cruft_around(PyObject* chunk)
{
  /* Who the hell decided to use decimal representation for Content-Length
   * but hexadecimal representation for chunk lengths btw!?! Fuck W3C */
  size_t chunklen = _Bytes_GET_SIZE(chunk);
  assert(chunklen);
  char buf[strlen("ffffffff") + 2];
  size_t n = sprintf(buf, "%x\r\n", (unsigned int)chunklen);
  PyObject* new_chunk = _Bytes_FromStringAndSize(NULL, n + chunklen + 2);
  char * new_chunk_p = (char *)_Bytes_AS_DATA(new_chunk);
  memcpy(new_chunk_p, buf, n);
  new_chunk_p += n;
  memcpy(new_chunk_p, _Bytes_AS_DATA(chunk), chunklen);
  new_chunk_p += chunklen;
  *new_chunk_p++ = '\r'; *new_chunk_p = '\n';
  assert(new_chunk_p == _Bytes_AS_DATA(new_chunk) + n + chunklen + 1);
  return new_chunk;
}


/***********************************************
 **************  portable_sendfile.h  *************
 ***********************************************/

Py_ssize_t portable_sendfile(int out_fd, int in_fd);

/*************************************/

#define SENDFILE_CHUNK_SIZE 16*1024

#if defined __APPLE__

  /* OS X */

  #include <sys/socket.h>
  #include <sys/types.h>

  Py_ssize_t portable_sendfile(int out_fd, int in_fd) {
    off_t len = SENDFILE_CHUNK_SIZE;
    if(sendfile(in_fd, out_fd, 0, &len, NULL, 0) == -1)
      return -1;
    return len;
  }

#elif defined(__FreeBSD__) || defined(__DragonFly__)

  #include <sys/socket.h>
  #include <sys/types.h>

  Py_ssize_t portable_sendfile(int out_fd, int in_fd) {
    off_t len;
    if (sendfile(in_fd, out_fd, 0, SENDFILE_CHUNK_SIZE, NULL, &len, 0) == -1) {
      return -1;
    }
    return len;
  }

#else

  /* Linux */

  #include <sys/sendfile.h>

  Py_ssize_t portable_sendfile(int out_fd, int in_fd) {
    return sendfile(out_fd, in_fd, NULL, SENDFILE_CHUNK_SIZE);
  }

#endif



/***********************************************
 **************  filewrapper.h  *************
 ***********************************************/

#define FileWrapper_CheckExact(x) ((x)->ob_type == &FileWrapper_Type)

PyTypeObject FileWrapper_Type;

typedef struct {
  PyObject_HEAD
  PyObject* file;
} FileWrapper;

void _init_filewrapper(void);

/*************************************/

static PyObject*
FileWrapper_New(PyTypeObject* cls, PyObject* args, PyObject* kwargs)
{
  PyObject* file;
  unsigned int ignored_blocksize;

  if(!PyArg_ParseTuple(args, "O|I:FileWrapper", &file, &ignored_blocksize))
    return NULL;

  if(!_File_Check(file)) {
    TYPE_ERROR("FileWrapper argument", "file", file);
    return NULL;
  }

  Py_INCREF(file);
  PyFile_IncUseCount((PyFileObject*)file);

  FileWrapper* wrapper = PyObject_NEW(FileWrapper, cls);
  wrapper->file = file;

  return (PyObject*)wrapper;
}

static PyObject*
FileWrapper_GetAttrO(PyObject* self, PyObject* name)
{
  return PyObject_GetAttr(((FileWrapper*)self)->file, name);
}

static PyObject*
FileWrapper_Iter(PyObject* self)
{
  return PyObject_GetIter(((FileWrapper*)self)->file);
}

static void
FileWrapper_dealloc(PyObject* self)
{
  PyFile_DecUseCount((PyFileObject*)((FileWrapper*)self)->file);
  Py_DECREF(((FileWrapper*)self)->file);
  PyObject_FREE(self);
}

PyTypeObject FileWrapper_Type = {
  PyVarObject_HEAD_INIT(NULL, 0)
  "FileWrapper",                    /* tp_name (__name__)                     */
  sizeof(FileWrapper),              /* tp_basicsize                           */
  0,                                /* tp_itemsize                            */
  (destructor)FileWrapper_dealloc,  /* tp_dealloc                             */
};

void _init_filewrapper(void)
{
  FileWrapper_Type.tp_new = FileWrapper_New;
  FileWrapper_Type.tp_iter = FileWrapper_Iter;
  FileWrapper_Type.tp_getattro = FileWrapper_GetAttrO;
  FileWrapper_Type.tp_flags |= Py_TPFLAGS_DEFAULT;
}



/*
 *
 *
 *
 *
 **/


static PyObject*
run(PyObject* self, PyObject* args)
{
  ServerInfo info;

  PyObject* socket;

  if(!PyArg_ParseTuple(args, "OO:server_run", &socket, &info.wsgi_app)) {
    return NULL;
  }

  info.sockfd = PyObject_AsFileDescriptor(socket);
  if (info.sockfd < 0) {
    return NULL;
  }

  info.host = NULL;
  if (PyObject_HasAttrString(socket, "getsockname")) {
    PyObject* sockname = PyObject_CallMethod(socket, "getsockname", NULL);
    if (sockname == NULL) {
      return NULL;
    }
    if (PyTuple_CheckExact(sockname) && PyTuple_GET_SIZE(sockname) == 2) {
      /* Standard (ipaddress, port) case */
      info.host = PyTuple_GET_ITEM(sockname, 0);
      info.port = PyTuple_GET_ITEM(sockname, 1);
    }
  }

  _initialize_request_module();
  server_run(&info);

  Py_RETURN_NONE;
}

static PyMethodDef Bjoern_FunctionTable[] = {
  {"server_run", (PyCFunction) run, METH_VARARGS, NULL},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef module = {
  PyModuleDef_HEAD_INIT,
  "bjoern",
  NULL,
  -1, /* size of per-interpreter state of the module,
         or -1 if the module keeps state in global variables. */
  Bjoern_FunctionTable,
  NULL, NULL, NULL, NULL,
};
#endif

#if PY_MAJOR_VERSION >= 3
  #define INIT_BJOERN PyInit__bjoern
#else
  #define INIT_BJOERN init_bjoern
#endif

PyMODINIT_FUNC INIT_BJOERN(void)
{
  _init_common();
  _init_filewrapper();

  PyType_Ready(&FileWrapper_Type);
  assert(FileWrapper_Type.tp_flags & Py_TPFLAGS_READY);
  PyType_Ready(&StartResponse_Type);
  assert(StartResponse_Type.tp_flags & Py_TPFLAGS_READY);
  Py_INCREF(&FileWrapper_Type);
  Py_INCREF(&StartResponse_Type);

#if PY_MAJOR_VERSION >= 3
  PyObject* bjoern_module = PyModule_Create(&module);
  if (bjoern_module == NULL) {
    return NULL;
  }

  PyModule_AddObject(bjoern_module, "version", Py_BuildValue("(iii)", 2, 0, 1));
  return bjoern_module;
#else
  PyObject* bjoern_module = Py_InitModule("_bjoern", Bjoern_FunctionTable);
  PyModule_AddObject(bjoern_module, "version", Py_BuildValue("(iii)", 2, 0, 1));
#endif

}
