# Deployment Guide for Chatbot Todo Web Application

## Pre-deployment Checklist

### Security
- [ ] All sensitive data removed from version control
- [ ] `.gitignore` properly configured
- [ ] Environment variables stored securely
- [ ] No hardcoded credentials in code

### Backend (for Hugging Face deployment)
- [ ] Update `ALLOWED_ORIGINS` in environment variables to include your frontend domain
- [ ] Use production database (PostgreSQL instead of SQLite if needed)
- [ ] Configure proper logging
- [ ] Enable HTTPS in production

### Frontend (for Vercel deployment)
- [ ] Update `NEXT_PUBLIC_API_BASE_URL` to point to your deployed backend
- [ ] Test all API calls against production backend
- [ ] Optimize assets and enable compression

## Deployment Steps

### Backend Deployment (Hugging Face Spaces)

1. **Prepare repository**:
   - Remove sensitive data from `.env` files
   - Ensure `.gitignore` excludes sensitive files
   - Test locally with environment variables

2. **Set up Hugging Face Space**:
   - Create a new Space with Docker enabled
   - Push your backend code to the Space repository

3. **Configure environment variables in Hugging Face**:
   - `DATABASE_URL`: Your production database URL
   - `SECRET_KEY`: A long, random secret key
   - `GEMINI_API_KEY`: Your Gemini API key
   - `ALLOWED_ORIGINS`: Comma-separated list of allowed origins (including your frontend URL)

4. **Update `ALLOWED_ORIGINS`**:
   - Add your frontend domain to the allowed origins list
   - Example: `https://your-frontend.vercel.app,http://localhost:3000`

### Frontend Deployment (Vercel)

1. **Prepare repository**:
   - Ensure `.env.local` is in `.gitignore`
   - Create `.env.production` with production API URL

2. **Deploy to Vercel**:
   - Connect your GitHub repository to Vercel
   - Set environment variables in Vercel dashboard:
     - `NEXT_PUBLIC_API_BASE_URL`: Your deployed backend URL

3. **Configure environment variables in Vercel**:
   - Go to Project Settings → Environment Variables
   - Add: `NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.com`

## Environment Variable Reference

### Backend `.env` (stored securely in deployment platform)
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@host:port/database_name

# Security Configuration
SECRET_KEY=your-super-secret-and-long-random-string-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,http://localhost:3000

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=app.log

# Database Pool Settings
DB_POOL_SIZE=20
DB_POOL_OVERFLOW=10

# Rate Limiting
RATE_LIMIT_MAX=100
RATE_LIMIT_WINDOW=3600

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
DEFAULT_AI_MODEL=gemini-1.5-flash
```

### Frontend `.env.local` (stored securely in deployment platform)
```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-domain.hf.space
```

## Testing After Deployment

1. **Backend API**:
   - Visit `https://your-backend-domain.hf.space/health` - should return `{"status": "healthy"}`
   - Test authentication endpoints
   - Verify task management endpoints work

2. **Frontend**:
   - Visit your Vercel domain
   - Test user registration and login
   - Verify task management functionality
   - Test AI chatbot functionality

## Troubleshooting

### Common Issues:
- **CORS errors**: Ensure `ALLOWED_ORIGINS` includes your frontend domain
- **Database connection errors**: Verify database URL is correct and accessible
- **JWT errors**: Check that `SECRET_KEY` is consistent and secure
- **API calls failing**: Verify `NEXT_PUBLIC_API_BASE_URL` points to the correct backend

### Monitoring:
- Check application logs in your deployment platform
- Monitor response times and error rates
- Set up alerts for critical failures