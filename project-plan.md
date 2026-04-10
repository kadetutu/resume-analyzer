---

# Plan: Resume Analysis Web Application

## TL;DR
Build a full-stack web application enabling users to upload resumes and compare them against job descriptions using AI analysis. Frontend will be a React SPA with Zustand state management and JWT auth; backend is a Python FastAPI service with PostgreSQL database, AI analysis engine, and rate limiting. The app follows three main flows: authentication → resume upload/job description input → AI analysis results display.

---

## Architecture Overview

### Technology Stack
**Frontend:** React + Vite, Tailwind CSS, Material UI, Zustand, JWT  
**Backend:** Python FastAPI, SQLModel ORM, Pydantic validation, PostgreSQL, PyTest  
**Security:** JWT token-based auth, bcrypt password hashing  
**Rate Limiting:** Subscription-based per-user rate limiting

### Directory Structure
```
resume-analyzer/
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ui/              (Material UI components)
│   │   │   ├── auth/            (LoginPage.jsx, SignupPage.jsx)
│   │   │   ├── dashboard/       (DashboardPage.jsx, ResumeUpload.jsx, JobDescInput.jsx)
│   │   │   ├── results/         (AnalysisResultsPage.jsx)
│   │   │   ├── common/          (Navbar.jsx, Footer.jsx, ErrorBoundary.jsx)
│   │   │   └── forms/           (LoginForm.jsx, SignupForm.jsx)
│   │   ├── pages/               (Index page structure)
│   │   ├── store/               (Zustand stores: auth, resumes, analysis)
│   │   ├── services/            (API client, auth service)
│   │   ├── hooks/               (Custom React hooks)
│   │   ├── utils/               (Helpers, validators, constants)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── auth.py         (Login, signup, refresh token endpoints)
│   │   │   │   ├── resumes.py      (Upload, retrieve resume endpoints)
│   │   │   │   ├── analysis.py     (Resume analysis endpoint)
│   │   │   │   └── __init__.py
│   │   │   └── __init__.py
│   │   ├── models/
│   │   │   ├── user.py            (SQLModel User schema)
│   │   │   ├── resume.py           (SQLModel Resume schema)
│   │   │   ├── analysis.py         (SQLModel Analysis result schema)
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── user.py            (Pydantic request/response schemas)
│   │   │   ├── resume.py
│   │   │   ├── analysis.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── auth_service.py     (JWT, password hashing logic)
│   │   │   ├── oauth2_service.py   (OAuth2 provider integration)
│   │   │   ├── ai_service.py       (OpenAI integration, analysis engine)
│   │   │   ├── user_service.py     (User CRUD operations)
│   │   │   ├── resume_service.py   (Resume CRUD, file handling)
│   │   │   ├── rate_limit_service.py  (Rate limiting logic)
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py           (Environment config, settings)
│   │   │   ├── security.py         (JWT utilities, password utilities)
│   │   │   ├── database.py         (DB connection, session management)
│   │   │   └── __init__.py
│   │   ├── middleware/
│   │   │   ├── auth_middleware.py  (JWT validation middleware)
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── file_handler.py     (Resume file parsing, storage)
│   │   │   ├── validators.py       (Input validation)
│   │   │   └── __init__.py
│   │   ├── main.py                 (FastAPI app setup)
│   │   └── __init__.py
│   ├── tests/
│   │   ├── test_auth.py            (Auth endpoint tests)
│   │   ├── test_oauth2.py          (OAuth2 flow tests)
│   │   ├── test_resumes.py         (Resume endpoint tests)
│   │   ├── test_analysis.py        (Analysis endpoint tests)
│   │   ├── test_auth_service.py    (Auth service unit tests)
│   │   ├── test_ai_service.py      (AI service tests)
│   │   ├── test_rate_limit_service.py  (Rate limiting tests)
│   │   ├── conftest.py             (PyTest fixtures)
│   │   └── __init__.py
│   ├── alembic/                     (Database migrations)
│   ├── requirements.txt
│   ├── .env.example
│   ├── pytest.ini
│   └── main.py                      (Entry point)
│
└── README.md
```

---

## Implementation Phases

