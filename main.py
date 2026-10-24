import asyncio
from raboter import Rabota

async def main():
    parser = Rabota(headless=True)

    await parser.browser_launch()
    



if __name__ = "__main__":
    asyncio.run(main())