
import os

accesslog = '-' # in log ra stdout

bind: str = f"0.0.0.0:{os.getenv('PORT') or 5000}"
timeout = 600

workers = 1 # bắt buộc bằng 1, xem tại https://flask-socketio.readthedocs.io/en/latest/deployment.html
threads = 5
worker_class = 'gevent' # dùng cho socketio
worker_connections = 1500
