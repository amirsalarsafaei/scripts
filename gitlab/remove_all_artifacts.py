import aiohttp

import asyncio

project_id = ''
private_token = ''
gitlab_host = ''


async def delete_job(session, job_id):
    async with session.delete(
            f'https://{gitlab_host}/api/v4/projects/{project_id}/jobs/{job_id}/artifacts',
            headers={"PRIVATE-TOKEN": private_token}
    ) as response:
        if response.status != 204:
            print(f"Failed to delete job {job_id}")


async def get_jobs(session, page):
    async with session.get(
            f'https://{gitlab_host}/api/v4/projects/{project_id}/jobs?page={page}&per_page=100',
            headers={"PRIVATE-TOKEN": private_token}
    ) as response:
        response.raise_for_status()
        return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        for page in range(1, 100000):
            print(page)
            jobs = await get_jobs(session, page)
            if not jobs:
                break  # No more jobs to process

            tasks = []
            for job in jobs:
                job_id = job['id']
                tasks.append(delete_job(session, job_id))

            await asyncio.gather(*tasks)


asyncio.run(main())
