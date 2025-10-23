#  Vist 🎁

A backend for wishlist app that allows users to create, share, and manage wishlists with friends and family. Vist provides a comprehensive solution for gift planning and social wishlist sharing.

## Features

- JWT based user authorization with email verification, and profile management (including password reset)
- Create and organize multiple wishlists with custom names
- Add gifts with images, prices, descriptions, and priority levels
- Friend system with friend requests and wishlist sharing
- Friends can book gifts to avoid duplicate purchases
- Advanced search across users and wishlists using `fuzzystrmatch`, `pg_trgm` extensions and Redis for cache layer
- Image upload and management for gifts and profiles using both MinIO or filesystem storage
- Admin panel for platform management

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/almost-a-mathematician/fastapi-vist-backend.git
cd fastapi_vist
```

### 2. Environment Configuration

Create a `.env` file in the `vist-app/` directory with the following configuration:

```env
# Database Configuration
DB_NAME=vist
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=pgdb
DB_PORT=5432

# Frontend URLs (Update these to match your frontend deployment)
FRONTEND_VERIFY_PAGE=https://vist.victorias.dev/auth/verify
FRONTEND_RESET_PW_PAGE=https://vist.victorias.dev/auth/reset-password

# Token Lifetimes (in minutes)
EMAIL_TOKEN_LIFETIME=10
ACCESS_TOKEN_LIFETIME=60
REFRESH_TOKEN_LIFETIME=720

# JWT Secrets (Generate secure random strings for production)
EMAIL_TOKEN_SECRET=email-token-secret
ACCESS_TOKEN_SECRET=access-token-secret
REFRESH_TOKEN_SECRET=refresh-token=secret

# Email Configuration (Configure with your SMTP provider)
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

# Email Rate Limiting
USER_MAIL_SEND_DELAY=15

# File Storage
STORAGE_PATH=./storage

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your-redis-password

# MinIO Configuration (Object Storage)
MINIO_ENDPOINT=minio:9000
MINIO_BUCKET_NAME=vist-images
MINIO_ACCESS_KEY=your-minio-access-key
MINIO_SECRET_KEY=your-minio-secret-key
MINIO_SECURE=0
```

### 3. Docker Deployment

The easiest way to run Vist is using Docker Compose:

```bash
cd vist-app
docker-compose up -d
```

This will start all required services:
- FastAPI application (port 8085)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- MinIO object storage (ports 9000, 9001)

### 4. Admin Access

To access the admin panel, ensure your user account has `is_admin=True` in the database. You can easily set this flag using `psql` utility

## 🌐 Live Deployment

The Vist platform is deployed and available at:

- API: [http://vist.victorias.dev](http://vist.victorias.dev)
- API documentation: [http://vist.victorias.dev/docs](http://vist.victorias.dev/docs)

## Development

### Database Migrations

To create a new migration after model changes:

```bash
cd vist-app
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Code Formatting

The project uses YAPF for code formatting. The project is already configured to run formatting on code save in VSCode, but also you can run the formatter manually: 
```bash
yapf -r -i .
```