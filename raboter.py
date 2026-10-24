import asyncio
import logging

from patchright.async_api import async_playwright


class Rabota:
    def __init__(self ,  , headless = True) -> None:
        self.link = 'https://rabota.by/?ysclid=mvm0pzubtp654429596'
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    async def browser_launch(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless, 
            channel="Chrome")
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        print("Browser is LAUNCHED...")
    


    async def browser_stop(self):
        if self.browser:
            await self.browser.close()
            print("Browser is CLOSED")

        if self.playwright:
            await self.playwright.stop()
            print("Playwright is STOPED")

    def __del__(self):
        print("Seccesefuly finished....OR NOT !!!")

