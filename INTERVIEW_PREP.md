# Interview Preparation Guide - The Last Show Project

## Project Overview
The Last Show is an AI-powered obituary generator application that allows users to create, manage, and share obituaries with AI-generated text, images, and text-to-speech audio capabilities.

**Tech Stack:**
- **Frontend:** Next.js 16 (React 19) with TypeScript
- **Backend:** FastAPI (Python) with PostgreSQL
- **Infrastructure:** Pulumi with AWS (S3, Lambda, Polly)
- **AI Services:** Groq AI for text generation, AWS Polly for TTS

---

## 1. Why Did You Choose Next.js?

### Key Reasons:

**1. Server-Side Rendering (SSR) and Server Components**
- Next.js 16 provides advanced server components that allow me to fetch data on the server before sending HTML to the client
- In `frontend/app/dashboard/page.tsx:12-17`, I use server-side authentication checks and data fetching:
  ```typescript
  export default async function DashboardPage() {
    const user = await getCurrentUser();
    if (!user) {
      redirect("/login");
    }
  ```
- This ensures unauthorized users are redirected before the page even renders on the client

**2. Server Actions for Secure Authentication**
- Next.js Server Actions (`frontend/app/actions/auth.ts`) allow secure server-side operations without exposing sensitive logic to the client
- JWT tokens are stored in HTTP-only cookies (`frontend/app/actions/auth.ts:31-36`), making them inaccessible to JavaScript and preventing XSS attacks:
  ```typescript
  cookieStore.set("access_token", data.access_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    maxAge: 60 * 30, // 30 minutes
  });
  ```

**3. Modern React 19 Features**
- Full support for React 19 with improved performance
- Built-in form handling with `useActionState` hook
- Automatic code splitting and optimization

**4. Built-in TypeScript Support**
- Type safety across the entire frontend codebase
- Better developer experience with autocomplete and error detection

**5. File-based Routing**
- Intuitive project structure with app directory
- Route groups like `(auth)` for organizing login/register pages without affecting URLs

**6. Production-Ready Features**
- Built-in image optimization
- API routes for backend integration
- Automatic static optimization
- Edge runtime support

---

## 2. Why Did You Choose Pulumi?

### Key Reasons:

**1. Infrastructure as Code (IaC) Using Real Programming Languages**
- Unlike CloudFormation (JSON/YAML) or Terraform (HCL), Pulumi uses Python (`infra/__main__.py`)
- This allows me to use familiar programming constructs like functions, loops, and conditionals
- Example from `infra/__main__.py:11-13`:
  ```python
  def name(resource: str) -> str:
      """Generate resource name: project-resource-stack"""
      return f"{project}-{resource}-{stack}"
  ```

**2. Easy AWS Resource Management**
- Created S3 buckets for images and audio with public read access
- Set up Lambda functions with proper IAM roles and permissions
- Configured CORS policies for cross-origin requests from the frontend

**3. Declarative and Reproducible Infrastructure**
- The entire AWS infrastructure is defined in code
- Can easily replicate the environment across different stages (dev, staging, prod)
- Version control for infrastructure changes

**4. Automatic Dependency Management**
- Pulumi automatically handles resource dependencies
- Example from `infra/__main__.py:74`: Lambda policy depends on public access block
  ```python
  opts=pulumi.ResourceOptions(depends_on=[images_bucket_public_access_block])
  ```

**5. Simplified Resource Creation**
- Created Lambda Function URLs instead of complex API Gateway setup
- Managed IAM roles and policies programmatically
- Easy outputs for environment variables (`infra/__main__.py:247-250`)

**6. Cost-Effective Architecture**
- Using Lambda Function URLs eliminates the need for API Gateway, reducing costs
- S3 for cheap storage
- Lambda for pay-per-use serverless compute

---

## 3. How Does the Project Work?

### Architecture Flow:

```
User Request → Next.js Frontend → FastAPI Backend → PostgreSQL Database
                                 ↓
                            AWS Lambda Functions
                                 ↓
                        S3 Buckets (Images/Audio)
```

### Key Components:

**Frontend (Next.js):**
- Server-rendered pages with authentication checks
- Server Actions for secure API calls
- Client components for interactive UI
- Cookie-based session management

**Backend (FastAPI):**
- RESTful API with JWT authentication
- User registration and login endpoints
- CRUD operations for obituaries
- Integration with AI services (Groq for text, Lambda for images/TTS)

**Database (PostgreSQL):**
- User table with hashed passwords
- Obituary table with relationships to users
- SQLAlchemy ORM for database operations

**Infrastructure (AWS):**
- **S3 Buckets:** Store images and audio files with public read access
- **Lambda Functions:**
  - Image upload handler
  - Text-to-speech generator using AWS Polly
- **Lambda Function URLs:** Direct HTTPS endpoints for Lambda invocations

---

## 4. How Does Authentication Work?

### Authentication Flow:

**Registration (`backend/app/routes/auth.py:15-31`):**
1. User submits email, password, and full name
2. Backend checks if email already exists
3. Password is hashed using bcrypt (`backend/app/services/auth_service.py:14-16`)
4. User record is created in the database
5. Auto-login after successful registration

**Login (`backend/app/routes/auth.py:33-55`):**
1. User submits email and password
2. Backend verifies credentials using bcrypt (`backend/app/services/auth_service.py:10-12`)
3. If valid, a JWT token is created with user's email as the subject
4. Token expires in 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES`)
5. Token is returned to frontend

**Token Generation (`backend/app/services/auth_service.py:18-29`):**
```python
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
```

**Token Storage (Frontend):**
- JWT stored in HTTP-only cookie (`frontend/app/actions/auth.ts:31-36`)
- Cookie settings:
  - `httpOnly: true` - JavaScript cannot access it (prevents XSS)
  - `secure: true` (production) - Only sent over HTTPS
  - `sameSite: 'lax'` - CSRF protection
  - `maxAge: 1800` (30 minutes) - Matches token expiration

---

## 5. How Do You Ensure Non-Authorized Users Can't Access Protected Routes?

### Backend Protection:

**Dependency Injection (`backend/app/dependencies.py:13-39`):**
```python
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    # Extract token from Authorization header
    token = credentials.credentials

    # Decode and validate token
    email = decode_access_token(token)

    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

    # Get user from database
    user = get_user_by_email(db, email=email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
```

**Protected Routes (`backend/app/routes/obituaries.py`):**
- `/auth/me` (line 57-63): Requires valid JWT token
- `/obituaries/my-obituaries` (line 110-122): Only returns current user's obituaries
- `POST /obituaries` (line 19-92): Only authenticated users can create
- `DELETE /obituaries/{id}` (line 144-165): Only owner can delete

**Authorization Example:**
```python
@router.delete("/{obituary_id}")
async def delete_obituary(
    obituary_id: str,
    current_user: User = Depends(get_current_user),  # ← Authentication check
    db: Session = Depends(get_db)
):
    # Verify ownership before deletion
    success = obituary_service.delete_obituary(
        db=db,
        obituary_id=obituary_id,
        user_id=current_user.id  # ← Authorization check
    )
```

### Frontend Protection:

**Server-Side Checks (`frontend/app/dashboard/page.tsx:12-17`):**
```typescript
export default async function DashboardPage() {
  const user = await getCurrentUser();

  if (!user) {
    redirect("/login");  // Redirect before page renders
  }
  // ... rest of component
}
```

**Token Validation (`frontend/lib/auth.ts:6-30`):**
```typescript
export async function getCurrentUser(): Promise<User | null> {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");

  if (!token) {
    return null;  // No token = not authenticated
  }

  // Verify token with backend
  const response = await fetch(`${API_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
    cache: "no-store",
  });

  if (!response.ok) {
    return null;  // Invalid token
  }

  return await response.json();
}
```

### Multi-Layer Security:

1. **HTTP-only Cookies:** Prevent XSS attacks
2. **Token Expiration:** 30-minute automatic logout
3. **Server-Side Validation:** Every protected API call validates the token
4. **Database Lookup:** Token email is verified against database records
5. **Ownership Checks:** Users can only modify their own resources
6. **CORS Configuration:** Only localhost:3000 can access the API (in development)

---

## 6. How Do You Generate JWT Tokens?

### Token Structure:

**Payload (`backend/app/routes/auth.py:50-53`):**
```python
access_token = create_access_token(
    data={"sub": user.email},  # Subject = user identifier
    expires_delta=access_token_expires
)
```

**Algorithm and Secret:**
- **Algorithm:** HS256 (HMAC with SHA-256)
- **Secret Key:** Stored in environment variables (`backend/app/config.py:8`)
- **Library:** `python-jose` for JWT operations

**Token Creation Process (`backend/app/services/auth_service.py:18-29`):**
1. Copy the data dictionary (contains user email in "sub" field)
2. Calculate expiration time (current time + 30 minutes)
3. Add expiration to the payload
4. Encode using SECRET_KEY and HS256 algorithm
5. Return the encoded JWT string

**Token Validation (`backend/app/services/auth_service.py:31-41`):**
```python
def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
```

### Security Features:

1. **Signed Tokens:** Can't be tampered with without the secret key
2. **Expiration:** Automatically invalid after 30 minutes
3. **No Sensitive Data:** Only stores user email (identifier)
4. **Stateless:** No need to store sessions in database

---

## 7. What Happens When the Token Expires?

### Current Implementation:

**Token Expiration Time:**
- **Access Token:** 30 minutes (`backend/app/config.py:10`)
- **Cookie Max Age:** 30 minutes (`frontend/app/actions/auth.ts:35`)

**When Token Expires:**
1. Backend returns 401 Unauthorized error
2. Frontend detects invalid token in `getCurrentUser()` (`frontend/lib/auth.ts:22-24`)
3. User is redirected to login page (`frontend/app/dashboard/page.tsx:15-17`)
4. User must log in again to get a new token

### Potential Improvements for Production:

**Option 1: Refresh Tokens (Not Currently Implemented)**
- Issue two tokens: short-lived access token + long-lived refresh token
- When access token expires, use refresh token to get new access token
- Refresh token stored in database with ability to revoke

**Option 2: Sliding Sessions**
- Extend token expiration on each request
- User stays logged in as long as they're active

**Option 3: Remember Me Feature**
- Optional longer expiration for convenience
- Balance security with user experience

---

## Demo Flow for Interview

### 1. Architecture Overview
Start with the high-level diagram:
```
User → Next.js (SSR + Server Actions)
       ↓
       FastAPI (JWT Auth + REST API)
       ↓
       PostgreSQL (User + Obituary Data)
       ↓
       AWS (S3 + Lambda + Polly)
```

### 2. Authentication Demo

**Show Registration:**
1. Open `/register` page
2. Fill in the form (explain form validation with Zod)
3. Submit and show how it redirects to dashboard
4. Mention password hashing with bcrypt

**Show Login:**
1. Open `/login` page
2. Enter credentials
3. Explain JWT generation in the Network tab
4. Show cookie storage in DevTools

### 3. Protected Routes Demo

**Backend Protection:**
1. Open `/docs` (FastAPI Swagger UI)
2. Try calling `/auth/me` without token → 401 error
3. Authenticate with token
4. Try `/obituaries/my-obituaries` → Success

**Frontend Protection:**
1. Log out
2. Try to access `/dashboard` directly → Redirects to login
3. Show code in `dashboard/page.tsx:15-17`

### 4. Authorization Demo

**Ownership Checks:**
1. Create an obituary as User A
2. Try to delete it as User B → 404 error
3. Show code in `obituaries.py:153-156`

### 5. Infrastructure Demo

**Pulumi Resources:**
1. Show `infra/__main__.py`
2. Run `pulumi stack output` to show deployed resources
3. Explain S3 buckets, Lambda functions, IAM roles

### 6. Token Lifecycle

**Show Expiration:**
1. Log in and note the time
2. Wait 30 minutes (or modify config for demo)
3. Try to access protected route → Redirects to login
4. Explain token validation in `auth_service.py:31-41`

---

## Common Interview Questions & Answers

### Q: Why not use NextAuth.js for authentication?
**A:** I wanted to learn the underlying mechanisms of JWT authentication and have full control over the implementation. This also allows me to use the same authentication system across different frontend frameworks if needed.

### Q: How would you handle token refresh?
**A:** I would implement a refresh token strategy:
- Store refresh token in HTTP-only cookie with longer expiration (7 days)
- Store refresh token in database with user_id for revocation capability
- Create `/auth/refresh` endpoint that validates refresh token and issues new access token
- Frontend middleware checks token expiration and automatically refreshes before requests

### Q: Why Pulumi over Terraform?
**A:** Pulumi allows me to use Python, which is already the language of my backend. This reduces context switching and allows me to use familiar constructs. I can also share types and utilities between infrastructure and application code.

### Q: How do you prevent CSRF attacks?
**A:** Multiple layers:
1. SameSite cookie attribute (`lax` mode)
2. CORS configuration limiting allowed origins
3. HTTP-only cookies prevent JavaScript access
4. Token validation on every request

### Q: What about rate limiting and brute force protection?
**A:** For production, I would add:
- Rate limiting middleware (e.g., `slowapi` for FastAPI)
- Account lockout after failed attempts
- CAPTCHA for repeated failures
- IP-based throttling

### Q: How do you handle database migrations?
**A:** I use Alembic (visible in `requirements.txt:1`). It allows:
- Version-controlled database schema changes
- Rollback capability
- Automatic migration generation from SQLAlchemy models

### Q: Why FastAPI instead of Django?
**A:** FastAPI offers:
- Better performance (async/await support)
- Automatic API documentation (Swagger UI)
- Modern Python type hints
- Lighter weight for API-focused applications
- Native Pydantic integration for validation

### Q: How do you test authentication?
**A:** I have test files set up:
- `backend/tests/test_auth_service.py` - Unit tests for auth functions
- `backend/tests/test_auth_routes.py` - Integration tests for endpoints
- `frontend/__tests__/actions/auth.test.ts` - Frontend action tests

---

## Key Technical Highlights to Mention

1. **Security-First Design:**
   - HTTP-only cookies
   - Password hashing with bcrypt
   - JWT with expiration
   - Environment variable management
   - CORS configuration

2. **Modern Tech Stack:**
   - React 19 with Server Components
   - Next.js 16 with App Router
   - FastAPI with async support
   - Infrastructure as Code with Pulumi

3. **Scalable Architecture:**
   - Serverless Lambda functions
   - Separate frontend/backend
   - Cloud storage with S3
   - Stateless authentication

4. **AI Integration:**
   - Groq API for obituary generation
   - AWS Polly for text-to-speech
   - Image upload handling

5. **Developer Experience:**
   - TypeScript for type safety
   - Automatic API documentation
   - Hot reload in development
   - Version control for infrastructure

---

## Quick Reference: File Locations

**Authentication:**
- Backend JWT service: `backend/app/services/auth_service.py`
- Backend auth routes: `backend/app/routes/auth.py`
- Backend dependencies: `backend/app/dependencies.py`
- Frontend auth library: `frontend/lib/auth.ts`
- Frontend auth actions: `frontend/app/actions/auth.ts`

**Configuration:**
- Backend settings: `backend/app/config.py`
- Infrastructure: `infra/__main__.py`
- Frontend package: `frontend/package.json`
- Backend requirements: `backend/requirements.txt`

**Protected Routes:**
- Dashboard page: `frontend/app/dashboard/page.tsx`
- Obituaries API: `backend/app/routes/obituaries.py`

---

## Final Tips for the Interview

1. **Be Confident:** You built this - you understand it better than anyone
2. **Start High-Level:** Give the architecture overview first
3. **Use Code Examples:** Reference specific files and line numbers
4. **Explain Trade-offs:** Show you understand alternatives
5. **Discuss Improvements:** Mention what you'd add for production
6. **Show Testing:** Mention the test files you've set up
7. **Security Focus:** Emphasize your security considerations
8. **Be Honest:** If you don't know something, say so and explain how you'd find out

Good luck with your interview!
