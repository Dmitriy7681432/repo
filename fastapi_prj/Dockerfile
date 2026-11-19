# Запуск docker docker run --name=my_first_container_v7 -p 1252:8000 my_first_image
# Просмотр образов docker images
# Сборка образа docker build -t my_first_image .
# При запуске docker fastapi будет по такому адресу http://localhost:1252/
FROM python:3.12

WORKDIR /app

COPY requirements.txt .
COPY wheels ./wheels
#RUN pip install --no-cache-dir --upgrade -r requirements.txt
#RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
#RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
# RUN pip install --no-cache-dir -i https://pypi.mirrors.ustc.edu.cn/simple/ --default-timeout=120 -r requirements.txt
# RUN pip install --no-cache-dir -i https://mirrors.huaweicloud.com/repository/pypi/simple --trusted-host mirrors.huaweicloud.com -r requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=./wheels -r requirements.txt

COPY . .

CMD ["python", "main9_docker.py"]