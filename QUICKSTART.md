# The Last Show - Quick Start Guide

## What's Working

✅ **Frontend (Next.js 16)**
- User authentication (login/register)
- Dashboard with obituary management
- Create obituary form
- SSR with proper loading states and error boundaries
- Security headers and CORS configuration

✅ **Backend (FastAPI)**
- JWT authentication with bcrypt
- PostgreSQL database
- AI obituary generation (Groq)
- Image upload to S3 (AWS Lambda)
- Text-to-speech with Amazon Polly (AWS Lambda)
- Full CRUD for obituaries

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run server
uvicorn app.main:app --reload
```

**Backend runs on**: `http://localhost:8000`
**API Docs**: `http://localhost:8000/docs`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

**Frontend runs on**: `http://localhost:3000`

### 3. Test the Application

1. Open `http://localhost:3000`
2. Register a new account
3. Login
4. Create an obituary with:
   - Name
   - Birth date
   - Death date
   - Optional: Upload a photo
5. View the generated obituary with AI text, image, and audio

## Environment Variables

### Backend (.env)

```env
# Required
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/the_last_show
SECRET_KEY=<generate-with-openssl-rand-hex-32>
GROQ_API_KEY=<get-from-console.groq.com>

# AWS Lambda URLs (already configured)
IMAGE_UPLOAD_LAMBDA_URL=https://o4vxwjt2d4psquagdlpn5iz73e0iopax.lambda-url.us-east-2.on.aws/
TTS_LAMBDA_URL=https://45uv5uo4rh4uk4civximfxq65u0kyfpl.lambda-url.us-east-2.on.aws/
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## What Each Service Does

### 🤖 AI Text Generation (Groq)
- Generates respectful, heartfelt obituary text
- Free tier available
- Get API key: https://console.groq.com

### 📸 Image Upload (AWS Lambda)
- Accepts base64-encoded images
- Uploads to S3
- Returns S3 URL
- Already configured and working

### 🎙️ Text-to-Speech (AWS Lambda + Amazon Polly)
- Converts obituary text to natural speech
- Uploads MP3 to S3
- Returns S3 URL
- Already configured and working

## Current Token Expiration

⚠️ **Token Configuration**:
- JWT Token: Expires in **30 minutes**
- Cookie: Expires in **7 days**

**What this means**: After 30 minutes, the token inside the cookie becomes invalid. You'll need to refresh the page to be redirected to login.

## Testing

### Test Backend Only

```bash
cd backend
python test_integration.py
```

This tests:
- User registration
- Login
- Obituary creation with AI, image, and TTS
- Fetching obituaries

### Test Full Stack

1. Start backend: `uvicorn app.main:app --reload`
2. Start frontend: `npm run dev`
3. Open browser: `http://localhost:3000`
4. Register → Login → Create Obituary

## Troubleshooting

### "Connection refused" error
- Make sure PostgreSQL is running
- Check DATABASE_URL in backend/.env

### "Groq API error"
- Verify GROQ_API_KEY in backend/.env
- Check rate limits at https://console.groq.com

### "Image upload failed"
- Lambda function might be slow (S3 upload)
- Check CloudWatch logs for your Lambda
- Timeout is set to 30 seconds

### "TTS generation failed"
- Lambda function processes text with Polly
- Check CloudWatch logs
- Timeout is set to 60 seconds

### Frontend shows "Failed to fetch"
- Make sure backend is running on port 8000
- Check NEXT_PUBLIC_API_URL in frontend/.env.local

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    User's Browser                        │
│              http://localhost:3000                       │
└──────────────────┬──────────────────────────────────────┘
                   │
                   │ Next.js 16 (SSR)
                   │ - Auth pages (login/register)
                   │ - Dashboard
                   │ - Obituary management
                   │
┌──────────────────▼──────────────────────────────────────┐
│              FastAPI Backend                             │
│           http://localhost:8000                          │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   JWT Auth  │  │  PostgreSQL  │  │   Groq AI     │  │
│  │   (bcrypt)  │  │   Database   │  │  (Text Gen)   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │        AWS Lambda Functions                      │   │
│  │  ┌────────────────┐  ┌───────────────────────┐  │   │
│  │  │ Image Upload   │  │  TTS (Polly)          │  │   │
│  │  │ → S3           │  │  → S3                 │  │   │
│  │  └────────────────┘  └───────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

## Next Steps

### Optional Improvements

1. **Fix Token Expiration Mismatch**
   - Either match cookie to 30 min
   - Or extend token to 7 days
   - Or implement refresh tokens

2. **Add Loading Indicators**
   - Show progress during image upload
   - Show progress during TTS generation

3. **Error Handling**
   - Better error messages for users
   - Auto-retry for failed uploads

4. **Production Deployment**
   - Deploy backend to AWS/Heroku
   - Deploy frontend to Vercel
   - Use production database
   - Enable HTTPS

## Support

For issues or questions:
1. Check backend logs: `uvicorn app.main:app --reload`
2. Check browser console for frontend errors
3. Check AWS CloudWatch for Lambda logs
4. Verify all environment variables are set correctly

---

**Everything is ready to use!** 🎉

Your Lambda functions are already configured and working. Just make sure:
1. PostgreSQL is running
2. You have a Groq API key
3. Both backend and frontend servers are running
