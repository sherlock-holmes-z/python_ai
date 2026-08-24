import asyncio
import time

import aiohttp


async def download_file(session, url):
    print(f"开始下载：{url}")
    response = await session.get(url)
    content = await response.read()
    with open(url[-10:] + ".jpg", "wb") as f:
        f.write(content)
    print(f"下载结束：{url}")
    await response.release()


async def main():
    url_list = [
        "https://images.pexels.com/photos/292442/pexels-photo-292442.jpeg?_gl=1*1vtgbgl*_ga*MTg0MDMwODQ4My4xNzc3MDMyOTEz*_ga_8JE65Q40S6*czE3ODc1ODc1MTgkbzIkZzAkdDE3ODc1ODc1MTgkajYwJGwwJGgw",
        "https://images.pexels.com/photos/1562/italian-landscape-mountains-nature.jpg?_gl=1*15h7l5o*_ga*MTg0MDMwODQ4My4xNzc3MDMyOTEz*_ga_8JE65Q40S6*czE3ODc1ODc1MTgkbzIkZzEkdDE3ODc1ODc1NDkkajI5JGwwJGgw",
    ]
    # 协程自动关闭资源使用async with
    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
