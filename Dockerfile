# 使用Python 3.11作为基础镜像
FROM python:3.11-slim as base

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# 安装系统依赖
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Poetry
RUN pip3 install poetry

# 复制项目文件
COPY pyproject.toml poetry.lock ./
COPY taskmanager ./taskmanager  

FROM base as app
# 安装项目依赖
RUN which poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# 暴露端口
EXPOSE 8000

# 设置启动命令（使用环境变量来决定启动Django还是Celery）
CMD if [ "$SERVICE_TYPE" = "celery" ]; then \
        celery -A taskmanager worker -l INFO; \
    elif [ "$SERVICE_TYPE" = "celery-beat" ]; then \
        celery -A taskmanager beat -l INFO; \
    else \
        python taskmanager/manage.py runserver 0.0.0.0:8000; \
    fi 