import asyncio

from app.services.github_service import get_github_installations


async def main():
    installations = await get_github_installations()
    print("Response:", installations)
    print("Total installations:", len(installations))
    for installation in installations:
      print(installation["id"])
      print(installation["accounts"]["login"])
      print(installation["target_type"])


asyncio.run(main())