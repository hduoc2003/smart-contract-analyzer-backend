# Sử dụng hình ảnh Python 3.10.12 trên Alpine Linux 3.18
FROM python:3.10.12
EXPOSE 5000

# Thiết lập thư mục làm việc
WORKDIR /smart-contract-analyzer-backend

# Sao chép tất cả các tệp từ thư mục hiện tại vào /smart-contract-analyzer-backend
COPY . .

# Cài package
RUN apt update && apt install -y curl nano

# Tạo môi trường ảo cho Mythril
WORKDIR /smart-contract-analyzer-backend/tools
RUN python -m venv mythril_venv
RUN ./mythril_venv/bin/pip install mythril

# Cài đặt các dependencies từ file linux_requirements.txt
WORKDIR /smart-contract-analyzer-backend
RUN pip install --no-cache-dir -r linux_requirements.txt

# Cài đặt solc
RUN python ./production/docker_build_script.py

CMD ["gunicorn", "-c", "gunicorn.config.py", "wsgi:app"]
