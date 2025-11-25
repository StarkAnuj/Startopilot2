# 🚀 AI Assistant Deployment Guide

## 🎯 Quick Start Deployment Options

### Option 1: Vercel (Recommended - Fastest) ⚡
**Best for**: Production deployment with global CDN and serverless functions

```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login to Vercel
vercel login

# 3. Deploy from root directory
vercel

# 4. Set environment variable in Vercel dashboard
# Add GEMINI_API_KEY in Project Settings > Environment Variables
```

### Option 2: Docker (Full Control) 🐳
**Best for**: Self-hosted deployment with complete control

```bash
# 1. Build and run with Docker Compose (easiest)
docker-compose up --build -d

# 2. Or build manually
docker build -t ai-assistant .
docker run -p 3000:3000 -p 8000:8000 -e GEMINI_API_KEY=your_key ai-assistant
```

### Option 3: Local Production Build 💻
**Best for**: Local testing and development

```bash
# Build frontend
cd frontend
npm run build
npm start

# In another terminal - run backend
cd ..
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

## 📋 Pre-Deployment Checklist

### 🔑 Required Environment Variables
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 🛠️ System Requirements
- **Node.js**: 18.x or higher
- **Python**: 3.11 or higher  
- **Memory**: Minimum 1GB RAM
- **Storage**: 500MB free space

### 🌐 Browser Compatibility
- ✅ Chrome 90+ (Recommended)
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 🎨 Deployment Platforms

### 1. 🔥 Vercel Deployment (Production-Ready)

#### Step-by-Step Vercel Setup:

1. **Fork/Clone Repository**
   ```bash
   git clone your-repo-url
   cd ai-assistant
   ```

2. **Install Dependencies**
   ```bash
   cd frontend && npm install
   cd ../
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   - Copy `.env.production` to `.env.local`
   - Add your `GEMINI_API_KEY`

4. **Deploy to Vercel**
   ```bash
   npx vercel --prod
   ```

5. **Set Environment Variables in Vercel Dashboard**
   - Go to Project Settings > Environment Variables
   - Add: `GEMINI_API_KEY` = `your_actual_api_key`

#### Vercel Configuration Features:
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Serverless functions
- ✅ Automatic deployments from Git
- ✅ Built-in analytics

### 2. 🐳 Docker Deployment

#### Quick Docker Setup:
```bash
# Clone and navigate
git clone your-repo
cd ai-assistant

# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Deploy with Docker Compose
docker-compose up -d

# Check status
docker-compose ps
docker-compose logs -f
```

#### Manual Docker Build:
```bash
# Build image
docker build -t ai-assistant .

# Run container
docker run -d \
  --name ai-assistant-app \
  -p 3000:3000 \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  ai-assistant

# Check logs
docker logs -f ai-assistant-app
```

### 3. 🏗️ Cloud Platform Deployments

#### AWS Deployment:
```bash
# Using AWS App Runner or ECS
# 1. Push Docker image to ECR
# 2. Create App Runner service
# 3. Configure environment variables
```

#### Google Cloud Platform:
```bash
# Using Cloud Run
gcloud run deploy ai-assistant \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances:
```bash
# Deploy to Azure
az container create \
  --resource-group myResourceGroup \
  --name ai-assistant \
  --image your-image \
  --ports 3000 8000
```

## 🔧 Configuration Options

### Environment Variables (Production):
```env
# Required
GEMINI_API_KEY=your_gemini_api_key

# Optional Performance Tuning
NODE_ENV=production
ENABLE_COMPRESSION=true
RESPONSE_CACHE_TTL=300
MAX_FILE_SIZE=10485760

# Security (Production)
CORS_ORIGINS=https://yourdomain.com
HTTPS_ONLY=true

# Monitoring
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=info
```

### Next.js Build Configuration:
```bash
# Standard build
npm run build

# Standalone build (for Docker)
BUILD_STANDALONE=true npm run build

# Static export (for CDN)
npm run export
```

## 🚀 Performance Optimization

### 1. Frontend Optimizations:
- ✅ Image optimization enabled
- ✅ Code splitting implemented
- ✅ Compression enabled
- ✅ Caching strategies in place

### 2. Backend Optimizations:
- ✅ Async request handling
- ✅ Response compression
- ✅ Connection pooling
- ✅ Request timeout limits

### 3. Infrastructure:
- ✅ CDN for static assets
- ✅ Load balancing (if needed)
- ✅ Health checks configured
- ✅ Automatic scaling

## 📊 Monitoring & Maintenance

### Health Check Endpoints:
- Frontend: `GET /` (Next.js ready check)
- Backend: `GET /health` (API health status)
- Combined: `GET /api/health` (Full system check)

### Logging:
```bash
# Docker logs
docker-compose logs -f

# Application logs
tail -f logs/app.log

# Error monitoring
# Configure Sentry or similar service
```

### Performance Monitoring:
- Response time tracking
- Error rate monitoring  
- Memory usage alerts
- CPU usage monitoring

## 🔐 Security Considerations

### Production Security:
1. **HTTPS Only**: Force HTTPS in production
2. **Environment Variables**: Never commit API keys
3. **CORS**: Configure allowed origins
4. **Rate Limiting**: Implement API rate limits
5. **Content Security Policy**: Add CSP headers

### Security Headers:
```javascript
// In next.config.js
async headers() {
  return [
    {
      source: '/:path*',
      headers: [
        {
          key: 'X-Frame-Options',
          value: 'DENY',
        },
        {
          key: 'X-Content-Type-Options', 
          value: 'nosniff',
        },
        {
          key: 'Referrer-Policy',
          value: 'origin-when-cross-origin',
        },
      ],
    },
  ]
}
```

## 🛠️ Troubleshooting Common Issues

### Issue 1: API Connection Failed
```bash
# Check backend is running
curl http://localhost:8000/health

# Verify environment variables
echo $GEMINI_API_KEY

# Check logs
docker logs container_name
```

### Issue 2: Build Failures
```bash
# Clear cache and rebuild
npm run clean
npm install
npm run build

# Python dependencies
pip install --upgrade -r requirements.txt
```

### Issue 3: Camera/Audio Access
- Ensure HTTPS in production
- Check browser permissions
- Verify certificate validity

## 📱 Mobile & PWA Support

### Progressive Web App Features:
- ✅ Service worker ready
- ✅ Manifest file configured
- ✅ Offline functionality
- ✅ Install prompts

### Mobile Optimizations:
- ✅ Responsive design
- ✅ Touch-friendly interface
- ✅ Optimized media handling
- ✅ Reduced bundle size

## 🎉 Post-Deployment Steps

1. **Test All Features**:
   - ✅ Camera functionality
   - ✅ Audio recording
   - ✅ AI responses
   - ✅ Voice playback

2. **Performance Testing**:
   - ✅ Load testing
   - ✅ Response time verification  
   - ✅ Mobile compatibility

3. **Monitoring Setup**:
   - ✅ Error tracking
   - ✅ Performance monitoring
   - ✅ Usage analytics

4. **Backup Strategy**:
   - ✅ Database backups (if applicable)
   - ✅ Configuration backups
   - ✅ Recovery procedures

---

## 🆘 Quick Help

### Get Support:
- 📖 Check the logs first
- 🐛 Review common issues above
- 🔍 Test individual components
- 📧 Contact support with error details

### Useful Commands:
```bash
# Check all services
docker-compose ps

# View real-time logs
docker-compose logs -f

# Restart services
docker-compose restart

# Update deployment
git pull && docker-compose up --build -d
```

**Your AI Assistant is now ready for production! 🚀**