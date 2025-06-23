# Configuration Gunicorn pour Cash Print
import multiprocessing

# Serveur
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Logs
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process
daemon = False
pidfile = "gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# SSL (si nécessaire)
# keyfile = "path/to/keyfile"
# certfile = "path/to/certfile"

# Performance
keepalive = 2
timeout = 30
graceful_timeout = 30
preload_app = True

# Sécurité
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190