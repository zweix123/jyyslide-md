import asyncio
import aiohttp
from tqdm.asyncio import tqdm


class UrlChecker:
    def __init__(self, urls: list[str], refs: list[str]) -> None:
        self.urls = urls
        self.refs = refs
        self.invalid_indexs = list()

    def __call__(self) -> list[(str, str)]:
        asyncio.run(self.check_urls())
        return zip(
            [self.urls[i] for i in self.invalid_indexs],
            [self.refs[i] for i in self.invalid_indexs],
        )

    async def check_url(self, index, session, pbar):
        try:
            async with session.get(self.urls[index]) as response:
                pbar.update(1)
                if response.status == 200:
                    pass

                else:
                    self.invalid_indexs.append(index)
        except:
            self.invalid_indexs.append(index)

    async def check_urls(self):
        async with aiohttp.ClientSession() as session:
            tasks = []
            n = len(self.urls)
            with tqdm(total=n) as pbar:
                for i in range(n):
                    task = asyncio.create_task(self.check_url(i, session, pbar))
                    tasks.append(task)
                for coroutine in asyncio.as_completed(tasks):
                    await coroutine


import requests


def down_image(img_url, save_file_path):
    resp = requests.get(img_url)
    with open(save_file_path, "wb") as f:
        f.write(resp.content)