### Phase 1: Backend Infrastructure (Can start in parallel with Phase 2)
**Status:** Not Started
**Dependencies:** None

1. **Database Setup** — Initialize PostgreSQL, create SQLModel models (User, Resume, AnalysisResult, SubscriptionTier, RateLimitLog, OAuth2Provider), setup Alembic migrations
2. **Core Configuration & Security** — Environment variables, JWT utilities, password hashing, token operations
3. **Authentication Service** — Email/password registration and login, JWT generation, refresh tokens
4. **OAuth2 Integration Service** — Google, GitHub, Facebook OAuth2 flows with secure token storage
5. **Authentication API Endpoints** — Register, login, refresh, logout, OAuth2 authorize/callback endpoints
6. **JWT Middleware & Authorization** — JWT validation, protected route decorators
7. **User Management Service** — User CRUD, subscription tier management
8. **Resume Management Service** — PDF/DOCX parsing, file upload/storage, resume CRUD
9. **AI Analysis Service** — OpenAI API integration, resume matching logic, token tracking
10. **Resume API Endpoints** — Upload, list, get, delete resume operations
11. **Rate Limiting & Subscription Service** — Subscription tier checking, usage tracking, quota enforcement
12. **Analysis API Endpoint** — Resume analysis endpoint with rate limiting
13. **Error Handling & Validation** — Custom exceptions, input validation, error middleware
14. **Testing Setup & Tests** — PyTest configuration, comprehensive test coverage (70%+)
15. **Documentation & Setup** — requirements.txt, .env.example, README.md
16. **Application Entry Point** — FastAPI app configuration, middleware stack, router registration

### Phase 2: Frontend Infrastructure (Can start in parallel with Phase 1)
**Status:** Not Started
**Dependencies:** None initially; Phase 3 depends on Phase 1 API completion

1. **Project Initialization** — React + Vite setup, dependencies, Tailwind CSS dark mode, ESLint/Prettier
2. **State Management** — Zustand stores (authStore, resumeStore, analysisStore, subscriptionStore)
3. **API Service Layer** — Axios client with JWT interceptor, auth/resume/analysis services
4. **Custom React Hooks** — useAuth, useResume, useAnalysis, useJWT
5. **Material UI Custom Components** — Button, Input, Card, Modal, Alert, Spinner, Textarea, FormError
6. **Common Components** — Navbar, Footer, ErrorBoundary, LoadingSpinner, Notification
7. **Authentication Components** — LoginPage, SignupPage, LoginForm, SignupForm, ProtectedRoute
8. **Dashboard Components** — DashboardPage, ResumeUpload, JobDescriptionInput, SubscriptionBanner
9. **Results Components** — AnalysisResultsPage, MatchScoreDisplay, KeywordMatches, MissingKeywords, Recommendations, ExportResults
10. **Utilities** — Validators, constants, helpers, dark mode toggle
11. **Main App Structure** — App.jsx with React Router, routing configuration
12. **Theme & Style Configuration** — Tailwind config, color palettes, dark mode colors
13. **Environment Configuration** — .env.example, .env.local
14. **Package & Build Configuration** — package.json, vite.config.js, ESLint, Prettier, index.html

### Phase 3: Integration & Refinement
**Status:** Pending Phase 1 & 2
**Dependencies:** Phase 1 backend API complete, Phase 2 frontend complete

1. **Backend-Frontend Connection** — Connect frontend to backend APIs, verify JWT lifecycle, test OAuth2 flows
2. **Complete User Flow Testing** — Test all authentication methods, resume upload, analysis, rate limiting, dark mode
3. **Error Scenario Testing** — Test invalid uploads, missing inputs, API failures, network errors
4. **Performance Optimization** — Bundle analysis, code splitting, database optimization, query tuning
5. **Security Review** — CORS verification, JWT security, password security, OAuth2 security, SQL injection prevention
6. **Documentation** — Comprehensive README files, API documentation, architecture docs, deployment guide
7. **Deployment Preparation** — Docker containers, docker-compose.yml, environment configuration
8. **Final Testing & QA** — Regression testing, cross-browser, mobile, accessibility, load testing, security audit

