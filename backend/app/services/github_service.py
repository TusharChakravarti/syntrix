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

async def create_installation_access_token(installation_id:int) -> str:
    token = create_github_jwt()

    headers = {
        "Authorization":f"Bearer {token}",
        "Accept":"application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"

    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"https://api.github.com/app/installations/{installation_id}/access_tokens",
         headers = headers
        )

    response.raise_for_status()

    return response.json()["token"]

async def get_installation_repositories(installation_id:int):
    access_token = await create_installation_access_token(installation_id)

    headers = {
        "Authorization":f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"

    }

    async with httpx.AsyncClient() as client:
        response = await client.get( "https://api.github.com/installation/repositories",
          headers = headers )
    response.raise_for_status()
    return response.json()["repositories"]

async def get_repository_branches(
        owner:str,
        repo:str,
        access_token:str
):
    headers = {
         "Authorization":f"Bearer {access_token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28"
    }

    branches = []
    async with httpx.AsyncClient() as client:
        page = 1

        while True:
            response = await client.get(f"https://api.github.com/repos/{owner}/{repo}/branches",
                headers=headers,
             params={
                 "per_page":100,
                 "page":page
             }

                                        )

            response.raise_for_status()

            data = response.json()

            if not data:
                break

            branches.extend(data)
            page+=1

    return branches







    



    


        