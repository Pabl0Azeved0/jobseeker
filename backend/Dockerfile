FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Adding non-root user
RUN useradd appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "jobseeker.wsgi:application", "--bind", "0.0.0.0:8000"]