---

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| **JWT (Access + Refresh Tokens)** | Balances security (short-lived access) with usability (long-lived refresh) |
| **OpenAI API** | Easy integration, scalable, no GPU required, fast MVP development |
| **PDF & DOCX Support** | Cover majority of resume formats using PyPDF2 and python-docx |
| **Subscription-Based Rate Limiting** | Flexible monetization model; supports Free/Pro/Enterprise tiers |
| **Full OAuth2 Implementation** | Reduces user friction, increases adoption, better user experience |
| **Zustand State Management** | Minimal boilerplate, excellent TypeScript support, lightweight |
| **SQLModel ORM** | Combines Pydantic validation with SQLAlchemy, FastAPI-native |
| **React + Vite** | Fast builds, excellent developer experience, broad ecosystem |

---

## Data Models & Schemas

### User Model
- id (Integer, Primary Key)
- email (String, Unique, Required)
- username (String, Unique)
- password_hash (String, Required)
- subscription_tier (String) — 'free', 'pro', 'enterprise'
- created_at (DateTime)
- updated_at (DateTime)

### Resume Model
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → User)
- file_name (String)
- file_path (String)
- file_content (Binary)
- content_text (String, Nullable) — extracted resume text
- uploaded_at (DateTime)

### AnalysisResult Model
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → User)
- resume_id (Integer, Foreign Key → Resume)
- job_description (String)
- match_score (Float)
- matched_keywords (JSON Array)
- missing_keywords (JSON Array)
- recommendations (JSON Array)
- analyzed_at (DateTime)

### SubscriptionTier Model
- id (Integer, Primary Key)
- tier_name (String) — 'free', 'pro', 'enterprise'
- monthly_limit (Integer)

### RateLimitLog Model
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key → User)
- analysis_count (Integer)
- subscription_tier_id (Integer, Foreign Key → SubscriptionTier)
- reset_date (DateTime)

### OAuth2Provider Model
- id (Integer, Primary Key)
- provider_name (String) — 'google', 'github', 'facebook'
- provider_user_id (String)
- user_id (Integer, Foreign Key → User)
- access_token (String, Encrypted)
- refresh_token (String, Encrypted, Nullable)
- created_at (DateTime)

---

## API Endpoints Summary

### Authentication
- `POST /api/v1/auth/register` — Register new user (email, password)
- `POST /api/v1/auth/login` — Login user (email, password)
- `POST /api/v1/auth/refresh` — Refresh access token
- `POST /api/v1/auth/logout` — Logout user
- `GET /api/v1/auth/google/authorize` — Google OAuth2 authorize
- `GET /api/v1/auth/google/callback` — Google OAuth2 callback
- `GET /api/v1/auth/github/authorize` — GitHub OAuth2 authorize
- `GET /api/v1/auth/github/callback` — GitHub OAuth2 callback
- `GET /api/v1/auth/facebook/authorize` — Facebook OAuth2 authorize
- `GET /api/v1/auth/facebook/callback` — Facebook OAuth2 callback

### Resumes
- `POST /api/v1/resumes/upload` — Upload resume file (multipart/form-data)
- `GET /api/v1/resumes` — List user's resumes
- `GET /api/v1/resumes/{resume_id}` — Get resume details
- `DELETE /api/v1/resumes/{resume_id}` — Delete resume

### Analysis
- `POST /api/v1/analysis/analyze` — Analyze resume against job description

---

## Complete Todo List

### PHASE 1: BACKEND INFRASTRUCTURE (85 Tasks)

#### 1.1 Database Setup & Configuration (10 tasks)
- [ ] Initialize PostgreSQL database
- [ ] Create Alembic migration environment
- [ ] Create SQLModel User model with subscription_tier field
- [ ] Create SQLModel Resume model
- [ ] Create SQLModel AnalysisResult model
- [ ] Create SQLModel SubscriptionTier model
- [ ] Create SQLModel RateLimitLog model
- [ ] Create SQLModel OAuth2Provider model
- [ ] Create database session management in app/core/database.py
- [ ] Generate and run initial migration

#### 1.2 Core Configuration & Security (5 tasks)
- [ ] Create .env and .env.example files with all required variables
- [ ] Create app/core/config.py with Pydantic Settings
- [ ] Implement JWT utilities in app/core/security.py (create, validate, refresh tokens)
- [ ] Implement password hashing utilities with bcrypt
- [ ] Create helper functions for token operations

