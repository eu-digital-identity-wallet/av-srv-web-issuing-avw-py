# ── Stage 1: Node build ───────────────────────────────────────────────────────
FROM node:lts-slim AS node-builder

WORKDIR /build

COPY package*.json ./
COPY tailwind.config.* ./
COPY postcss.config.* ./
COPY assets/ ./assets/
COPY app/ ./app/

RUN npm install
RUN npm run build

# ── Stage 2: Python deps ──────────────────────────────────────────────────────
FROM python:3.13-slim AS python-builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 3: runtime ──────────────────────────────────────────────────────────
FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libffi8 \
    libssl3 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-builder /install /usr/local
COPY --from=node-builder /build/app/static/css/tailwind.css ./app/static/css/tailwind.css
COPY . .

ENV FLASK_APP=app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]