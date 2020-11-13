FROM python:3.7-slim

# 设置镜像的时区为上海
ENV TZ Asia/Shanghai

RUN sed -i 's#http://deb.debian.org#https://mirrors.163.com#g' /etc/apt/sources.list


# 安装vim
RUN apt update && apt install -y vim

# 安装python环境
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r /code/requirements.txt

COPY . /code
# 设置工作目录
WORKDIR /code

CMD python dtw.py