"""Gunicorn設定ファイル"""
import os

# サーバー設定
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
workers = int(os.getenv('GUNICORN_WORKERS', '2'))
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# プロセス設定
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# ログ設定
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# セキュリティ設定
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# パフォーマンス設定
worker_tmp_dir = "/dev/shm" if os.path.exists("/dev/shm") else None