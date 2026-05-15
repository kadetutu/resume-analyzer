# Resume Analyzer Backend

Production-ready FastAPI backend for resume analysis application.

## Features

- **JWT Authentication** — Secure token-based authentication with refresh tokens
- **OAuth2 Integration** — Support for Google, GitHub, and Facebook login
- **Resume Processing** — PDF and DOCX file parsing with text extraction
- **AI Analysis** — OpenAI GPT integration for resume-to-job-description matching
- **Rate Limiting** — Subscription-based usage limits (Free/Pro/Enterprise)
- **Database** — PostgreSQL with SQLModel ORM and Alembic migrations
- **Testing** — Comprehensive PyTest suite with 70%+ coverage

## Project Structure

```
backend/
├── app/
│   ├── api/v1/              # API endpoints
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── services/            # Business logic
│   ├── core/                # Configuration, security, database
│   ├── middleware/          # Authentication middleware
│   ├── utils/               # Utilities (validators, file handlers)
│   └── main.py              # FastAPI app setup
├── tests/                   # PyTest test suite
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── pytest.ini               # PyTest configuration
└── main.py                  # Application entry point
```

## Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- OpenAI API key

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update with your configuration:

```bash
cp .env.example .env
```

Edit `.env` with:
- Database URL: `postgresql://user:password@localhost:5432/resume_analyzer_db`
- OpenAI API key
- JWT secret key
- OAuth2 credentials (optional)

### 4. Create Database

```bash
python -m alembic upgrade head
```

Or initialize tables directly:

```bash
python -c "from app.core.database import create_db_and_tables; create_db_and_tables()"
```

### 5. Run Application

```bash
python main.py
```

API will be available at `http://localhost:8000`
- Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` — Register new user
- `POST /api/v1/auth/login` — Login user
- `POST /api/v1/auth/refresh` — Refresh access token
- `POST /api/v1/auth/logout` — Logout user
- `GET /api/v1/auth/me` — Get current user profile

### Resumes

- `POST /api/v1/resumes/upload` — Upload resume file
- `GET /api/v1/resumes` — List user's resumes
- `GET /api/v1/resumes/{id}` — Get resume details
- `DELETE /api/v1/resumes/{id}` — Delete resume

### Analysis

- `POST /api/v1/analysis/analyze` — Analyze resume against job description

## Testing

Run tests with PyTest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_auth.py -v
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens with short expiration (30 min access, 7 day refresh)
- CORS configured for frontend URL only
- Rate limiting based on subscription tier
- No sensitive data logged

## Configuration

Key environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/resume_analyzer_db
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key
FRONTEND_URL=http://localhost:5173
MAX_RESUME_FILE_SIZE=5242880
FREE_TIER_MONTHLY_LIMIT=10
PRO_TIER_MONTHLY_LIMIT=100
ENTERPRISE_TIER_MONTHLY_LIMIT=1000
```

## Deployment

### Docker

Build and run with Docker:

```bash
docker build -t resume-analyzer-backend .
docker run -p 8000:8000 --env-file .env resume-analyzer-backend
```

### Production Checklist

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `ENVIRONMENT=production` and `DEBUG=false`
- [ ] Configure proper database (PostgreSQL)
- [ ] Setup OpenAI API key
- [ ] Configure HTTPS/SSL
- [ ] Setup rate limiting/DDoS protection
- [ ] Enable CORS for production domain only
- [ ] Setup monitoring and logging
- [ ] Run security audit

## Architecture Decisions

| Decision | Rationale |
|----------|-----------|
| **FastAPI** | Type-safe, async-capable, excellent developer experience |
| **SQLModel** | Combines Pydantic validation with SQLAlchemy ORM |
| **JWT + Refresh Tokens** | Balances security with usability |
| **OpenAI API** | Scalable AI without GPU infrastructure |
| **Subscription Tiers** | Flexible monetization model |
| **PyTest** | Comprehensive testing with fixtures and plugins |

## Troubleshooting

### Database Connection Error

Ensure PostgreSQL is running and `DATABASE_URL` is correct:

```bash
psql postgres://user:password@localhost:5432/resume_analyzer_db
```

### OpenAI API Error

Verify API key is valid:

```bash
python -c "import openai; openai.api_key='your-key'; print(openai.Model.list())"
```

### Port Already in Use

Change port in main.py or use:

```bash
python main.py --port 8001
```

## Contributing

1. Follow PEP 8 style guide
2. Write tests for new features
3. Maintain 70%+ test coverage
4. Document API changes
5. Use type hints on all functions

## License

MIT License
