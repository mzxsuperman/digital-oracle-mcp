FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .
RUN uv pip install --system "fastmcp>=2.0" "git+https://github.com/komako-workshop/digital-oracle.git@v1.0.3"

COPY mcp_server.py .

EXPOSE 8800

CMD ["python", "mcp_server.py", "--sse"]
