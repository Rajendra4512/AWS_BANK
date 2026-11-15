FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    OPENBLAS_NUM_THREADS=1 \
    OMP_NUM_THREADS=1 \
    MKL_NUM_THREADS=1

WORKDIR /srv

# Copy dependency requirements and downloaded Linux wheels
COPY requirements.txt .
COPY wheels/ /srv/wheels/

# Install dependencies completely offline
RUN python -m pip install \
    --no-index \
    --find-links=/srv/wheels \
    --no-cache-dir \
    -r requirements.txt \
    && useradd -m -u 10001 app \
    && rm -rf /srv/wheels

# Copy application source
COPY app ./app

# Create application data directories
RUN mkdir -p /srv/data /srv/artifacts \
    && chown -R app:app /srv

USER app

EXPOSE 7005

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7005", "--workers", "1"]