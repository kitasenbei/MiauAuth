<p align="center">
  <img src="assets/logo.png" alt="MiauAuth" width="128">
</p>

<h1 align="center">MiauAuth</h1>

<p align="center">
  osu! OAuth identity provider — authenticate users and get JWTs with their profile data.
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#integration">Integration</a> •
  <a href="#endpoints">Endpoints</a> •
  <a href="#deployment">Deployment</a>
</p>

---

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Configure your osu! OAuth credentials
python main.py
```

Create an osu! OAuth app at [osu.ppy.sh/home/account/edit#oauth](https://osu.ppy.sh/home/account/edit#oauth)

## Integration

**1. Redirect to login**
```javascript
window.location.href = 'https://your-miauauth.com/auth/login';
```

**2. Handle callback**
```javascript
const token = new URLSearchParams(location.search).get('token');
if (token) localStorage.setItem('token', token);
```

**3. JWT payload**
```json
{
  "osu_id": 12345678,
  "username": "peppy",
  "country_code": "AU",
  "avatar_url": "https://a.ppy.sh/12345678",
  "exp": 1234567890
}
```

**4. Verify tokens**
```javascript
// Option A: Use verify endpoint (no secret needed)
const { valid, user } = await fetch(`/auth/verify?token=${token}`).then(r => r.json());

// Option B: Verify locally with shared SECRET_KEY
import jwt from 'jsonwebtoken';
const payload = jwt.verify(token, SECRET_KEY);
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /auth/login` | Redirects to osu! OAuth |
| `GET /auth/callback` | OAuth callback, redirects with JWT |
| `GET /auth/verify?token=xxx` | Verify token, returns `{ valid, user }` |
| `GET /health` | Health check |

## Deployment

**Docker**
```bash
docker build -t miauauth .
docker run -p 8001:8001 --env-file .env miauauth
```

**AWS Lambda**
```bash
# Manual zip
./lambda/build.sh
# Upload lambda/deployment.zip, handler: main.handler

# Or use SAM
cd lambda && sam build && sam deploy --guided
```

## Configuration

| Variable | Description |
|----------|-------------|
| `OSU_CLIENT_ID` | osu! OAuth client ID |
| `OSU_CLIENT_SECRET` | osu! OAuth client secret |
| `OSU_REDIRECT_URI` | Callback URL (must match osu! settings) |
| `SECRET_KEY` | JWT signing key |
| `ALLOWED_ORIGINS` | CORS origins (comma-separated) |
| `DEFAULT_REDIRECT` | Fallback redirect URL |

## License

MIT
