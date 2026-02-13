# Multi-stage Dockerfile for PetHelper Bot

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user first so we can install packages into their home
RUN useradd -m -u 1000 botuser

# Copy Python dependencies into botuser's home (Python looks in ~/.local when running as botuser)
COPY --from=builder /root/.local /home/botuser/.local
RUN chown -R botuser:botuser /home/botuser/.local
ENV PATH=/home/botuser/.local/bin:$PATH

# Copy application code
COPY . .

# Create logs dir (not in repo due to .gitignore) so botuser can write
RUN mkdir -p /app/logs

RUN chown -R botuser:botuser /app

USER botuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the bot
CMD ["python", "main.py"]
