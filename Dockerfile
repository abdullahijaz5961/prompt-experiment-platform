FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY data ./data
COPY scripts ./scripts
COPY dashboard ./dashboard
COPY config ./config
RUN pip install --no-cache-dir -e .
ENV PYTHONUNBUFFERED=1
CMD ["prompt-lab", "serve", "--host", "0.0.0.0", "--port", "8609"]
