# MiauAuth

osu! OAuth authentication microservice. Handles OAuth flow and issues JWT tokens.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your values:
   ```bash
   cp .env.example .env
   ```

3. Register an OAuth application at https://osu.ppy.sh/home/account/edit#oauth

4. Run:
   ```bash
   python main.py
   ```

   Or with Docker:
   ```bash
   docker build -t miauauth .
   docker run -p 8001:8001 --env-file .env miauauth
   ```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /auth/login` | Redirects to osu! OAuth |
| `GET /auth/callback` | OAuth callback, returns JWT via redirect |
| `GET /health` | Health check |

## Flow

1. Frontend redirects user to `/auth/login`
2. User authenticates on osu!
3. osu! redirects back to `/auth/callback`
4. Service syncs user with your main backend via `POST /internal/users/sync`
5. User is redirected to frontend with `?token=<jwt>`

## Backend Integration

Your main backend needs a `POST /internal/users/sync` endpoint that:
- Accepts `{ osu_id, username, flag_code }`
- Validates `X-Internal-Secret` header
- Returns user object with `{ id, osu_id, username, is_staff }`

Use the same `SECRET_KEY` and `INTERNAL_SECRET` on both services.
