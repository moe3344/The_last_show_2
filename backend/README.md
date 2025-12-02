# The Last Show - Backend API

AI-powered obituary generator with text-to-speech and image upload capabilities.

## Features

- **AI Text Generation**: Uses Groq (free ChatGPT alternative) to generate heartfelt obituaries
- **Image Upload**: Uploads photos to S3 via AWS Lambda
- **Text-to-Speech**: Converts obituaries to audio using Amazon Polly via AWS Lambda
- **User Authentication**: JWT-based auth with bcrypt password hashing
- **PostgreSQL Database**: Stores users and obituaries

## Tech Stack

- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Database
- **Groq**: AI text generation (free!)
- **AWS Lambda**: Serverless functions for image upload and TTS
- **Amazon Polly**: Text-to-speech service
- **Amazon S3**: Media storage

## Setup Instructions

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
```

Required environment variables:
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret (generate with `openssl rand -hex 32`)
- `GROQ_API_KEY`: Get free API key from https://console.groq.com
- `IMAGE_UPLOAD_LAMBDA_URL`: Your AWS Lambda function URL for image upload
- `TTS_LAMBDA_URL`: Your AWS Lambda function URL for TTS

### 3. Setup Database

```bash
# Make sure PostgreSQL is running
# Create database
createdb the_last_show

# Tables will be created automatically when you run the app
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication

- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info (protected)

### Obituaries

- `POST /obituaries/` - Create obituary with AI, image, and TTS (protected)
- `GET /obituaries/` - Get all public obituaries
- `GET /obituaries/my-obituaries` - Get user's obituaries (protected)
- `GET /obituaries/{id}` - Get specific obituary
- `DELETE /obituaries/{id}` - Delete obituary (protected, owner only)

## Complete Flow

1. **User registers/logs in**
   - Receives JWT token

2. **User creates obituary**
   - Provides: name, birth date, death date, optional image
   - Backend:
     - Generates obituary text using Groq AI
     - Uploads image to S3 (if provided)
     - Saves obituary to database
     - Generates audio using Amazon Polly
     - Updates obituary with audio URL

3. **User can view/manage obituaries**
   - See list of their obituaries
   - View individual obituaries with text, image, and audio
   - Delete their own obituaries

## Testing

Run the integration test script:

```bash
# Make sure the API is running first
python test_integration.py
```

This will test the complete flow:
1. User registration
2. Login
3. Obituary creation with AI, image upload, and TTS
4. Fetching obituaries

## AWS Lambda Functions

You need two Lambda functions:

### Image Upload Lambda

**Trigger**: Lambda Function URL
**Purpose**: Upload base64-encoded images to S3

**Expected Request**:
```json
{
  "image": "base64-encoded-image-data",
  "filename": "photo.jpg"
}
```

**Expected Response**:
```json
{
  "image_url": "https://your-bucket.s3.amazonaws.com/images/uuid.jpg"
}
```

### TTS Lambda

**Trigger**: Lambda Function URL
**Purpose**: Convert text to speech using Amazon Polly and upload to S3

**Expected Request**:
```json
{
  "text": "Obituary text here...",
  "obituary_id": "uuid-of-obituary"
}
```

**Expected Response**:
```json
{
  "audio_url": "https://your-bucket.s3.amazonaws.com/audio/uuid.mp3"
}
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # Database models
│   │   ├── user.py
│   │   └── obituary.py
│   ├── routes/          # API endpoints
│   │   ├── auth.py
│   │   └── obituaries.py
│   ├── schemas/         # Pydantic schemas
│   │   ├── user.py
│   │   └── obituary.py
│   ├── services/        # Business logic
│   │   ├── ai_service.py       # Groq AI integration
│   │   ├── auth_service.py     # JWT & password hashing
│   │   ├── lambda_service.py   # AWS Lambda calls
│   │   ├── obituary_service.py # CRUD operations
│   │   └── user_service.py     # User management
│   ├── config.py        # Settings
│   ├── database.py      # DB connection
│   ├── dependencies.py  # FastAPI dependencies
│   └── main.py          # Application entry point
├── venv/                # Virtual environment
├── .env                 # Environment variables (not in git)
├── .env.example         # Example env file
├── requirements.txt     # Python dependencies
└── test_integration.py  # Integration tests
```

## Troubleshooting

### Database Connection Error
```bash
# Make sure PostgreSQL is running
# Check your DATABASE_URL in .env
```

### Lambda Timeout
```bash
# Image upload timeout: 30 seconds
# TTS timeout: 60 seconds
# Check Lambda function logs in AWS CloudWatch
```

### Groq API Error
```bash
# Verify your API key
# Check rate limits: https://console.groq.com
```

## Development

```bash
# Install dev dependencies
pip install httpx pytest pytest-asyncio

# Run tests
pytest

# Format code
black app/

# Type checking
mypy app/
```

## License

MIT