#### 1.3 Authentication Service - Email/Password (5 tasks)
- [ ] Create app/schemas/user.py with Pydantic models
- [ ] Create app/services/auth_service.py with register_user(), login_user()
- [ ] Implement password validation logic (strength requirements)
- [ ] Add email format validation and uniqueness check
- [ ] Create token refresh logic with refresh token rotation

#### 1.4 OAuth2 Integration Service (6 tasks)
- [ ] Create app/services/oauth2_service.py
- [ ] Implement Google OAuth2 flow (authorize_url, exchange_code, get_user_info)
- [ ] Implement GitHub OAuth2 flow
- [ ] Implement Facebook OAuth2 flow
- [ ] Create method to link OAuth2 account to existing user or create new user
- [ ] Store OAuth2 tokens securely in database

#### 1.5 Authentication API Endpoints (11 tasks)
- [ ] Create app/api/v1/auth.py router
- [ ] POST /api/v1/auth/register endpoint
- [ ] POST /api/v1/auth/login endpoint
- [ ] POST /api/v1/auth/refresh endpoint
- [ ] POST /api/v1/auth/logout endpoint
- [ ] GET /api/v1/auth/google/authorize endpoint
- [ ] GET /api/v1/auth/google/callback endpoint
- [ ] GET /api/v1/auth/github/authorize endpoint
- [ ] GET /api/v1/auth/github/callback endpoint
- [ ] GET /api/v1/auth/facebook/authorize endpoint
- [ ] GET /api/v1/auth/facebook/callback endpoint

#### 1.6 JWT Middleware & Authorization (3 tasks)
- [ ] Create app/middleware/auth_middleware.py
- [ ] Implement JWT validation middleware
- [ ] Create dependency injection for protected routes

#### 1.7 User Management Service (3 tasks)
- [ ] Create app/services/user_service.py
- [ ] Implement get_user_profile() with subscription tier info
- [ ] Create update_subscription_tier() method

#### 1.8 Resume Management Service (7 tasks)
- [ ] Create app/services/resume_service.py
- [ ] Implement PDF parsing using PyPDF2
- [ ] Implement DOCX parsing using python-docx
- [ ] Create upload_resume() method
- [ ] Create extract_text_from_resume() method
- [ ] Create methods for resume CRUD operations
- [ ] Implement file validation (format, size)

#### 1.9 AI Analysis Service - OpenAI Integration (5 tasks)
- [ ] Create app/services/ai_service.py
- [ ] Initialize OpenAI client with API key
- [ ] Create analyze_resume() method to call OpenAI API
- [ ] Design and implement prompt structure for resume matching
- [ ] Implement response parsing and error handling

#### 1.10 Resume API Endpoints (4 tasks)
- [ ] Create app/api/v1/resumes.py router
- [ ] POST /api/v1/resumes/upload endpoint
- [ ] GET /api/v1/resumes and GET /api/v1/resumes/{resume_id} endpoints
- [ ] DELETE /api/v1/resumes/{resume_id} endpoint

#### 1.11 Rate Limiting & Subscription Service (5 tasks)
- [ ] Create app/services/rate_limit_service.py
- [ ] Implement check_subscription_limit() method
- [ ] Implement log_analysis_usage() method
- [ ] Create reset_usage_count() method
- [ ] Implement rate limiting decorator for protected endpoints

#### 1.12 Analysis API Endpoint (1 task)
- [ ] POST /api/v1/analysis/analyze endpoint with rate limiting and subscription checks

#### 1.13 Error Handling & Validation (4 tasks)
- [ ] Create app/utils/validators.py
- [ ] Create custom exception classes
- [ ] Add global error handler middleware
- [ ] Implement input validation for all endpoints

#### 1.14 Testing Setup & Tests (8 tasks)
- [ ] Create tests/conftest.py with PyTest fixtures
- [ ] Create comprehensive auth tests (email/password and OAuth2)
- [ ] Create resume endpoint and service tests
- [ ] Create analysis endpoint tests
- [ ] Create AI service tests
- [ ] Create rate limiting tests
- [ ] Setup pytest.ini
- [ ] Achieve 70%+ test coverage

