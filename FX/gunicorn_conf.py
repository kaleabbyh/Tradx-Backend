# import json
import multiprocessing
import os

workers_per_core_str = os.getenv("GUNICORN_WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("GUNICORN_MAX_WORKERS", "10")
use_max_workers = None

if max_workers_str:
    use_max_workers = int(max_workers_str)

web_concurrency_str = os.getenv("GUNICORN_WEB_CONCURRENCY", None)
host = os.getenv("BACKEND_HOST", "0.0.0.0")
port = os.getenv("BACKEND_PORT", "8000")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")

if bind_env:
    use_bind = bind_env
else:
    use_bind = f"{host}:{port}"

cores = multiprocessing.cpu_count()
workers_per_core = (float(workers_per_core_str) * 2) + 1
default_web_concurrency = workers_per_core * cores

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if use_max_workers:
        web_concurrency = min(web_concurrency, use_max_workers)

accesslog_var = os.getenv("GUNICORN_ACCESS_LOG", "-")
use_accesslog = accesslog_var or None
errorlog_var = os.getenv("GUNICORN_ERROR_LOG", "-")
use_errorlog = errorlog_var or None
graceful_timeout_str = os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "60")
timeout_str = os.getenv("GUNICORN_TIMEOUT", "60")
keepalive_str = os.getenv("GUNICORN_KEEP_ALIVE", "5")
max_requests_str = os.getenv("GUNICORN_MAX_REQUESTS", "0")


# Gunicorn config variables
# worker_class = "FX.workers.ConfigurableWorker"
loglevel = use_loglevel.lower()
workers = web_concurrency
bind = use_bind
errorlog = use_errorlog
# create the folder if no exist
if not os.path.exists("/tmp/shm"):
    os.makedirs("/tmp/shm")
worker_tmp_dir = "/tmp/shm"
accesslog = use_accesslog
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)
max_requests = int(max_requests_str)

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "use_max_workers": use_max_workers,
    "web_concurrency": web_concurrency,
    "host": host,
    "port": port,
    "cores": cores,
}

# print(json.dumps(log_data))
