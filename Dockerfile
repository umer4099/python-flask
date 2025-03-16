# ===========================
# 1st Stage: Builder
# ===========================
FROM python:3.10 AS builder

# Set working directory
WORKDIR /app

# Install system dependencies required by psycopg2
RUN apt-get update && apt-get install -y libpq-dev

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN pip install --no-cache-dir --user -r requirements.txt

# ===========================
# 2nd Stage: Final, Lightweight Image
# ===========================
FROM python:3.10-slim

# Install only runtime dependencies for psycopg2
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home appuser

# Set working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Change ownership for security
RUN chown -R appuser:appuser /app /home/appuser

# Switch to non-root user
USER appuser

# Set PATH to use installed dependencies
ENV PATH="/home/appuser/.local/bin:$PATH"

# Expose application port
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