#### 1.15 Documentation & Setup (3 tasks)
- [ ] Create backend/requirements.txt with all dependencies
- [ ] Create backend/.env.example with template environment variables
- [ ] Create backend/README.md with setup instructions

#### 1.16 Application Entry Point (2 tasks)
- [ ] Create backend/main.py entry point
- [ ] Configure FastAPI app, middleware stack, and router registration

---

### PHASE 2: FRONTEND INFRASTRUCTURE (90 Tasks)

#### 2.1 Project Initialization (5 tasks)
- [ ] Initialize React + Vite project in /frontend
- [ ] Install all dependencies (react-router-dom, zustand, tailwindcss, @mui/material, axios, jwt-decode, etc.)
- [ ] Configure Tailwind CSS with dark mode support
- [ ] Configure ESLint and Prettier
- [ ] Setup Vite config with API proxy

#### 2.2 State Management - Zustand Stores (4 tasks)
- [ ] Create store/authStore.js (user, tokens, login/logout actions, localStorage persistence)
- [ ] Create store/resumeStore.js (resumes list, selected resume, upload/delete actions)
- [ ] Create store/analysisStore.js (analysis results, loading state, error handling)
- [ ] Create store/subscriptionStore.js (subscription tier, usage tracking)

#### 2.3 API Service Layer (4 tasks)
- [ ] Create services/apiClient.js with Axios + JWT interceptor
- [ ] Create services/authService.js (register, login, OAuth2, logout, refresh)
- [ ] Create services/resumeService.js (upload, list, get, delete)
- [ ] Create services/analysisService.js (analyze endpoint)

#### 2.4 Custom React Hooks (4 tasks)
- [ ] Create hooks/useAuth.js (auth state, operations, token management)
- [ ] Create hooks/useResume.js (resume state, operations)
- [ ] Create hooks/useAnalysis.js (analysis state, operations)
- [ ] Create hooks/useJWT.js (token decode, expiration check, refresh)

#### 2.5 Material UI Custom Components (8 tasks)
- [ ] Create components/ui/Button.jsx
- [ ] Create components/ui/Input.jsx
- [ ] Create components/ui/Card.jsx
- [ ] Create components/ui/Modal.jsx
- [ ] Create components/ui/Alert.jsx
- [ ] Create components/ui/Spinner.jsx
- [ ] Create components/ui/Textarea.jsx
- [ ] Create components/ui/FormError.jsx

#### 2.6 Common Components (5 tasks)
- [ ] Create components/common/Navbar.jsx (user menu, theme toggle, logout)
- [ ] Create components/common/Footer.jsx
- [ ] Create components/common/ErrorBoundary.jsx
- [ ] Create components/common/LoadingSpinner.jsx
- [ ] Create components/common/Notification.jsx (toast notifications)

#### 2.7 Authentication Components (5 tasks)
- [ ] Create components/auth/LoginPage.jsx (email/password form, OAuth2 buttons)
- [ ] Create components/auth/SignupPage.jsx (registration form)
- [ ] Create components/forms/LoginForm.jsx (reusable form)
- [ ] Create components/forms/SignupForm.jsx (reusable form)
- [ ] Create components/auth/ProtectedRoute.jsx (route wrapper)

#### 2.8 Dashboard Components (4 tasks)
- [ ] Create components/dashboard/DashboardPage.jsx (main layout)
- [ ] Create components/dashboard/ResumeUpload.jsx (drag-and-drop, file handling)
- [ ] Create components/dashboard/JobDescriptionInput.jsx (textarea, submit)
- [ ] Create components/dashboard/SubscriptionBanner.jsx (usage display)

#### 2.9 Results Components (6 tasks)
- [ ] Create components/results/AnalysisResultsPage.jsx (main results container)
- [ ] Create components/results/MatchScoreDisplay.jsx (visual score display)
- [ ] Create components/results/KeywordMatches.jsx (matched keywords display)
- [ ] Create components/results/MissingKeywords.jsx (missing keywords display)
- [ ] Create components/results/Recommendations.jsx (AI recommendations)
- [ ] Create components/results/ExportResults.jsx (download/share functionality)

