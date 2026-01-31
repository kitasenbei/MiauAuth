# MiauAuth

osu! OAuth identity provider. Authenticates users via osu! and returns a JWT with their profile data.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create an osu! OAuth application at https://osu.ppy.sh/home/account/edit#oauth

3. Copy `.env.example` to `.env` and configure:
   ```bash
   cp .env.example .env
   ```

4. Run:
   ```bash
   python main.py
   ```

## Integration

### 1. Redirect to login
```javascript
window.location.href = 'https://your-miauauth-instance.com/auth/login';
```

### 2. Handle the callback
After auth, user is redirected back with `?token=<jwt>`:
```javascript
const params = new URLSearchParams(window.location.search);
const token = params.get('token');
if (token) {
  localStorage.setItem('token', token);
}
```

### 3. JWT Payload
The token contains:
```json
{
  "osu_id": 12345678,
  "username": "peppy",
  "country_code": "AU",
  "avatar_url": "https://a.ppy.sh/12345678",
  "exp": 1234567890
}
```

### 4. Verify the token

**Option A: Use the verify endpoint (no secret needed)**
```javascript
const res = await fetch(`https://your-miauauth.com/auth/verify?token=${token}`);
const { valid, user } = await res.json();
```

**Option B: Verify locally (share SECRET_KEY with your backend)**
```python
import jwt
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /auth/login` | Redirects to osu! OAuth |
| `GET /auth/callback` | Handles OAuth callback, redirects with JWT |
| `GET /auth/verify?token=xxx` | Verify token, returns `{ valid, user }` |
| `GET /health` | Health check |

## Configuration

| Variable | Description |
|----------|-------------|
| `OSU_CLIENT_ID` | osu! OAuth client ID |
| `OSU_CLIENT_SECRET` | osu! OAuth client secret |
| `OSU_REDIRECT_URI` | Callback URL (must match osu! app settings) |
| `SECRET_KEY` | JWT signing key (share with your backend) |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) |
| `DEFAULT_REDIRECT` | Fallback redirect URL |
