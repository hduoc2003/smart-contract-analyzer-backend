#!/bin/bash
# Tạo nhóm người dùng 'docker'

# Thêm người dùng vào nhóm Docker để tránh lỗi permission denied
usermod -aG docker www-data

# Set quyền truy cập cho Docker socket
chmod 666 /var/run/docker.sock

# Thực hiện lệnh khởi chạy thực tế của ứng dụng
exec "$@"