#### 2.10 Utilities (4 tasks)
- [ ] Create utils/validators.js (email, password, file validation)
- [ ] Create utils/constants.js (API endpoints, error messages, UI constants)
- [ ] Create utils/helpers.js (token helpers, formatting utilities)
- [ ] Create utils/darkModeToggle.js (theme management, localStorage)

#### 2.11 Main App Structure (3 tasks)
- [ ] Create App.jsx with React Router setup and route definitions
- [ ] Create main.jsx entry point
- [ ] Create index.css with global styles and Tailwind imports

#### 2.12 Theme & Style Configuration (3 tasks)
- [ ] Create tailwind.config.js with dark mode configuration
- [ ] Define color palette (light and dark modes)
- [ ] Configure responsive breakpoints and component spacing

#### 2.13 Environment Configuration (2 tasks)
- [ ] Create .env.example with template variables
- [ ] Create .env.local for development

#### 2.14 Package & Build Configuration (5 tasks)
- [ ] Create frontend/package.json with dependency list and scripts
- [ ] Create frontend/vite.config.js with development config
- [ ] Create frontend/.eslintrc.json with linting rules
- [ ] Create frontend/.prettierrc for code formatting
- [ ] Create frontend/index.html entry HTML

---

### PHASE 3: INTEGRATION & REFINEMENT (50 Tasks)

#### 3.1 Backend-Frontend Connection (6 tasks)
- [ ] Configure frontend API client to connect to backend
- [ ] Test all API calls from frontend
- [ ] Verify JWT token generation and storage
- [ ] Test OAuth2 flows end-to-end
- [ ] Verify CORS configuration
- [ ] Fix any integration issues

#### 3.2 Complete User Flow Testing (10 tasks)
- [ ] Test email/password registration flow
- [ ] Test email/password login flow
- [ ] Test Google OAuth2 login
- [ ] Test GitHub OAuth2 login
- [ ] Test Facebook OAuth2 login
- [ ] Test resume upload and display
- [ ] Test analysis flow (submit, process, display results)
- [ ] Test rate limiting (hit limit and verify error)
- [ ] Test subscription tier transitions
- [ ] Test logout and token refresh

#### 3.3 Error Scenario Testing (8 tasks)
- [ ] Test invalid file uploads (wrong format, too large)
- [ ] Test missing job description
- [ ] Test API calls without JWT token
- [ ] Test expired token handling
- [ ] Test rate limit exceeded responses
- [ ] Test network connectivity errors
- [ ] Test OpenAI API failures
- [ ] Test duplicate email registration

#### 3.4 Performance Optimization (6 tasks)
- [ ] Analyze frontend bundle size
- [ ] Implement code splitting for routes
- [ ] Optimize resume file uploads (streaming, compression)
- [ ] Add database indexes for frequently queried fields
- [ ] Test page load times (target < 3s)
- [ ] Test analysis response times (target < 10s)

#### 3.5 Security Review (6 tasks)
- [ ] Verify CORS headers
- [ ] Verify JWT tokens are securely stored
- [ ] Verify password hashing implementation
- [ ] Verify OAuth2 secrets are not exposed
- [ ] Test SQL injection prevention
- [ ] Test rate limiting effectiveness

#### 3.6 Documentation (6 tasks)
- [ ] Create comprehensive frontend README
- [ ] Create comprehensive backend README
- [ ] Create API documentation with endpoints and examples
- [ ] Create Architecture documentation with diagrams
- [ ] Create database schema documentation
- [ ] Create deployment guide

#### 3.7 Deployment Preparation (6 tasks)
- [ ] Create Dockerfile for backend
- [ ] Create Dockerfile for frontend
- [ ] Create docker-compose.yml
- [ ] Test Docker build and run
- [ ] Setup environment variables for staging and production
- [ ] Create deployment checklist

#### 3.8 Final Testing & QA (8 tasks)
- [ ] Full regression testing of all features
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile device testing
- [ ] Accessibility testing (WCAG compliance)
- [ ] Load testing (simulate concurrent users)
- [ ] Security penetration testing
- [ ] User acceptance testing
- [ ] Performance benchmarking

---

