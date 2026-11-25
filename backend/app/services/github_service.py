import jwt
import time
from pathlib import Path
import httpx
from app.core.config import settings

def create_github_jwt() ->str:
    private_key_path = Path(settings.github_private_key_path)

    if not private_key_path.is_absolute():
        private_key_path = Path.cwd() / private_key_path

    private_key  = private_key_path.read_text(encoding="utf-8")
    now = int(time.time())

    payload = {
        "iat":now - 60,
        "exp":now+(10*60),
        "iss":str(settings.github_app_id)
    }

    token = jwt.encode(
        payload,
        private_key,
        algorithm="RS256"
    )

    return token

async def get_github_installations():
    token = create_github_jwt()

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept":"application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.github.com/app/installations",
            headers=headers
        )

    response.raise_for_status()

    return response.json()
