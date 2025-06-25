import os

# CHEMIN CORRIGÉ vers le projet
BASE_DIR = '/var/www/cashprint'

# Liaison et workers
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging avec le BON chemin
accesslog = os.path.join(BASE_DIR, 'logs/access.log')
errorlog = os.path.join(BASE_DIR, 'logs/error.log')
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s>

# Process naming
proc_name = 'cashprint_gunicorn'

# Process
pidfile = os.path.join(BASE_DIR, 'gunicorn.pid')
user = "cashprint"
group = "www-data"

# Application
chdir = BASE_DIR
preload_app = True
raw_env = [
    'DJANGO_SETTINGS_MODULE=cashprint_project.settings',
]

