import asyncio

from app.services.github_service import     get_github_installations,get_installation_repositories,create_installation_access_token,get_repository_branches


async def main():
    installations = await get_github_installations()
    installation_id = installations[0]["id"]
    access_token = await create_installation_access_token(installation_id)
    repositories = await get_installation_repositories(installation_id)
    print("Total repositories:",len(repositories))

    for repo in repositories:
        owner,reponame = repo["full_name"].split("/")

        branches = await get_repository_branches(
            owner,
            reponame,
            access_token
        )
        print(f"\nRepository: {repo['full_name']}")
        print("Total branches:",len(branches))

        for branch in branches:
            print("Branch:",branch["name"])
            print("Commit SHA",branch["commit"]["sha"])

         
        
   


asyncio.run(main())



