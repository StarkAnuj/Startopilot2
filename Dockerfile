# Multi-stage Docker build for AI Assistant
FROM node:18-alpine AS frontend-builder

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

# Python backend stage
FROM python:3.11-slim AS backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy API code
COPY api/ ./api/

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/.next ./frontend/.next
COPY --from=frontend-builder /app/frontend/public ./frontend/public
COPY --from=frontend-builder /app/frontend/package.json ./frontend/

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "🚀 Starting AI Assistant..."\n\
# Start backend\n\
cd /app && python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 &\n\
echo "✅ Backend started on port 8000"\n\
# Start frontend\n\
cd /app/frontend && npm start &\n\
echo "✅ Frontend started on port 3000"\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# Expose ports
EXPOSE 3000 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["/app/start.sh"]