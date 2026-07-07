# Stage 1: Build dependencies
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Install packages into the user directory for easy migration to the runner stage
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Production runner
FROM python:3.11-slim as runner

WORKDIR /app

# Create a secure non-root user
RUN groupadd -g 10001 appuser && \
    useradd -u 10001 -g appuser -s /bin/sh -m appuser

# Copy dependencies and application files
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Adjust permissions so that appuser can run the server and write files if needed
RUN chown -R appuser:appuser /app

USER appuser

# Configure environment path and runtime variables
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
