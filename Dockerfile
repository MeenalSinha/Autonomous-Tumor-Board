FROM python:3.10-slim

LABEL maintainer="Autonomous Tumor Board Team"
LABEL description="AI-assisted multidisciplinary tumor board preparation system"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p data/outputs data/uploads data/sample_cases

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command (Streamlit UI)
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]

# Alternative: Run FastAPI backend
# CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