## Expected Deliverables by Phase

### Phase 1 (Backend) — ~85 Tasks
✅ Fully functional FastAPI backend with all endpoints  
✅ PostgreSQL database with Alembic migrations  
✅ JWT + OAuth2 authentication (Google, GitHub, Facebook)  
✅ Resume management system with PDF/DOCX parsing  
✅ OpenAI integration for resume analysis  
✅ Subscription-based rate limiting  
✅ PyTest test suite with 70%+ coverage  
✅ Comprehensive documentation and setup guide  

### Phase 2 (Frontend) — ~90 Tasks
✅ Fully functional React SPA with Vite  
✅ Zustand state management  
✅ Material UI + Tailwind CSS components  
✅ Dark mode support with theme toggle  
✅ JWT + OAuth2 authentication UI  
✅ Resume upload with drag-and-drop  
✅ Analysis results display with visualizations  
✅ Comprehensive error handling and validation  
✅ Responsive design (mobile/tablet/desktop)  
✅ Documentation and setup guide  

### Phase 3 (Integration & Refinement) — ~50 Tasks
✅ Fully integrated full-stack application  
✅ All user flows tested end-to-end  
✅ Security audit passed  
✅ Performance optimization completed  
✅ Docker containerization  
✅ Complete documentation  
✅ Production-ready deployment  

**Total Tasks:** 225+

---

## Success Criteria

### Backend Success Criteria
- All API endpoints return correct status codes and response formats
- JWT tokens are validated on all protected routes
- Rate limiting prevents exceeding subscription tier limits
- Resume files are parsed correctly and text extracted
- OpenAI API integration works reliably with error handling
- Database migrations run without errors
- All PyTests pass with 70%+ coverage
- No SQL injection vulnerabilities
- No XSS vulnerabilities
- No sensitive data logged

### Frontend Success Criteria
- React app builds without errors
- All routes render correctly and navigate seamlessly
- Forms validate input and display errors
- Resume upload with drag-and-drop works smoothly
- Analysis results display with proper formatting
- Dark mode toggle persists across sessions
- JWT tokens are correctly stored and sent with requests
- Unauthorized access is blocked and redirects to login
- All Material UI components are styled consistently
- Mobile responsive layout works on all screen sizes
- Page load time < 3 seconds
- Analysis response time < 10 seconds

### Integration Success Criteria
- Complete user registration and login flows work
- OAuth2 logins integrate seamlessly
- Resume upload and analysis flows complete end-to-end
- Rate limiting prevents abuse
- Error messages are user-friendly
- All pages load and function correctly
- Dark mode works across all pages
- No console errors or warnings
- Admin can verify all data in database

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| OpenAI API rate limits | Implement token-based limiting, add retry logic with exponential backoff |
| Large resume file uploads | Implement file size limits, streaming uploads, background processing |
| JWT token expiration | Implement automatic refresh tokens, handle 401 gracefully |
| Database performance | Add indexes, optimize queries, implement caching |
| OAuth2 provider downtime | Add fallback auth methods, graceful error handling |
| Security vulnerabilities | Follow OWASP guidelines, security audit, penetration testing |

---

## Timeline Estimate

- **Phase 1 (Backend):** 4-6 weeks
- **Phase 2 (Frontend):** 4-6 weeks  
- **Phase 3 (Integration & Refinement):** 2-3 weeks
- **Total:** 10-15 weeks

---

## Next Steps

1. ✅ Plan approved
2. → Start Phase 1: Backend Infrastructure
3. → Start Phase 2: Frontend Infrastructure (in parallel)
4. → Phase 3: Integration when both phases are substantially complete

---

**Plan Created:** 2026-04-10  
**Status:** Ready for Implementation  
**Confirmed Requirements:** OpenAI API, PDF/DOCX support, OAuth2/JWT auth, subscription-based rate limiting

---

## Copy Instructions

1. **Select all text above** (Ctrl+A)
2. **Copy** (Ctrl+C)
3. **Open or create** `/resume-analyzer/plan.md` in VS Code
4. **Paste** (Ctrl+V)
5. **Save** (Ctrl+S)

The plan is now ready for implementation! All 225+ tasks are organized by phase with checkboxes for tracking progress.