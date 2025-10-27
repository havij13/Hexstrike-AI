# HexStrike AI - Deployment Fix Guide

## 🚨 Issue Analysis

The Render deployment is failing because:
1. **aiohttp build failure**: The `aiohttp==3.8.6` package can't build wheels on Python 3.13
2. **Missing system dependencies**: Some packages require additional build tools
3. **Resource constraints**: Render's free tier has limited build time and memory

## 🔧 Immediate Fixes

### 1. Use the Fixed Dockerfile

Replace your current Dockerfile with `Dockerfile.render`:

```dockerfile
# Optimized for Render deployment
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    HEXSTRIKE_PORT=8888 \
    HEXSTRIKE_HOST=0.0.0.0

# Install minimal dependencies
RUN apt-get update && apt-get install -y \
    curl wget git build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Use fixed requirements
COPY requirements-minimal.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY hexstrike_server.py hexstrike_mcp.py ./
RUN mkdir -p logs data config

EXPOSE ${PORT:-8888}
CMD python3 hexstrike_server.py --port ${PORT:-8888}
```

### 2. Update Requirements

Use the fixed `requirements-minimal.txt`:

```txt
Flask>=2.3.0
Flask-CORS>=4.0.0
flask-restx>=1.3.0
psutil>=5.9.0
requests>=2.31.0
beautifulsoup4>=4.12.0
aiohttp>=3.9.0
python-dotenv>=1.0.0
gunicorn>=21.0.0
prometheus-client>=0.19.0
```

### 3. Update Render Configuration

In your Render dashboard:

1. **Build Command**: `echo "Building HexStrike AI..."`
2. **Start Command**: `python3 hexstrike_server.py --port $PORT`
3. **Dockerfile Path**: `Dockerfile.render`
4. **Environment Variables**:
   - `PYTHON_ENV=production`
   - `LOG_LEVEL=INFO`

## 🚀 Quick Deployment Steps

### Option 1: Minimal Deployment (Recommended for Render)

1. **Create minimal server** (already created as `hexstrike_minimal.py`):
   ```bash
   # Use the minimal server for testing
   cp hexstrike_minimal.py hexstrike_server.py
   ```

2. **Deploy to Render**:
   - Use `Dockerfile.render`
   - Use `requirements-minimal.txt`
   - Set start command: `python3 hexstrike_server.py --port $PORT`

3. **Test deployment**:
   ```bash
   curl https://your-app.onrender.com/health
   ```

### Option 2: Local Testing First

1. **Run the fix script**:
   ```bash
   chmod +x scripts/fix-deployment.sh
   ./scripts/fix-deployment.sh
   ```

2. **Test locally**:
   ```bash
   docker build -f Dockerfile.lightweight -t hexstrike-test .
   docker run -p 8888:8888 hexstrike-test
   curl http://localhost:8888/health
   ```

3. **Deploy after successful local test**

## 🔍 Troubleshooting

### If Build Still Fails

1. **Use Python 3.10 instead**:
   ```dockerfile
   FROM python:3.10-slim
   ```

2. **Install packages individually**:
   ```dockerfile
   RUN pip install Flask==2.3.3 && \
       pip install Flask-CORS==4.0.0 && \
       pip install requests==2.31.0
   ```

3. **Use pre-built wheels**:
   ```dockerfile
   RUN pip install --only-binary=all -r requirements.txt
   ```

### If Memory Issues Occur

1. **Reduce dependencies**:
   ```txt
   # Absolute minimum
   Flask==2.3.3
   requests==2.31.0
   gunicorn==21.2.0
   ```

2. **Use multi-stage build**:
   ```dockerfile
   FROM python:3.11-slim as builder
   # Install dependencies
   
   FROM python:3.11-slim as runtime
   # Copy only what's needed
   ```

## 🎯 Alternative Deployment Options

### Railway (Often More Reliable)

1. **Connect GitHub repo to Railway**
2. **Use `railway.toml` configuration**
3. **Deploy automatically on push**

### Fly.io

1. **Install Fly CLI**
2. **Run `fly launch`**
3. **Use `fly.toml` configuration**

### Docker Hub + Cloud Run

1. **Build and push to Docker Hub**:
   ```bash
   docker build -f Dockerfile.render -t your-username/hexstrike-ai .
   docker push your-username/hexstrike-ai
   ```

2. **Deploy to Google Cloud Run**:
   ```bash
   gcloud run deploy hexstrike-ai \
     --image your-username/hexstrike-ai \
     --port 8888 \
     --allow-unauthenticated
   ```

## 📊 Monitoring Deployment

### Health Check Endpoints

- **Health**: `/health`
- **API Status**: `/api`
- **Metrics**: `/metrics`

### Log Monitoring

```bash
# Render logs
render logs --service your-service-name

# Railway logs
railway logs

# Docker logs
docker logs container-name
```

## 🔒 Security Considerations

### For Production Deployment

1. **Add authentication**:
   ```python
   from flask_httpauth import HTTPBasicAuth
   auth = HTTPBasicAuth()
   ```

2. **Rate limiting**:
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=get_remote_address)
   ```

3. **HTTPS only**:
   ```python
   from flask_talisman import Talisman
   Talisman(app, force_https=True)
   ```

## 🎉 Success Indicators

Your deployment is successful when:

- ✅ Health endpoint returns 200: `curl https://your-app.onrender.com/health`
- ✅ API responds: `curl https://your-app.onrender.com/api`
- ✅ No error logs in deployment console
- ✅ Metrics endpoint works: `curl https://your-app.onrender.com/metrics`

## 📞 Support

If you continue having issues:

1. **Check the logs** in your deployment platform
2. **Test locally first** with the lightweight Dockerfile
3. **Use the minimal server** for initial deployment
4. **Gradually add features** once basic deployment works

The key is to start minimal and add complexity incrementally!